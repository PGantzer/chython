# -*- coding: utf-8 -*-
#
#  Copyright 2020-2023 Ramil Nugmanov <nougmanoff@protonmail.com>
#  This file is part of chython.
#
#  chython is free software; you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program; if not, see <https://www.gnu.org/licenses/>.
#
from ...exceptions import EmptyMolecule, InvalidCharge, InvalidV2000


common_isotopes = {'H': 1, 'He': 4, 'Li': 7, 'Be': 9, 'B': 11, 'C': 12, 'N': 14, 'O': 16, 'F': 19, 'Ne': 20, 'Na': 23,
                   'Mg': 24, 'Al': 27, 'Si': 28, 'P': 31, 'S': 32, 'Cl': 35, 'Ar': 40, 'K': 39, 'Ca': 40, 'Sc': 45,
                   'Ti': 48, 'V': 51, 'Cr': 52, 'Mn': 55, 'Fe': 56, 'Co': 59, 'Ni': 59, 'Cu': 64, 'Zn': 65, 'Ga': 70,
                   'Ge': 73, 'As': 75, 'Se': 79, 'Br': 80, 'Kr': 84, 'Rb': 85, 'Sr': 88, 'Y': 89, 'Zr': 91, 'Nb': 93,
                   'Mo': 96, 'Tc': 98, 'Ru': 101, 'Rh': 103, 'Pd': 106, 'Ag': 108, 'Cd': 112, 'In': 115, 'Sn': 119,
                   'Sb': 122, 'Te': 128, 'I': 127, 'Xe': 131, 'Cs': 133, 'Ba': 137, 'La': 139, 'Ce': 140, 'Pr': 141,
                   'Nd': 144, 'Pm': 145, 'Sm': 150, 'Eu': 152, 'Gd': 157, 'Tb': 159, 'Dy': 163, 'Ho': 165, 'Er': 167,
                   'Tm': 169, 'Yb': 173, 'Lu': 175, 'Hf': 178, 'Ta': 181, 'W': 184, 'Re': 186, 'Os': 190, 'Ir': 192,
                   'Pt': 195, 'Au': 197, 'Hg': 201, 'Tl': 204, 'Pb': 207, 'Bi': 209, 'Po': 209, 'At': 210, 'Rn': 222,
                   'Fr': 223, 'Ra': 226, 'Ac': 227, 'Th': 232, 'Pa': 231, 'U': 238, 'Np': 237, 'Pu': 244, 'Am': 243,
                   'Cm': 247, 'Bk': 247, 'Cf': 251, 'Es': 252, 'Fm': 257, 'Md': 258, 'No': 259, 'Lr': 260, 'Rf': 261,
                   'Db': 270, 'Sg': 269, 'Bh': 270, 'Hs': 270, 'Mt': 278, 'Ds': 281, 'Rg': 281, 'Cn': 285, 'Nh': 278,
                   'Fl': 289, 'Mc': 289, 'Lv': 293, 'Ts': 297, 'Og': 294}
_ctf_data = {'R': 'is_radical', 'C': 'charge', 'I': 'isotope'}
_charge_map = {'  0': 0, '  1': 3, '  2': 2, '  3': 1, '  4': 0, '  5': -1, '  6': -2, '  7': -3}


def parse_mol_v2000(data):
    line = data[3]

    atoms_count = int(line[0:3])
    bonds_count = int(line[3:6])
    if not atoms_count:
        raise EmptyMolecule

    log = []
    title = data[1].strip() or None
    atoms = []
    bonds = []
    stereo = []
    hydrogens = {}
    dat = {}

    for line in data[4: 4 + atoms_count]:
        try:
            charge = _charge_map[line[36:39]]
        except KeyError:
            raise InvalidCharge
        element = line[31:34].strip()
        isotope = line[34:36]

        if element in 'AL':
            raise ValueError('queries not supported')
        elif element == 'D':
            element = 'H'
            if isotope != ' 0':
                raise ValueError('isotope on deuterium atom')
            isotope = 2
        elif isotope != ' 0':
            try:
                isotope = common_isotopes[element] + int(isotope)
            except KeyError:
                raise ValueError('invalid element symbol')
        else:
            isotope = None

        mapping = line[60:63]
        atoms.append({'element': element, 'charge': charge, 'isotope': isotope, 'is_radical': False,
                      'mapping': int(mapping) if mapping else 0, 'x': float(line[0:10]), 'y': float(line[10:20]),
                      'z': float(line[20:30])})

    for line in data[4 + atoms_count: 4 + atoms_count + bonds_count]:
        a1, a2 = int(line[0:3]) - 1, int(line[3:6]) - 1
        s = line[9:12]
        if s == '  1':
            stereo.append((a1, a2, 1))
        elif s == '  6':
            stereo.append((a1, a2, -1))
        elif s != '  0':
            log.append(f'unsupported or invalid stereo: {line}')
        b = int(line[6:9])
        if b == 9:  # added ad-hoc for bond type 9
            b = 8
            log.append(f'coordinate bond replaced with special: {line}')
        bonds.append((a1, a2, b))

    for line in data[4 + atoms_count + bonds_count:]:
        if line.startswith('M  END'):
            break
        elif line.startswith('M  ALS'):
            raise ValueError('list of atoms not supported')
        elif line.startswith(('M  ISO', 'M  RAD', 'M  CHG')):
            _type = _ctf_data[line[3]]
            for i in range(int(line[6:9])):
                i8 = i * 8
                atom = int(line[10 + i8:13 + i8])
                if not atom or atom > len(atoms):
                    raise InvalidV2000('invalid atoms number')
                atom = atoms[atom - 1]
                atom[_type] = int(line[14 + i8:17 + i8])

        elif line.startswith('M  STY'):
            for i in range(int(line[6:9])):
                i8 = i * 8
                if (st := line[14 + i8:17 + i8]) == 'DAT':
                    dat[int(line[10 + i8:13 + i8])] = {}
                elif st == 'SUP':
                    dat[int(line[10 + i8:13 + i8])] = {'type': 'MDL_SUP'}
        elif line.startswith('M  SAL'):
            i = int(line[7:10])
            if i in dat:
                dat[i]['atoms'] = tuple(int(line[14 + 4 * i:17 + 4 * i]) - 1 for i in range(int(line[10:13])))
        elif line.startswith('M  SDT'):
            i = int(line[7:10])
            if i in dat:
                dat[i]['type'] = line.split()[-1].lower()
        elif line.startswith('M  SED'):
            i = int(line[7:10])
            if i in dat:
                dat[i]['value'] = line[10:].strip().replace('/', '').lower()
        elif line.startswith('M  SMT'):
            i = int(line[7:10])
            if i in dat:
                dat[i]['value'] = line[10:].strip()
        elif not line.startswith('M  SDD'):
            log.append(f'ignored line: {line}')

    for a in atoms:
        if a['is_radical']:  # int to bool
            a['is_radical'] = True
    for x in dat.values():
        try:
            _type = x['type']
            if _type == 'mrv_implicit_h':
                _atoms = x['atoms']
                value = x['value']
                if len(_atoms) != 1 or _atoms[0] == -1 or not value:
                    raise InvalidV2000(f'MRV_IMPLICIT_H spec invalid {x}')
                hydrogens[_atoms[0]] = int(value[6:])
            else:
                log.append(f'ignored data: {x}')
        except KeyError:
            raise InvalidV2000(f'Invalid SGROUP {x}')

    return {'title': title, 'atoms': atoms, 'bonds': bonds, 'stereo': stereo, 'hydrogens': hydrogens,
            'meta': None, 'log': log}


__all__ = ['parse_mol_v2000', 'common_isotopes']
