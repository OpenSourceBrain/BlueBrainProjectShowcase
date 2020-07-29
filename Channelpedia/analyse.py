from pyneuroml.analysis.NML2ChannelAnalysis import generate_lems_channel_analyser

known_parameters = {}
#                                             low v,   step,  hi v,  delay,  duration,  base v, tot dur, erev                                
known_parameters["Channelpedia_HCN1_9"] =     (-120,   10,    -40,    25,     150,       -40,    200,     -45)                              
known_parameters["Channelpedia_Ca_P_Q_5"] =   (-60,    10,    90,    1,      10,        -70,    12,      135.0)                        
known_parameters["Channelpedia_Ih_14"] =      (-120,   10,   -40,    100,    700,       -40,    1000,    -45)                   
known_parameters["Channelpedia_Kir21_44"] =   (-180,   10,     0,    100,    600,       0,      800,     135)
         
default_parameters = {}

default_parameters["na"] =                    (-100,   20,     100,   20,    100,       0,      140,     55)
default_parameters["k"] =                     (-100,   20,     100,   20,    400,       0,      500,     -80)
default_parameters["ca"] =                    (-100,   20,     100,   50,    400,       0,      500,     120)


def generate(channel_file, channel, gates, temperature, ion = '?'):
    
    print("Generating LEMS analyser for %s"%channel_file)
    ca_conc = 1e-5
    ion = ion.lower()
    print('---- Generating for %s in %s (gates: %s) with ion: %s'%(channel, channel_file, gates, ion))
    if channel in known_parameters:
        params = known_parameters[channel]
        print('Using:')
        print(params)
        min_target_voltage = params[0]
        step_target_voltage = params[1]
        max_target_voltage = params[2]
        clamp_delay = params[3]
        clamp_duration = params[4]
        clamp_base_voltage = params[5]
        duration = params[6]
        erev = params[7]
        
    elif ion in default_parameters:
        params = default_parameters[ion]
        print('Using:')
        print(params)
        min_target_voltage = params[0]
        step_target_voltage = params[1]
        max_target_voltage = params[2]
        clamp_delay = params[3]
        clamp_duration = params[4]
        clamp_base_voltage = params[5]
        duration = params[6]
        erev = params[7]
        
    else:
        print('Using defaults!')
        min_target_voltage = -100
        step_target_voltage = 20
        max_target_voltage = 20
        clamp_delay=25 
        clamp_duration=150
        clamp_base_voltage=-70
        duration = 100
        erev = 0
        
    return generate_lems_channel_analyser(channel_file, channel, min_target_voltage, \
                      step_target_voltage, max_target_voltage, clamp_delay, \
                      clamp_duration, clamp_base_voltage, duration, erev, gates, temperature, ca_conc, False)


if __name__ == '__main__':


    channel_file = "HCN1.channel.nml"
    channel = "Channelpedia_HCN1_9"
    new_lems_file = "LEMS_Test_HCN1.xml"

    info = generate(channel_file, channel, ["m"], 32)
                      
    print(info)
                      
    lf = open(new_lems_file, 'w')
    lf.write(info)
    lf.close()
                  
    channel_file = "Cav2.1.channel.nml"
    channel = "Channelpedia_Ca_P_Q_5"
    new_lems_file = "LEMS_Test_Cav2.1.xml"

    info = generate(channel_file, channel, ["m"], 32)
                      
    print(info)
                      
    lf = open(new_lems_file, 'w')
    lf.write(info)
    lf.close()
    
    
    '''           
    channel_file = "../../../testChanMV/inact_kv.channel.nml"
    channel = "inact_kv"
    new_lems_file = "LEMS_Test_inact_kv.xml"

    info = generate_lems_channel_analyser_(channel_file, channel, ["n", "h"], 32)
                      
    print info
                      
    lf = open(new_lems_file, 'w')
    lf.write(info)
    lf.close()'''
                      
    
