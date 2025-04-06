MakeSupercell
==============================
[//]: # (Badges)
[![GitHub Actions Build Status](https://github.com/REPLACE_WITH_OWNER_ACCOUNT/makesupercell/workflows/CI/badge.svg)](https://github.com/REPLACE_WITH_OWNER_ACCOUNT/makesupercell/actions?query=workflow%3ACI)
[![codecov](https://codecov.io/gh/REPLACE_WITH_OWNER_ACCOUNT/MakeSupercell/branch/main/graph/badge.svg)](https://codecov.io/gh/REPLACE_WITH_OWNER_ACCOUNT/MakeSupercell/branch/main)


A python package to generate supercell from CIF with unique atom sequence for all polymoprhs of a molecular crystal.

## Authors:
- [Pradip Si](https://www.valsson.info/members/pradip-si), University of North Texas

## Requirments
- ASE
- Pymatgen
- Rdkit
- Open babel
- NumPy
- COD Tools [cod-tools](https://wiki.crystallography.net/cod-tools/)

## Instructions 
1. Add missing Hs if required for any polymorphs and generate new CIF with added Hs.

2. Select one polymorphs as a template (preferably choose a unit cell with one molecule).

#### Use three main modules for template and non-template (with one and more than one molecule) polymorphs to make the supercell.
```
import makesupercell
makesupercell.process_template("1241883.cif", "3,3,3") 
makesupercell.process_nontemplate("2008952.cif", "3,3,3")
makesupercell.process_nontemplate_morethanone("1822444.cif", "3,3,3")
```


## Acknowledgements
The development of this tool was supported by a DOE Early Career Award (BES Condensed Phase and Interfacial Molecular Science (CPIMS) / DE-SC0024283)



### Copyright

Copyright (c) 2025, Pradip Si


#### Acknowledgements
 
Project based on the 
[Computational Molecular Science Python Cookiecutter](https://github.com/molssi/cookiecutter-cms) version 1.10.
