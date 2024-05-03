import itertools

import numpy as np
from nipype.interfaces import fsl
import logging
import time

from ..HOUSE.handler import HOUSE
from .utils import *

config = None
config_path = ''
config_filename = ''


def statmap_file_setup(func):
    file_location = config.input_folder_name

    if config.output_folder_name != 'DEFAULT':
        output_folder = f"statmaps/{config.output_folder_name}"
    elif func == 'Image SNR':
        output_folder = 'statmaps/imageSNR_report'
    elif func == 'Temporal SNR':
        output_folder = 'statmaps/temporalSNR_report'

    if config.base_folder in ("", " "):
        print('Select the directory which contains the subject folders.')
        base_sub_location = Utils.file_browser(title='Select the directory which contains the subject folders')

    else:
        base_sub_location = config.base_folder

    # Create dictionary from each participant directory
    participant_dir, _ = Utils.find_participant_dirs(base_sub_location)
    participants = {participant: None for participant in participant_dir}

    for participant in participants:
        # Find all nifti and analyze files
        participants[participant] = Utils.find_files(f"{participant}/{file_location}", "hdr", "nii.gz", "nii")

        Utils.check_and_make_dir(f"{participant}/statmaps")
        Utils.check_and_make_dir(f"{participant}/{output_folder}", delete_old=True)
        Utils.save_config(f"{participant}/{output_folder}", config_path, config_filename,
                          additional_info=[f"statistical_map_created = '{func}'\n"],
                          new_config_name='statmap_config')

    return participants, output_folder, file_location


def calculate_sigma_in_volumes(file_path):
    data = nib.load(file_path)
    TR = data.header['pixdim'][4]  # Find TR

    # Equation found here: https://www.jiscmail.ac.uk/cgi-bin/webadmin?A2=FSL;f6fd75a6.1709
    return 1 / (2 * config.highpass_filter_cutoff * TR)


def temporalSNR_calc(file, no_ext_file, output_folder):
    fsl.maths.MeanImage(in_file=file, out_file=f'{output_folder}/{no_ext_file}_tMean.nii.gz').run()  # Mean over time

    fsl.maths.StdImage(in_file=file,
                       out_file=f'{output_folder}/{no_ext_file}_tStd.nii.gz').run()  # Standard dev over time

    # tMean / tStd
    fsl.maths.BinaryMaths(operation='div', in_file=f'{output_folder}/{no_ext_file}_tMean.nii.gz',
                          operand_file=f'{output_folder}/{no_ext_file}_tStd.nii.gz',
                          out_file=f'{output_folder}/{no_ext_file}_tSNR.nii.gz').run()

    # Threshold volume so any tSNR values above 1000 are set to 0
    fsl.maths.Threshold(in_file=f'{output_folder}/{no_ext_file}_tSNR.nii.gz', thresh=1000.0, direction='above',
                        out_file=f'{output_folder}/{no_ext_file}_tSNR.nii.gz').run()


def imageSNR_calc(func_file, noise_file, no_ext_file, output_folder, participant_dir):
    fsl.maths.MeanImage(in_file=func_file,
                        out_file=f'{output_folder}/{no_ext_file}_tMean.nii.gz').run()  # Mean over time

    if config.noise_volume:
        file, _ = Utils.load_brain(noise_file)

        # Std dev of entire volume
        if config.iSNR_std_use_only_nonzero_voxels:
            noise_value = file[file != 0].std()
        else:
            noise_value = file.std()

    else:
        base_sub_location = Path(participant_dir).parents[0]
        participant_name = os.path.split(Path(participant_dir))[1]

        noise_value_csv = pd.read_csv(f'{base_sub_location}/noiseValues.csv')
        noise_value = float(noise_value_csv[noise_value_csv['Participant'] == participant_name]['Background noise'])

    # tMean / Std
    fsl.maths.BinaryMaths(operation='div',
                          in_file=f'{output_folder}/{no_ext_file}_tMean.nii.gz',
                          operand_value=noise_value,
                          out_file=f'{output_folder}/{no_ext_file}_iSNR.nii.gz').run()

    if config.magnitude_correction:
        magnitude_correction(f'{output_folder}/{no_ext_file}_iSNR.nii.gz')


def magnitude_correction(file_name):
    fsl.maths.BinaryMaths(in_file=file_name, operation='mul', operand_value=0.7, out_file=file_name).run()


def save_to_preprocessed_folder(data, header, no_ext_file, participant, method):
    with open(f'{participant}/{config.input_folder_name}_preprocessed/changes_made_to_files.txt', 'a+') as f:
        f.seek(0)  # Go to start of file
        f.write(f'{no_ext_file}: {method}\n')

    data = Utils.save_brain(data, '', no_ext_file, f'{participant}/{config.input_folder_name}_preprocessed', header)

    return data


def highpass_filtering(file_path, output_folder, no_ext_file):
    sigma_in_volumes = calculate_sigma_in_volumes(file_path)

    fsl.maths.MeanImage(in_file=f'{file_path}', out_file=f'{output_folder}/{no_ext_file}_tMean.nii.gz').run()

    fsl.TemporalFilter(in_file=f'{file_path}',
                       out_file=f'{output_folder}/{no_ext_file}_filtered.nii.gz',
                       highpass_sigma=sigma_in_volumes).run()

    fsl.maths.BinaryMaths(operation='add', in_file=f'{output_folder}/{no_ext_file}_tMean.nii.gz',
                          operand_file=f'{output_folder}/{no_ext_file}_filtered.nii.gz',
                          out_file=f'{output_folder}/{no_ext_file}_filtered_restoredmean.nii.gz').run()

    return f'{output_folder}/{no_ext_file}_filtered_restoredmean.nii.gz', \
           f'{output_folder}/{no_ext_file}_filtered.nii.gz'


def delete_files(redundant_files):
    for file in redundant_files:
        os.remove(file)


def create_statmaps(func, file, no_ext_file, noise_file, output_folder, participant):
    if func == 'Image SNR':
        imageSNR_calc(file, noise_file, no_ext_file, output_folder, participant)
    elif func == 'Temporal SNR':
        temporalSNR_calc(file, no_ext_file, output_folder)


def prepare_statmap_files(func, file, no_ext_file, output_folder, participant):
    noise_file = None

    redundant_files = []
    outliers = []

    # Save original copy of file which may be overwritten later, however allows this folder to always be used
    data, header = Utils.load_brain(file)
    Utils.save_brain(data, '', no_ext_file, f'{participant}/{config.input_folder_name}_preprocessed', header)

    if func == 'Image SNR' and config.noise_volume:
        file = f'{participant}/func_volumes/{no_ext_file}.nii.gz'
        noise_file = f'{participant}/noise_volume/{no_ext_file}_noise_volume.nii.gz'

        if not os.path.exists(file) or not os.path.exists(noise_file):
            raise FileNotFoundError('Could not find separate noise and functional volumes. '
                                    'Run the "separate noise volumes" utility to create these files.')

    if config.remove_motion_outliers:
        file, outlier_timepoints, outlier_files = remove_motion_outliers(file, no_ext_file, output_folder, participant)
        redundant_files.extend(outlier_files)
        outliers.extend(outlier_timepoints)

    if config.motion_correction:
        output = f'{output_folder}/{no_ext_file}_motion_corrected.nii.gz'

        fsl.MCFLIRT(in_file=file, out_file=output).run()
        file = output

        data, header = Utils.load_brain(file)
        file = save_to_preprocessed_folder(data, header, no_ext_file, participant, 'Motion corrected data')

    if config.spatial_smoothing:
        fsl.SUSAN(in_file=file, fwhm=config.smoothing_fwhm, brightness_threshold=config.smoothing_brightness_threshold,
                  out_file=f'{output_folder}/{no_ext_file}_smoothed.nii.gz').run()
        file = f'{output_folder}/{no_ext_file}_smoothed.nii.gz'

    if config.temporal_filter:
        file, redundant_file = highpass_filtering(file, output_folder, no_ext_file)
        redundant_files.extend([file, redundant_file])

    return file, noise_file, redundant_files, outliers


def remove_motion_outliers(file, no_ext_file, output_folder, participant):
    outlier_file = f'{output_folder}/{no_ext_file}_outliers.txt'
    outlier_plot = f'{output_folder}/{no_ext_file}_metrics.png'
    outlier_values = f'{output_folder}/{no_ext_file}_metrics.txt'

    fsl.MotionOutliers(in_file=file, out_file=outlier_file,
                       out_metric_plot=outlier_plot,
                       out_metric_values=outlier_values).run()

    with open(f'{output_folder}/{no_ext_file}_outliers.txt') as f:
        lines = f.readlines()

    outlier_timepoints = []
    for time_point, line in enumerate(lines):
        outlier_check = line.replace(" ", "").find('1')
        if outlier_check != -1:
            outlier_timepoints.append(time_point)

    data, header = Utils.load_brain(file)
    data = np.delete(data, outlier_timepoints, axis=3)

    # Save copy of motion outlier removed files as it may make registration better during main analysis
    file = save_to_preprocessed_folder(data, header, no_ext_file, participant, 'Removed motion outlier timepoints')

    return file, [no_ext_file, len(outlier_timepoints)], [outlier_file, outlier_plot, outlier_values]


def process_files_for_statmaps(file, participant, output_folder, file_location, func, cfg):
    global config
    config = cfg

    no_ext_file = Utils.strip_ext(file)
    file = f"{participant}/{file_location}/{file}"
    output_folder = f'{participant}/{output_folder}'

    if config.verbose:
        print(f'        Analysing file: {no_ext_file}')

    file, noise_file, redundant_files, outliers = prepare_statmap_files(func, file, no_ext_file, output_folder, participant)
    create_statmaps(func, file, no_ext_file, noise_file, output_folder, participant)

    delete_files(redundant_files)

    return outliers


def calculate_statistical_maps(participants, output_folder, file_location, func):
    if config.multicore_processing:
        pool = Utils.start_processing_pool()
    else:
        pool = None

    if config.verbose:
        print(f'\nSearching in folder: {config.input_folder_name}'
              f'\nSaving output in directory: {output_folder}')

    for participant_dir, files in participants.items():
        if config.verbose:
            print(f'\nCreating statistical maps for participant: {participant_dir.split("/")[-1]}'
                  f'\n      Creating statmaps for {len(files)} files')

        Utils.check_and_make_dir(f'{participant_dir}/{config.input_folder_name}_preprocessed', delete_old=True)

        # Save blank txt file
        with open(f'{participant_dir}/{config.input_folder_name}_preprocessed/changes_made_to_files.txt', 'w') as f:
            f.write('')

        iterable = zip(files,
                       itertools.repeat(participant_dir),
                       itertools.repeat(output_folder),
                       itertools.repeat(file_location),
                       itertools.repeat(func),
                       itertools.repeat(config))

        if config.multicore_processing:
            outliers = list(pool.starmap(process_files_for_statmaps, iterable))
        else:
            outliers = list(itertools.starmap(process_files_for_statmaps, iterable))

        if config.remove_motion_outliers:
            outliers = pd.DataFrame(columns=['File', 'Outliers removed'], data=outliers).sort_values('Outliers removed')

            with open(f"{participant_dir}/{output_folder}/number_of_outliers_removed.csv", "w") as f:
                f.write(outliers.to_csv(index=False))

    if config.multicore_processing:
        Utils.join_processing_pool(pool, restart=False)


def main(func, version, config_file, path=None):
    global config, config_path, config_filename

    start_time = time.time()
    Utils.checkversion(version)

    # Set global variables
    config_path = f'{Path(os.path.abspath(__file__)).parents[1]}/configuration_profiles/maps'
    config_filename = config_file

    # Load config file
    config = Utils.load_config(config_path, config_file, path=path)

    logging.getLogger('nipype.workflow').setLevel(0)  # Suppress workflow terminal output

    if func == 'Image SNR' and not config.noise_volume and config.verbose:
        print('"Noise volume included in time series" is false. Trying to find values for each participant in '
              'noiseValues.csv instead. If this is not correct, set "Noise volume included in time series" to true.\n')

    if func in ['Add Gaussian noise', 'Add motion', 'Separate noise volumes']:
        print('\n--------------------------------\n'
              '-------- Running utility --------\n'
              '--------------------------------\n'
              f'\nRunning {func} utility.\n')

        HOUSE(config, func)

    else:
        if config.verbose:
            print('\n--------------------------------\n'
                  '--- Statistical map creation ---\n'
                  '--------------------------------\n'
                  f'\nCreating {func} maps.\n')

        participants, output_folder, file_location = statmap_file_setup(func)
        calculate_statistical_maps(participants, output_folder, file_location, func)

    if config.verbose:
        print(f"\n--- Completed in {round((time.time() - start_time), 2)} seconds ---\n\n")
