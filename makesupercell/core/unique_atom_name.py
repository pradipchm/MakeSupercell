#!/usr/bin/env python

import argparse

def rename_atoms(input_pdb, output_pdb):
    """
    Rename atoms in a PDB file by appending numerical indices to element symbols.

    Parameters:
    input_pdb (str): Path to the input PDB file.
    output_pdb (str): Path to save the renamed PDB file.
    """
    atom_counters = {}

    with open(input_pdb, "r") as infile, open(output_pdb, "w") as outfile:
        for line in infile:
            if line.startswith(("HETATM", "ATOM")):
                atom_type = line[76:78].strip()  # Extract element symbol

                # Increment atom count
                atom_counters[atom_type] = atom_counters.get(atom_type, 0) + 1

                # Format new atom name (e.g., S1, O1, N1)
                new_atom_name = f"{atom_type}{atom_counters[atom_type]}"

                # Construct new line with updated atom name (PDB format ensures 4-character width)
                new_line = f"{line[:12]}{new_atom_name:<4}{line[16:]}"
                outfile.write(new_line)
            else:
                outfile.write(line)

    print(f"Renamed PDB saved as {output_pdb}")
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Rename atoms in a PDB file with unique identifiers.")
    parser.add_argument("--input", required=True, help="Input PDB file")
    parser.add_argument("--output", required=True, help="Output PDB file with renamed atoms")
    args = parser.parse_args()

    rename_atoms(args.input, args.output)