import matplotlib.pyplot as plt
import numpy as np
import re
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.pyplot as plt
# from utilities.measure_numbers import MEASURE_NUMBERS_INV
from utilities_v2.find_integers import find_first_and_second_integers
# from design_choices.measure_colors import MEASURE_COLORS

def base_figure(data, action_pairs, action_transitions, measure_numbers_inv, offsets, preferred_dict_inv,
                measures_in_pathways, savepath, measure_colors, with_pathways, unique_lines, replacing_measure,
                with_logos):
    """
    Creates and saves a figure representing pathways with actions, transitions, and optional logos.

    Parameters:
    - data: Dict containing plotting data organized by measure.
    - action_pairs: Dict storing coordinates for Begin and End actions by measure and instance.
    - action_transitions: List of transitions, each represented as a tuple (start, year, end) or (start, end, year).
    - measure_numbers_inv: Dict mapping measure numbers to their inverse mappings.
    - offsets: Dict mapping measures to their offsets for vertical positioning.
    - preferred_dict_inv: Dict for inverse mapping of preferred measures.
    - measures_in_pathways: Dict mapping pathways to their associated measures.
    - savepath: Path to save the resulting figure.
    - measure_colors: Dict mapping measure identifiers to color strings.
    - with_pathways: Boolean indicating whether to include pathways information.
    - unique_lines: Boolean indicating whether each new x-position should get a unique instance number.
    - replacing_measure: Dict mapping measures to their replacements.
    - with_logos: Boolean indicating whether to add logos to the plot.

    Returns:
    - None
    """

    line_width_marker = 2
    size_marker = 150
    line_width_line = 2

    # Create a new figure and axis for plotting
    fig, ax = plt.subplots(figsize=(4, 8))

    # Add markers to the plot
    ax = add_actions(ax, data, line_width_marker, size_marker)

    # Add horizontal lines to the plot
    ax = add_horizontal_lines(ax, action_pairs, line_width_line, measures_in_pathways, with_pathways, unique_lines,
                              replacing_measure, measure_colors)

    # Add vertical lines to the plot
    ax = add_vertical_lines(ax, action_transitions, action_pairs, offsets, line_width_line, measure_colors)

    plt.xlabel('Years')
    plt.ylabel('Measures')
    plt.title('Base Pathways Map')

    if with_logos:
        ax = add_logos(ax, preferred_dict_inv, measure_numbers_inv)

        # Hide the y-axis
        ax.yaxis.set_visible(False)

        # Hide all spines except the bottom one
        for spine in ['top', 'right', 'left']:
            ax.spines[spine].set_visible(False)
    else:
        # Retrieve and modify y-axis tick labels
        ytick_labels = ax.get_yticklabels()
        new_labels = []
        for ytick in ytick_labels:
            _, y_pos = ytick.get_position()
            ylabel = preferred_dict_inv.get(y_pos, None)

            if ylabel is None:
                new_labels.append('empty')
            elif ylabel == '0':
                new_labels.append('current')
            else:
                new_labels.append(measure_numbers_inv[int(ylabel)])

        ax.set_yticklabels(new_labels)
        ax.yaxis.set_visible(True)

        # Hide all spines except the bottom one
        for spine in ['top', 'right', 'left']:
            ax.spines[spine].set_visible(False)

    # Ensure the bottom spine is visible
    ax.spines['bottom'].set_visible(True)

    # Save the plot to the specified path
    plt.savefig(savepath)
    plt.show()


def add_actions(ax, data, line_width_marker, size_marker):
    """
    Adds action markers to the plot.

    Parameters:
    - ax: The matplotlib axis to add markers to.
    - data: Dict containing plotting data organized by measure.
    - line_width_marker: Width of the marker lines.
    - size_marker: Size of the markers.

    Returns:
    - ax: The matplotlib axis with added markers.
    """
    for measure, points in data.items():
        for point in points:
            x, y = point[0]
            ax.scatter(x, y, color=point[2], marker=point[1], edgecolors=point[2], facecolors=point[3],
                       linewidth=line_width_marker, s=size_marker, zorder=3)
    return ax


def add_horizontal_lines(ax, action_pairs, line_width_line, measures_in_pathways, with_pathways, unique_lines,
                         replacing_measure, measure_colors):
    """
    Adds horizontal lines to the plot representing actions and pathways.

    Parameters:
    - ax: The matplotlib axis to add lines to.
    - action_pairs: Dict storing coordinates for Begin and End actions by measure and instance.
    - line_width_line: Width of the lines.
    - measures_in_pathways: Dict mapping pathways to their associated measures.
    - with_pathways: Boolean indicating whether to include pathways information.
    - unique_lines: Boolean indicating whether each new x-position should get a unique instance number.
    - replacing_measure: Dict mapping measures to their replacements.
    - measure_colors: Dict mapping measure identifiers to color strings.

    Returns:
    - ax: The matplotlib axis with added horizontal lines.
    """
    if with_pathways and unique_lines:
        # Plot current measure
        coords = action_pairs[('0', '0')]
        begin_coords = coords['Begin']
        end_coords = coords['End']
        measure, instance = ('0', '0')

        ax.plot([begin_coords[0], end_coords[0]], [begin_coords[1], end_coords[1]],
                color=measure_colors[measure], linewidth=line_width_line, zorder=1)

        for pathway, measures in measures_in_pathways.items():
            measures_split = [tuple(item.replace(']', '').split('[')) for item in measures]
            relevant_measures = {}
            for measure_with_instance in measures_split:
                if len(measure_with_instance) > 1:  # ignore current
                    year = action_pairs[measure_with_instance]['Begin'][0]
                    relevant_measures[year] = measure_with_instance

            sorted_years = sorted(relevant_measures)  # sorted by year to ensure proper line buildup
            old_keys = []
            for year in sorted_years:
                measure_instance = relevant_measures[year]
                x_offset = 0

                # Add main new measure added
                coords = action_pairs[measure_instance]
                begin_coords = coords['Begin']
                end_coords = coords['End']
                measure, instance = measure_instance
                ax.plot([begin_coords[0], end_coords[0]], [begin_coords[1], end_coords[1]],
                        color=measure_colors[measure], linewidth=line_width_line, zorder=1)

                for previous in old_keys:
                    # Check if new measure replaces a previous measure
                    potentially_replacing_measures = old_keys + [measure]
                    would_be_replaced_measures = [replacing_measure.get(item) for item in
                                                  potentially_replacing_measures]
                    would_be_replaced_measures = [item for sublist in would_be_replaced_measures for item in sublist]

                    if previous in would_be_replaced_measures:
                        pass
                    else:
                        # Add differently colored line for previously implemented measures still active
                        x_offset -= 0.04
                        ax.plot([begin_coords[0], end_coords[0]],
                                [begin_coords[1] + x_offset, end_coords[1] + x_offset],
                                color=measure_colors[previous], linewidth=line_width_line, zorder=1)

                old_keys.append(measure)
    else:
        for (measure, instance), coords in action_pairs.items():
            if 'Begin' in coords and 'End' in coords:
                begin_coords = coords['Begin']
                end_coords = coords['End']
                ax.plot([begin_coords[0], end_coords[0]], [begin_coords[1], end_coords[1]],
                        color=measure_colors[measure], linewidth=line_width_line, zorder=1)
    return ax


def add_vertical_lines(ax, action_transitions, action_pairs, offsets, line_width_line, measure_colors):
    """
    Adds vertical lines to the plot representing action transitions.

    Parameters:
    - ax: The matplotlib axis to add lines to.
    - action_transitions: List of transitions, each represented as a tuple (start, year, end) or (start, end, year).
    - action_pairs: Dict storing coordinates for Begin and End actions by measure and instance.
    - offsets: Dict mapping measures to their offsets for vertical positioning.
    - line_width_line: Width of the lines.
    - measure_colors: Dict mapping measure identifiers to color strings.

    Returns:
    - ax: The matplotlib axis with added vertical lines.
    """
    for transition in action_transitions:
        if isinstance(transition[2], int):
            print('This is a horizontal line (one measure)', transition)
        else:
            print('This is a vertical line (transition between measures)', transition)
            # Extract the measure and instance from the start action
            start_measure, start_instance = find_first_and_second_integers(transition[0])
            end_measure, end_instance = find_first_and_second_integers(transition[2])

            # Extract the x position
            end_x_pos = transition[1]

            # Apply an offset based on the measure group
            if start_measure != '0':  # Only one vertical line for the tipping point of the current state
                group_offset = offsets.get(start_measure, 0)
                end_x_pos += group_offset

            # Use the adjusted coordinates from the action_pairs to draw the line
            if (start_measure, start_instance) in action_pairs:
                if 'Begin' in action_pairs[(start_measure, start_instance)]:
                    start_y_pos = action_pairs[(start_measure, start_instance)]['Begin'][1]
                    end_y_pos = action_pairs[(end_measure, end_instance)]['End'][1]
                    ax.plot([end_x_pos, end_x_pos], [start_y_pos, end_y_pos],
                            color=measure_colors[start_measure], linewidth=line_width_line, zorder=1)
    return ax


def getImage(path):
    """
    Reads an image from the specified path and returns an OffsetImage object.

    Parameters:
    - path: The path to the image file.

    Returns:
    - OffsetImage object with the image.
    """
    return OffsetImage(plt.imread(path), zoom=0.05)


def add_logos(axes, preferred_dict_inv, measure_numbers_inv):
    """
    Adds logos to the y-axis of the plot based on preferred measures.

    Parameters:
    - axes: The matplotlib axis to add logos to.
    - preferred_dict_inv: Dict for inverse mapping of preferred measures.
    - measure_numbers_inv: Dict mapping measure numbers to their inverse mappings.

    Returns:
    - axes: The matplotlib axis with added logos.
    """
    ytick_labels = axes.get_yticklabels()

    for ytick in ytick_labels:
        _, y_pos = ytick.get_position()
        ylabel = preferred_dict_inv.get(y_pos, None)

        if ylabel == '0' or ylabel == None:
            pass
        else:
            # Add logo for the measure
            imagebox = getImage(f'logos/{measure_numbers_inv[int(ylabel)]}.png')
            ab = AnnotationBbox(imagebox, (0, y_pos),
                                xybox=(0, 0),
                                xycoords=("axes fraction", "data"),
                                boxcoords="offset points",
                                box_alignment=(0, .5),  # Align logos to the bottom
                                bboxprops={"edgecolor": "none"}, frameon=False)
            axes.add_artist(ab)

    return axes