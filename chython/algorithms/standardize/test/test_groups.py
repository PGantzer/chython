# -*- coding: utf-8 -*-
#
#  Copyright 2023 Ramil Nugmanov <nougmanoff@protonmail.com>
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
from chython import smiles
from pytest import mark


data = [
        ('CP(C)(C)C', 'C[P+](C)(C)C'),
        ('CB1(C)[H]B(C)(C)[H]1', 'CB1(C)~[H]B(C)(C)~[H]1'),
        ('[O]N(C)[NH]', '[O-][N+](C)=N'), ('[O]N(C)[CH2]', '[O-][N+](C)=C'),
        ('[O]S(C)(C)[O]', 'O=S(C)(C)=O'), ('[O]S(C)(C)[S]', 'O=S(C)(C)=S'),
        ('BN(C)=C', 'B~N(C)=C'),
        ('B=N(C)(C)C', 'B~N(C)(C)C'),
        ('BS(C)C', 'B~S(C)C'), ('BO(C)C', 'B~O(C)C'),
        ('[B-]=[N+](C)C', 'BN(C)C'), ('C[B-]=[N+]C', 'CBNC'), ('[B-]=[N+]', 'BN'),
        ('[O-][B+3]([O-])([O-])[O-]', 'O[B-](O)(O)O'),
        ('[O-]B(O)(O)O', 'O[B-](O)(O)O'),
        ('OB(O)(O)O', 'O[B-](O)(O)O'),
        ('CN(C)(C)C', 'C[N+](C)(C)C'),
        ('C=N(=O)O', 'C[N+](=O)[O-]'),
        ('C=N(=O)C', 'C=[N+]([O-])C'), ('O=N(=O)C', 'O=[N+]([O-])C'), ('N=N(=O)C', 'N=[N+]([O-])C'),
        ('C=[N+]([O-])O', 'C[N+](=O)[O-]'),
        ('CN(=O)=N(=O)C', 'C[N+]([O-])=[N+]([O-])C'),
        ('CN(=O)=N(=N)C', 'C[N+]([O-])=[N+]([NH-])C'), ('CN(=O)=N(=NC)C', 'C[N+]([O-])=[N+]([N-]C)C'),
        ('C=N(=N)C', 'C=[N+]([N-])C'), ('C=N(=NC)C', 'C=[N+]([N-]C)C'), ('N=N(=N)C', 'N=[N+]([N-])C'),
        ('[N-][N+](=O)C', 'N=[N+]([O-])C'), ('C[N-][N+](=O)C', 'CN=[N+]([O-])C'),
        ('[O-]N(=O)=O', '[O-][N+](=O)[O-]'),
        ('CN(:O):O', 'C[N+](=O)[O-]'),
        ('O=[N-]=O', '[O-]N=O'),
        ('O=N#N', 'O=[N+]=[N-]'), ('C=N#N', 'C=[N+]=[N-]'), ('N=N#N', 'N=[N+]=[N-]'),
        ('[O-][N+]#N', 'O=[N+]=[N-]'), ('C[CH-][N+]#N', 'CC=[N+]=[N-]'), ('[NH-][N+]#N', 'N=[N+]=[N-]'),
        ('C[N+]#N=[N-]', 'CN=[N+]=[N-]'),
        ('CN=N=N', 'CN=[N+]=[N-]'),
        ('CNN#N', 'CN=[N+]=[N-]'),
        ('[N-]#N=NC', '[N-]=[N+]=NC'),
        ('[N-]=N#N', '[N-]=[N+]=[N-]'),
        ('CC#N=N', 'CC=[N+]=[N-]'),
        ('CC#N=NC', 'CC#[N+][N-]C'), ('CC#N=O', 'CC#[N+][O-]'),
        ('NN#C', '[NH-][N+]#C'), ('ON#CC', '[O-][N+]#CC'), ('SN#CC', '[S-][N+]#CC'),
        ('CNN#C', 'C[N-][N+]#C'),
        ('N[N+]#[C-]', '[NH-][N+]#C'), ('O[N+]#[C-]', '[O-][N+]#C'), ('S[N+]#[C-]', '[S-][N+]#C'),
        ('CN[N+]#[C-]', 'C[N-][N+]#C'),
        ('CN#C', 'C[N+]#[C-]'),
        ('C[C-]=[N+]=N', 'CC=[N+]=[N-]'),

        ('OS(=N)(=N)O', 'O=S(N)(N)=O'), ('OS(=N)(=N)C', 'O=S(N)(=N)C')
]


@mark.parametrize('raw,result', data)
def test_group(raw, result):
    tmp = smiles(raw)
    tmp.standardize()
    assert tmp == smiles(result), f'{raw} > {tmp} != {result}'