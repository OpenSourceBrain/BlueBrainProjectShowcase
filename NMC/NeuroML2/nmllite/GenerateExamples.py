from neuromllite import *
from neuromllite.NetworkGenerator import *
from neuromllite.utils import create_new_model
import sys

sys.path.append("..")

'''
bAC217_L4_MC_5fa0a62bd0_0_0.cell.nml      cADpyr229_L23_PC_c292d67a2e_0_0.cell.nml     cADpyr231_L6_TPC_L4_117b9dfb71_0_0.cell.nml  cNAC187_L1_HAC_f8c9772d9d_0_0.cell.nml    Soma_AllNML2.cell.nml
bNAC219_L1_DAC_a9ae5cbbf5_0_0.cell.nml    cADpyr230_L4_SS_1afeb14f17_0_0.cell.nml      cADpyr232_L5_TTPC1_0fb1ca4724_0_0.cell.nml   cNAC187_L23_NBC_9d37c4b1f8_0_0.cell.nml
cADpyr229_L23_PC_5ecbf9b163_0_0.cell.nml  cADpyr231_L6_TPC_L1_44f2206f70_0_0.cell.nml  cADpyr232_L5_UTPC_d736225429_0_0.cell.nml    cSTUT189_L23_LBC_e6e8f83407_0_0.cell.nml

'''
colors = {'RS':'0 0 0.8', 'FS':'0.8 0 0', 'LTS':'0 0 0.8', 'IB':'0.8 0 0', 'IBR':'0.8 0 0'}
colors = {'cADpyr229_L23_PC_c292d67a2e_0_0':'0 0 0.8', 'cNAC187_L23_NBC_9d37c4b1f8_0_0':'0.8 0 0'}

def generate(cell, duration=3000, config='IClamp',parameters = None):
    
    reference = "%s_%s"%(config, cell)

    cell_id = '%s'%cell
    cell_nmll = Cell(id=cell_id, neuroml2_source_file='../%s.cell.nml'%(cell))
 
    ################################################################################
    ###   Add some inputs
    
    if 'IClamp' in config:
        
        if not parameters:
            parameters = {}
            parameters['stim_amp'] = '350pA'
        
        input_source = InputSource(id='iclamp_0', 
                                   neuroml2_input='PulseGenerator', 
                                   parameters={'amplitude':'stim_amp', 'delay':'500ms', 'duration':'2000ms'})
      
        
    else:

        if not parameters:
            parameters = {}
            parameters['average_rate'] = '100 Hz'
            parameters['number_per_cell'] = '10'
            
        input_source = InputSource(id='pfs0', 
                                   neuroml2_input='PoissonFiringSynapse', 
                                   parameters={'average_rate':'average_rate', 
                                               'synapse':syn_exc.id, 
                                               'spike_target':"./%s"%syn_exc.id})
                                               
    sim, net = create_new_model(reference,
                     duration, 
                     dt=0.025, # ms 
                     temperature=34, # degC
                     default_region='Cortex',
                     parameters = parameters,
                     cell_for_default_population=cell_nmll,
                     color_for_default_population=colors[cell],
                     input_for_default_population=input_source)

    return sim, net



if __name__ == "__main__":
    
    if '-all' in sys.argv:
        for cell in colors:
            generate(cell, 3000, config="IClamp")
            
        
    else:
        
        #sim, net = generate('cADpyr229_L23_PC_c292d67a2e_0_0', 3000, config="IClamp")
        sim, net = generate('cNAC187_L23_NBC_9d37c4b1f8_0_0', 3000, config="IClamp",parameters={'stim_amp':'30pA'})
        
        check_to_generate_or_run(sys.argv, sim)
    
