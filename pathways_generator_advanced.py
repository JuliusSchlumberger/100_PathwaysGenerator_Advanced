import json
import numpy as np
from utilities._optimize_positions import create_optimized_positions
from utilities._create_marker_dictionary import create_marker_dictionary
from utilities._instance_dictionary import create_instance_dictionary
from utilities._base_figure import base_figure, other_figure
from utilities._get_network_dicts import get_network_dicts
import matplotlib.pyplot as plt

class Pathways_Generator_Advanced():
    """
    Generates visual representations of pathways with optional optimization and logos.

    Parameters:
    - input_file: Path to the input file containing sequences and pathways information.
    - file_sequence_only: Path to save the extracted sequences only.
    - file_tipping_points: Path to the file containing tipping points.
    - file_offset: Path to save the optimal offset JSON file.
    - file_base: Path to save the optimal base y-values JSON file.
    - savepath: Path to save the resulting figure.
    - renaming_dict: Dictionary for renaming measures.
    - replacing_measure: Dictionary mapping measures to their replacements.
    - measure_numbers_inv: Dictionary mapping measure numbers to their inverse mappings.
    - max_x_offset: Maximum x-offset value.
    - max_y_offset: Maximum y-offset value.
    - measure_colors: Dictionary mapping measure identifiers to color strings.
    - with_pathways: Boolean indicating whether to include pathways information.
    - unique_lines: Boolean indicating whether each new x-position should get a unique instance number.
    - optimize: Boolean indicating whether to optimize the positions.
    - num_iterations: Optional; the number of iterations to run for optimization. If False, all permutations are considered.
    - with_logos: Boolean indicating whether to add logos to the plot.

    Returns:
    - None
    """
    def __init__(self, measure_colors, measure_numbers_inv,replacing_measure, with_pathways, unique_lines, input_with_pathways):
        self.with_pathways = with_pathways  # design choice
        self.input_with_pathways = input_with_pathways  # whether input file contains pathway numbers
        self.unique_lines = unique_lines
        self.measure_colors = measure_colors
        self.measure_numbers_inv = measure_numbers_inv
        self.replacing_measure = replacing_measure

    def create_start_files(self, input_file_with_pathways, file_sequence_only, file_tipping_points, renaming_dict,
                      max_x_offset, initial_measures_in_pathways=False, initial_base_y_values=False, instance_dict=False, initial_max_instance=False, x_position_dict=False):

        # Create files from pathways generator input files
        actions, action_transitions, base_y_values, x_offsets, measures_in_pathways = get_network_dicts(self,
            input_file_with_pathways, file_sequence_only, file_tipping_points, renaming_dict, max_x_offset)
        if initial_measures_in_pathways:
            # Update set of measures in pathways
            for pathway in measures_in_pathways.keys():
                initial_measures = initial_measures_in_pathways[pathway]
                new_measures = measures_in_pathways[pathway]
                measures_in_pathways[pathway] = np.concatenate(
                    [initial_measures, [m for m in new_measures if m not in initial_measures]], axis=0)

        if initial_base_y_values:
            # Avoid that specific numbers are overriding each other because of different order in input files
            initial_keys = list(initial_base_y_values.keys())
            new_keys = list(base_y_values.keys())
            all_keys = set(initial_keys + new_keys)
            num_y_positions = len(all_keys)

            pos_y_positions = np.linspace(0, int(np.floor(num_y_positions / 2)), int(np.floor(num_y_positions / 2)) + 1)
            neg_y_positions = np.linspace(-int(np.ceil(num_y_positions / 2)), 0, int(np.ceil(num_y_positions / 2)) + 1)[::-1]
            all_y_positions = np.concatenate([pos_y_positions, neg_y_positions[1:]], axis=0)
            base_y_values = {}
            for tick, y_key in enumerate(all_keys):
                base_y_values[y_key] = all_y_positions[tick]

        # Get number of instances with different tipping points per measure, decide if lines with same tipping point are overlaid or not
        if not instance_dict:
            instance_dict = {}  # Dictionary to store instance numbers for each measure
        if not initial_max_instance:
            initial_max_instance = 0  # Track the highest instance number assigned
        if not x_position_dict:
            x_position_dict = {}  # Dictionary to track end positions for measures
        instance_dict, max_instance, x_position_dict = create_instance_dictionary(self, actions, instance_dict, initial_max_instance, x_position_dict)

        return instance_dict, actions, action_transitions, base_y_values, x_offsets, measures_in_pathways, max_instance, x_position_dict

    def prepare_files(self, instance_dict, actions, action_transitions, base_y_values, x_offsets, measures_in_pathways, max_instance, max_y_offset, file_offset, file_base, optimize=False, num_iterations=False):
        # Calculate y-offsets for instances
        y_offsets1 = np.linspace(0, max_y_offset, int(np.floor(max_instance / 2)) + 1)
        y_offsets2 = np.linspace(-max_y_offset, 0, int(np.ceil(max_instance / 2)) + 1)[::-1]

        # Initialize the rearranged list
        rearranged_offsets = []

        # Interleave the values from y_offsets1 and y_offsets2
        for i in range(1,len(y_offsets1)):
            rearranged_offsets.append(y_offsets1[i])
            rearranged_offsets.append(y_offsets2[i])

        # Insert the zero value at the beginning
        rearranged_offsets.insert(0, 0.0)
        y_offsets = {i: rearranged_offsets[i - 1] for i in range(1, max_instance + 1)}  # Map offsets to instance numbers

        if optimize:
            # Optimize positions to minimize total vertical distance
            preferred_base, preferred_offset = create_optimized_positions(self,
                base_y_values, instance_dict, y_offsets, actions, action_transitions, file_offset, file_base,
                num_iterations)
        else:
            # Load precomputed preferred offset and base y-values from files
            with open(f'{file_offset}.json', 'r') as file:
                preferred_offset = json.load(file)

            with open(f'{file_base}.json', 'r') as file:
                preferred_base = json.load(file)

        # Create an inverse dictionary for preferred base y-values
        preferred_dict_inv = {v: k for k, v in preferred_base.items()}

        # Initialize a dictionary to store begin and end coordinates for each measure and instance
        action_pairs, data = create_marker_dictionary(self, actions, preferred_base, instance_dict, preferred_offset,
                                                      )
        return data, action_pairs, action_transitions, x_offsets, preferred_dict_inv, measures_in_pathways


    def create_base_figure(self, data, action_pairs, action_transitions, x_offsets, preferred_dict_inv,
                measures_in_pathways,
                with_logos):

        # Create a new figure and axis for plotting
        self.fig, self.ax = plt.subplots(figsize=(8, 8))

        # Generate the base figure and save it
        base_figure(self, data, action_pairs, action_transitions, x_offsets, preferred_dict_inv,
                    measures_in_pathways,
                    with_logos)

    def add_other_map(self,  data, action_pairs, action_transitions, x_offsets, preferred_dict_inv,
                    measures_in_pathways,
                    with_logos):
        other_figure(self, data, action_pairs, action_transitions, x_offsets, preferred_dict_inv,
                    measures_in_pathways,
                    with_logos)

