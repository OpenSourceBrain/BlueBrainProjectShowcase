#!/usr/bin/env python

""" 
    Create an NeuroML 2.0 version of the templates stored in a json file
    
    Authors: Werner van Geit, Padraig Gleeson
"""

import json
import logging
logging.basicConfig(level=logging.DEBUG, format='%(message)s')

import neuroml
import neuroml.writers
import neuroml.utils

# pylint: disable=C0103, W0142

ion_erevs = {
    'na': '50.0 mV',
    'k': '-85.0 mV',
    'hcn': '-45.0 mV',
    'ca': 'nernst',
    'pas': 'pas',
}

channel_ions = {
    'Ih': 'hcn',
    'NaTa_t': 'na',
    'NaTs2_t': 'na',
    'Nap_Et2': 'na',
    'K_Tst': 'k',
    'K_Pst': 'k',
    'SKv3_1': 'k',
    'SK_E2': 'k',
    'StochKv': 'k',
    'KdShu2007': 'k',
    'Im': 'k',
    'Ca': 'ca',
    'Ca_HVA': 'ca',
    'Ca_LVAst': 'ca',
    'pas': 'pas',
    'CaDynamics_E2': 'ca'
}

channel_substitutes = {
    'StochKv': 'StochKv_deterministic'
}


''' Due to the use of 1e-4 in BREAKPOINT in StochKv.mod: ik = 1e-4 * gk * (v - ek) '''
density_scales = {
    'StochKv': 1e-4
}


default_capacitances = {
    'axonal': "1.0 uF_per_cm2",
    'somatic': "1.0 uF_per_cm2",
    'basal': "1.0 uF_per_cm2",
    'apical': "1.0 uF_per_cm2",
}

cell_type_vs_firing_type = {'bNAC':'bNAC_1',
                            'cAC':'cACint_237',
                            'cNAC':'cNAC_149',
                            'dNAC':'dNAC_1',
                            'bAC':'bAC_1',
                            'bIR':'bIR_1',
                            'bSTUT':'bSTUT_1',
                            'cIR':'cIR_1',
                            'cSTUT':'cSTUT_7',
                            'dSTUT':'dSTUT_1',
                            'L23PC':'cADpyr_229',
                            'L4PC':'cADpyr_230',
                            'L5PC':'cADpyr_232',  
                            'L6PC':'cADpyr_231'}

biophysical_properties_vs_types = {}

included_channels = {}
    
    
def parse_templates_json(templates_json="templates.json",
                         ignore_chans = [],
                         save_example_files=False,
                         verbose=False):

    with open(templates_json, "r") as templates_json_file:
        json_cells = json.load(templates_json_file)

    concentrationModels = ''

    for firing_type_u in json_cells:
        
        if verbose: print("\n ---------------   %s "%(firing_type_u))
        firing_type = str(firing_type_u)
        cell_dict = json_cells[firing_type]

        nml_doc = neuroml.NeuroMLDocument(id=firing_type)

        # Membrane properties
        #

        included_channels[firing_type] = []
        channel_densities = []
        channel_density_nernsts = []
        channel_density_non_uniform_nernsts = []
        channel_density_non_uniforms = []
        species = []
        
        for section_list in cell_dict['forsecs']:
            for parameter_name in cell_dict['forsecs'][section_list]:
                value = cell_dict['forsecs'][section_list][parameter_name]
                if verbose: print("   --- %s, %s: %s "%(section_list,parameter_name,value))
                if parameter_name == 'g_pas':
                    channel = 'pas'
                    arguments = {}
                    cond_density = "%s S_per_cm2" % value
                    if verbose: print('    - Adding %s with %s'%(channel, cond_density))
                    
                    channel_nml2_file = "%s.channel.nml"%channel
                    if channel_nml2_file not in included_channels[firing_type]:
                        nml_doc.includes.append(
                            neuroml.IncludeType(
                                href="../../NeuroML2/%s" %
                                channel_nml2_file))
                        included_channels[firing_type].append(channel_nml2_file)

                    erev = cell_dict['forsecs'][section_list]['e_pas']
                    erev = "%s mV" % erev
                    
                    arguments["cond_density"] = cond_density
                    arguments['ion_channel'] = channel
                    arguments["ion"] = "non_specific"
                    arguments["erev"] = erev
                    arguments["id"] = "%s_%s" % (section_list, parameter_name)
                    
                    channel_class = 'ChannelDensity'
                    density = getattr(neuroml, channel_class)(**arguments)

                    channel_densities.append(density)
        
        for section_list in cell_dict['parameters']:
            for parameter_name in cell_dict['parameters'][section_list]:
                if parameter_name != 'e_pas' and 'CaDynamics_E2' not in parameter_name:
                    
                    parameter_dict = cell_dict['parameters'][section_list][parameter_name]
                    if verbose: print("   --- %s, %s: %s "%(section_list,parameter_name,parameter_dict))
                    channel = parameter_dict['channel']
                    
                    if channel not in ignore_chans:

                        arguments = {}
                        cond_density = None
                        variable_parameters = None
                        if parameter_dict['distribution']['disttype'] == "uniform":
                            value = float(parameter_dict['distribution']['value'])
                            if channel in density_scales:
                                value = value * density_scales[channel]
                            cond_density = "%s S_per_cm2" % value
                        else:
                            new_expr = '1e4 * (%s)'%parameter_dict['distribution']['value'].replace('x','p').replace('epp','exp')
                            iv = neuroml.InhomogeneousValue(inhomogeneous_parameters="PathLengthOver_%s"%section_list,
                                                            value=new_expr)
                            variable_parameters = [
                                neuroml.VariableParameter(
                                    segment_groups=section_list,
                                    parameter='condDensity',
                                    inhomogeneous_value=iv)]

                        channel_name  = channel
                        if channel in channel_substitutes:
                            channel_name = channel_substitutes[channel]
                            
                        channel_nml2_file = "%s.channel.nml"%channel_name
                        if channel_nml2_file not in included_channels[firing_type]:
                            nml_doc.includes.append(
                                neuroml.IncludeType(
                                    href="../../NeuroML2/%s" %
                                    channel_nml2_file))
                            included_channels[firing_type].append(channel_nml2_file)

                        arguments['ion'] = channel_ions[channel]
                        erev = ion_erevs[arguments["ion"]]

                        channel_class = 'ChannelDensity'

                        if erev == "nernst":
                            erev = None
                            channel_class = 'ChannelDensityNernst'
                        elif erev == "pas":
                            erev = cell_dict['parameters'] \
                                [section_list]['e_pas']['distribution']\
                                ['value']
                            erev = "%s mV" % erev
                            arguments["ion"] = "non_specific"
                            
                        if variable_parameters is not None:
                            channel_class += 'NonUniform'
                        else:
                            arguments["segment_groups"] = section_list

                        if erev is not None:
                            arguments["erev"] = erev
                        arguments["id"] = "%s_%s" % (section_list, parameter_name)
                        if cond_density is not None:
                            arguments["cond_density"] = cond_density
                        arguments['ion_channel'] = channel_name
                        if variable_parameters is not None:
                            arguments['variable_parameters'] = variable_parameters

                        density = getattr(neuroml, channel_class)(**arguments)

                        if channel_class == "ChannelDensityNernst":
                            channel_density_nernsts.append(density)
                        elif channel_class == "ChannelDensityNernstNonUniform":
                            channel_density_non_uniform_nernsts.append(density)
                        elif channel_class == "ChannelDensityNonUniform":
                            channel_density_non_uniforms.append(density)
                        else:
                            channel_densities.append(density)
                            
                elif 'gamma_CaDynamics_E2' in parameter_name:
                    
                    parameter_dict = cell_dict['parameters'][section_list][parameter_name]
                    
                    model = 'CaDynamics_E2_NML2__%s_%s'%(firing_type,section_list)
                    value = parameter_dict['distribution']['value']    
                    concentrationModels+='<concentrationModel id="%s" ion="ca" '%model +\
                                         'type="concentrationModelHayEtAl" minCai="1e-4 mM" ' +\
                                         'gamma="%s" '%value
                                         
                elif 'decay_CaDynamics_E2' in parameter_name:
                    # calcium_model = \
                    #    neuroml.DecayingPoolConcentrationModel(ion='ca')
                    model = 'CaDynamics_E2_NML2__%s_%s'%(firing_type,section_list)
                    species.append(neuroml.Species(
                        id='ca',
                        ion='ca',
                        initial_concentration='5.0E-11 mol_per_cm3',
                        initial_ext_concentration='2.0E-6 mol_per_cm3',
                        concentration_model=model,
                        segment_groups=section_list))
                        
                    channel_nml2_file = 'CaDynamics_E2_NML2.nml'
                    if channel_nml2_file not in included_channels[firing_type]:
                        included_channels[firing_type].append(channel_nml2_file)
                        
                    parameter_dict = cell_dict['parameters'][section_list][parameter_name]
                    value = parameter_dict['distribution']['value']  
                    concentrationModels+='decay="%s ms" depth="0.1 um"/>  <!-- For group %s in %s-->\n\n'%(value,section_list,firing_type)

        capacitance_overwrites = {}
        for section_list in cell_dict['forsecs']:
            for parameter_name in cell_dict['forsecs'][section_list]:
                if parameter_name == "cm" and section_list != 'all':
                    value = cell_dict['forsecs'][section_list][parameter_name]
                    capacitance_overwrites[
                        section_list] = "%s uF_per_cm2" % value

        specific_capacitances = []
        for section_list in default_capacitances:
            if section_list in capacitance_overwrites:
                capacitance = capacitance_overwrites[section_list]
            else:
                capacitance = default_capacitances[section_list]
            specific_capacitances.append(
                neuroml.SpecificCapacitance(value=capacitance,
                                            segment_groups=section_list))

        init_memb_potentials = [neuroml.InitMembPotential(
            value="-80 mV", segment_groups='all')]

        # 10mV is default for Neuron spike threshold in NetCon
        # https://www.neuron.yale.edu/neuron/static/py_doc/modelspec/programmatic/network/netcon.html
        spike_threshes = [neuroml.SpikeThresh(value="10mV", segment_groups='all')]

        membrane_properties = neuroml.MembraneProperties(
            channel_densities=channel_densities,
            channel_density_nernsts=channel_density_nernsts,
            channel_density_non_uniform_nernsts=channel_density_non_uniform_nernsts,
            channel_density_non_uniforms=channel_density_non_uniforms,
            specific_capacitances=specific_capacitances,
            init_memb_potentials=init_memb_potentials,
            spike_threshes=spike_threshes)

        # Intracellular Properties
        #
        resistivities = []
        resistivities.append(neuroml.Resistivity(
            value="100 ohm_cm", segment_groups='all'))

        intracellular_properties = neuroml.IntracellularProperties(
            resistivities=resistivities,
            species=species)

        # Cell construction
        #
        biophysical_properties = \
            neuroml.BiophysicalProperties(id="biophys",
                                          intracellular_properties=
                                          intracellular_properties,
                                          membrane_properties=
                                          membrane_properties)

        biophysical_properties_vs_types[firing_type] = biophysical_properties

        if save_example_files:
            cell = neuroml.Cell(id=firing_type,
                                notes="\n*************************\nThis is not a physiologically constrained cell model!!\n"+\
                                      "It is only for testing formatting of the biophysicalProperties extracted from templates.json\n*************************\n",
                                biophysical_properties=biophysical_properties)

            nml_doc.cells.append(cell)
            
            cell.morphology = neuroml.Morphology(id="morph")
            
            cell.morphology.segments.append(neuroml.Segment(id='0',
                                                            name='soma',
                                                            proximal=neuroml.Point3DWithDiam(x=0,y=0,z=0,diameter=10),
                                                            distal=neuroml.Point3DWithDiam(x=0,y=20,z=0,diameter=10)))
                                                            
            cell.morphology.segment_groups.append(neuroml.SegmentGroup(id="soma",
                                                                       neuro_lex_id="sao864921383",
                                                                       members=[neuroml.Member("0")]))
                                                            
            cell.morphology.segments.append(neuroml.Segment(id='1',
                                                            name='axon',
                                                            parent=neuroml.SegmentParent(segments='0',fraction_along="0"),
                                                            proximal=neuroml.Point3DWithDiam(x=0,y=0,z=0,diameter=2),
                                                            distal=neuroml.Point3DWithDiam(x=0,y=-50,z=0,diameter=2)))
                                                            
            cell.morphology.segment_groups.append(neuroml.SegmentGroup(id="axon",
                                                                       neuro_lex_id="sao864921383",
                                                                       members=[neuroml.Member("1")]))
                                                            
            cell.morphology.segments.append(neuroml.Segment(id='2',
                                                            name='basal_dend',
                                                            parent=neuroml.SegmentParent(segments='0'),
                                                            proximal=neuroml.Point3DWithDiam(x=0,y=20,z=0,diameter=3),
                                                            distal=neuroml.Point3DWithDiam(x=50,y=20,z=0,diameter=3)))
                                                            
            cell.morphology.segment_groups.append(neuroml.SegmentGroup(id="basal_dend",
                                                                       neuro_lex_id="sao864921383",
                                                                       members=[neuroml.Member("2")]))
                                                            
            cell.morphology.segments.append(neuroml.Segment(id='3',
                                                            name='apical_dend1',
                                                            parent=neuroml.SegmentParent(segments='0'),
                                                            proximal=neuroml.Point3DWithDiam(x=0,y=20,z=0,diameter=3),
                                                            distal=neuroml.Point3DWithDiam(x=0,y=120,z=0,diameter=3)))
            cell.morphology.segments.append(neuroml.Segment(id='4',
                                                            name='apical_dend2',
                                                            parent=neuroml.SegmentParent(segments='0'),
                                                            proximal=neuroml.Point3DWithDiam(x=0,y=120,z=0,diameter=3),
                                                            distal=neuroml.Point3DWithDiam(x=0,y=220,z=0,diameter=3)))
                                                            
            cell.morphology.segment_groups.append(neuroml.SegmentGroup(id="apical_dend",
                                                                       neuro_lex_id="sao864921383",
                                                                       members=[neuroml.Member("3"),neuroml.Member("4")]))
                                                            
                                                            
            cell.morphology.segment_groups.append(neuroml.SegmentGroup(id="somatic",includes=[neuroml.Include("soma")]))
            cell.morphology.segment_groups.append(neuroml.SegmentGroup(id="axonal", includes=[neuroml.Include("axon")]))
            
            sg = neuroml.SegmentGroup(id="basal", includes=[neuroml.Include("basal_dend")])
            sg.inhomogeneous_parameters.append(neuroml.InhomogeneousParameter(id="PathLengthOver_"+"basal",
                                                                              variable="x",
                                                                              metric="Path Length from root",
                                                                              proximal=neuroml.ProximalDetails(translation_start="0")))
            cell.morphology.segment_groups.append(sg)
            
            sg = neuroml.SegmentGroup(id="apical", includes=[neuroml.Include("apical_dend")])
            sg.inhomogeneous_parameters.append(neuroml.InhomogeneousParameter(id="PathLengthOver_"+"apical",
                                                                              variable="x",
                                                                              metric="Path Length from root",
                                                                              proximal=neuroml.ProximalDetails(translation_start="0")))
            cell.morphology.segment_groups.append(sg)
                                                            

            nml_filename = 'test/%s.cell.nml' % firing_type
            neuroml.writers.NeuroMLWriter.write(nml_doc, nml_filename)

            logging.debug("Written cell file to: %s", nml_filename)

            neuroml.utils.validate_neuroml2(nml_filename)
            
            
            conc_mod_file = open('test/concentrationModel.txt','w')
            conc_mod_file.write(concentrationModels)
            conc_mod_file.close()
            


def get_biophysical_properties(cell_type, ignore_chans=[], templates_json="templates.json"):
    
    parse_templates_json(templates_json=templates_json, ignore_chans=ignore_chans, save_example_files=False)
    firing_type = cell_type_vs_firing_type[cell_type]
    print("Retrieving biophys props for: %s (%s) from %s"%(cell_type,firing_type,biophysical_properties_vs_types.keys()))
    return biophysical_properties_vs_types[str(firing_type)], included_channels[str(firing_type)]


def main():
    parse_templates_json(save_example_files=True, verbose=True)
    
if __name__ == "__main__":
    main()