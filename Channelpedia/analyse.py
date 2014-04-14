import airspeed

MAX_COLOUR = (255, 0, 0)
MIN_COLOUR = (255, 255, 0)

def get_colour_hex(fract):
    rgb = [ hex(int(x + (y-x)*fract)) for x, y in zip(MIN_COLOUR, MAX_COLOUR) ]
    col = "#"
    for c in rgb: col+= ( c[2:4] if len(c)==4 else "00")
    return col

def merge_with_template(model, templfile):
    with open(templfile) as f:
        templ = airspeed.Template(f.read())
    return templ.merge(model)


def generate_lems(templfile, channel_file, channel, min_target_voltage, \
                  step_target_voltage, max_target_voltage, clamp_delay, \
                  clamp_duration, clamp_base_voltage):
                      
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
        print info

    model = {"channel_file":        channel_file, 
             "channel":             channel, 
             "target_voltages" :    target_voltages_map,
             "clamp_delay":         clamp_delay,
             "clamp_duration":      clamp_duration,
             "clamp_base_voltage":  clamp_base_voltage}

    merged = merge_with_template(model, templfile)

    return merged



if __name__ == '__main__':

    ####################   Main info  ####################

    templfile = "LEMS_Test_template.xml"
    channel_file = "HCN1.channel.nml"
    channel = "Channelpedia_HCN1_9"
    min_target_voltage = -100
    step_target_voltage = 20
    max_target_voltage = 20
    clamp_delay=25 
    clamp_duration=150
    clamp_base_voltage=-70
    
    new_lems_file = "LEMS_Test_HCN1.xml"
    
    #######################################################

    info = generate_lems(templfile, channel_file, channel, min_target_voltage, \
                      step_target_voltage, max_target_voltage, clamp_delay, \
                      clamp_duration, clamp_base_voltage)
                      
    print info
                      
    lf = open(new_lems_file, 'w')
    lf.write(info)
    lf.close()
                      
    
