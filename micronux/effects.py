# module effects.py
#
# definitions and functions for effects


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
'f': ['sync', tempo_sync]
}
chorus['name'] = 'chorus'

theta_flanger = chorus.copy()
theta_flanger['a'][1]['min'] = -100
theta_flanger['name'] = 'theta flanger'

thru_0_flanger = theta_flanger.copy()
thru_0_flanger['name'] = 'thru 0 flanger'

super_phaser = theta_flanger.copy()
super_phaser['b'] = ['frequency', notch_frequency]
string_phaser = super_phaser.copy()
super_phaser['f'] = ['stages', stages]
super_phaser['g'] = ['sync', tempo_sync]

super_phaser['name'] = 'super phaser'
string_phaser['name'] = 'string phaser'

vocoder = {
'a': ['gain', analysis_gain],
'b': ['sibilance', sibilance_boost],
'c': ['decay', decay],
'd': ['band shift', band_shift],
'e': ['synthesis in', synthesis_input],
'f': ['analysis in', analysis_signal_in],
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

effects_list = [
bypass, super_phaser, string_phaser,
theta_flanger, thru_0_flanger, chorus, vocoder,
mono_delay, stereo_delay, split_LR_delay, hall_reverb,
plate_reverb, room_reverb
]

if __name__ == "__main__":
    for effect in effects_list:
        for setting in effect:
            print(effect[setting])
        print('----------------------------------')
