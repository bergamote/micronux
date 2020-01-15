# module: definitions
#
# useful lists and dics

def get_button_groups(window):
    button_groups = [
        window.osc_1_waveform,
        window.osc_2_waveform,
        window.osc_3_waveform
    ]
    return button_groups

easy_numbers = [
'QDial',
'QSlider',
'QDoubleSpinBox'
]
easy_strings = [
'QLabel',
'QLineEdit'
]

units = {
'%': 'pct',
' s': 's',
' ms': 'ms',
' Hz': 'hz',
' KHz': 'khz'
}
percentages = [
'level',
'shape',
'res',
'keytrack',
'envamt',
'drift',
'detune',
'wheel',
'smoothing',
'mix'
]

keywords = {
'positive': '+',
'negative': '-',
'filter 1 mix': 'f1 mix',
'filter 2 mix': 'f2 mix',
'3 -> 2 -> 1': '3 > 2 > 1',
'2+3 -> 1': '2+3 > 1',
'2 -> 1': '2 > 1',
'linear': 'lin',
'm1 wheel': 'm1 slider',
'm2 wheel': 'm2 slider'
}

mark_positive = ['semi','fine','octave']


# setings better names for display
nicer_names = {
'semi':'semitone',
'fine':'cent',
'balance':'f1 | f2  ',
'mix':    'wet|dry  ',
'amount':'fm amount',
'freq':'frequency',
'res':'resonance',
'envamt':'env amount',
'wheel':'slider'
}
