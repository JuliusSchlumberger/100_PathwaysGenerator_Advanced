import itertools
from utilities_v2.create_marker_dictionary import create_marker_dictionary
from utilities_v2.find_integers import find_first_and_second_integers

import numpy as np
import json


def create_optimized_positions(base_y_values, instance_dict, y_offsets, actions, action_transitions, file_offset,
                               file_base, measure_colors, num_iterations=False):
    """
    Finds the optimal combination of base y-values and y-offsets to minimize total vertical distance for action transitions.

    Parameters:
    - base_y_values: Dict of base y-values keyed by measure identifiers.
    - instance_dict: Dict mapping measures to their instances.
    - y_offsets: Dict of y-offsets keyed by instance numbers.
    - actions: Dict of action data keyed by composite identifiers including measure and instance.
    - action_transitions: List of transitions, each represented as a tuple (start, year, end) or (start, end, year).
    - file_offset: Path to save the optimal offset JSON file.
    - file_base: Path to save the optimal base y-values JSON file.
    - measure_colors: Dict mapping measures to color strings.
    - num_iterations: Optional; the number of iterations to run. If False, all permutations are considered.

    Returns:
    - preferred_base: Dict of base y-values for the optimal combination.
    - preferred_offset: Dict of y-offsets for the optimal combination.
    """

    tick = 0
    offset_permutations = list(itertools.permutations(y_offsets.values()))  # Generate all permutations of y-offsets
    base_y_values_permutations = list(
        itertools.permutations(base_y_values.values()))  # Generate all permutations of base y-values
    preferred_offset = None  # Default or initial value for preferred offsets
    preferred_base = None  # Default or initial value for preferred base y-values

    base_y_values_keys = list(base_y_values.keys())  # Extract keys for base y-values
    y_offsets_keys = list(y_offsets.keys())  # Extract keys for y-offsets

    y_dist_min = 300000  # Initialize minimum distance to a large value
    if num_iterations:
        print('iterations cover ',
              np.round(num_iterations / (len(offset_permutations) * len(base_y_values_permutations)), 3) * 100,
              '% of all possible permutations.')
    else:
        num_iterations = len(offset_permutations) * len(base_y_values_permutations)  # Total number of permutations
        print(num_iterations)

    for base_permutation in base_y_values_permutations:
        # Create a dictionary for the current permutation of base y-values
        base_y_values_permutation = {base_y_values_keys[i]: base_permutation[i] for i in range(len(base_permutation))}

        for off_permutation in offset_permutations:
            # Create a dictionary for the current permutation of y-offsets
            offset_permutation = {str(y_offsets_keys[i]): off_permutation[i] for i in range(len(off_permutation))}

            if tick > num_iterations:
                break  # Stop if the number of iterations exceeds the limit
            else:
                y_dist = 0
                # Calculate the total vertical distance for the current permutation
                action_pairs, _ = create_marker_dictionary(actions, base_y_values_permutation, instance_dict,
                                                           offset_permutation, measure_colors)

                for transition in action_transitions:
                    # Determine the type of transition (vertical or horizontal) and extract relevant information
                    if isinstance(transition[1], int):
                        start_measure, start_instance = find_first_and_second_integers(transition[0])
                        end_measure, end_instance = find_first_and_second_integers(transition[2])

                        # Use the adjusted coordinates from the action_pairs to calculate the vertical distance
                        if (start_measure, start_instance) in action_pairs:
                            if 'Begin' in action_pairs[(start_measure, start_instance)]:
                                start_y_pos = action_pairs[(start_measure, start_instance)]['Begin'][1]
                                end_y_pos = action_pairs[(end_measure, end_instance)]['End'][1]

                                y_dist += abs(start_y_pos - end_y_pos)  # Sum the absolute distances

                if y_dist < y_dist_min:
                    # Update the minimum distance and preferred permutations if a better combination is found
                    print('new distance:', y_dist)
                    print(f'{np.round(tick / (len(offset_permutations) * len(base_y_values_permutations)), 3) * 100}%')
                    y_dist_min = y_dist
                    preferred_offset = offset_permutation
                    preferred_base = base_y_values_permutation
                tick += 1

    # Save the optimal offset dictionary to a JSON file
    with open(f'{file_offset}.json', 'w') as file:
        json.dump(preferred_offset, file)

    # Save the optimal base y-values dictionary to a JSON file
    with open(f'{file_base}.json', 'w') as file:
        json.dump(preferred_base, file)

    return preferred_base, preferred_offset