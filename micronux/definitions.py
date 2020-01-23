# module: definitions
#
# useful lists and dics

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
' KHz': 'khz',
'% f1': 'bal',
'% fx1': 'fxbal'
}
unit_ratios = {
'ms': 1000,
's': 1000000,
'hz': 1000,
'khz': 1000000
}

nicer_names = {
'positive': '+',
'negative': '-',
'filter 1 mix': 'f1 mix',
'filter 2 mix': 'f2 mix',
'3 -> 2 -> 1': '3 > 2 > 1',
'2+3 -> 1': '2+3 > 1',
'2 -> 1': '2 > 1',
'linear': 'lin',
'm1 wheel': 'm1 slider',
'm2 wheel': 'm2 slider',
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

mark_positive = ['semi','fine','octave']

lcd_messages = {
'clear': ['','',''],
'startup': ['alesi','s','micronux'],
'receiving': ['MIDI','','waiting'],
'receive_error': ['error',':(','try again'],
'receive_success': ['sysex',':)','received'],
'file_loaded': ['file',':)','loaded'],
'file_error': ['error',':(','bad file']
}
