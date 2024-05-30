def round_to_nearest_5(x):
    """Round a number to the nearest multiple of 5."""
    return round(x / 5) * 5

def process_file(input_filepath, output_filepath):
    with open(input_filepath, 'r') as infile, open(output_filepath, 'w') as outfile:
        for line in infile:
            parts = line.strip().split(' ')
            # Assuming the value to round is always in the second part
            value = int(float(parts[1]))
            rounded_value = round_to_nearest_5(value)
            parts[1] = str(rounded_value)
            outfile.write(' '.join(parts) + '\n')

# Specify your input and output file paths
# input_filepath = 'path/to/your/input_file.txt'
# output_filepath = 'path/to/your/output_file.txt'

input_filepath = f'inputs/all_tp_timings_flood_agr_no_interaction.txt'
output_filepath = 'inputs/all_tp_timings_flood_agr_no_interaction_rounded.txt'



# Process the file
process_file(input_filepath, output_filepath)
