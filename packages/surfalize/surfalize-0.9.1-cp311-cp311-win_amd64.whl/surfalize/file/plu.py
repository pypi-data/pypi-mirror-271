import dateutil
import numpy as np
from .common import read_binary_layout, RawSurface

NON_MEASURED_VALUE = 1000001

DATE_SIZE = 128
COMMENT_SIZE = 256

LAYOUT_CALIBRATION = (
    ('yres', 'I', False),
    ('xres', 'I', False),
    ('N_tall', 'I', True),
    ('dy_multip', 'f', True),
    ('mppx', 'f', False),
    ('mppy', 'f', False),
    ('x_0', 'f', True),
    ('y_0', 'f', True),
    ('mpp_tall', 'f', True),
    ('z0', 'f', True)
)

LAYOUT_MEASURE_CONFIG = (
   ('type', 'I', True),
   ('algorithm', 'I', True),
   ('method', 'I', True),
   ('objective', 'I', True),
   ('area', 'I', True),
   ('xres_area', 'I', True),
   ('yres_area', 'I', True),
   ('xres', 'I', False),
   ('yres', 'I', False),
   ('na', 'I', True),
   ('incr_z', 'd', True),
   ('range', 'f', True),
   ('n_planes', 'I', True),
   ('tpc_umbral_F', 'I', True),
   ('restore', 'b', True),
   ('num_layers', 'b', True),
   ('version', 'b', True),
   ('config_hardware', 'b', True),
   ('stack_in_num', 'b', True),
   (None, 3, None),
   ('factorio_delmacio', 'I', True)
)

def read_plu(filepath, read_image_layers=False, encoding='utf-8'):
    with open(filepath, 'rb') as filehandle:
        date_block = filehandle.read(DATE_SIZE)
        timestamp = dateutil.parser.parse(date_block.decode().rstrip('\x00'))
        filehandle.seek(COMMENT_SIZE + 4, 1)
        calibration = read_binary_layout(filehandle, LAYOUT_CALIBRATION, encoding=encoding)
        measure_config = read_binary_layout(filehandle, LAYOUT_MEASURE_CONFIG, encoding=encoding)
        data_length = calibration['xres'] * calibration['yres']
        data = np.fromfile(filehandle, dtype=np.float32, count=data_length)
        image_layers = {}
        if read_image_layers:
            filehandle.seek(16, 1) # skip 16 bytes, no idea what they are doing
            img = np.fromfile(filehandle, dtype=np.uint8, count=data_length * 3)
            img = img.reshape(calibration['yres'], calibration['xres'], 3)
            if np.all((img[:, :, 0] == img[:, :, 1]) & (img[:, :, 0] == img[:, :, 2])):
                image_layers['Grayscale'] = img[:, :, 0]
            else:
                image_layers['RGB'] = img
    data = data.reshape((calibration['yres'], calibration['xres']))
    data[data == NON_MEASURED_VALUE] = np.nan

    step_x = calibration['mppx']
    step_y = calibration['mppy']

    metadata = {'timestamp': timestamp}

    return RawSurface(data, step_x, step_y, image_layers=image_layers, metadata=metadata)

