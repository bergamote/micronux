# module: definitions
#
# useful lists, dicts and effects details


def get_button_groups(win):
    return [
        win.osc_1_waveform,
        win.osc_2_waveform,
        win.osc_3_waveform
    ]

def get_edge_track_points(win):
    return [
        win.tracking_point_m16,
        win.tracking_point_m15,
        win.tracking_point_m14,
        win.tracking_point_m13,
        win.tracking_point_13,
        win.tracking_point_14,
        win.tracking_point_15,
        win.tracking_point_16
    ]

def last_word(str, sep='_'):
    return str.split(sep)[-1]

def rm_last_word(str, sep='_'):
    return str.rsplit(sep, 1)[0]

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
    '%': '%',
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
    'm1 wheel': 'm1 slider',
    'm2 wheel': 'm2 slider',
    'semi': 'semitone',
    'fine': 'cent',
    'balance': ' f1 | f2  ',
    'mix': ' dry|wet  ',
    'amount': 'fm amount',
    'freq': 'frequency',
    'res': 'resonance',
    'envamt': 'env amount',
    'wheel': 'slider',
    'sus': 'sustain',
    'fx': 'fx1',
}

mark_positive = ['semi','fine','octave']

lcd_messages = {
    'clear': ['','',''],
    'startup': ['alesi','s','micronux'],
    'receiving': ['MIDI','...','waiting'],
    'receive_error': ['MIDI',':(','error'],
    'receive_success': ['sysex',':)','received'],
    'open_success': ['',':)','loaded'],
    'open_error': ['',':(','error'],
    'save_success': ['',':)','saved'],
    'save_error': ['',':(','error'],
    'revert': ['','','reverted'],
    'send_success': ['',':)','sent'],
    'send_error': ['',':(','not sent']
}

general_inputs = [
    'note-on velocity',
    'release velocity',
    'key track',
    'm1 slider',
    'm2 slider',
    'pitch wheel',
    'sustain pedal',
    'expression pedal',
    'amp env level',
    'filter env level',
    'pitch/mod env level',
    'lfo 1 sine',
    'lfo 1 cosine',
    'lfo 1 triangle',
    'lfo 1 cos-triangle',
    'lfo 1 saw',
    'lfo 1 cos-saw',
    'lfo 1 square',
    'lfo 1 cos-square',
    'lfo 2 sine',
    'lfo 2 cosine',
    'lfo 2 triangle',
    'lfo 2 cos-triangle',
    'lfo 2 saw',
    'lfo 2 cos-saw',
    'lfo 2 square',
    'lfo 2 cos-square',
    'voice random',
    'global random',
    'portamento level',
    'portamento effect',
    'midi channel pressure',
    'midi poly aftertouch',
    'key track extreme'
]

sh_inputs = general_inputs.copy()
sh_inputs.extend([
    'tracking generator',
    'step track'
])

tracking_inputs = general_inputs.copy()
tracking_inputs.append(
    'sh output'
)

mod_inputs = general_inputs.copy()
mod_inputs.insert(0, 'none')
mod_inputs.extend([
    'sh output',
    'tracking generator',
    'step track'
])

mod_dests = [
    'none',
    'voice pitch',
    'voice pitch narrow',
    'unison detune',
    'portamento time',
    'osc 1 shape',
    'osc 1 pitch full',
    'osc 1 pitch narrow',
    'osc 1 level',
    'osc 1 balance',
    'osc 2 shape',
    'osc 2 pitch full',
    'osc 2 pitch narrow',
    'osc 2 level',
    'osc 2 balance',
    'osc 3 shape',
    'osc 3 pitch full',
    'osc 3 pitch narrow',
    'osc 3 level',
    'osc 3 balance',
    'osc fm level',
    'ring mod level',
    'ring mod balance',
    'noise level',
    'noise balance',
    'ext in level',
    'ext in balance',
    'filter 1 freq',
    'filter 1 res',
    'filter 1 env mod',
    'filter 1 keytrack',
    'filter 1 level',
    'filter 1 pan',
    'f1->f2 level',
    'filter 2 freq',
    'filter 2 res',
    'filter 2 env mod',
    'filter 2 keytrack',
    'filter 2 level',
    'filter 2 pan',
    'pre-filter level',
    'pre-filter pan',
    'lfo 1 rate',
    'lfo 1 amplitude',
    'lfo 2 rate',
    'lfo 2 amplitude',
    's&h rate',
    's&h amplitude',
    's&h smoothing',
    'drive level',
    'program level',
    'main/aux balance',
    'pan',
    'amp env amplitude',
    'amp env rate',
    'amp env attack',
    'amp env decay',
    'amp env sust time',
    'amp env sust level',
    'amp env release',
    'filter env amplitude',
    'filter env rate',
    'filter env attack',
    'filter env decay',
    'filter env sust time',
    'filter env sust level',
    'filter env release',
    'p/m env amplitude',
    'p/m env rate',
    'p/m env attack',
    'p/m env decay',
    'p/m env sust time',
    'p/m env sust level',
    'p/m env release',
    'effects mix',
    'effects parameter a',
    'effects parameter b',
    'effects parameter c',
    'effects parameter d',
    'dummy'
]

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
