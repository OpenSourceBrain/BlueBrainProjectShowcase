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

default_capacitances = {
    'axonal': "1.0 uF_per_cm2",
    'somatic': "1.0 uF_per_cm2",
    'basal': "1.0 uF_per_cm2",
    'apical': "1.0 uF_per_cm2",
}

biophysical_properties_vs_etypes = {}

included_channels = {}

def main():
    parse_templates_json(save_example_files=True)
    
    
def parse_templates_json(templates_json="templates.json",
                         ignore_chans = [],
                         save_example_files=False):

    with open(templates_json, "r") as templates_json_file:
        json_cells = json.load(templates_json_file)


    for cell_name in json_cells:
        cell_dict = json_cells[cell_name]
        
        etype = cell_name.split('_')[0]

        nml_doc = neuroml.NeuroMLDocument(id=cell_name)

        # Membrane properties
        #

        included_channels[etype] = []
        channel_densities = []
        channel_density_nernsts = []
        species = []
        
        for section_list in cell_dict['parameters']:
            for parameter_name in \
                    json_cells[cell_name]['parameters'][section_list]:
                if parameter_name != 'e_pas' and 'CaDynamics_E2' not in parameter_name:
                    
                    parameter_dict = cell_dict['parameters'][section_list][parameter_name]
                    
                    channel = parameter_dict['channel']
                    
                    if channel not in ignore_chans:

                        arguments = {}
                        cond_density = None
                        variable_parameters = None
                        if parameter_dict['distribution']['disttype'] == "uniform":
                            value = parameter_dict['distribution']['value']
                            cond_density = "%s mS_per_cm2" % value
                        else:
                            variable_parameters = [
                                neuroml.VariableParameter(
                                    segment_groups=section_list,
                                    parameter=parameter_name)]

                        channel_nml2_file = "%s.channel.nml"%channel
                        if channel_nml2_file not in included_channels[etype]:
                            nml_doc.includes.append(
                                neuroml.IncludeType(
                                    href="../../channels/nml/%s" %
                                    channel_nml2_file))
                            included_channels[etype].append(channel_nml2_file)

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

                        if erev is not None:
                            arguments["erev"] = erev
                        arguments["id"] = "%s_%s" % (section_list, parameter_name)
                        if cond_density is not None:
                            arguments["cond_density"] = cond_density
                        arguments["segment_groups"] = section_list
                        arguments['ion_channel'] = channel
                        if variable_parameters is not None:
                            arguments['variable_parameters'] = variable_parameters

                        density = getattr(neuroml, channel_class)(**arguments)

                        if channel_class == "ChannelDensityNernst":
                            channel_density_nernsts.append(density)
                        else:
                            channel_densities.append(density)
                        
                elif 'decay_CaDynamics_E2' in parameter_name:
                    # calcium_model = \
                    #    neuroml.DecayingPoolConcentrationModel(ion='ca')

                    species.append(neuroml.Species(
                        id='ca',
                        initial_concentration='1.0E-4 mM',
                        initial_ext_concentration='1.0E-4 mM',
                        concentration_model='CaDynamics_E2_NML2',
                        segment_groups=section_list))
                        
                    channel_nml2_file = 'CaDynamics_E2_NML2.nml'
                    if channel_nml2_file not in included_channels[etype]:
                        included_channels[etype].append(channel_nml2_file)

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
            value="-65 mV", segment_groups='all')]

        membrane_properties = neuroml.MembraneProperties(
            channel_densities=channel_densities,
            channel_density_nernsts=channel_density_nernsts,
            specific_capacitances=specific_capacitances,
            init_memb_potentials=init_memb_potentials)

        # Intracellular Properties
        #
        resistivities = []
        resistivities.append(neuroml.Resistivity(
            value="1 ohm_cm", segment_groups='all'))

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

        biophysical_properties_vs_etypes[etype] = biophysical_properties

        if save_example_files:
            cell = neuroml.Cell(id=cell_name,
                                biophysical_properties=biophysical_properties)
            cell.name = cell_name
            cell.id = cell_name

            print cell_name

            nml_doc.cells.append(cell)


            nml_filename = '%s.cell.nml' % cell_name
            with open(nml_filename, 'w') as nml_file:
                neuroml.writers.NeuroMLWriter.write(nml_doc, nml_file)

            logging.debug("Written channel file to: %s", nml_filename)

            with open(nml_filename, 'r') as nml_file:
                neuroml.utils.validate_neuroml2(nml_file)

def get_biophysical_properties(etype, ignore_chans=[], templates_json="templates.json"):
    
    parse_templates_json(templates_json=templates_json, ignore_chans=ignore_chans, save_example_files=False)
    print("Retrieving biophys props for: %s from %s"%(etype,biophysical_properties_vs_etypes.keys()))
    return biophysical_properties_vs_etypes[str(etype)], included_channels[str(etype)]

if __name__ == "__main__":
    main()