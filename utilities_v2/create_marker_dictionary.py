import numpy as np


def create_marker_dictionary(actions, base_y_values, instance_dict, y_offsets, measure_colors):
    """
    Processes musical actions to create dictionaries for plotting and line drawing.

    Parameters:
    - actions: Dict of action data keyed by composite identifiers including measure and instance.
    - base_y_values: Dict mapping measure identifiers to base y-values.
    - instance_dict: Dict mapping measures to another dict that maps instances to unique numbers.
    - y_offsets: Dict mapping unique instance numbers to y-offsets for vertical positioning.
    - measure_colors: Dict mapping measure identifiers to color strings.

    Returns:
    - action_pairs: Dict for storing Begin and End coordinates by measure and instance.
    - data: Organized list of tuples containing adjusted y-values, markers, colors, and face colors for plotting.
    """

    action_pairs = {}  # Stores the coordinate pairs for drawing lines between points.
    data = {}  # Stores visual plotting data organized by measure.

    # Iterate through each action to parse and process its components
    for key, value in actions.items():
        parts = key.split('[')  # Split the key to extract measure and instance information
        measure = parts[0].split('(')[1][1:]  # Extract measure part
        instance = parts[1].split(']')[0]  # Extract instance part
        base_y = base_y_values.get(measure, 0)  # Get base y-value for the measure, default to 0

        # Setup marker styles and colors based on action type
        marker = 'o'
        action_type = "Begin" if "Begin" in key else "End"
        color = measure_colors[measure]  # Color for the measure
        facecolor = 'w' if "End" in key else color  # Hollow for "End", filled for "Begin"

        # Adjust y-value based on the instance's unique number and its offset
        instance_number = instance_dict[measure][instance]
        y_adjustment = y_offsets[str(instance_number)]
        value_adjusted = np.array([value[0], int(base_y) + y_adjustment])  # Adjust y-value

        # Organize data by measure for plotting
        if measure not in data:
            data[measure] = []
        data[measure].append((value_adjusted, marker, color, facecolor))

        # Prepare action_pairs for line drawing
        coord_key = (measure, instance)
        if coord_key not in action_pairs:
            action_pairs[coord_key] = {}
        action_pairs[coord_key][action_type] = value_adjusted

    return action_pairs, data  # Return the dictionaries for plotting and drawing