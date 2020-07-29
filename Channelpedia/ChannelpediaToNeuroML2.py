import neuroml
import neuroml.writers as writers

import lems.api as lems

import xml.etree.ElementTree as ET

# This is available at https://github.com/OpenSourceBrain/OSB_API
import osb.metadata
import osb.resources

import sys


def channelpedia_xml_to_neuroml2(cpd_xml, nml2_file_name, unknowns=""):
    
    
    info = 'Automatic conversion of Channelpedia XML file to NeuroML2\n'+\
           'Uses: https://github.com/OpenSourceBrain/BlueBrainProjectShowcase/blob/master/Channelpedia/ChannelpediaToNeuroML2.py'
    print(info)
    
    root = ET.fromstring(cpd_xml)
        
    channel_id='Channelpedia_%s_%s'%(root.attrib['ModelName'].replace("/","_").replace(" ","_").replace(".","_"), root.attrib['ModelID'])
    
    doc = neuroml.NeuroMLDocument()
    
    metadata = osb.metadata.RDF(info)
    
    
    ion = root.findall('Ion')[0]
    chan = neuroml.IonChannelHH(id=channel_id,
                          conductance='10pS',
                          species=ion.attrib['Name'],
                          notes="This is an automated conversion to NeuroML 2 of an ion channel model from Channelpedia. "+
                          "\nThe original channel model file can be found at: http://channelpedia.epfl.ch/ionchannels/%s"%root.attrib['ID']+
                          "\n\nConversion scripts at https://github.com/OpenSourceBrain/BlueBrainProjectShowcase")
    
    chan.annotation = neuroml.Annotation()
    
    model_url_template = 'http://channelpedia.epfl.ch/ionchannels/%s/hhmodels/%s.xml'
    desc = osb.metadata.Description(channel_id)
    metadata.descriptions.append(desc)
    osb.metadata.add_simple_qualifier(desc, \
                                      'bqmodel', \
                                      'isDerivedFrom', \
                                      model_url_template%(root.attrib['ID'], root.attrib['ModelID']), \
                                      "Channelpedia channel ID: %s, ModelID: %s; direct link to original XML model" % (root.attrib['ID'], root.attrib['ModelID']))
    
    channel_url_template = 'http://channelpedia.epfl.ch/ionchannels/%s'
    osb.metadata.add_simple_qualifier(desc, \
                                      'bqmodel', \
                                      'isDescribedBy', \
                                      channel_url_template%(root.attrib['ID']), \
                                      "Channelpedia channel ID: %s; link to main page for channel" % (root.attrib['ID']))
    
    for reference in root.findall('Reference'):
        pmid = reference.attrib['PubmedID']
        #metadata = update_metadata(chan, metadata, channel_id, "http://identifiers.org/pubmed/%s"%pmid)
        ref_info = reference.text
        osb.metadata.add_simple_qualifier(desc, \
                                          'bqmodel', \
                                          'isDescribedBy', \
                                          osb.resources.PUBMED_URL_TEMPLATE % (pmid), \
                                          ("PubMed ID: %s is referenced in original XML\n"+\
                                          "                                 %s") % (pmid, ref_info))
            
    for environment in root.findall('Environment'):
        for animal in environment.findall('Animal'):

            species = animal.attrib['Name'].lower()

            if species:
                if species in osb.resources.KNOWN_SPECIES:
                    known_id = osb.resources.KNOWN_SPECIES[species]
                    osb.metadata.add_simple_qualifier(desc, \
                                                      'bqbiol', \
                                                      'hasTaxon', \
                                                      osb.resources.NCBI_TAXONOMY_URL_TEMPLATE % known_id, \
                                                      "Known species: %s; taxonomy id: %s" % (species, known_id))
                else:
                    print("Unknown species: %s"%species)
                    unknowns += "Unknown species: %s\n"%species
                    
        for cell_type_el in environment.findall('CellType'):
            cell_type = cell_type_el.text.strip().lower()

            if cell_type:
                if cell_type in osb.resources.KNOWN_CELL_TYPES:
                    known_id = osb.resources.KNOWN_CELL_TYPES[cell_type]
                    osb.metadata.add_simple_qualifier(desc, \
                                                      'bqbiol', \
                                                      'isPartOf', \
                                                      osb.resources.NEUROLEX_URL_TEMPLATE % known_id, \
                                                      "Known cell type: %s; taxonomy id: %s" % (cell_type, known_id))
                else:
                    print("Unknown cell_type: %s"%cell_type)
                    unknowns += "Unknown cell_type: %s\n"%cell_type

        
    print("Currently unknown: <<<%s>>>"%unknowns)
                          
    comp_types = {}
    for gate in root.findall('Gates'):
        
        eq_type = gate.attrib['EqType']
        gate_name = gate.attrib['Name']
        target = chan.gates
        
        if eq_type == '1':
            g = neuroml.GateHHUndetermined(id=gate_name, type='gateHHtauInf', instances=int(float(gate.attrib['Power'])))
        elif eq_type == '2':
            g = neuroml.GateHHUndetermined(id=gate_name, type='gateHHrates', instances=int(float(gate.attrib['Power'])))
        
        for inf in gate.findall('Inf_Alpha'):
            equation = check_equation(inf.findall('Equation')[0].text)
            
            if eq_type == '1':
                new_comp_type = "%s_%s_%s"%(channel_id, gate_name, 'inf')
                g.steady_state = neuroml.HHVariable(type=new_comp_type)

                comp_type = lems.ComponentType(new_comp_type, extends="baseVoltageDepVariable")

                comp_type.add(lems.Constant('TIME_SCALE', '1 ms', 'time'))
                comp_type.add(lems.Constant('VOLT_SCALE', '1 mV', 'voltage'))

                comp_type.dynamics.add(lems.DerivedVariable(name='V', dimension="none", value="v / VOLT_SCALE"))
                comp_type.dynamics.add(lems.DerivedVariable(name='x', dimension="none", value="%s"%equation, exposure="x"))

                comp_types[new_comp_type] = comp_type
                
            elif eq_type == '2':
                new_comp_type = "%s_%s_%s"%(channel_id, gate_name, 'alpha')
                g.forward_rate = neuroml.HHRate(type=new_comp_type)

                comp_type = lems.ComponentType(new_comp_type, extends="baseVoltageDepRate")

                comp_type.add(lems.Constant('TIME_SCALE', '1 ms', 'time'))
                comp_type.add(lems.Constant('VOLT_SCALE', '1 mV', 'voltage'))

                comp_type.dynamics.add(lems.DerivedVariable(name='V', dimension="none", value="v / VOLT_SCALE"))
                comp_type.dynamics.add(lems.DerivedVariable(name='r', dimension="per_time", value="%s / TIME_SCALE"%equation, exposure="r"))

                comp_types[new_comp_type] = comp_type
                
            
        for tau in gate.findall('Tau_Beta'):
            equation = check_equation(tau.findall('Equation')[0].text)
            
            if eq_type == '1':
                new_comp_type = "%s_%s_tau"%(channel_id, gate_name)
                g.time_course = neuroml.HHTime(type=new_comp_type)

                comp_type = lems.ComponentType(new_comp_type, extends="baseVoltageDepTime")

                comp_type.add(lems.Constant('TIME_SCALE', '1 ms', 'time'))
                comp_type.add(lems.Constant('VOLT_SCALE', '1 mV', 'voltage'))

                comp_type.dynamics.add(lems.DerivedVariable(name='V', dimension="none", value="v / VOLT_SCALE"))
                comp_type.dynamics.add(lems.DerivedVariable(name='t', dimension="time", value="(%s) * TIME_SCALE"%equation, exposure="t"))

                comp_types[new_comp_type] = comp_type
                
            elif eq_type == '2':
                new_comp_type = "%s_%s_%s"%(channel_id, gate_name, 'beta')
                g.reverse_rate = neuroml.HHRate(type=new_comp_type)

                comp_type = lems.ComponentType(new_comp_type, extends="baseVoltageDepRate")

                comp_type.add(lems.Constant('TIME_SCALE', '1 ms', 'time'))
                comp_type.add(lems.Constant('VOLT_SCALE', '1 mV', 'voltage'))

                comp_type.dynamics.add(lems.DerivedVariable(name='V', dimension="none", value="v / VOLT_SCALE"))
                comp_type.dynamics.add(lems.DerivedVariable(name='r', dimension="per_time", value="%s  / TIME_SCALE"%equation, exposure="r"))

                comp_types[new_comp_type] = comp_type
        
        target.append(g)
                          

    doc.ion_channel_hhs.append(chan)

    doc.id = channel_id

    writers.NeuroMLWriter.write(doc,nml2_file_name)

    print("Written NeuroML 2 channel file to: "+nml2_file_name)

    for comp_type_name in comp_types.keys():
        comp_type = comp_types[comp_type_name]
        ct_xml = comp_type.toxml()
        
        # Quick & dirty pretty printing..
        ct_xml = ct_xml.replace('<Const','\n        <Const')
        ct_xml = ct_xml.replace('<Dyna','\n        <Dyna')
        ct_xml = ct_xml.replace('</Dyna','\n        </Dyna')
        ct_xml = ct_xml.replace('<Deriv','\n            <Deriv')
        ct_xml = ct_xml.replace('</Compone','\n    </Compone')
        
        # print("Adding definition for %s:\n%s\n"%(comp_type_name, ct_xml))
        nml2_file = open(nml2_file_name, 'r')
        orig = nml2_file.read()
        new_contents = orig.replace("</neuroml>", "\n    %s\n\n</neuroml>"%ct_xml)
        nml2_file.close()
        nml2_file = open(nml2_file_name, 'w')
        nml2_file.write(new_contents)
        nml2_file.close()

    print("Inserting metadata...")
    nml2_file = open(nml2_file_name, 'r')
    orig = nml2_file.read()
    new_contents = orig.replace("<annotation/>", "\n        <annotation>\n%s        </annotation>\n"%metadata.to_xml("            "))
    nml2_file.close()
    nml2_file = open(nml2_file_name, 'w')
    nml2_file.write(new_contents)
    nml2_file.close()
        

    ###### Validate the NeuroML ######    

    from neuroml.utils import validate_neuroml2

    validate_neuroml2(nml2_file_name)
    
    return unknowns
    
def check_equation(eqn):
    eqn = eqn.replace("v", "V")
    eqn = eqn.replace("- -", "+")
    return eqn



if __name__ == '__main__':

    if len(sys.argv) == 2:
        target = sys.argv[1]
    else:
        target = 'HCN1'
    test_file = target+'.xml'
    contents = open(test_file, 'r').read()
    
    unknowns = channelpedia_xml_to_neuroml2(contents, target+'.channel.nml')

    unknowns_file = open('unknowns','w')
    unknowns_file.write("No unknowns!" if len(unknowns)==0 else unknowns)
    unknowns_file.close()



