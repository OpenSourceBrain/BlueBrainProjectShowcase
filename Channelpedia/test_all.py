import osb.utils

from ChannelpediaToNeuroML2 import channelpedia_xml_to_neuroml2
from analyse import generate

from bs4 import BeautifulSoup
import os

import xml.etree.ElementTree as ET

import neuroml.loaders as loaders

contents = osb.utils.get_page("http://channelpedia.epfl.ch/reports/model")

soup = BeautifulSoup(contents)

from pyneuroml import pynml

count = 0
valid = 0

temperature = 32  # Unused in Channelpedia...

unknowns = ""

max_chans = 1000

for link in soup.find_all('a'):
    href = link.get('href')
    # /ionchannels/189/hhmodels/37.xml
    if "ionchannels" in href and "hhmodels" in href and href.endswith(".xml") and max_chans > 0:
        url = "http://channelpedia.epfl.ch%s"%href
        print("Retrieving: "+ url)
        count += 1
        cpd_xml = osb.utils.get_page(url)

        root = ET.fromstring(cpd_xml)

        channel_id='Channelpedia_%s_%s'%(root.attrib['ModelName'].replace("/","_").replace(" ","_").replace(".","_"), root.attrib['ModelID'])
        
        print("Channel id: %s"%channel_id)
        
        file_out = open("test/%s.xml"%channel_id, 'w')
        file_out.write(cpd_xml)
        file_out.close()
        
        nml2_file_name = "%s.channel.nml"%channel_id
        nml2_file_path = "test/"+nml2_file_name
        unknowns = channelpedia_xml_to_neuroml2(cpd_xml, nml2_file_path, unknowns)
        
        pynml.validate_neuroml2(nml2_file_path)
        
        doc = loaders.NeuroMLLoader.load(nml2_file_path)
        #print dir(doc)
        gates = []
        for ic in doc.ion_channel_hhs:
            if ic.id == channel_id:
                for g in ic.gates:
                    gates.append(g.id)

        new_lems_file = "LEMS_Test_%s.xml"%channel_id
    
        lems_helper = generate(nml2_file_path, channel_id, gates, temperature, ion=doc.ion_channel_hhs[0].species)
        
        file_out = open(new_lems_file, 'w')
        file_out.write(lems_helper)
        file_out.close()
        
        success = pynml.run_lems_with_jneuroml("LEMS_Test_%s.xml"%channel_id, 
                           nogui=True, 
                           load_saved_data=False, 
                           plot=False, 
                           exec_in_dir = ".",
                           verbose=True,
                           exit_on_fail = False)
                           
        if success: 
            valid +=1
        else:
            os.rename(nml2_file_path, nml2_file_path+".broken")
        
        max_chans -=1

        
print("\nFound %i models in Channelpedia XML format, converted %i to valid NeuroML2\n"%(count,valid))

unknowns_file = open('unknowns','w')
unknowns_file.write("No unknowns!" if len(unknowns)==0 else unknowns)
unknowns_file.close()