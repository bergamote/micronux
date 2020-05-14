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
    'ringmod': 'ring mod',
    'extin': 'ext in',
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

sync_mult = [
'16','12','10 2/3','8','6','5 1/3',
'4','3','2 2/3','2','1 1/2','1 1/3',
'1','3/4','2/3','1/2','3/8','1/3',
'1/4','3/16','1/6', '1/8',
'3/32','1/12','1/16'
]

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

midi_cc = []
for i in range(1,120):
    midi_cc.append('midi cc '+str(i))



sh_inputs = general_inputs.copy()
sh_inputs.extend([
    'tracking generator',
    'step track',
])
sh_inputs.extend(midi_cc)

tracking_inputs = general_inputs.copy()
tracking_inputs.append(
    'sh output'
)
tracking_inputs.extend(midi_cc)

mod_inputs = general_inputs.copy()
mod_inputs.insert(0, 'none')
mod_inputs.extend([
    'sh output',
    'tracking generator',
    'step track'
])
mod_inputs.extend(midi_cc)

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

# min/max values
percents = {
    'min': 0,
    'max': 100,
    'unit': '%'
}
wide_percents = {
    'min': -100,
    'max': 100,
    'unit': '%'
}
freq = {
    'min': 10,
    'max': 4800,
    'unit': 'mhz'
}
time = {
    'min': 1,
    'max': 340,
    'unit': 'ms'
}
mono_time = {
    'min': 1,
    'max': 680,
    'unit': 'ms'
}
switch = {
    'min': 0,
    'max': 1,
}
stages = {
    'min': 0,
    'max': 5,
}
tri_state = {
    'min': 0,
    'max': 2
}
param_disp = {
'sync': ['off','on'],
'shape': ['sine','tri'],
'stages': ['4','8','16','32','48','64'],
'synthesis': ['fx ','L','L+R'],
'analysis': ['fx ','R','L+R']
}


# fx details
chorus = {
    'a': ['feedback', percents],
    'b': ['delay', percents],
    'c': ['rate', freq],
    'd': ['depth', percents],
    'e': ['shape', switch],
    'f': ['sync', switch],
    'g': ['---', False],
    'name': 'chorus'
}

theta_flanger = chorus.copy()
theta_flanger['a'] = ['feedback', wide_percents]
theta_flanger['name'] = 'theta flanger'

thru_0_flanger = theta_flanger.copy()
thru_0_flanger['name'] = 'thru 0 flanger'

super_phaser = theta_flanger.copy()
super_phaser['b'] = ['notch', percents]
super_phaser['f'] = ['stages', stages]
super_phaser['g'] = ['sync', switch]
super_phaser['name'] = 'super phaser'

string_phaser = chorus.copy()
string_phaser['b'] = ['notch', percents]
string_phaser['name'] = 'string phaser'

vocoder = {
    'a': ['gain', wide_percents],
    'b': ['sibilance', percents],
    'c': ['decay', percents],
    'd': ['band', wide_percents],
    'e': ['synthesis', tri_state],
    'f': ['analysis', tri_state],
    'g': ['mix', percents],
    'name': 'vocoder'
}

mono_delay = {
    'a': ['time', mono_time],
    'b': ['regen', percents],
    'c': ['brightness', percents],
    'd': ['sync', switch]
}
mono_delay['name'] = 'mono delay'

stereo_delay = mono_delay.copy()
stereo_delay['a'] = ['time', time]
stereo_delay['name'] = 'stereo delay'

split_LR_delay = stereo_delay.copy()
split_LR_delay['a'] = ['left', time]
split_LR_delay['d'] = ['right', time]
split_LR_delay['name'] = 'split L/R delay'

hall_reverb = {
    'a': ['diffusion', percents],
    'b': ['decay', percents],
    'c': ['brightness', percents],
    'd': ['color', time]
}
hall_reverb['name'] = 'hall reverb'
plate_reverb = hall_reverb.copy()
plate_reverb['name'] = 'plate reverb'
room_reverb = hall_reverb.copy()
room_reverb['name'] = 'room reverb'

param_letters = 'abcdefg'
bypass_settings = ['---', False]
bypass = {}
for i in param_letters:
    bypass[i] = bypass_settings
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
fx_synced = [
    'super phaser',
    'string phaser',
    'theta flanger',
    'thru 0 flanger',
    'chorus',
    'mono delay',
    'stereo delay'
]
sync_switches = [
    'fx_param_g',
    'fx_param_f',
    'fx2_param_d'
]

knobs_assign = [
    'Voice Unison',
    'Voice Polyphony',
    'Voice UsnDetune',
    'Voice Portamnto',
    'Voice PortaType',
    'Voice PortaTime',
    'Voice Pitch Whl',
    'Voice AnlgDrift',
    'Voice Osc Sync',
    'Voice FM Amount',
    'Voice FM Type',
    'Osc 1 Waveform',
    'Osc 1 Waveshape',
    'Osc 1 Octave',
    'Osc 1 Transpose',
    'Osc 1 Pitch',
    'Osc 1 PWhlRange',
    'Osc 2 Waveform',
    'Osc 2 Waveshape',
    'Osc 2 Octave',
    'Osc 2 Transpose',
    'Osc 2 Pitch',
    'Osc 2 PWhlRange',
    'Osc 3 Waveform',
    'Osc 3 Waveshape',
    'Osc 3 Octave',
    'Osc 3 Transpose',
    'Osc 3 Pitch',
    'Osc 3 PWhlRange',
    'Pre Osc 1 Level',
    'Pre Osc 2 Level',
    'Pre Osc 3 Level',
    'Pre Ringm Level',
    'Pre Noise Level',
    'Pre ExtIn Level',
    'Pre Osc 1 Balnc',
    'Pre Osc 2 Balnc',
    'Pre Osc 3 Balnc',
    'Pre Ringm Balnc',
    'Pre Noise Balnc',
    'Pre ExtIn Balnc',
    'Pre Series Lvl',
    'Pre Noise Type',
    'Filter 1 Type',
    'Filter 1 Freq',
    'Filter 1 Res',
    'Filter 1 Keytrk',
    'Filter 1 EnvAmt',
    'Filter 2 Offset',
    'Filter 2 Type',
    'Filter 2 Freq',
    'Filter 2 Res',
    'Filter 2 Keytrk',
    'Filter 2 EnvAmt',
    'Post Fltr 1 Lvl',
    'Post Fltr 2 Lvl',
    'Post Preflt Lvl',
    'Post Fltr 1 Pan',
    'Post Fltr 2 Pan',
    'Post Preflt Pan',
    'Post Preflt Src',
    'Post Flt 1 Sign',
    'Out Drive Type',
    'Out Drive Level',
    'Out Pgm Level',
    'Out Fx Mix',
    'Env 1 Atk Time',
    'Env 1 Atk Slope',
    'Env 1 Dcy Time',
    'Env 1 Dcy Slope',
    'Env 1 Sus Time',
    'Env 1 Sus Level',
    'Env 1 Rel Time',
    'Env 1 Rel Slope',
    'Env 1 Velocity',
    'Env 1 Reset',
    'Env 1 Freerun',
    'Env 1 Loop',
    'Env 1 SusPedal',
    'Env 2 Atk Time',
    'Env 2 Atk Slope',
    'Env 2 Dcy Time',
    'Env 2 Dcy Slope',
    'Env 2 Sus Time',
    'Env 2 Sus Level',
    'Env 2 Rel Time',
    'Env 2 Rel Slope',
    'Env 2 Velocity',
    'Env 2 Reset',
    'Env 2 Freerun',
    'Env 2 Loop',
    'Env 2 SusPedal',
    'Env 3 Atk Time',
    'Env 3 Atk Slope',
    'Env 3 Dcy Time',
    'Env 3 Dcy Slope',
    'Env 3 Sus Time',
    'Env 3 Sus Level',
    'Env 3 Rel Time',
    'Env 3 Rel Slope',
    'Env 3 Velocity',
    'Env 3 Reset',
    'Env 3 Freerun',
    'Env 3 Loop',
    'Env 3 SusPedal',
    'LFO 1 TempoSync',
    'LFO 1 Rate',
    'LFO 1 Reset',
    'LFO 1 M1 Slider',
    'LFO 2 TempoSync',
    'LFO 2 Rate',
    'LFO 2 Reset',
    'LFO 2 M1 Slider',
    'S/H TempoSync',
    'S/H Rate',
    'S/H Reset',
    'S/H Input',
    'S/H Smoothing',
    'Track Input',
    'Track Preset',
    'Track Grid',
    'Track Point -16',
    'Track Point -15',
    'Track Point -14',
    'Track Point -13',
    'Track Point -12',
    'Track Point -11',
    'Track Point -10',
    'Track Point -9',
    'Track Point -8',
    'Track Point -7',
    'Track Point -6',
    'Track Point -5',
    'Track Point -4',
    'Track Point -3',
    'Track Point -2',
    'Track Point -1',
    'Track Center',
    'Track Point 1',
    'Track Point 2',
    'Track Point 3',
    'Track Point 4',
    'Track Point 5',
    'Track Point 6',
    'Track Point 7',
    'Track Point 8',
    'Track Point 9',
    'Track Point 10',
    'Track Point 11',
    'Track Point 12',
    'Track Point 13',
    'Track Point 14',
    'Track Point 15',
    'Track Point 16',
    'Category',
    'Knob X Param',
    'Knob Y Param',
    'Knob Z Param',
    'Filter 2 Freq Offset',
    'LFO 1 Rate Sync',
    'LFO 2 Rate Sync',
    'S/H Rate Sync'
]
