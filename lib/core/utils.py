
from pandas import DataFrame
import numpy as np

def jump_to_keyword(fid, keyword):
    while True:
        line = fid.readline()
        if not line:
            return None
        elif keyword in line:
            return line

def parse_klarf(klarf_path):
    """
    parse klarf format file and return a pandas dataframe
    """

    fid = open(klarf_path)

    ## read Defect Record Spec
    rows = list()
    while True:
        line_image_name = jump_to_keyword(fid, 'TiffFileName')
        if not line_image_name:
            break
        if not jump_to_keyword(fid, 'DefectList'):
            break
        line_attr = fid.readline()

        image_name = line_image_name.strip(';\n').split(' ')[-1]
        attr = line_attr.strip(';\n').split(' ')
        rows.append([image_name] + attr)

    fid.seek(0)
    line_specs = jump_to_keyword(fid, 'DefectRecordSpec')
    specs = line_specs.strip(';\n').split(' ')[2:]
    cols = ['IMAGENAME'] + specs

    rows = np.array(rows)
    cols = np.array(cols)

    assert len(cols) <= rows.shape[1], "#DefectRecordSpec mismatch"
    rows = rows[:,:len(cols)]

    df = DataFrame(rows, columns=cols)

    ## read other info
    fid.seek(0)
    line_die_size = jump_to_keyword(fid, 'DiePitch')
    wh = line_die_size.strip(';\n').split(' ')[1:]
    die_size = float(wh[0]), float(wh[1])

    ## get setup id
    fid.seek(0)
    line_setup = jump_to_keyword(fid, 'SetupID')
    setup_id = line_setup.split(' ')[1].strip('"')
    
    
    fid.close()

    return dict(
        defects = df,
        die_size_xy = die_size,
        setup_id = setup_id
    )