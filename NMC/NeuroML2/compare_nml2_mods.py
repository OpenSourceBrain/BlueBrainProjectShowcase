
import matplotlib.pyplot as pylab
import os.path


chans = ['K_Tst', 'K_Pst', 'NaTa_t', 'Nap_Et2', 'NaTs2_t', 'Ih', 'Ca_LVAst', 'Ca_HVA', 'SKv3_1', 'KdShu2007']

problematic = ['Im']

gates = ['m', 'h']

for channel_id in chans:
    

    vramp_lems_file  = '%s.rampV.lems.dat'%(channel_id)

    ts = []
    volts = []
    for line in open(vramp_lems_file):
        ts.append(float(line.split()[0])*1000)
        volts.append(float(line.split()[1])*1000)
    
    fig = pylab.figure()
    fig.canvas.set_window_title("Time Course(s) of activation variables of %s"%(channel_id))

    pylab.xlabel('Membrane potential (mV)')
    pylab.ylabel('Time Course - tau (ms)')
    pylab.grid('on')

    for gate in gates:
        
        tau_lems_file  = '%s.%s.tau.lems.dat'%(channel_id, gate)
        
        if os.path.isfile(tau_lems_file):
            taus = []
            for line in open(tau_lems_file):
                ts.append(float(line.split()[0])*1000)
                taus.append(float(line.split()[1])*1000)

            pylab.plot(volts, taus, linestyle='-', linewidth=2, label="LEMS %s %s tau"%(channel_id, gate))

            tau_mod_file  = '../NEURON/%s.%s.tau.dat'%(channel_id, gate)
            vs = []
            taus = []
            for line in open(tau_mod_file):
                vs.append(float(line.split()[0]))
                taus.append(float(line.split()[1]))

            pylab.plot(vs, taus, '--x', label="Mod %s %s tau"%(channel_id, gate))
            
            
    pylab.legend()
    
    
    fig = pylab.figure()
    fig.canvas.set_window_title("Steady state(s) of activation variables of %s"%(channel_id))

    pylab.xlabel('Membrane potential (mV)')
    pylab.ylabel('Steady state (inf)')
    pylab.grid('on')

    for gate in gates:
        
        inf_lems_file  = '%s.%s.inf.lems.dat'%(channel_id, gate)
        
        if os.path.isfile(inf_lems_file):
            infs = []
            for line in open(inf_lems_file):
                infs.append(float(line.split()[1]))

            pylab.plot(volts, infs, linestyle='-', linewidth=2, label="LEMS %s %s inf"%(channel_id, gate))
            
            inf_mod_file  = '../NEURON/%s.%s.inf.dat'%(channel_id, gate)
            vs = []
            infs = []
            for line in open(inf_mod_file):
                vs.append(float(line.split()[0]))
                infs.append(float(line.split()[1]))

            pylab.plot(vs, infs, '--x', label="Mod %s %s inf"%(channel_id, gate))
            
    pylab.legend()
    
pylab.show()
