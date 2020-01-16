# module effects.py
#
# definitions and functions for effects

from PySide2 import QtWidgets

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

fx_type_list = [
    bypass,
    super_phaser,
    string_phaser,
    theta_flanger,
    thru_0_flanger,
    chorus,
    vocoder
]

fx2_type_list = [
    bypass,
    mono_delay,
    stereo_delay,
    split_LR_delay,
    hall_reverb,
    plate_reverb,
    room_reverb
]

if __name__ == "__main__":
    for effect in effects_list:
        for setting in effect:
            print(effect[setting])
        print('----------------------------------')


# Focus selected effect tab and update
# labels and widgets' min/max
def switch(mx):
    tool_box = mx.window.fx_toolBox
    fx_widget = mx.app.focusWidget()
    if fx_widget.objectName() == 'fx_type':
        tool_box.setCurrentIndex(0)
        tool_box.setItemText(0,fx_widget.currentText())
        set_fx(mx, 1)
    elif fx_widget.objectName() == 'fx2_type':
        tool_box.setCurrentIndex(1)
        tool_box.setItemText(1,fx_widget.currentText())
        set_fx(mx, 2)

def set_fx(mx, fx_num):
    if fx_num == 1:
        fx = fx_type_list[mx.window.fx_type.currentIndex()]
        labels = mx.window.fx_1.findChildren(QtWidgets.QLabel)
        for label in labels:
            name = label.objectName()
            param = name[-1:]
            text = fx[param][0]
            label.setText(text)
        dials = mx.window.fx_1.findChildren(QtWidgets.QDial)
        for dial in dials:
            name = dial.objectName()
            param = name[-1:]
            if fx[param][1]:
                min = fx[param][1]['min']
                max = fx[param][1]['max']
                dial.setRange(min, max)
            else:
                dial.setRange(0, 0)

    if fx_num == 2:
        fx2 = fx2_type_list[mx.window.fx2_type.currentIndex()]
        labels = mx.window.fx_2.findChildren(QtWidgets.QLabel)
        for label in labels:
            name = label.objectName()
            param = name[-1:]
            label.setText(fx2[param][0])
        dials = mx.window.fx_2.findChildren(QtWidgets.QDial)
        for dial in dials:
            name = dial.objectName()
            param = name[-1:]
            if fx2[param][1]:
                min = fx2[param][1]['min']
                max = fx2[param][1]['max']
                dial.setRange(min, max)
            else:
                dial.setRange(0, 0)
