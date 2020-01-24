# module: definitions
#
# useful lists, dicts and effects details


def get_button_groups(win):
    group = []
    group.append(win.osc_1_waveform)
    group.append(win.osc_2_waveform)
    group.append(win.osc_3_waveform)
    return group

easy_numbers = [
    'QDial',
    'QSlider',
    'QDoubleSpinBox'
]
easy_strings = [
    'QLabel',
    'QLineEdit'
]
waveforms = {
    'sin': 'sine',
    'tri': 'tri/saw',
    'pul': 'pulse'
}

chbox = {
'checked': ['on', 'offset'],
'unchecked': ['off', 'absolute']
}

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
    'receiving': ['MIDI','...','waiting'],
    'receive_error': ['error',':(','try again'],
    'receive_success': ['sysex',':)','received'],
    'file_loaded': ['file',':)','loaded'],
    'file_error': ['error',':(','bad file']
}



###############################
# FX - effect related settings
###############################

feedback = manual_delay = lfo_depth = notch_frequency = \
sibilance_boost = decay = analysis_mix = \
regeneration_percentage = brightness = diffusion = {
    'min': 0,
    'max': 100,
    'unit': '%'
}
lfo_rate = {
    'min': 10,
    'max': 4800,
    'unit': 'hz'
}
lfo_shape = tempo_sync = {
    'min': 0,
    'max': 1,
}
stages = {
    'min': 0,
    'max': 5,
}
analysis_gain = band_shift = {
    'min': -100,
    'max': 100
}
synthesis_input = analysis_signal_in = {
    'min': 0,
    'max': 2
}
delay_time = left_delay_time = right_delay_time = color = {
    'min': 1,
    'max': 340,
    'unit': 'ms'
}


chorus = {
    'a': ['feedback', feedback],
    'b': ['delay', manual_delay],
    'c': ['rate', lfo_rate],
    'd': ['depth', lfo_depth],
    'e': ['shape', lfo_shape],
    'f': ['sync', tempo_sync],
    'g': ['---', False],
    'name': 'chorus'
}

theta_flanger = chorus.copy()
theta_flanger['a'][1]['min'] = -100
theta_flanger['name'] = 'theta flanger'

thru_0_flanger = theta_flanger.copy()
thru_0_flanger['name'] = 'thru 0 flanger'

super_phaser = theta_flanger.copy()
super_phaser['b'] = ['freq', notch_frequency]
string_phaser = super_phaser.copy()
super_phaser['f'] = ['stages', stages]
super_phaser['g'] = ['sync', tempo_sync]

super_phaser['name'] = 'super phaser'
string_phaser['name'] = 'string phaser'

vocoder = {
    'a': ['gain', analysis_gain],
    'b': ['sibilance', sibilance_boost],
    'c': ['decay', decay],
    'd': ['band', band_shift],
    'e': ['synthesis', synthesis_input],
    'f': ['analysis', analysis_signal_in],
    'g': ['mix', analysis_mix],
    'name': 'vocoder'
}

mono_delay = {
    'a': ['time', delay_time],
    'b': ['regen', regeneration_percentage],
    'c': ['brightness', brightness],
    'd': ['sync', tempo_sync]
}
mono_delay['name'] = 'mono delay'

stereo_delay = mono_delay.copy()
stereo_delay['name'] = 'stereo delay'

split_LR_delay = mono_delay.copy()
split_LR_delay['a'] = ['left', left_delay_time]
split_LR_delay['d'] = ['right', right_delay_time]
split_LR_delay['name'] = 'split L/R delay'

hall_reverb = {
    'a': ['diffusion', diffusion],
    'b': ['decay', decay],
    'c': ['brightness', brightness],
    'd': ['color', color]
}
hall_reverb['name'] = 'hall reverb'
plate_reverb = hall_reverb.copy()
plate_reverb['name'] = 'plate reverb'
room_reverb = hall_reverb.copy()
room_reverb['name'] = 'room reverb'

bypass = {
    'a': ['---', False],
    'b': ['---', False],
    'c': ['---', False],
    'd': ['---', False],
    'e': ['---', False],
    'f': ['---', False],
    'g': ['---', False],
}
bypass['name'] = 'bypass'


fx_types = {
    'bypass' : bypass,
    'super phaser': super_phaser,
    'string phaser': string_phaser,
    'theta flanger': theta_flanger,
    'thru 0 flanger': thru_0_flanger,
    'chorus': chorus,
    'vocoder': vocoder,
    'mono delay': mono_delay,
    'stereo delay': stereo_delay,
    'split L/R delay': split_LR_delay,
    'hall reverb': hall_reverb,
    'plate reverb': plate_reverb,
    'room reverb': room_reverb
}
