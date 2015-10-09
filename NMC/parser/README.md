**Still in development!**
**Use with caution!**

These are scripts to facilitate extracting NeuroML2 versions of the BBP cell models.

This is based on the export_to_neuroml2() method in PyNeuroML, with some BBP specific extras.

Requirements:
* Latest github version of pyNeuroML (pypi version is too old): https://github.com/NeuroML/pyNeuroML
* To install the pyNeuroML dependencies, see: https://github.com/NeuroML/pyNeuroML/issues/13
* Neuron with python support, in case you want to run the parser in parallel Neuron should be compiled without X11 support

To execute these scripts, first run:

    nrnivmodl ../NEURON/

This compiles the NMODL files for the ion channels into this directory. Then type:

    python  ParseAll.py

To run the parallel version of the parser:
    
    python ParseAll.py -parallel
