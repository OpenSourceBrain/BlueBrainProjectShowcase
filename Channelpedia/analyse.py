import airspeed

TEMPLATE_FILE = "LEMS_Test_template.xml"
    
MAX_COLOUR = (255, 0, 0)
MIN_COLOUR = (255, 255, 0)

known_parameters = {}
#                                             low v,   step,  hi v,  delay,  duration,  base v, tot dur, erev                                
known_parameters["Channelpedia_HCN1_9"] =     (-100,   20,    20,    25,     150,       -70,    200,     80)                              
known_parameters["Channelpedia_Ca_P_Q_5"] =   (-60,    10,    90,    1,      10,        -70,    12,      135.0)                        
known_parameters["Channelpedia_Ih_14"] =      (-120,   10,   -40,    100,    700,       -40,    1000,    -45)                   
known_parameters["Channelpedia_Kir21_44"] =   (-180,   10,     0,    100,    600,       0,      800,     135)


def get_colour_hex(fract):
    rgb = [ hex(int(x + (y-x)*fract)) for x, y in zip(MIN_COLOUR, MAX_COLOUR) ]
    col = "#"
    for c in rgb: col+= ( c[2:4] if len(c)==4 else "00")
    return col

def merge_with_template(model, templfile):
    with open(templfile) as f:
        templ = airspeed.Template(f.read())
    return templ.merge(model)


def generate_lems_channel_analyser_(channel_file, channel, gates):

    if known_parameters.has_key(channel):
        params = known_parameters[channel]
        min_target_voltage = params[0]
        step_target_voltage = params[1]
        max_target_voltage = params[2]
        clamp_delay = params[3]
        clamp_duration = params[4]
        clamp_base_voltage = params[5]
        duration = params[6]
        erev = params[7]
        
    else:
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
                      clamp_duration, clamp_base_voltage, duration, erev, gates)

def generate_lems_channel_analyser(channel_file, channel, min_target_voltage, \
                      step_target_voltage, max_target_voltage, clamp_delay, \
                      clamp_duration, clamp_base_voltage, duration, erev, gates):
                      
    target_voltages = []
    v = min_target_voltage
    while v <= max_target_voltage:
        target_voltages.append(v)
        v+=step_target_voltage

    target_voltages_map = []
    for t in target_voltages:
        fract = float(target_voltages.index(t)) / (len(target_voltages)-1)
        info = {}
        info["v"] = t
        info["v_str"] = str(t).replace("-", "min")
        info["col"] = get_colour_hex(fract)
        target_voltages_map.append(info)
        #print info

    model = {"channel_file":        channel_file, 
             "channel":             channel, 
             "target_voltages" :    target_voltages_map,
             "clamp_delay":         clamp_delay,
             "clamp_duration":      clamp_duration,
             "clamp_base_voltage":  clamp_base_voltage,
             "duration":  duration,
             "erev":  erev,
             "gates":  gates}

    merged = merge_with_template(model, TEMPLATE_FILE)

    return merged



if __name__ == '__main__':


    channel_file = "HCN1.channel.nml"
    channel = "Channelpedia_HCN1_9"
    new_lems_file = "LEMS_Test_HCN1.xml"

    info = generate_lems_channel_analyser_(channel_file, channel, ["m"])
                      
    print info
                      
    lf = open(new_lems_file, 'w')
    lf.write(info)
    lf.close()
                  
    channel_file = "Cav2.1.channel.nml"
    channel = "Channelpedia_Ca_P_Q_5"
    new_lems_file = "LEMS_Test_Cav2.1.xml"

    info = generate_lems_channel_analyser_(channel_file, channel, ["m"])
                      
    print info
                      
    lf = open(new_lems_file, 'w')
    lf.write(info)
    lf.close()
                      
    
