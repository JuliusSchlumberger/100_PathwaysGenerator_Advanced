
renaming_dict = {
    'current': '0'
}
max_x_offset = .7 # will do adjustments in horizontal direction. Needs adjustment if lines of different measures start overlap.
max_y_offset = .48 # will do adjustments in vertical direction between instances. Needs adjustment if markers overlap.

replacing_measure = {   # if measure is not replacing any measure, empty list, else populate the lists
    '0': [],
    '1': [],
    '2': [],
    '3': [],
    '4': [],
    '5': [],
    '6': [],
    '7': [],
    '8': [],
    '9': [],
    '10': [],
    # blueish group
    '11': ['12', '13','15'],
    '12': [],
    '13': [],
    '14': [],
    '15': ['11', '12', '13', '14'],
    # greenish group
    '16': [],
    '17': [],
    '18': [],
    '19': [],
}

measure_colors = {
            '0': '#bfbfbf',
            '1': '#ffcc99',
            '2': '#ffaa66',
            '3': '#ff8800',
            '4': '#cc6e00',
            '5': '#994c00',
            '6':'#cec3e6',
            '7': '#9d94cc',
            '8': '#4e429f',
            '9': '#2e2570',
            '10': '#b3cde3',
            '11': '#6497b1',
            '12': '#03396c',
            '13': '#011f4b',
            '14': '#011a30',
            '15': '#005b96',
            '16': '#b2dfdb',
            '17': '#00897b',
            '18': '#00695c',
            '19': '#004d40'
        }

measure_numbers = {
            'no_measure': 0,
            'd_resilient_crops': 1,
            'd_rain_irrigation': 2,
            'd_gw_irrigation': 3,
            'd_riv_irrigation': 4,
            'd_soilm_practice': 5,
            'd_multimodal_transport': 6,
            'd_medium_ships': 7,
            'd_small_ships': 8,
            'd_dredging': 9,
            'f_resilient_crops': 10,
            'f_ditches': 11,
            'f_local_support': 12,
            'f_dike_elevation_s': 13,
            'f_dike_elevation_l': 14,
            'f_maintenance': 15,
            'f_room_for_river': 16,
            'f_wet_proofing_houses': 17,
            'f_local_protect': 18,
            'f_awareness_campaign': 19
        }

measure_numbers_inv = {}

for k, v in measure_numbers.items():
    measure_numbers_inv[v] = k

