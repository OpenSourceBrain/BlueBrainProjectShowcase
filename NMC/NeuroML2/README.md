## NeuroML 2 versions of BBP Neocortical Microcircuit Collaboration Portal cell models

The cell models which are available from the Blue Brain Project [Neocortical Microcircuit 
Collaboration Portal](https://bbp.epfl.ch/nmc-portal/microcircuit) are in NEURON format. These 
have been converted to [NeuroML 2](https://www.neuroml.org/neuromlv2) format using the code 
[here](https://github.com/OpenSourceBrain/BlueBrainProjectShowcase/tree/master/NMC/parser).

These are the cell models used in the publication: Reconstruction and Simulation of Neocortical Microcircuitry, Markram et al. 2015, [Cell, Volume 163, Issue 2, 456-492](http://www.cell.com/cell/pdf/S0092-8674%2815%2901191-5.pdf)

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

Image files of NeuroML 2 cells and networks can be generated in SVG format:

    jnml cADpyr229_L23_PC_5ecbf9b163_0_0.cell.nml -svg
    
![L23](https://raw.githubusercontent.com/OpenSourceBrain/BlueBrainProjectShowcase/master/NMC/NeuroML2/images/L23.png)

There is also a (less well developed) export to PNG format:

    jnml cADpyr229_L23_PC_5ecbf9b163_0_0.cell.nml -png


#### Analyse channel properties

Information can be extracted from ion channels in neuroML2 format using [pyNeuroML](https://github.com/NeuroML/pyNeuroML):

    pynml-channelanalysis NaTa_t.channel.nml  -erev 55 -stepTargetVoltage 10 -clampDuration 5 -i -duration 7 -clampDelay 1

![NaTa](https://raw.githubusercontent.com/OpenSourceBrain/BlueBrainProjectShowcase/master/NMC/NeuroML2/images/NaTa.png)


#### Map models to NEURON format

Install [NEURON](http://www.neuron.yale.edu/neuron/download). 

    jnml LEMS_L1_HAC_cNAC187_1.xml -neuron
    nrnivmodl
    nrngui LEMS_L1_HAC_cNAC187_1_nrn.py

![NEURON](https://raw.githubusercontent.com/OpenSourceBrain/BlueBrainProjectShowcase/master/NMC/NeuroML2/images/NEURON.png)


#### Visualise the cell models with the OSB 3D Explorer

Cells and networks in valid NeuroML 2 can be visualised and analysed in the Open Source Brain 3D explorer. See 
[here](http://opensourcebrain.org/projects/blue-brain-project-showcase/repository/revisions/master/show/NMC/NeuroML2?explorer=https%3A%2F%2Fraw.githubusercontent.com%2FOpenSourceBrain%2FBlueBrainProjectShowcase%2Fmaster%2FNMC%2FNeuroML2%2FcADpyr232_L5_TTPC1_0fb1ca4724_0_0.cell.nml) for an example:


![OSB](https://raw.githubusercontent.com/OpenSourceBrain/BlueBrainProjectShowcase/master/NMC/NeuroML2/images/OSB.jpg)


#### Current limitations

The majority of the cell models in the BBP circuit are fully deterministic, but there are some (stuttering cells) which include stochastic ion channels, which introduces random fluctuations into the voltage traces. The NEURON mechanism for this channel (StochKv) is [here](https://github.com/OpenSourceBrain/BlueBrainProjectShowcase/blob/master/NMC/NEURON/StochKv.mod). 

A deterministic version of this ion channel is used in the NeuroML2 models. A comparison of the stochastic and deterministic mod files can be found [here](https://github.com/OpenSourceBrain/BlueBrainProjectShowcase/tree/master/NMC/NEURON/test) and a NeuroML2/LEMS version of the stochastic StochKv channel model [is planned](https://github.com/OpenSourceBrain/BlueBrainProjectShowcase/issues/5).
