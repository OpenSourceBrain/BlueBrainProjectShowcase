
from pyneuroml import pynml
from neuroml import *
import os
import math


max_per_layer = 100
layers = ['L1','L23', 'L4', 'L5', 'L6']

radius = 210.0
t1=-165.0
t2=-149.0
t3=-353.0
t4=-190.0
t5=-526.0
t6=-700.0
ys = {}

ys['L1']=[0,t1]
ys['L23']=[t1,t1+t2+t3]
ys['L4']=[t1+t2+t3,t1+t2+t3+t4]
ys['L5']=[t1+t2+t3+t4,t1+t2+t3+t4+t5]
ys['L6']=[t1+t2+t3+t4+t5,t1+t2+t3+t4+t5+t6]



net_ref = "CellTypesPerLayer"
net_doc = NeuroMLDocument(id=net_ref)

net = Network(id=net_ref)
net_doc.networks.append(net)

count = 0

cells = {}
cells['L1'] = ['bNAC219_L1_DAC_a9ae5cbbf5_0_0.cell.nml', 
               'cNAC187_L1_HAC_f8c9772d9d_0_0.cell.nml']
cells['L23'] = ['cSTUT189_L23_LBC_e6e8f83407_0_0.cell.nml', 
                'cADpyr229_L23_PC_c292d67a2e_0_0.cell.nml']
cells['L4'] = ['bAC217_L4_MC_5fa0a62bd0_0_0.cell.nml',
               'cADpyr230_L4_SS_1afeb14f17_0_0.cell.nml']
cells['L5'] = ['cADpyr232_L5_TTPC1_0fb1ca4724_0_0.cell.nml',
               'cADpyr232_L5_UTPC_d736225429_0_0.cell.nml']
cells['L6'] = ['cADpyr231_L6_TPC_L1_44f2206f70_0_0.cell.nml',
               'cADpyr231_L6_TPC_L4_117b9dfb71_0_0.cell.nml']


cells['L1'] = ['bNAC219_L1_DAC_a9ae5cbbf5_0_0.cell.nml']
cells['L23'] = ['cADpyr229_L23_PC_c292d67a2e_0_0.cell.nml']
cells['L4'] = ['bAC217_L4_MC_5fa0a62bd0_0_0.cell.nml']
cells['L5'] = ['cADpyr232_L5_TTPC1_0fb1ca4724_0_0.cell.nml']
cells['L6'] = ['cADpyr231_L6_TPC_L1_44f2206f70_0_0.cell.nml']

for layer in ['L1','L23','L4','L5','L6']:
    for cell in cells[layer]:

        net_doc.includes.append(IncludeType(cell))
        bbp_ref = cell.split('.')[0]

        pop = Population(id="Pop_%s"%bbp_ref, component=bbp_ref, type="populationList")

        net.populations.append(pop)

        inst = Instance(id="0")
        pop.instances.append(inst)
        
	X=count*300
	Z=0

	Y = ys[layer][1] + 0.5*(ys[layer][0] - ys[layer][1])
        inst.location = Location(x=X, y=Y, z=Z)
        
        count+=1

net_file = '%s.net.nml'%(net_ref)
writers.NeuroMLWriter.write(net_doc, net_file)

print("Written network with %i cells in network to: %s"%(count,net_file))

pynml.nml2_to_svg(net_file)
