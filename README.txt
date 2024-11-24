Kumar, A., Shahul, A. K., & Bhalla, U. S. (2024). Mechanisms and implications of high depolarization baseline offsets in conductance-based neuronal models (p. 2024.01.11.575308). bioRxiv. https://doi.org/10.1101/2024.01.11.575308


Requirements:
1. A debian based linux system such as Ubuntu or Linux mint. All codes will work on WSL in Windows too. Other systems were not tested.
2. python3.8-3.12. Not tested on other python versions.
3. pymoose (must be built from source by following the instructions here - https://github.com/BhallaLab/moose-core)
4. NEURON with python support (https://nrn.readthedocs.io/en/8.2.6/)

Requirements to regenerate data:
5. goMultiprocessing (https://github.com/analkumar2/parallelize-forloops)
6. brute_curvefit (https://github.com/analkumar2/brute_curvefit)

Folder descriptions:
expdata - Contains raw experimental data
Fig1-9, SuppFigS1 - Contatins scripts to generate paper figures
FigAbstract - Abstract figure
helperScripts - Contains script to generate some data and utility scripts
Kinetics - Contains files that describe ion channel kinetics used in this study
