
import tables   # pytables for HDF5 support

import neuroml
from neuroml.hdf5.NetworkContainer import *
import random


class BlueBrainConnectomeParser():
    
    
    def __init__(self):
        self.DUMMY_CELL_ID = 'dummy_cell'
        self.current_population = None
        self.nml_doc = neuroml.NeuroMLDocument(id="BlueBrainConnectome")
        

        iafCell0 = neuroml.IafCell(id=self.DUMMY_CELL_ID,
                           C="1.0 nF",
                           thresh = "-50mV",
                           reset="-65mV",
                           leak_conductance="10 nS",
                           leak_reversal="-65mV")

        self.nml_doc.iaf_cells.append(iafCell0)


    def parse(self, filename):

        self.network = NetworkContainer(id=filename.split('/')[-1].split('.')[0])
        self.nml_doc.id=self.network.id
        self.nml_doc.networks.append(self.network)
        
        h5file=tables.open_file(filename,mode='r')

        print("Opened HDF5 file: %s"%(h5file.filename))

        self.parse_group(h5file.root.populations)
        
        print(self.nml_doc.summary())

        h5file.close()


    def parse_group(self, g):
        print("Parsing group: "+ str(g)+", name: "+g._v_name)

        for node in g:
            print("Sub node: %s, class: %s, name: %s (parent: %s)"   % (node,node._c_classid,node._v_name, g._v_name))

            if node._c_classid == 'GROUP':
                if g._v_name=='populations':
                    pop_id = node._v_name.replace('-','_')
                    self.current_population = PopulationContainer(id=pop_id, component=self.DUMMY_CELL_ID, size=0, type='populationList')
                    print("  Adding new Population: %s"%self.current_population)
                    self.network.populations.append(self.current_population)
                    
                    p = neuroml.Property(tag='color', value='%s %s %s'%(random.random(),random.random(),random.random()))
                    self.current_population.properties.append(p)
                    
                self.parse_group(node)

            if self._is_dataset(node):
                self.parse_dataset(node)
                
                
        self.current_population = None


    def save_to_hdf5(self,file_name):
        
        from neuroml.writers import NeuroMLHdf5Writer
    
        NeuroMLHdf5Writer.write(self.nml_doc,file_name)
        
        print("Written to %s"%file_name)


    def save_to_xml(self,file_name):
        
        from neuroml.writers import NeuroMLWriter
    
        NeuroMLWriter.write(self.nml_doc,file_name)
        
        print("Written to %s"%file_name)
        

    def _is_dataset(self, node):
          return node._c_classid == 'ARRAY' or node._c_classid == 'CARRAY'   


    def parse_dataset(self, d):
        print("Parsing dataset/array: "+ str(d))
        if self.current_population and d.name=='locations':
            
            self.current_population.size = d.shape[0]
            print("   There are %i cells in: %s"%(self.current_population.size, self.current_population.id))
            for i in range(0, d.shape[0]):
                row = d[i,:]
                instance = neuroml.Instance(i)
                instance.location = neuroml.Location(row[0],row[1],row[2])
                self.current_population.instances.append(instance)
                
                #print("    Row %i: %s"%(i,row))
    
    
if __name__ == '__main__':

    file_name = 'cons_locs_pathways_mc0_Column.h5'

    bbp = BlueBrainConnectomeParser()
    
    bbp.parse(file_name)   
    
    nml_h5_file_name = 'BBP.net.nml.h5'
    
    bbp.save_to_hdf5(nml_h5_file_name)
    
    nml_file_name = 'BBP.net.nml'
    
    bbp.save_to_xml(nml_file_name)