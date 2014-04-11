import osb.utils

from ChannelpediaToNeuroML2 import channelpedia_xml_to_neuroml2

from bs4 import BeautifulSoup

import xml.etree.ElementTree as ET

contents = osb.utils.get_page("http://channelpedia.epfl.ch/reports/model")

soup = BeautifulSoup(contents)

print soup.title.string
count = 0

unknowns = ""

for link in soup.find_all('a'):
    href = link.get('href')
    # /ionchannels/189/hhmodels/37.xml
    if "ionchannels" in href and "hhmodels" in href and href.endswith(".xml"):
        url = "http://channelpedia.epfl.ch%s"%href
        print("Retrieving: "+ url)
        count += 1
        cpd_xml = osb.utils.get_page(url)

        root = ET.fromstring(cpd_xml)

        channel_id='Channelpedia_%s_%s'%(root.attrib['ModelName'].replace("/","_").replace(" ","_"), root.attrib['ModelID'])
        
        print("Channel id: %s"%channel_id)
        
        file_out = open("test/%s.xml"%channel_id, 'w')
        file_out.write(cpd_xml)
        file_out.close()
        
        unknowns = channelpedia_xml_to_neuroml2(cpd_xml, "test/%s.channel.nml"%channel_id, unknowns)

        
print("\nFound %i models in Channelpedia XML format\n"%count)

unknowns_file = open('unknowns','w')
unknowns_file.write("No unknowns!" if len(unknowns)==0 else unknowns)
unknowns_file.close()