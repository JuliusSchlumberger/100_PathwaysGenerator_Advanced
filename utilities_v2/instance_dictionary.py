import numpy as np


def create_instance_dictionary(actions, unique_lines):
    """
    Creates a dictionary mapping measures to their instances with unique numbers assigned to each instance.

    Parameters:
    - actions: Dict of actions with keys that include measure and instance information.
    - unique_lines: Boolean indicating whether each new x-position should get a unique instance number or reuse
                    close x-positions for the same instance number.

    Returns:
    - instance_dict: Dictionary where each measure maps to another dictionary of instances with their unique numbers.
    - max_index: The highest instance number assigned across all measures.
    """

    instance_dict = {}  # Dictionary to store instance numbers for each measure
    x_position_dict = {}  # Dictionary to track end positions for measures
    max_index = 0  # Track the highest instance number assigned

    for key, value in actions.items():
        if key.startswith('ActionEnd'):
            # Split the key to extract measure and instance information
            parts = key.split('[')
            measure = parts[0].split('(')[1][1:]  # Extract measure part
            instance = parts[1].split(']')[0]  # Extract instance part
            x_position = value[0]  # Get the x-position from the value

            if measure not in x_position_dict:
                x_position_dict[measure] = {}

            if unique_lines:
                # Assign unique instance numbers to new x-positions
                if measure not in instance_dict:
                    instance_dict[measure] = {}
                    x_position_dict[measure][x_position] = 1  # Start instance numbering from 1
                else:
                    # Increment the instance number for a new x-position
                    new_index = max(x_position_dict[measure].values()) + 1
                    x_position_dict[measure][x_position] = new_index
                    if new_index > max_index:
                        max_index = new_index
            else:
                # Reuse instance numbers for x-positions that are close
                found = False
                for x_pos in x_position_dict[measure]:
                    if np.isclose(x_pos, x_position, atol=0.1):  # Check if positions are approximately the same
                        instance_number = x_position_dict[measure][x_pos]
                        found = True
                        break

                if not found:
                    # Assign a new instance number for a new x-position
                    if measure not in instance_dict:
                        instance_dict[measure] = {}
                        x_position_dict[measure][x_position] = 1  # Start instance numbering from 1
                    else:
                        # Increment the instance number for a new x-position
                        new_index = max(x_position_dict[measure].values()) + 1
                        x_position_dict[measure][x_position] = new_index
                        if new_index > max_index:
                            max_index = new_index

            # Assign the determined instance number to the instance
            instance_number = x_position_dict[measure][x_position]
            instance_dict[measure][instance] = instance_number  # Store the instance number in the dictionary

    print(instance_dict)  # Print the resulting dictionary for debugging
    return instance_dict, max_index  # Return the instance dictionary and the highest instance number assigned

