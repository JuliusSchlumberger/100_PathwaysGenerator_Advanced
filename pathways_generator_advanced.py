import json
import numpy as np
from utilities._optimize_positions import create_optimized_positions
from utilities._create_marker_dictionary import create_marker_dictionary
from utilities._instance_dictionary import create_instance_dictionary
from utilities._base_figure import base_figure
from utilities._get_network_dicts import get_network_dicts

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
    def __init__(self, measure_colors, measure_numbers_inv,replacing_measure, with_pathways, unique_lines):
        self.with_pathways = with_pathways
        self.unique_lines = unique_lines
        self.measure_colors = measure_colors
        self.measure_numbers_inv = measure_numbers_inv
        self.replacing_measure = replacing_measure

    def prepare_files(self, input_file_with_pathways, file_sequence_only, file_tipping_points, renaming_dict,
                      max_x_offset, max_y_offset, file_offset, file_base, optimize=True, num_iterations=False):
        # Create files from pathways generator input files
        actions, action_transitions, base_y_values, x_offsets, measures_in_pathways = get_network_dicts(self,
            input_file_with_pathways, file_sequence_only, file_tipping_points, renaming_dict, max_x_offset)

        # Get number of instances with different tipping points per measure, decide if lines with same tipping point are overlaid or not
        instance_dict, max_instance = create_instance_dictionary(self, actions)

        # Calculate y-offsets for instances
        y_offsets1 = np.linspace(0, max_y_offset, int(np.floor(max_instance / 2)) + 1)
        y_offsets2 = np.linspace(-max_y_offset, 0, int(np.ceil(max_instance / 2)) + 1)
        y_offsets = np.concatenate(
            (y_offsets2[:-1], y_offsets1))  # Concatenate arrays without duplicating the middle value (zero)
        y_offsets = {i: y_offsets[i - 1] for i in range(1, max_instance + 1)}  # Map offsets to instance numbers

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
                savepath, with_logos):

        # Generate the base figure and save it
        base_figure(self, data, action_pairs, action_transitions, x_offsets, preferred_dict_inv,
                    measures_in_pathways,
                    savepath, with_logos)
        # return fig, ax

