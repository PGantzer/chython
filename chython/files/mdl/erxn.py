# -*- coding: utf-8 -*-
#
#  Copyright 2020-2024 Ramil Nugmanov <nougmanoff@protonmail.com>
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
from .emol import parse_mol_v3000
from ...exceptions import EmptyMolecule, EmptyReaction, InvalidV2000


def parse_rxn_v3000(data, *, ignore=True):
    tmp = data[4][13:].split()
    reactants_count = int(tmp[0])
    products_count = int(tmp[1]) + reactants_count
    reagents_count = (int(tmp[2]) if len(tmp) == 3 else 0) + products_count

    if not reagents_count:
        raise EmptyReaction

    title = data[1].strip() or None
    log = []
    molecules = []

    start = 1
    for n in range(0, reagents_count):
        try:
            start = next(n for n, x in enumerate(data[start + 5:], start + 5) if x.startswith('M  V30 BEGIN CTAB'))
        except StopIteration:
            raise InvalidV2000

        try:
            molecules.append(parse_mol_v3000(data[start:], _header=False))
        except ValueError as e:
            if isinstance(e, EmptyMolecule):
                log.append(f'ignored empty molecule {n}')
            elif ignore:
                log.append(f'ignored molecule {n} with {e}')
            else:
                raise

            if (lm := len(molecules)) < reactants_count:
                reactants_count -= 1
                products_count -= 1
                reagents_count -= 1
            elif lm < products_count:
                products_count -= 1
                reagents_count -= 1
            else:
                reagents_count -= 1

    return {'reactants': molecules[:reactants_count], 'products': molecules[reactants_count:products_count],
            'reagents': molecules[products_count:], 'title': title, 'log': log}


__all__ = ['parse_rxn_v3000']
