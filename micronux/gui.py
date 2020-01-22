# module: gui.py
#
# Import PySide2, load .ui file
# and show window.
# note: main needs sys module and
# end with sys.exit(app.exec_())

import sys
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QFileDialog, QDialog
from PySide2.QtCore import QFile, Qt
from PySide2.QtGui import QIcon


from micronux.definitions import lcd_messages
from micronux import midi
import micronux.definitions as df
import micronux.exporter as exp
import micronux.effects as fx

### just to remove an ugly error message
from PySide2.QtCore import QCoreApplication
QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)

class micronux_ui:
    """gui object"""

    def __init__(self, settings_list, allSettings):
        self.app = QApplication(sys.argv)
        self.app.setStyle('fusion')

        self.settings_list = settings_list
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

        self.prev_setting = ''

        self.button_groups = [
            self.win.osc_1_waveform,
            self.win.osc_2_waveform,
            self.win.osc_3_waveform
        ]

        self.loaded = False


    def pass_to_lcd(self):
        focused = self.app.focusWidget()
        t = type(focused).__name__
        if (t == 'QDial') or (t == 'QSlider'):
            val = focused.value()
            set = self.allSettings[focused.objectName()]
            self.lcd_update(set, val)


    def fx_switch(self):
        fx.switch(self)


    def lcd_update(self, setting, val):
        v, u = setting.disp_val(val)
        self.lcdV.setText(v)
        self.lcdU.setText(u)
        if self.prev_setting != setting.widget_name:
            self.lcdN.setText(setting.label)
            self.prev_setting = setting.widget_name


    def lcd_message(self, type):
        msg = lcd_messages
        if type in msg:
            self.lcdV.setText(msg[type][0])
            self.lcdU.setText(msg[type][1])
            self.lcdN.setText(msg[type][2])


    def pass_to_exp(self):
        if self.loaded:
            exp.setting_changed(self)


    def connect_widgets(self):
        # Connecting buttongroups
        for group in self.button_groups:
            group.buttonClicked.connect(self.pass_to_exp)

        # Connecting widgets
        for widget in self.app.allWidgets():
            w_name = widget.objectName()
            w_type = type(widget).__name__
            if w_type in df.easy_numbers:
                widget.valueChanged.connect(self.pass_to_exp)
                # pass slider values to 'lcd'
                if (w_type == 'QDial') or (w_type == 'QSlider'):
                    widget.valueChanged.connect(self.pass_to_lcd)
            elif w_type == 'QComboBox':
                widget.currentIndexChanged.connect(self.pass_to_exp)
                if w_name.startswith('fx') and w_name.endswith('type'):
                    widget.currentIndexChanged.connect(self.fx_switch)
            elif w_type == 'QCheckBox':
                widget.stateChanged.connect(self.pass_to_exp)

        # Show and connect MIDI ports combobox
        midi_ports = midi.list_midi_ports()
        if len(midi_ports):
            for port in midi_ports:
                self.win.ctrl_midi_port.addItems([port])
        else:
            self.win.ctrl_midi_port.addItems(['No MIDI port'])

        def change_midi_port():
            port_name = self.win.ctrl_midi_port.currentText()
            mx.midi_port = midi.check_midi_port(port_name)

        self.win.ctrl_midi_port.currentIndexChanged.connect(change_midi_port)


    def assign_values(self, settings_list, allSettings):
        self.loaded = False
        # Assign values to widgets
        for group in self.button_groups:
            for button in group.buttons():
                button_name = button.objectName().rsplit('_', 1)[-1]
                value = allSettings[group.objectName()].value
                if value.startswith(button_name):
                    button.toggle()

        for widget in self.app.allWidgets():
            w_name = widget.objectName()
            w_type = type(widget).__name__
            if w_name in settings_list:
                value = allSettings[w_name].value

                if w_type == 'QCheckBox':
                    if (value == 'on') or (value == 'offset'):
                        widget.setChecked(True)
                    elif (value == 'off') or (value == 'absolute'):
                        widget.setChecked(False)

                elif w_type == 'QComboBox':
                    # display better dropdown choices
                    keyword = allSettings[w_name].trim_val
                    if value in df.keywords:
                        keyword = df.keywords[value]
                    new_index = widget.findText(keyword)
                    widget.setCurrentIndex(new_index)

                    if w_name == 'fx_type':
                        self.win.fx_toolBox.setItemText(
                            0, widget.currentText() )
                        fx.set_fx(self, 1)
                        if widget.currentText() == 'bypass':
                            self.win.fx_toolBox.setCurrentIndex(1)
                    if w_name == 'fx2_type':
                        self.win.fx_toolBox.setItemText(
                            1, widget.currentText() )
                        fx.set_fx(self, 2)
                        if widget.currentText() == 'bypass':
                            self.win.fx_toolBox.setCurrentIndex(0)

                elif w_type in df.easy_numbers:
                    widget.setValue(allSettings[w_name].normalise_val())

                elif w_type in df.easy_strings:
                    widget.setText(value)

        self.win.setWindowTitle(allSettings['name'].value+" | Micronux")
        self.win.output_level.setFocus()


        self.loaded = True
