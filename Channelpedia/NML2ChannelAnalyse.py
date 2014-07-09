#!/usr/bin/env python

#
#
#   A script which can be run to generate a LEMS file to analyse the behaviour of channels in NeuroML 2
#   
#   For usage information type:
#       python NML2ChannelAnalyse.py
#
#  For a list of the dependencies for this script see https://github.com/OpenSourceBrain/BlueBrainProjectShowcase/blob/master/.travis.yml
#
#

import argparse

import neuroml.loaders as loaders

import airspeed
import sys
import os.path

TEMPLATE_FILE = "LEMS_Test_template.xml"
    
MAX_COLOUR = (255, 0, 0)
MIN_COLOUR = (255, 255, 0)

print("\n") 


def process_args():
    """ 
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser(description="A script which can be run to generate a LEMS file to analyse the behaviour of channels in NeuroML 2")

    parser.add_argument('channelFile', type=str, metavar='<NeuroML 2 Channel file>', 
                        help='Name of the NeuroML 2 file')
                        
    parser.add_argument('channelId', type=str, metavar='<Channel Id>', 
                        help='Id of the channel in the NeuroML 2 file ')
                        
    parser.add_argument('-v',
                        action='store_true',
                        default=False,
                        help="Verbose output")
                        
    parser.add_argument('-minV', 
                        type=int,
                        metavar='<min v>',
                        default=-100,
                        help='Minimum voltage to test (integer, mV)')
                        
    parser.add_argument('-maxV', 
                        type=int,
                        metavar='<max v>',
                        default=100,
                        help='Maximum voltage to test (integer, mV)')
                        
    parser.add_argument('-temperature', 
                        type=float,
                        metavar='<temperature>',
                        default=6.3,
                        help='Temperature (float, celsius)')
                        
                        
    return parser.parse_args()


def get_colour_hex(fract):
    rgb = [ hex(int(x + (y-x)*fract)) for x, y in zip(MIN_COLOUR, MAX_COLOUR) ]
    col = "#"
    for c in rgb: col+= ( c[2:4] if len(c)==4 else "00")
    return col

def merge_with_template(model, templfile):
    if not os.path.isfile(templfile):
        templfile = os.path.join(os.path.dirname(sys.argv[0]), templfile)
    with open(templfile) as f:
        templ = airspeed.Template(f.read())
    return templ.merge(model)


def generate_lems_channel_analyser(channel_file, channel, min_target_voltage, \
                      step_target_voltage, max_target_voltage, clamp_delay, \
                      clamp_duration, clamp_base_voltage, duration, erev, gates, temperature):
                      
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
             "gates":  gates,
             "temperature":  temperature}

    merged = merge_with_template(model, TEMPLATE_FILE)

    return merged

def main():

    args = process_args()
        
    verbose = args.v
    
    ## Get name of channel mechanism to test

    if verbose: print "Going to test channel from file: "+ args.channelFile
    
    step_target_voltage = 20
    clamp_delay=10 
    clamp_duration=80
    clamp_base_voltage=-70
    duration = 100
    erev = 0

    if not os.path.isfile(args.channelFile):
        print("File could not be found: %s!\n"%args.channelFile)
        exit(1)
    doc = loaders.NeuroMLLoader.load(args.channelFile)
    gates = []
    channels = []
    for c in doc.ion_channel_hhs: channels.append(c)
    for c in doc.ion_channel: channels.append(c)
    
    for ic in channels:
        print("Checking channel "+ic.id)
        if ic.id == args.channelId:
            for g in ic.gates:
                gates.append(g.id)
            for g in ic.gate_hh_tau_infs:
                gates.append(g.id)
               
    if len(gates) == 0:
        print("No gates found in a channel with ID %s"%args.channelId)
        exit()
    
    lems_content = generate_lems_channel_analyser(args.channelFile, args.channelId, args.minV, \
                      step_target_voltage, args.maxV, clamp_delay, \
                      clamp_duration, clamp_base_voltage, duration, erev, gates, args.temperature)
                      
    new_lems_file = "LEMS_Test_%s.xml"%args.channelId

                      
    lf = open(new_lems_file, 'w')
    lf.write(lems_content)
    lf.close()
        
    print("Written generated LEMS file to %s\n"%new_lems_file)
    
    


if __name__ == '__main__':
    main()
