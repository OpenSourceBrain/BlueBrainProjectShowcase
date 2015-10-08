## NeuroML 2 versions of BBP Neocortical Microcircuit Collaboration Portal cell models

The cell models which are available from the Blue Brain Project [Neocortical Microcircuit 
Collaboration Portal](https://bbp.epfl.ch/nmc-portal/microcircuit) are in NEURON format. These 
have been converted to [NeuroML 2](https://www.neuroml.org/neuromlv2) format using the code 
[here](https://github.com/OpenSourceBrain/BlueBrainProjectShowcase/tree/master/NMC/parser).

### Using the NeuroML 2 models

#### Installation

Install [jNeuroML](https://github.com/NeuroML/jNeuroML). Installation from source is 
recommended, using the latest development version, i.e.

    git clone git://github.com/NeuroML/jNeuroML.git neuroml_dev/jNeuroML
    cd neuroml_dev/jNeuroML
    python getNeuroML.py development

Ensure the `jnml` executable is present on your PATH. 

#### Validating the NeuroML 2 files

To check validity of the NeuroML2 files use:

    jnml -validate cNAC187_L1_HAC_f8c9772d9d_0_0.cell.nml

#### Convert cells and networks to graphical format

    jnml cNAC187_L1_HAC_f8c9772d9d_0_0.cell.nml -svg

#### Map models to NEURON format

    jnml LEMS_L1_HAC_cNAC187_1.xml -neuron
    nrnivmodl
    nrngui LEMS_L1_HAC_cNAC187_1_nrn.py