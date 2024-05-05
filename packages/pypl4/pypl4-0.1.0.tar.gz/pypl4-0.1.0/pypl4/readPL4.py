import mmap
import struct

import numpy as np

from errors.ReadError import FileNotPL4Error
from pypl4.pl4 import PL4


def readfile(file: str) -> object:
    try:
        if '.pl4' in file:
            arq: object = open(file, 'rb')
        else:
            raise FileNotPL4Error
    except FileNotFoundError:
        raise FileNotFoundError('File not found!')
    except FileNotPL4Error:
        raise FileNotPL4Error('It is not a pl4 file!')
    else:
        return arq


def readPL4(pl4file: str):
    miscData = {
        'deltat': 0.0,
        'nvar': 0,
        'pl4size': 0,
        'steps': 0,
        'tmax': 0.0,
    }

    file = readfile(pl4file)
    pl4 = mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ)

    miscData['deltat'] = struct.unpack('<f', pl4[40:44])[0]
    miscData['nvar'] = struct.unpack('<L', pl4[48:52])[0] // 2
    miscData['pl4size'] = struct.unpack('<L', pl4[56:60])[0] - 1
    miscData['steps'] = (
        miscData['pl4size'] - 5 * 16 - miscData['nvar'] * 16
    ) // ((miscData['nvar'] + 1) * 4)
    miscData['tmax'] = (miscData['steps'] - 1) * miscData['deltat']

    dfHEAD = dict(TYPE=[], FROM=[], TO=[])

    for i in range(0, miscData['nvar']):
        pos = 5 * 16 + i * 16
        h = struct.unpack('3x1c6s6s', pl4[pos : pos + 16])
        dfHEAD['TYPE'].append(int(h[0]))
        dfHEAD['FROM'].append(h[1])
        dfHEAD['TO'].append(h[2])

    dfHEAD['FROM'] = [
        str(dfHEAD['FROM'][i].decode('utf-8')).replace(' ', '')
        for i in range(len(dfHEAD['FROM']))
    ]
    dfHEAD['TO'] = [
        str(dfHEAD['TO'][i].decode('utf-8')).replace(' ', '')
        for i in range(len(dfHEAD['TO']))
    ]

    expsize = (5 + miscData['nvar']) * 16 + miscData['steps'] * (
        miscData['nvar'] + 1
    ) * 4

    nullbytes = 0
    if miscData['pl4size'] > expsize:
        nullbytes = miscData['pl4size'] - expsize

    data = np.memmap(
        file,
        dtype=np.float32,
        mode='r',
        shape=(miscData['steps'], miscData['nvar'] + 1),
        offset=(5 + miscData['nvar']) * 16 + nullbytes,
    )

    file.close()

    return PL4(miscData, dfHEAD, data)
