import neuroml
import neuroml.writers as writers

import lems.api as lems

import xml.etree.ElementTree as ET

def channelpedia_xml_to_neuroml2(cpd_xml, nml2_file_name):
    
    print('Converting Channelpedia XML to NeuroML2')
    
    root = ET.fromstring(cpd_xml)
    print root.attrib
    for child in root:
        print child.tag, child.attrib
        
    channel_id='Channelpedia_%s_%s'%(root.attrib['ModelName'], root.attrib['ModelID'])
    
    doc = neuroml.NeuroMLDocument()
    
    ion = root.findall('Ion')[0]
    chan = neuroml.IonChannelHH(id=channel_id,
                          conductance='10pS',
                          species=ion.attrib['Name'],
                          notes="This is an automated conversion to NeuroML 2 of an ion channel model from Channelpedia. "
                          "\nThe original model can be found at: http://channelpedia.epfl.ch/ionchannels/%s"%root.attrib['ID'])
                          
    comp_types = {}
    for gate in root.findall('Gates'):
        
        gate_type= 'gateHHtauInf'
        g = neuroml.GateHHTauInf(id=gate.attrib['Name'],instances=int(float(gate.attrib['Power'])), type=gate_type)
        
        for inf in gate.findall('Inf_Alpha'):
            equation = check_equation(inf.findall('Equation')[0].text)
            new_comp_type = "%s_inf"%(channel_id)
            g.steady_state = neuroml.HHVariable(type=new_comp_type)
            
            comp_type = lems.ComponentType(new_comp_type, extends="baseVoltageDepVariable")

            comp_type.add(lems.Constant('TIME_SCALE', '1 ms', 'time'))
            comp_type.add(lems.Constant('VOLT_SCALE', '1 mV', 'voltage'))
     
            comp_type.dynamics.add(lems.DerivedVariable(name='x', dimension="none", value="%s"%equation, exposure="x"))
            comp_type.dynamics.add(lems.DerivedVariable(name='V', dimension="none", value="v / VOLT_SCALE"))
          
            comp_types[new_comp_type] = comp_type
            
        for tau in gate.findall('Tau_Beta'):
            equation = check_equation(tau.findall('Equation')[0].text)
            
            new_comp_type = "%s_tau"%(channel_id)
            g.time_course = neuroml.HHTime(type=new_comp_type)
            
            comp_type = lems.ComponentType(new_comp_type, extends="baseVoltageDepTime")

            comp_type.add(lems.Constant('TIME_SCALE', '1 ms', 'time'))
            comp_type.add(lems.Constant('VOLT_SCALE', '1 mV', 'voltage'))
     
            comp_type.dynamics.add(lems.DerivedVariable(name='t', dimension="none", value="(%s) * TIME_SCALE"%equation, exposure="t"))
            comp_type.dynamics.add(lems.DerivedVariable(name='V', dimension="none", value="v / VOLT_SCALE"))
          
            comp_types[new_comp_type] = comp_type
        
        chan.gates.append(g)
                          

    doc.ion_channel_hhs.append(chan)

    doc.id = channel_id

    writers.NeuroMLWriter.write(doc,nml2_file_name)

    print("Written NeuroML 2 channel file to: "+nml2_file_name)

    for comp_type_name in comp_types.keys():
        comp_type = comp_types[comp_type_name]
        ct_xml = comp_type.toxml().replace("><", ">\n    <")
        print("Adding definition for %s:\n%s\n"%(comp_type_name, ct_xml))
        nml2_file = open(nml2_file_name, 'r')
        orig = nml2_file.read()
        new_contents = orig.replace("</neuroml>", "    %s\n</neuroml>"%ct_xml)
        nml2_file.close()
        nml2_file = open(nml2_file_name, 'w')
        nml2_file.write(new_contents)
        nml2_file.close()
        

    ###### Validate the NeuroML ######    

    from neuroml.utils import validate_neuroml2

    validate_neuroml2(nml2_file_name)
    
def check_equation(eqn):
    eqn = eqn.replace("v", "V")
    eqn = eqn.replace("- -", "+")
    return eqn

if __name__ == '__main__':
    target = 'HCN1'
    test_file = target+'.xml'
    contents = open(test_file, 'r').read()
    channelpedia_xml_to_neuroml2(contents, target+'.channel.nml')


