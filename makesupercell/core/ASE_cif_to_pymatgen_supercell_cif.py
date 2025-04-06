#!/usr/bin/env python

from ase.io import read
from pymatgen.io.ase import AseAtomsAdaptor

def make_supercell(cif_input, cell_matrix, cif_output):

    """
    Function generates a supecell from a single molecule cif file.

    Parameters:
    ----------

    cif_input : str
        cif file for the single molecule
    cell_matrix : number array (e.g : 3,3,3)
        the matrix of the suprecell, how much the cell will replicate in three directions
    cif_output : str
        cif file of generated suprecell

    """
    atoms = read(cif_input)
    matrix = list(map(int, cell_matrix.split(',')))
    pymatgen_struc = AseAtomsAdaptor.get_structure(atoms)
    supercell = pymatgen_struc.make_supercell(matrix)
    supercell.to(filename=cif_output)

    if __name__ == '__main__':
        import argparse
        parser = argparse.ArgumentParser(description='Generate PBC supercell from cif file',
                                        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        parser.add_argument('--input', metavar='cif file', default='in.cif',
                            help='(in) file name of the original cif file')
        parser.add_argument('--matrix', metavar='list of numbers', default='3,3,3',
                            help='(in) size of the supercell in all three directions')
        parser.add_argument('--output', metavar='cif file', default='out.cif',
                            help='(out) file name for the supercell')

        args = parser.parse_args()
        make_supercell(args.input, args.matrix, args.output)
