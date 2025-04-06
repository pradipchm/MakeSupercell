import glob
import os
from .reorder_atoms import reorder_pdb, validate  # Import the reorder_atoms function

def batch_reorder(template_pdb="template.pdb"):
    """
    Batch processes all PDB files matching 'mol*.pdb' by reordering atoms.

    Parameters:
    ----------
    template_pdb : str
        Template PDB file used for reordering.
    """
    pdb_files = glob.glob("mol*.pdb")  # Find all matching PDB files
    if not pdb_files:
        print("No PDB files found.")
        return

    for file in pdb_files:
        output_file = file.replace(".pdb", "_reorder.pdb")

        reorder_pdb(mol_pdb_fname=file, template_pdb_fname=template_pdb, output_pdb_fname=output_file)
        validate(template_pdb_fname=template_pdb, output_pdb_fname=output_file)
if __name__ == "__main__":
    batch_reorder()
