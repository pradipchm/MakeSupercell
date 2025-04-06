import glob
import os
import subprocess
import argparse

from .core import ASE_cif_to_pymatgen_supercell_cif, batch_reorder
from .core import reorder_atoms, mapping_sequence, unique_atom_name

def convert_cif_to_sdf(cif_file, sdf_file):
    """Equivalent of PATH=/usr/bin:$PATH codcif2sdf input.cif > output.sdf"""
    # Create modified environment
    env = os.environ.copy()
    env['PATH'] = f"/usr/bin:{env['PATH']}"  # Prepend /usr/bin to existing PATH
    
    with open(sdf_file, 'w') as output_file:
        subprocess.run(
            ["codcif2sdf", cif_file],
            stdout=output_file,
            check=True,
            env=env
        )

def process_template(cif_file, matrix):

    cif_base = cif_file.split(".")[0]

    # Step 1: Convert CIF to PDB
    sdf_file = f"{cif_base}.sdf"
    pdb_file = f"{cif_base}.pdb"
    
    convert_cif_to_sdf(cif_file, sdf_file)


    subprocess.run(["obabel", sdf_file, "-O", pdb_file], check=True)

    # Step 2: Remove CONECT lines from PDB
    with open(pdb_file, "r") as f:
        lines = f.readlines()

    with open(pdb_file, "w") as f:
        for line in lines:
            if not line.startswith("CONECT"):
                f.write(line)

    # Step 3: Rename unique atom names (Assuming function is available)
    unique_pdb_file = f"{cif_base}_unique.pdb"
    unique_atom_name.rename_atoms(pdb_file, unique_pdb_file)

    # Step 4: Copy unique PDB as template
    subprocess.run(["cp", unique_pdb_file, "template.pdb"], check=True)

    # Step 5: Generate supercell CIF using ASE script with matrix (Assuming function is available)
    supercell_cif = "supercell.cif"
    ASE_cif_to_pymatgen_supercell_cif.make_supercell(cif_file, matrix, supercell_cif)

    # Step 6: Convert supercell CIF to SDF
    supercell_sdf = supercell_cif.replace(".cif", ".sdf")
    

    convert_cif_to_sdf(supercell_cif, supercell_sdf)
    
    # Step 7: Convert SDF to multiple PDBs
    subprocess.run(
        ["obabel", supercell_sdf, "-O", "mol.pdb", "-m", "--separate"], check=True
    )

    # Step 8: Remove CONECT lines from generated PDBs
    for pdb_file in os.listdir():
        if pdb_file.startswith("mol") and pdb_file.endswith(".pdb"):
            with open(pdb_file, "r") as f:
                lines = f.readlines()

            with open(pdb_file, "w") as f:
                for line in lines:
                    if not line.startswith("CONECT"):
                        f.write(line)

    # Step 9: Run batch reorder script (Assuming function is available)
    batch_reorder.batch_reorder()

    ## Step 10: Join reordered PDB files into a single supercell PDB
    pdb_files = glob.glob("mol*_reorder.pdb")

    if pdb_files:
        # Pass the expanded list of files to subprocess
        subprocess.run(
            ["obabel", *pdb_files, "-O", "supercell.pdb", "--join"], check=True
        )
    else:
        print("No matching files found.")

    # Step 11: Clean up intermediate PDB files
    for pdb_file in os.listdir():
        if pdb_file.startswith("mol") and pdb_file.endswith(".pdb"):
            os.remove(pdb_file)

    # Step 12: Perform final mapping sequence using template with matrix (Assuming function is available)
    reordered_supercell_pdb = f"{cif_base}_supercell_reorder.pdb"
    mapping_sequence.reorder_atoms(
        "template.pdb", "supercell.pdb", reordered_supercell_pdb, cif_file, matrix
    )

    print(
        f"Processing completed. Final reordered supercell PDB: {reordered_supercell_pdb}"
    )


def process_nontemplate(cif_file, matrix):

    cif_base = cif_file.split('.')[0]

    # Step 1: Convert CIF to PDB
    sdf_file = f"{cif_base}.sdf"
    pdb_file = f"{cif_base}.pdb"
    
    convert_cif_to_sdf(cif_file, sdf_file)

    subprocess.run(["obabel", sdf_file, "-O", pdb_file], check=True)

    # Step 2: Remove CONECT lines from PDB
    with open(pdb_file, 'r') as f:
        lines = f.readlines()

    with open(pdb_file, 'w') as f:
        for line in lines:
            if not line.startswith("CONECT"):
                f.write(line)

    # Step 3: Rename unique atom names (Assuming function is available)
    unique_pdb_file = f"{cif_base}_unique.pdb"
    unique_atom_name.rename_atoms(pdb_file, unique_pdb_file)

    # Step 4: Reorder atoms based on unique PDB (Assuming function is available)
    reordered_pdb_file = f"{cif_base}_reordered.pdb"
    reorder_atoms.reorder_pdb(unique_pdb_file, "template.pdb", reordered_pdb_file)
    reorder_atoms.validate(template_pdb_fname="template.pdb", output_pdb_fname=reordered_pdb_file)

    print("Atom reordering complete. Proceeding with supercell generation...")

    # Step 5: Generate supercell CIF using ASE script with matrix (Assuming function is available)
    supercell_cif = "supercell.cif"
    ASE_cif_to_pymatgen_supercell_cif.make_supercell(cif_file, matrix, supercell_cif)

    # Step 6: Convert supercell CIF to SDF
    supercell_sdf = supercell_cif.replace(".cif", ".sdf")
    # Execute the command with the updated environment
    convert_cif_to_sdf(supercell_cif, supercell_sdf)

    # Step 7: Convert SDF to multiple PDBs
    subprocess.run(["obabel", supercell_sdf, "-O", "mol.pdb", "-m", "--separate"], check=True)

    # Step 8: Remove CONECT lines from generated PDBs
    for pdb_file in os.listdir():
        if pdb_file.startswith("mol") and pdb_file.endswith(".pdb"):
            with open(pdb_file, 'r') as f:
                lines = f.readlines()

            with open(pdb_file, 'w') as f:
                for line in lines:
                    if not line.startswith("CONECT"):
                        f.write(line)
    # Step 9: Run batch reorder script (Assuming function is available)
    batch_reorder.batch_reorder()
    
    # Step 10: Join reordered PDB files into a single supercell PDB
    pdb_files = glob.glob("mol*_reorder.pdb")

    if pdb_files:
        subprocess.run(["obabel", *pdb_files, "-O", "supercell.pdb", "--join"], check=True)
    else:
        print("No matching files found.")

    # Step 11: Clean up intermediate PDB files
    for pdb_file in os.listdir():
        if pdb_file.startswith("mol") and pdb_file.endswith(".pdb"):
            os.remove(pdb_file)

    # Step 12: Perform final mapping sequence using reordered PDB as template
    reordered_supercell_pdb = f"{cif_base}_supercell_reorder.pdb"
    mapping_sequence.reorder_atoms(reordered_pdb_file, "supercell.pdb", reordered_supercell_pdb, cif_file, matrix)

    print(f"Processing completed. Final reordered supercell PDB: {reordered_supercell_pdb}")


def process_nontemplate_morethanone(cif_file, matrix):
    cif_base = cif_file.split('.')[0]

    # Step 1: Convert CIF to PDB
    sdf_file = f"{cif_base}.sdf"
    pdb_file = f"{cif_base}.pdb"
    
    # Run conversion
    convert_cif_to_sdf(cif_file, sdf_file)

    subprocess.run(["obabel", sdf_file, "-O", pdb_file], check=True)

    # Step 2: Remove CONECT lines from PDB
    with open(pdb_file, 'r') as f:
        lines = f.readlines()
    with open(pdb_file, 'w') as f:
        for line in lines:
            if not line.startswith("CONECT"):
                f.write(line)

    # Step 3: Convert SDF to multiple PDBs
    subprocess.run(["obabel", sdf_file, "-O", f"{cif_base}_mol.pdb", "-m", "--separate"], check=True)

    # Step 4: Remove CONECT lines from all generated PDB files
    for pdb in glob.glob(f"{cif_base}_mol*.pdb"):
        with open(pdb, 'r') as f:
            lines = f.readlines()
        with open(pdb, 'w') as f:
            for line in lines:
                if not line.startswith("CONECT"):
                    f.write(line)

    # Step 5: Reorder atoms in the first molecule
    reordered_pdb_file = f"{cif_base}_mol1_reorder.pdb"
    reorder_atoms.reorder_pdb (f"{cif_base}_mol1.pdb", "template.pdb", reordered_pdb_file)
    reorder_atoms.validate(template_pdb_fname="template.pdb", output_pdb_fname=reordered_pdb_file)
    print("Atom reordering complete. Proceeding with supercell generation...")

    # Step 6: Generate supercell CIF using ASE script with matrix
    supercell_cif = "supercell.cif"
    ASE_cif_to_pymatgen_supercell_cif.make_supercell(cif_file, matrix, supercell_cif)

    # Step 7: Convert supercell CIF to SDF
    supercell_sdf = supercell_cif.replace(".cif", ".sdf")
    # Execute the command with the updated environment
    convert_cif_to_sdf(supercell_cif, supercell_sdf)

    # Step 8: Convert SDF to multiple PDBs
    subprocess.run(["obabel", supercell_sdf, "-O", "mol.pdb", "-m", "--separate"], check=True)
    
    # Step 9: Remove CONECT lines from generated PDBs
    for pdb_file in glob.glob("mol*.pdb"):
        with open(pdb_file, 'r') as f:
            lines = f.readlines()
        with open(pdb_file, 'w') as f:
            for line in lines:
                if not line.startswith("CONECT"):
                    f.write(line)

    # Step 10: Run batch reorder script
    batch_reorder.batch_reorder()

    # Step 11: Join reordered PDB files into a single supercell PDB
    pdb_files = glob.glob("mol*_reorder.pdb")
    if pdb_files:
        subprocess.run(["obabel", *pdb_files, "-O", "supercell.pdb", "--join"], check=True)
    else:
        print("No matching reordered files found.")

    # Step 12: Clean up intermediate PDB files
    for pdb_file in glob.glob("mol*.pdb"):
        os.remove(pdb_file)

    # Step 13: Perform final mapping sequence using reordered PDB as template
    reordered_supercell_pdb = f"{cif_base}_supercell_reorder.pdb"
    mapping_sequence.reorder_atoms("template.pdb", "supercell.pdb", reordered_supercell_pdb, cif_file, matrix)

    print(f"Processing completed. Final reordered supercell PDB: {reordered_supercell_pdb}")

