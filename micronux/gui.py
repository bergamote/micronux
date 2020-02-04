# module: gui.py
#
# user interface


import sys
from PySide2 import QtWidgets
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile, Qt, QTimer, QCoreApplication
from PySide2.QtGui import QIcon

from micronux import midi, exporter
import micronux.definitions as df


### just to remove an ugly error message
QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)


class micronux_ui:
    """gui object"""

    def __init__(self, allSettings):
        self.app = QtWidgets.QApplication(sys.argv)
        self.app.setStyle('fusion')

        self.allSettings = allSettings

        ui_file = QFile('micronux/micronux.ui')
        ui_file.open(QFile.ReadOnly)
        loader = QUiLoader()
        self.win = loader.load(ui_file)
        ui_file.close()

        self.win.setWindowTitle('Micronux')
        self.win.setWindowIcon(QIcon('micronux/icon.png'))

        self.lcdV = self.win.display_setting_value
        self.lcdU = self.win.display_setting_unit
        self.lcdN = self.win.display_setting_name

        self.button_groups = df.get_button_groups(self.win)

        self.loaded = False

    # Update fx toolBox on fx change
    def fx_switch(self):
        if self.loaded:
            fx = self.app.focusWidget()
            tb = self.win.fx_toolBox
            f = 0
            if '2' in fx.objectName():
                f = 1
            self.fx_setup(f + 1)
            tb.setItemText(f,fx.currentText())
            if fx.currentText() != 'bypass':
                tb.setCurrentIndex(f)

    # Update fx labels and widgets' min/max
    def fx_setup(self, fx_num):
        if fx_num == 1:
            fx_group = self.win.fx_1
            fx_sel = self.win.fx_type.currentText()
        elif fx_num == 2:
            fx_group = self.win.fx_2
            fx_sel = self.win.fx2_type.currentText()

        fx_detail = df.fx_types[fx_sel]
        labels = fx_group.findChildren(QtWidgets.QLabel)
        for label in labels:
            param = label.objectName()[-1:]
            label.setText(fx_detail[param][0])
        dials = fx_group.findChildren(QtWidgets.QDial)
        for dial in dials:
            param = dial.objectName()[-1:]
            if fx_detail[param][1]:
                min = fx_detail[param][1]['min']
                max = fx_detail[param][1]['max']
                dial.setRange(min, max)
            else:
                dial.setRange(0, 0)


    def pass_to_exp(self):
        if self.loaded:
            exporter.setting_changed(self)


    def pop_down(self):
        self.win.pop.hide()

    def pop_up(self):
        self.win.pop.show()
        self.win.pop.raise_()


    def lcd_update(self):
        if self.loaded:
            focused = self.app.focusWidget()
            cur_name = focused.objectName()
            label = ''
            if 'waveform' in focused.objectName():
                cur_name = df.rm_last_word(cur_name)
                label = self.allSettings[cur_name].label
            else:
                cur_widget = self.allSettings[cur_name]
                label = cur_widget.label
            t = type(focused).__name__
            val = ''
            unit = ''
            # changing fx param min/max changes
            # values even tho they're not focused
            if (t == 'QDial') or (t == 'QSlider'):
                value = focused.value()
                val, unit = cur_widget.disp_val(value)
                label = cur_widget.label
                if len(label) == 1 and not label.isdigit():
                    # fx params
                    tb = focused.parent()
                    if df.last_word(tb.objectName()) == '2':
                        fx = self.win.fx2_type.currentText()
                    else:
                        fx = self.win.fx_type.currentText()
                    fx_detail = df.fx_types[fx][label]
                    label = fx_detail[0]
                    if len(fx_detail[1]) == 3:
                        unit = fx_detail[1]['unit']
                tool_tip = self.allSettings[cur_name].label+'<br>'+val+unit
                focused.setToolTip(tool_tip)
            if label.endswith(('type', 'time', 'level')):
                label = df.rm_last_word(cur_name).replace('_',' ')
                if label.startswith('env '):
                    label = label.split()[-1]
            if label in df.nicer_names:
                label = df.nicer_names[label]
            self.lcdV.setText(val)
            self.lcdU.setText(unit)
            self.lcdN.setText(label)


    def lcd_message(self, type):
        msg = df.lcd_messages
        if type in msg:
            self.lcdV.setText(msg[type][0])
            self.lcdU.setText(msg[type][1])
            self.lcdN.setText(msg[type][2])

    def lcd_clear(self):
        self.lcdV.setText('')
        self.lcdU.setText('')
        self.lcdN.setText('')


    def update_midi_ports(self):
        self.win.ctrl_midi_port.clear()
        midi_ports = midi.list_midi_ports()
        enabled_buttons = [
            self.win.ctrl_receive,
            self.win.ctrl_send,
            self.win.ctrl_auto_send
        ]
        if len(midi_ports):
            for port in midi_ports:
                self.win.ctrl_midi_port.addItems([port])
            for b in enabled_buttons:
                b.setEnabled(True)
        else:
            self.win.ctrl_midi_port.addItems(['No MIDI port'])
            self.win.ctrl_midi_port.setEnabled(False)
            for b in enabled_buttons:
                b.setEnabled(False)

    def set_track_points(self):
        start_style = '::handle:vertical {background:'
        style = start_style+'#999}'
        sel_preset = self.win.tracking_preset.currentText()
        sel_num = self.win.tracking_numpoints.currentText()
        if sel_preset == 'custom':
            style = start_style+'#444}'
        group = self.win.tracking_groupBox
        track_sliders = group.findChildren(QtWidgets.QSlider)
        etp = df.get_edge_track_points(self.win)
        for widget in track_sliders:
            if sel_num == '12' and widget in etp:
                widget.setStyleSheet(start_style+'#999}')
            else:
                widget.setStyleSheet(style)

    def map_widgets(self, allSettings, startup=False):
        self.allSettings = allSettings
        self.loaded = False
        # Assign values to widgets
        for group in self.button_groups:
            for button in group.buttons():
                button_name = df.last_word(button.objectName())
                value = allSettings[group.objectName()].value
                if value.startswith(button_name):
                    button.toggle()
            if startup:
                group.buttonClicked.connect(self.pass_to_exp)
                group.buttonClicked.connect(self.lcd_update)

        for widget in self.app.allWidgets():
            w_name = widget.objectName()
            w_type = type(widget).__name__
            if w_name in allSettings:
                value = allSettings[w_name].value

                if w_type == 'QCheckBox':
                    if value in df.chbox['checked']:
                        widget.setChecked(True)
                    elif value in df.chbox['unchecked']:
                        widget.setChecked(False)
                    if startup:
                        widget.stateChanged.connect(self.pass_to_exp)
                        widget.stateChanged.connect(self.lcd_update)
                elif w_type == 'QComboBox':
                    # Fill in input combo boxes
                    if w_name == 'sh_input':
                        if startup:
                            widget.addItems(df.sh_inputs)
                    if w_name == 'tracking_input':
                        if startup:
                            widget.addItems(df.tracking_inputs)
                    if w_name.startswith('mod_') and w_name.endswith('_source'):
                        if startup:
                            widget.addItems(df.mod_inputs)
                    if w_name.startswith('mod_') and w_name.endswith('_dest'):
                        if startup:
                            widget.addItems(df.mod_dests)
                    if w_name.startswith('knob_'):
                        # copy from x knob
                        if startup:
                            if 'x' not in w_name:
                                x = self.win.knob_x_param
                                inputs_list = [x.itemText(i) for i in range(x.count())]
                                widget.addItems(inputs_list)
                    # Display better dropdown choices
                    keyword = allSettings[w_name].trim_val
                    if value in df.nicer_names:
                        keyword = df.nicer_names[value]
                    new_index = widget.findText(keyword)
                    widget.setCurrentIndex(new_index)
                    if startup:
                        widget.currentIndexChanged.connect(self.pass_to_exp)
                        widget.currentIndexChanged.connect(self.lcd_update)
                    if w_name == 'tracking_numpoints' or w_name == 'tracking_preset':
                        self.set_track_points()
                        if startup:
                            widget.currentIndexChanged.connect(self.set_track_points)
                    # focus fx tabs
                    if w_name.startswith('fx') and w_name.endswith('type'):
                        f = 0
                        if '2' in w_name:
                            f = 1
                        self.win.fx_toolBox.setItemText(
                            f, widget.currentText() )
                        self.fx_setup(f + 1)
                        if widget.currentText() != 'bypass':
                            self.win.fx_toolBox.setCurrentIndex(f)
                        if startup:
                            widget.currentIndexChanged.connect(self.fx_switch)


                elif w_type == 'QDial' or w_type == 'QSlider':
                    norm_val = allSettings[w_name].normalise_val()
                    widget.setValue(norm_val)
                    val, unit = allSettings[w_name].disp_val(norm_val)
                    tool_tip = allSettings[w_name].label+'<br>'+val+unit
                    widget.setToolTip(tool_tip)
                    if startup:
                        widget.sliderReleased.connect(self.pass_to_exp)
                        widget.valueChanged.connect(self.lcd_update)

                elif w_type == 'QLabel' or w_type == 'QLineEdit':
                    widget.setText(value)

        if startup:
            self.update_midi_ports()
            self.win.ctrl_midi_update.clicked.connect(self.update_midi_ports)

        self.win.setWindowTitle(allSettings['name'].value+" | Micronux")
        self.win.output_level.setFocus()

        self.loaded = True
