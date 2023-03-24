#!/bin/bash
set -ex

python ChannelpediaToNeuroML2.py HCN1
pynml LEMS_Test_HCN1.xml &

python ChannelpediaToNeuroML2.py Cav2.1
pynml LEMS_Test_Cav2.1.xml &

 
