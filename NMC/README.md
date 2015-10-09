#### BBP Neocortical Microcircuit to NeuroML 2

This directory contains code for converting cell models from the [Neocortical Microcircuit Collaboration Portal](https://bbp.epfl.ch/nmc-portal/microcircuit)
to NeuroML 2.

#### [Parser](parser)

This directory contains a number of examples of cell models in NEURON format downloaded as zip files from the NMC site, e.g. 
[L23_PC_cADpyr229_1](parser/L23_PC_cADpyr229_1). It also contains scripts in python for [parsing these](parser/ParseAll.py) 
and generating the corresponding cell models in NeuroML2.


#### [NeuroML 2 cell models](NeuroML2)

This directory contains a number of cell models exported in NeuroML 2 format, e.g. 
[cADpyr229_L23_PC_5ecbf9b163_0_0.cell.nml](https://github.com/OpenSourceBrain/BlueBrainProjectShowcase/blob/master/NMC/NeuroML2/cADpyr229_L23_PC_5ecbf9b163_0_0.cell.nml).

See [here](https://github.com/OpenSourceBrain/BlueBrainProjectShowcase/blob/master/NMC/NeuroML2/README.md) for more.


#### [NEURON code](NEURON)

This directory contains a number of the original NEURON files (e.g. the NMODL files) used for the BBP models. This directory 
is mainly used for testing the models and comparing the NeuroML2 versions to the original NEURON models.


#### OSB 3D Explorer

Cells and networks in valid NeuroML 2 can be visualised and analysed in the Open Source Brain 3D explorer. See 
[here](http://opensourcebrain.org/projects/blue-brain-project-showcase/repository/revisions/master/show/NMC/NeuroML2?explorer=https%3A%2F%2Fraw.githubusercontent.com%2FOpenSourceBrain%2FBlueBrainProjectShowcase%2Fmaster%2FNMC%2FNeuroML2%2FcADpyr232_L5_TTPC1_0fb1ca4724_0_0.cell.nml) for an example:


![OSB](https://raw.githubusercontent.com/OpenSourceBrain/BlueBrainProjectShowcase/master/NMC/NeuroML2/images/OSB.jpg)

