"""

md_tests.py

A series of tests to validate basic repo functionality and verify either "correct"
inference behavior, or - when operating in environments other than the training
environment - acceptable deviation from the correct results.

This module should not depend on anything else in this repo outside of the 
tests themselves, even if it means some duplicated code (e.g. for downloading files),
since much of what it tries to test is, e.g., imports.

"""

#%% Imports and constants

### Only standard imports belong here, not MD-specific imports ###

import os
import json
import glob
import tempfile
import urllib
import urllib.request
import zipfile
import subprocess
import argparse


#%% Classes

class MDTestOptions:
    """
    Options controlling test behavior.
    """
    
    ## Required ##
    
    #: Force CPU execution
    disable_gpu = False
    
    #: If GPU execution is requested, but a GPU is not available, should we error?
    cpu_execution_is_error = False
    
    #: Skip tests related to video processing
    skip_video_tests = False
    
    #: Skip tests launched via Python functions (as opposed to CLIs)
    skip_python_tests = False
    
    #: Skip CLI tests
    skip_cli_tests = False
    
    #: Force a specific folder for temporary input/output
    scratch_dir = None
    
    #: Where does the test data live?
    test_data_url = 'https://lila.science/public/md-test-package.zip'
    
    #: Download test data even if it appears to have already been downloaded
    force_data_download = False
    
    #: Unzip test data even if it appears to have already been unzipped
    force_data_unzip = False
    
    #: By default, any unexpected behavior is an error; this forces most errors to
    #: be treated as warnings.
    warning_mode = False
    
    #: How much deviation from the expected detection coordinates should we allow before
    #: a disrepancy becomes an error?
    max_coord_error = 0.001
    
    #: How much deviation from the expected confidence values should we allow before
    #: a disrepancy becomes an error?    
    max_conf_error = 0.005
    
    #: Current working directory when running CLI tests
    cli_working_dir = None
    
    #: YOLOv5 installation, only relevant if we're testing run_inference_with_yolov5_val. 
    #:
    #: If this is None, we'll skip that test.
    yolo_working_folder = None

# ...class MDTestOptions()


#%% Support functions

def get_expected_results_filename(gpu_is_available):
    """
    Expected results vary just a little across inference environments, particularly
    between PT 1.x and 2.x, so when making sure things are working acceptably, we 
    compare to a reference file that matches the current environment.
    
    This function gets the correct filename to compare to current results, depending
    on whether a GPU is available.
    
    Args:
        gpu_is_available (bool): whether a GPU is available
        
    Returns:
        str: relative filename of the results file we should use (within the test
        data zipfile)
    """
    
    if gpu_is_available:
        hw_string = 'gpu'
    else:
        hw_string = 'cpu'
    import torch
    torch_version = str(torch.__version__)
    if torch_version.startswith('1'):
        assert torch_version == '1.10.1', 'Only tested against PT 1.10.1 and PT 2.x'
        pt_string = 'pt1.10.1'
    else:
        assert torch_version.startswith('2'), 'Unknown torch version: {}'.format(torch_version)
        pt_string = 'pt2.x'
    
    # A hack for now to account for the fact that even with acceleration enabled and PT2 
    # installed, Apple silicon appears to provide the same results as CPU/PT1 inference
    try:
        import torch
        m1_inference = torch.backends.mps.is_built and torch.backends.mps.is_available()
        if m1_inference:
            hw_string = 'cpu'
        pt_string = 'pt1.10.1'
    except Exception:
        pass
    
    return 'md-test-results-{}-{}.json'.format(hw_string,pt_string)
    
    
def download_test_data(options=None):
    """
    Downloads the test zipfile if necessary, unzips if necessary.
    
    Args:
        options (MDTestOptions, optional): see MDTestOptions for details
        
    Returns:
        MDTestOptions: the same object passed in as input, or the options that
        were used if [options] was supplied as None
    """

    if options is None:
        options = MDTestOptions()
        
    if options.scratch_dir is None:        
        tempdir_base = tempfile.gettempdir()
        scratch_dir = os.path.join(tempdir_base,'md-tests')
    else:
        scratch_dir = options.scratch_dir
    
    os.makedirs(scratch_dir,exist_ok=True)    
    
    # See whether we've already downloaded the data zipfile
    download_zipfile = True        
    if not options.force_data_download:
        local_zipfile = os.path.join(scratch_dir,options.test_data_url.split('/')[-1])
        if os.path.isfile(local_zipfile):
            url_info = urllib.request.urlopen(options.test_data_url).info()
            remote_size = int(url_info['Content-Length'])
            target_file_size = os.path.getsize(local_zipfile)
            if remote_size == target_file_size:
                download_zipfile = False
    
    if download_zipfile:
        print('Downloading test data zipfile')
        urllib.request.urlretrieve(options.test_data_url, local_zipfile)
        print('Finished download to {}'.format(local_zipfile))
    else:
        print('Bypassing test data zipfile download for {}'.format(local_zipfile))
    
    
    ## Unzip data
    
    zipf = zipfile.ZipFile(local_zipfile)    
    zip_contents = zipf.filelist
    
    # file_info = zip_contents[1]
    for file_info in zip_contents:
        
        expected_size = file_info.file_size
        if expected_size == 0:
            continue
        fn_relative = file_info.filename
        target_file = os.path.join(scratch_dir,fn_relative)
        unzip_file = True
        if (not options.force_data_unzip) and os.path.isfile(target_file):
            existing_file_size = os.path.getsize(target_file)
            if existing_file_size == expected_size:
                unzip_file = False
        if unzip_file:
            os.makedirs(os.path.dirname(target_file),exist_ok=True)
            with open(target_file,'wb') as f:
                f.write(zipf.read(fn_relative))
            
    # ...for each file in the zipfile
    
    # Warn if file are present that aren't expected
    test_files = glob.glob(os.path.join(scratch_dir,'**/*'), recursive=True)
    test_files = [os.path.relpath(fn,scratch_dir).replace('\\','/') for fn in test_files]
    test_files_set = set(test_files)
    expected_images_set = set(zipf.namelist())
    for fn in expected_images_set:
        if fn.endswith('/'):
            continue
        assert fn in test_files_set, 'File {} is missing from the test image folder'.format(fn)
    
    # Populate the test options with test data information
    options.scratch_dir = scratch_dir
    options.all_test_files = test_files
    options.test_images = [fn for fn in test_files if os.path.splitext(fn.lower())[1] in ('.jpg','.jpeg','.png')]
    options.test_videos = [fn for fn in test_files if os.path.splitext(fn.lower())[1] in ('.mp4','.avi')]    
    options.test_videos = [fn for fn in options.test_videos if 'rendered' not in fn]
        
    print('Finished unzipping and enumerating test data')
    
    return options

# ...def download_test_data(...)


def is_gpu_available(verbose=True):
    """
    Checks whether a GPU (including M1/M2 MPS) is available.
    
    Args:
        verbose (bool, optional): enable additional debug console output
    
    Returns:
        bool: whether a GPU is available
    """
    
    # Import torch inside this function, so we have a chance to set CUDA_VISIBLE_DEVICES
    # before checking GPU availability.
    import torch
    gpu_available = torch.cuda.is_available()
    
    if gpu_available:
        if verbose:
            print('CUDA available: {}'.format(gpu_available))
            device_ids = list(range(torch.cuda.device_count()))
            if len(device_ids) > 1:
                print('Found multiple devices: {}'.format(str(device_ids)))
    else:
        try:
            gpu_available = torch.backends.mps.is_built and torch.backends.mps.is_available()
        except AttributeError:
            pass
        if gpu_available:
            print('Metal performance shaders available')
    
    if not gpu_available:
        print('No GPU available')
        
    return gpu_available            
        
    
#%% CLI functions

# These are copied from process_utils.py to avoid imports outside of the test
# functions.

os.environ["PYTHONUNBUFFERED"] = "1"

def execute(cmd):
    """
    Runs [cmd] (a single string) in a shell, yielding each line of output to the caller.
    
    Args:
        cmd (str): command to run
    
    Returns:
        int: the command's return code, always zero, otherwise a CalledProcessError is raised
    """
 
    # https://stackoverflow.com/questions/4417546/constantly-print-subprocess-output-while-process-is-running
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                             shell=True, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)
    return return_code


def execute_and_print(cmd,print_output=True):
    """
    Runs [cmd] (a single string) in a shell, capturing (and optionally printing) output.
    
    Args:
        cmd (str): command to run
        print_output (bool, optional): whether to print output from [cmd]
    
    Returns:
        dict: a dictionary with fields "status" (the process return code) and "output"
        (the content of stdout)
    """

    to_return = {'status':'unknown','output':''}
    output=[]
    try:
        for s in execute(cmd):
            output.append(s)
            if print_output:
                print(s,end='',flush=True)
        to_return['status'] = 0
    except subprocess.CalledProcessError as cpe:
        print('execute_and_print caught error: {}'.format(cpe.output))
        to_return['status'] = cpe.returncode
    to_return['output'] = output
   
    return to_return


#%% Python tests

def run_python_tests(options):
    """
    Runs Python-based (as opposed to CLI-based) package tests.
    
    Args:
        options (MDTestOptions): see MDTestOptions for details
    """
    
    print('\n*** Starting module tests ***\n')
    
    ## Prepare data
    
    download_test_data(options)
    
    
    ## Run inference on an image
    
    from megadetector.detection import run_detector
    from megadetector.visualization import visualization_utils as vis_utils
    model_file = 'MDV5A'
    image_fn = os.path.join(options.scratch_dir,options.test_images[0])
    model = run_detector.load_detector(model_file)
    pil_im = vis_utils.load_image(image_fn)
    result = model.generate_detections_one_image(pil_im) # noqa

    
    ## Run inference on a folder
    
    from megadetector.detection.run_detector_batch import load_and_run_detector_batch,write_results_to_file
    from megadetector.utils import path_utils

    image_folder = os.path.join(options.scratch_dir,'md-test-images')
    assert os.path.isdir(image_folder), 'Test image folder {} is not available'.format(image_folder)
    inference_output_file = os.path.join(options.scratch_dir,'folder_inference_output.json')
    image_file_names = path_utils.find_images(image_folder,recursive=True)
    results = load_and_run_detector_batch('MDV5A', image_file_names, quiet=True)
    _ = write_results_to_file(results,inference_output_file,
                              relative_path_base=image_folder,detector_file=model_file)

    # Read results
    with open(inference_output_file,'r') as f:
        results_from_file = json.load(f) # noqa
    

    ## Verify results

    # Read expected results
    expected_results_filename = get_expected_results_filename(is_gpu_available(verbose=False))
    
    with open(os.path.join(options.scratch_dir,expected_results_filename),'r') as f:
        expected_results = json.load(f)
            
    filename_to_results = {im['file'].replace('\\','/'):im for im in results_from_file['images']}
    filename_to_results_expected = {im['file'].replace('\\','/'):im for im in expected_results['images']}
    
    assert len(filename_to_results) == len(filename_to_results_expected), \
        'Error: expected {} files in results, found {}'.format(
            len(filename_to_results_expected),
            len(filename_to_results))
    
    max_coord_error = 0
    max_conf_error = 0
    
    # fn = next(iter(filename_to_results.keys()))
    for fn in filename_to_results.keys():
                
        actual_image_results = filename_to_results[fn]
        expected_image_results = filename_to_results_expected[fn]
        
        if 'failure' in actual_image_results:
            assert 'failure' in expected_image_results and \
                'detections' not in actual_image_results and \
                'detections' not in expected_image_results
            continue
        assert 'failure' not in expected_image_results
        
        actual_detections = actual_image_results['detections']
        expected_detections = expected_image_results['detections']
        
        s = 'expected {} detections for file {}, found {}'.format(
            len(expected_detections),fn,len(actual_detections))
        s += '\nExpected results file: {}\nActual results file: {}'.format(
            expected_results_filename,inference_output_file)
        
        if options.warning_mode:
            if len(actual_detections) != len(expected_detections):
                print('Warning: {}'.format(s))
            continue
        assert len(actual_detections) == len(expected_detections), \
            'Error: {}'.format(s)
        
        # i_det = 0
        for i_det in range(0,len(actual_detections)):
            actual_det = actual_detections[i_det]
            expected_det = expected_detections[i_det]
            assert actual_det['category'] == expected_det['category']
            conf_err = abs(actual_det['conf'] - expected_det['conf'])
            coord_differences = []
            for i_coord in range(0,4):
                coord_differences.append(abs(actual_det['bbox'][i_coord]-expected_det['bbox'][i_coord]))
            coord_err = max(coord_differences)
            
            if conf_err > max_conf_error:
                max_conf_error = conf_err
            if coord_err > max_coord_error:
                max_coord_error = coord_err
        
        # ...for each detection
        
    # ...for each image
    
    if not options.warning_mode:
        
        assert max_conf_error <= options.max_conf_error, \
            'Confidence error {} is greater than allowable ({})'.format(
                max_conf_error,options.max_conf_error)
        
        assert max_coord_error <= options.max_coord_error, \
            'Coord error {} is greater than allowable ({})'.format(
                max_coord_error,options.max_coord_error)
        
    print('Max conf error: {}'.format(max_conf_error))
    print('Max coord error: {}'.format(max_coord_error))


    ## Postprocess results
    
    from megadetector.postprocessing.postprocess_batch_results import \
        PostProcessingOptions,process_batch_results
    postprocessing_options = PostProcessingOptions()
    
    postprocessing_options.md_results_file = inference_output_file
    postprocessing_options.output_dir = os.path.join(options.scratch_dir,'postprocessing_output')
    postprocessing_options.image_base_dir = image_folder
    
    postprocessing_results = process_batch_results(postprocessing_options)
    assert os.path.isfile(postprocessing_results.output_html_file), \
        'Postprocessing output file {} not found'.format(postprocessing_results.output_html_file)
    
    
    ## Partial RDE test
    
    from megadetector.postprocessing.repeat_detection_elimination.repeat_detections_core import \
        RepeatDetectionOptions,find_repeat_detections
    
    rde_options = RepeatDetectionOptions()
    rde_options.occurrenceThreshold = 2
    rde_options.confidenceMin = 0.001
    rde_options.outputBase = os.path.join(options.scratch_dir,'rde_working_dir')
    rde_options.imageBase = image_folder
    rde_output_file = inference_output_file.replace('.json','_filtered.json')
    assert rde_output_file != inference_output_file
    rde_results = find_repeat_detections(inference_output_file, rde_output_file, rde_options)
    assert os.path.isfile(rde_results.filterFile),\
        'Could not find RDE output file {}'.format(rde_results.filterFile)
        
    
    # TODO: add remove_repeat_detections test here
    #
    # It's already tested in the CLI tests, so this is not urgent.
    
    if not options.skip_video_tests:
        
        ## Video test (single video)
       
        from megadetector.detection.process_video import ProcessVideoOptions, process_video
        
        video_options = ProcessVideoOptions()
        video_options.model_file = 'MDV5A'
        video_options.input_video_file = os.path.join(options.scratch_dir,options.test_videos[0])
        video_options.output_json_file = os.path.join(options.scratch_dir,'single_video_output.json')
        video_options.output_video_file = os.path.join(options.scratch_dir,'video_scratch/rendered_video.mp4')
        video_options.frame_folder = os.path.join(options.scratch_dir,'video_scratch/frame_folder')
        video_options.frame_rendering_folder = os.path.join(options.scratch_dir,'video_scratch/rendered_frame_folder')    
        video_options.render_output_video = True
        # video_options.keep_rendered_frames = False
        # video_options.keep_rendered_frames = False
        video_options.force_extracted_frame_folder_deletion = True
        video_options.force_rendered_frame_folder_deletion = True
        # video_options.reuse_results_if_available = False
        # video_options.reuse_frames_if_available = False
        video_options.recursive = True
        video_options.verbose = False
        video_options.fourcc = 'mp4v'
        # video_options.rendering_confidence_threshold = None
        # video_options.json_confidence_threshold = 0.005
        video_options.frame_sample = 5    
        video_options.n_cores = 5
        # video_options.debug_max_frames = -1
        # video_options.class_mapping_filename = None
        
        _ = process_video(video_options)
    
        assert os.path.isfile(video_options.output_video_file), \
            'Python video test failed to render output video file'
        assert os.path.isfile(video_options.output_json_file), \
            'Python video test failed to render output .json file'
            
        
        ## Video test (folder)
        
        from megadetector.detection.process_video import ProcessVideoOptions, process_video_folder
        
        video_options = ProcessVideoOptions()
        video_options.model_file = 'MDV5A'
        video_options.input_video_file = os.path.join(options.scratch_dir,
                                                      os.path.dirname(options.test_videos[0]))
        video_options.output_json_file = os.path.join(options.scratch_dir,'video_folder_output.json')
        # video_options.output_video_file = None
        video_options.frame_folder = os.path.join(options.scratch_dir,'video_scratch/frame_folder')
        video_options.frame_rendering_folder = os.path.join(options.scratch_dir,'video_scratch/rendered_frame_folder')    
        video_options.render_output_video = False
        # video_options.keep_rendered_frames = False
        # video_options.keep_rendered_frames = False
        video_options.force_extracted_frame_folder_deletion = True
        video_options.force_rendered_frame_folder_deletion = True
        # video_options.reuse_results_if_available = False
        # video_options.reuse_frames_if_available = False
        video_options.recursive = True
        video_options.verbose = False
        # video_options.fourcc = None
        # video_options.rendering_confidence_threshold = None
        # video_options.json_confidence_threshold = 0.005
        video_options.frame_sample = 5    
        video_options.n_cores = 5
        # video_options.debug_max_frames = -1
        # video_options.class_mapping_filename = None
        
        _ = process_video_folder(video_options)
    
        assert os.path.isfile(video_options.output_json_file), \
            'Python video test failed to render output .json file'
        
    # ...if we're not skipping video tests
    
    print('\n*** Finished module tests ***\n')

# ...def run_python_tests(...)


#%% Command-line tests

def run_cli_tests(options):
    """
    Runs CLI (as opposed to Python-based) package tests.
    
    Args:
        options (MDTestOptions): see MDTestOptions for details
    """
    
    print('\n*** Starting CLI tests ***\n')
    
    ## chdir if necessary
    
    if options.cli_working_dir is not None:
        os.chdir(options.cli_working_dir)
    
    
    ## Prepare data
    
    download_test_data(options)
    
    
    ## Run inference on an image
    
    model_file = 'MDV5A'
    image_fn = os.path.join(options.scratch_dir,options.test_images[0])
    output_dir = os.path.join(options.scratch_dir,'single_image_test')
    if options.cli_working_dir is None:
        cmd = 'python -m megadetector.detection.run_detector'
    else:
        cmd = 'python megadetector/detection/run_detector.py'
    cmd += ' {} --image_file {} --output_dir {}'.format(
        model_file,image_fn,output_dir)
    print('Running: {}'.format(cmd))
    cmd_results = execute_and_print(cmd)
    
    if options.cpu_execution_is_error:
        gpu_available_via_cli = False
        for s in cmd_results['output']:
            if 'GPU available: True' in s:
                gpu_available_via_cli = True
                break
        if not gpu_available_via_cli:
            raise Exception('GPU execution is required, but not available')

    
    ## Run inference on a folder
    
    image_folder = os.path.join(options.scratch_dir,'md-test-images')
    assert os.path.isdir(image_folder), 'Test image folder {} is not available'.format(image_folder)
    inference_output_file = os.path.join(options.scratch_dir,'folder_inference_output.json')
    if options.cli_working_dir is None:
        cmd = 'python -m megadetector.detection.run_detector_batch'
    else:
        cmd = 'python megadetector/detection/run_detector_batch.py'
    cmd += ' {} {} {} --recursive'.format(
        model_file,image_folder,inference_output_file)
    cmd += ' --output_relative_filenames --quiet --include_image_size'
    cmd += ' --include_image_timestamp --include_exif_data'
    print('Running: {}'.format(cmd))
    cmd_results = execute_and_print(cmd)
    
    # Make sure a coherent file got written out, but don't verify the results, leave that
    # to the Python tests.
    with open(inference_output_file,'r') as f:
        results_from_file = json.load(f) # noqa
    

    ## Postprocessing
    
    postprocessing_output_dir = os.path.join(options.scratch_dir,'postprocessing_output_cli')
    
    if options.cli_working_dir is None:
        cmd = 'python -m megadetector.postprocessing.postprocess_batch_results'
    else:
        cmd = 'python megadetector/postprocessing/postprocess_batch_results.py'
    cmd += ' {} {}'.format(
        inference_output_file,postprocessing_output_dir)
    cmd += ' --image_base_dir {}'.format(image_folder)
    print('Running: {}'.format(cmd))
    cmd_results = execute_and_print(cmd)
                
    
    ## RDE
    
    rde_output_dir = os.path.join(options.scratch_dir,'rde_output_cli')
    
    if options.cli_working_dir is None:
        cmd = 'python -m megadetector.postprocessing.repeat_detection_elimination.find_repeat_detections'
    else:
        cmd = 'python  megadetector/postprocessing/repeat_detection_elimination/find_repeat_detections.py'
    cmd += ' {}'.format(inference_output_file)
    cmd += ' --imageBase {}'.format(image_folder)
    cmd += ' --outputBase {}'.format(rde_output_dir)
    cmd += ' --occurrenceThreshold 1' # Use an absurd number here to make sure we get some suspicious detections
    print('Running: {}'.format(cmd))
    cmd_results = execute_and_print(cmd)    
    
    # Find the latest filtering folder
    filtering_output_dir = os.listdir(rde_output_dir)
    filtering_output_dir = [fn for fn in filtering_output_dir if fn.startswith('filtering_')]
    filtering_output_dir = [os.path.join(rde_output_dir,fn) for fn in filtering_output_dir]
    filtering_output_dir = [fn for fn in filtering_output_dir if os.path.isdir(fn)]
    filtering_output_dir = sorted(filtering_output_dir)[-1]
    
    print('Using RDE filtering folder {}'.format(filtering_output_dir))
    
    filtered_output_file = inference_output_file.replace('.json','_filtered.json')
    
    if options.cli_working_dir is None:
        cmd = 'python -m megadetector.postprocessing.repeat_detection_elimination.remove_repeat_detections'
    else:
        cmd = 'python  megadetector/postprocessing/repeat_detection_elimination/remove_repeat_detections.py'
    cmd += ' {} {} {}'.format(inference_output_file,filtered_output_file,filtering_output_dir)
    print('Running: {}'.format(cmd))
    cmd_results = execute_and_print(cmd)
    
    assert os.path.isfile(filtered_output_file), \
        'Could not find RDE output file {}'.format(filtered_output_file)
    
    
    ## Run inference on a folder (tiled)
    
    image_folder = os.path.join(options.scratch_dir,'md-test-images')
    tiling_folder = os.path.join(options.scratch_dir,'tiling-folder')
    inference_output_file_tiled = os.path.join(options.scratch_dir,'folder_inference_output_tiled.json')
    if options.cli_working_dir is None:
        cmd = 'python -m megadetector.detection.run_tiled_inference'
    else:
        cmd = 'python megadetector/detection/run_tiled_inference.py'
    cmd += ' {} {} {} {}'.format(
        model_file,image_folder,tiling_folder,inference_output_file_tiled)
    cmd += ' --overwrite_handling overwrite'
    print('Running: {}'.format(cmd))
    cmd_results = execute_and_print(cmd)
    
    with open(inference_output_file_tiled,'r') as f:
        results_from_file = json.load(f) # noqa
        
    
    ## Run inference on a folder (augmented)
    
    if options.yolo_working_folder is None:
        
        print('Bypassing YOLOv5 val tests, no yolo folder supplied')
        
    else:
    
        image_folder = os.path.join(options.scratch_dir,'md-test-images')
        yolo_results_folder = os.path.join(options.scratch_dir,'yolo-output-folder')
        yolo_symlink_folder = os.path.join(options.scratch_dir,'yolo-symlink_folder')
        inference_output_file_yolo_val = os.path.join(options.scratch_dir,'folder_inference_output_yolo_val.json')
        if options.cli_working_dir is None:
            cmd = 'python -m megadetector.detection.run_inference_with_yolov5_val'
        else:
            cmd = 'python megadetector/detection/run_inference_with_yolov5_val.py'
        cmd += ' {} {} {}'.format(
            model_file,image_folder,inference_output_file_yolo_val)
        cmd += ' --yolo_working_folder {}'.format(options.yolo_working_folder)
        cmd += ' --yolo_results_folder {}'.format(yolo_results_folder)
        cmd += ' --symlink_folder {}'.format(yolo_symlink_folder)
        cmd += ' --augment_enabled 1'
        # cmd += ' --no_use_symlinks'
        cmd += ' --overwrite_handling overwrite'
        print('Running: {}'.format(cmd))
        cmd_results = execute_and_print(cmd)
        
        with open(inference_output_file_yolo_val,'r') as f:
            results_from_file = json.load(f) # noqa
        
        
    if not options.skip_video_tests:
            
        ## Video test
        
        model_file = 'MDV5A'
        video_inference_output_file = os.path.join(options.scratch_dir,'video_inference_output.json')
        output_video_file = os.path.join(options.scratch_dir,'video_scratch/cli_rendered_video.mp4')
        frame_folder = os.path.join(options.scratch_dir,'video_scratch/frame_folder_cli')
        frame_rendering_folder = os.path.join(options.scratch_dir,'video_scratch/rendered_frame_folder_cli')        
        
        video_fn = os.path.join(options.scratch_dir,options.test_videos[-1])
        output_dir = os.path.join(options.scratch_dir,'single_video_test_cli')
        if options.cli_working_dir is None:
            cmd = 'python -m megadetector.detection.process_video'
        else:
            cmd = 'python megadetector/detection/process_video.py'
        cmd += ' {} {}'.format(model_file,video_fn)
        cmd += ' --frame_folder {} --frame_rendering_folder {} --output_json_file {} --output_video_file {}'.format(
            frame_folder,frame_rendering_folder,video_inference_output_file,output_video_file)
        cmd += ' --render_output_video --fourcc mp4v'
        cmd += ' --force_extracted_frame_folder_deletion --force_rendered_frame_folder_deletion --n_cores 5 --frame_sample 3'
        print('Running: {}'.format(cmd))
        cmd_results = execute_and_print(cmd)

    # ...if we're not skipping video tests
    
    
    ## Run inference on a folder (again, so we can do a comparison)
    
    image_folder = os.path.join(options.scratch_dir,'md-test-images')
    model_file = 'MDV5B'
    inference_output_file_alt = os.path.join(options.scratch_dir,'folder_inference_output_alt.json')
    if options.cli_working_dir is None:
        cmd = 'python -m megadetector.detection.run_detector_batch'
    else:
        cmd = 'python megadetector/detection/run_detector_batch.py'
    cmd += ' {} {} {} --recursive'.format(
        model_file,image_folder,inference_output_file_alt)
    cmd += ' --output_relative_filenames --quiet --include_image_size'
    cmd += ' --include_image_timestamp --include_exif_data'
    print('Running: {}'.format(cmd))
    cmd_results = execute_and_print(cmd)
    
    with open(inference_output_file_alt,'r') as f:
        results_from_file = json.load(f) # noqa
    
    
    ## Compare the two files
    
    comparison_output_folder = os.path.join(options.scratch_dir,'results_comparison')
    image_folder = os.path.join(options.scratch_dir,'md-test-images')
    results_files_string = '"{}" "{}"'.format(
        inference_output_file,inference_output_file_alt)
    if options.cli_working_dir is None:
        cmd = 'python -m megadetector.postprocessing.compare_batch_results'
    else:
        cmd = 'python megadetector/postprocessing/compare_batch_results.py'
    cmd += ' {} {} {}'.format(comparison_output_folder,image_folder,results_files_string)
    print('Running: {}'.format(cmd))
    cmd_results = execute_and_print(cmd)
    
    assert cmd_results['status'] == 0, 'Error generating comparison HTML'
    assert os.path.isfile(os.path.join(comparison_output_folder,'index.html')), \
        'Failed to generate comparison HTML'
    
    print('\n*** Finished CLI tests ***\n')
    
# ...def run_cli_tests(...)


#%% Main test wrapper

def run_tests(options):
    """
    Runs Python-based and/or CLI-based package tests.
    
    Args:
        options (MDTestOptions): see MDTestOptions for details
    """
    
    # Prepare data folder
    download_test_data(options)    
    
    if options.disable_gpu:
        os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
        
    # Verify GPU
    gpu_available = is_gpu_available()
    
    # If the GPU is required and isn't available, error
    if options.cpu_execution_is_error and (not gpu_available):
        raise ValueError('GPU not available, and cpu_execution_is_error is set')
    
    # If the GPU should be disabled, verify that it is
    if options.disable_gpu:
        assert (not gpu_available), 'CPU execution specified, but the GPU appears to be available'
        
    # Run python tests
    if not options.skip_python_tests:
        run_python_tests(options)
    
    # Run CLI tests
    if not options.skip_cli_tests:
        run_cli_tests(options)


#%% Interactive driver

if False:
    
    pass

    #%%
    
    options = MDTestOptions()
    
    options.disable_gpu = False
    options.cpu_execution_is_error = False
    options.skip_video_tests = False
    options.skip_python_tests = False
    options.skip_cli_tests = False
    options.scratch_dir = None
    options.test_data_url = 'https://lila.science/public/md-test-package.zip'
    options.force_data_download = False
    options.force_data_unzip = False
    options.warning_mode = True
    options.max_coord_error = 0.001
    options.max_conf_error = 0.005
    options.cli_working_dir = r'c:\git\MegaDetector'
    options.yolo_working_folder = r'c:\git\yolov5'


    #%%
    
    run_tests(options)
    
    
#%% Command-line driver

def main():

    options = MDTestOptions()
    
    parser = argparse.ArgumentParser(
        description='MegaDetector test suite')
    
    parser.add_argument(
        '--disable_gpu',
        action='store_true',
        help='Disable GPU operation')
    
    parser.add_argument(
        '--cpu_execution_is_error',
        action='store_true',
        help='Fail if the GPU appears not to be available')
    
    parser.add_argument(
        '--scratch_dir',
        default=None,
        type=str,
        help='Directory for temporary storage (defaults to system temp dir)')
    
    parser.add_argument(
        '--skip_video_tests',
        action='store_true',
        help='Skip tests related to video (which can be slow)')
        
    parser.add_argument(
        '--skip_python_tests',
        action='store_true',
        help='Skip python tests')
        
    parser.add_argument(
        '--skip_cli_tests',
        action='store_true',
        help='Skip CLI tests')
        
    parser.add_argument(
        '--force_data_download',
        action='store_true',
        help='Force download of the test data file, even if it\'s already available')
    
    parser.add_argument(
        '--force_data_unzip',
        action='store_true',
        help='Force extraction of all files in the test data file, even if they\'re already available')
    
    parser.add_argument(
        '--warning_mode',
        action='store_true',
        help='Turns numeric/content errors into warnings')
    
    parser.add_argument(
        '--max_conf_error',
        type=float,
        default=options.max_conf_error,
        help='Maximum tolerable confidence value deviation from expected (default {})'.format(
            options.max_conf_error))
    
    parser.add_argument(
        '--max_coord_error',
        type=float,
        default=options.max_coord_error,
        help='Maximum tolerable coordinate value deviation from expected (default {})'.format(
            options.max_coord_error))

    parser.add_argument(
        '--cli_working_dir',
        type=str,
        default=None,
        help='Working directory for CLI tests')

    # token used for linting
    #
    # no_arguments_required
        
    args = parser.parse_args()
        
    options.disable_gpu = args.disable_gpu
    options.cpu_execution_is_error = args.cpu_execution_is_error
    options.skip_video_tests = args.skip_video_tests
    options.skip_python_tests = args.skip_python_tests
    options.skip_cli_tests = args.skip_cli_tests
    options.scratch_dir = args.scratch_dir
    options.warning_mode = args.warning_mode
    options.force_data_download = args.force_data_download
    options.max_conf_error = args.max_conf_error
    options.max_coord_error = args.max_coord_error
    options.cli_working_dir = args.cli_working_dir

    run_tests(options)
    
if __name__ == '__main__':
    main()
