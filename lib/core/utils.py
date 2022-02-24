
from pandas import DataFrame
import numpy as np

def jump_to_keyword(fid, keyword):
    while True:
        try:
            line = next(fid)
        except:
            return None
        if keyword in line:
            return line


def parse_klarf_lines(klarf_lines):
    """
    parse klarf content (list of strings) and return a pandas dataframe
    """
    ## read Defect Record Spec
    rows = list()
    fid = iter(klarf_lines)
    while True:
        line_image_name = jump_to_keyword(fid, 'TiffFileName')
        if not line_image_name:
            break
        if not jump_to_keyword(fid, 'DefectList'):
            break
        line_attr = next(fid)

        image_name = line_image_name.strip(';\n').split(' ')[-1]
        attr = line_attr.strip(';\n').split(' ')
        rows.append([image_name] + attr)

    fid = iter(klarf_lines)
    line_specs = jump_to_keyword(fid, 'DefectRecordSpec')
    specs = line_specs.strip(';\n').split(' ')[2:]
    cols = ['IMAGENAME'] + specs

    rows = np.array(rows)
    cols = np.array(cols)

    if rows.size > 0:
        assert len(cols) <= rows.shape[1], "#DefectRecordSpec mismatch"
        rows = rows[:,:len(cols)]
    else:
        rows = rows.reshape([-1, len(cols)])

    df = DataFrame(rows, columns=cols)

    ## read other info
    fid = iter(klarf_lines)
    line_die_size = jump_to_keyword(fid, 'DiePitch')
    wh = line_die_size.strip(';\n').split(' ')[1:]
    die_size = float(wh[0]), float(wh[1])

    ## get setup id
    fid = iter(klarf_lines)
    line_setup = jump_to_keyword(fid, 'SetupID')
    setup_id = line_setup.split(' ')[1].strip('"')

    ## get device id
    fid = iter(klarf_lines)
    line_device = jump_to_keyword(fid, 'DeviceID')
    device_id = line_device.split('"')[1].strip(";")

    ## get lot id
    fid = iter(klarf_lines)
    line = jump_to_keyword(fid, 'LotID')
    lot_id = line.split('"')[1].strip(";")

    ## get step id
    fid = iter(klarf_lines)
    line = jump_to_keyword(fid, 'StepID')
    step_id = line.split('"')[1].strip(";")

    ## get wafer id
    fid = iter(klarf_lines)
    line = jump_to_keyword(fid, 'WaferID')
    wafer_id = line.split('"')[1].strip(";")

    return dict(
        defects = df,
        die_size_xy = die_size,
        setup_id = setup_id,
        device_id = device_id,
        lot_id = lot_id,
        step_id = step_id,
        wafer_id = wafer_id
    )


def parse_klarf(klarf_path):
    """
    parse klarf format file and return a pandas dataframe
    """
    with open(klarf_path) as fid:
        klarf_lines = [line for line in fid.readlines()]

    return parse_klarf_lines(klarf_lines)