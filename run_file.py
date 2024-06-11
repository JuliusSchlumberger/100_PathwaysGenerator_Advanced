from pathways_generator_advanced import Pathways_Generator_Advanced
from utilities.static_inputs import *

# no interaction files
input_file_with_pathways = 'inputs/dashboard/all_sequences_flood_agr_Wp_50%.txt'
file_sequence_only = 'inputs/dashboard/all_sequences_flood_agr_Wp_50%_only_sequences.txt'
file_tipping_points = 'inputs/dashboard/all_tp_timings_flood_agr_Wp_50%.txt'

# interaction files
input_file_with_pathways_with_interaction = 'inputs/dashboard/all_sequences_flood_agr_Wp_50%_flood_agr&drought_agr.txt'
file_sequence_only_with_interaction = 'inputs/dashboard/all_sequences_flood_agr_Wp_50%_flood_agr&drought_agr_only_sequences.txt'
file_tipping_points_with_interaction = 'inputs/dashboard/all_tp_timings_flood_agr_Wp_50%_flood_agr&drought_agr.txt'

# File paths for optimized positions
file_offset = 'optimized_offset'
file_base = 'optimized_base'

savepath_base = 'figures/dashboard/base_figure.svg'
savepath_base_i = 'figures/dashboard/base_figure_i.svg'
savepath_difference_plot = 'figures/dashboard/interaction_figure.svg'

# Initiate new Pathways Map
with_pathways = True    # account for pathways information [no effect at the moment]
unique_lines = True     # if True unique vertical lines. If 'with_pathways' also True, also unique horizontal lines per pw
input_with_pathways = True  # if True, input file contains information on pws as well.
optimize_positions = True   # automatically adjusts the position of the measures to minimize vertical distance
num_interations = False # if integer, indicates after how many iterations stop optimizing. Else all combinations run

NewPathwayMaps = Pathways_Generator_Advanced(measure_colors, measure_numbers_inv, replacing_measure,
                                             with_pathways=with_pathways, unique_lines=unique_lines,
                                             input_with_pathways=input_with_pathways)

# Create data for no-interaction plot
initial_instance_dict, actions, action_transitions, \
initial_base_y_values, x_offsets, initial_measures_in_pathways, \
initial_max_instance, initial_x_position_dict = NewPathwayMaps.create_start_files(input_file_with_pathways, file_sequence_only,
                                                                          file_tipping_points, renaming_dict, max_x_offset)

# Create data for interaction plot
instance_dict, actions_i, action_transitions_i, \
base_y_values, x_offsets, measures_in_pathways, \
max_instance, x_position_dict = NewPathwayMaps.create_start_files(input_file_with_pathways_with_interaction,
                                                                  file_sequence_only_with_interaction,
                                                                  file_tipping_points_with_interaction,
                                                                  renaming_dict,
                                                                  max_x_offset,
                                                                  initial_measures_in_pathways,
                                                                  initial_base_y_values,
                                                                  initial_instance_dict,
                                                                  initial_max_instance,
                                                                  initial_x_position_dict)

# no interactions
data, action_pairs, action_transitions, x_offsets, \
preferred_dict_inv, measures_in_pathways = NewPathwayMaps.prepare_files(instance_dict, actions, action_transitions,
                                                                        base_y_values, x_offsets, measures_in_pathways,
                                                                        max_instance, max_y_offset,
                                                                        file_offset, file_base,
                                                                        optimize=optimize_positions,
                                                                        num_iterations=num_interations)

# with interactions
data_i, action_pairs_i, action_transitions_i, x_offsets, \
preferred_dict_inv, measures_in_pathways = NewPathwayMaps.prepare_files(instance_dict, actions_i, action_transitions_i,
                                                                        base_y_values, x_offsets, measures_in_pathways,
                                                                        max_instance, max_y_offset,
                                                                        file_offset, file_base)

# Create base figure for no interactions
NewPathwayMaps.create_base_figure(data, action_pairs, action_transitions, x_offsets, preferred_dict_inv,
                measures_in_pathways,
                with_logos=True)
# Safe figure without interactions
NewPathwayMaps.fig.savefig(savepath_base, dpi=800)
# add in grey the pathways with interactions
NewPathwayMaps.add_other_map(data_i, action_pairs_i, action_transitions_i, x_offsets, preferred_dict_inv,
                measures_in_pathways,
                with_logos=True)
NewPathwayMaps.fig.savefig(savepath_difference_plot, dpi=800)

# Create base figure for with interactions
NewPathwayMaps.create_base_figure(data_i, action_pairs_i, action_transitions_i, x_offsets, preferred_dict_inv,
                measures_in_pathways,
                with_logos=True)
NewPathwayMaps.fig.savefig(savepath_base_i, dpi=800)