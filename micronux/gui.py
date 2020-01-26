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

    def __init__(self, settings_list, allSettings):
        self.app = QtWidgets.QApplication(sys.argv)
        self.app.setStyle('fusion')

        self.settings_list = settings_list
        self.allSettings = allSettings

        ui_file = QFile('micronux/micronux.ui')
        ui_file.open(QFile.ReadOnly)
        loader = QUiLoader()
        self.win = loader.load(ui_file)
        ui_file.close()

        sw = self.win
        sw.setWindowTitle('Micronux')
        sw.setWindowIcon(QIcon('micronux/icon.png'))

        self.lcdV = sw.display_setting_value
        self.lcdU = sw.display_setting_unit
        self.lcdN = sw.display_setting_name

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
        focused = self.app.focusWidget()
        t = type(focused).__name__
        # changing fx param min/max changes
        # values even tho they're not focused
        if (t == 'QDial') or (t == 'QSlider'):
            value = focused.value()
            cur_widget = self.allSettings[focused.objectName()]
            val, unit = cur_widget.disp_val(value)
            label = cur_widget.label
            if len(label) == 1:
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
            self.lcdV.setText(val)
            self.lcdU.setText(unit)
            self.lcdN.setText(label)


    def lcd_message(self, type):
        msg = df.lcd_messages
        if type in msg:
            self.lcdV.setText(msg[type][0])
            self.lcdU.setText(msg[type][1])
            self.lcdN.setText(msg[type][2])


    def update_midi_ports(self):
        self.win.ctrl_midi_port.clear()
        midi_ports = midi.list_midi_ports()
        if len(midi_ports):
            for port in midi_ports:
                self.win.ctrl_midi_port.addItems([port])
            self.win.ctrl_send.setEnabled(True)
            self.win.ctrl_auto_send.setEnabled(True)
        else:
            self.win.ctrl_midi_port.addItems(['No MIDI port'])
            self.win.ctrl_send.setEnabled(False)
            self.win.ctrl_auto_send.setEnabled(False)

    def map_widgets(self, settings_list, allSettings, connect=False):
        self.loaded = False
        # Assign values to widgets
        for group in self.button_groups:
            for button in group.buttons():
                button_name = df.last_word(button.objectName())
                value = allSettings[group.objectName()].value
                if value.startswith(button_name):
                    button.toggle()
            if connect:
                group.buttonClicked.connect(self.pass_to_exp)

        for widget in self.app.allWidgets():
            w_name = widget.objectName()
            w_type = type(widget).__name__
            if w_name in settings_list:
                value = allSettings[w_name].value

                if w_type == 'QCheckBox':
                    if value in df.chbox['checked']:
                        widget.setChecked(True)
                    elif value in df.chbox['unchecked']:
                        widget.setChecked(False)
                    if connect:
                        widget.stateChanged.connect(self.pass_to_exp)

                elif w_type == 'QComboBox':
                    # display better dropdown choices
                    keyword = allSettings[w_name].trim_val
                    if value in df.nicer_names:
                        keyword = df.nicer_names[value]
                    new_index = widget.findText(keyword)
                    widget.setCurrentIndex(new_index)
                    if connect:
                        widget.currentIndexChanged.connect(self.pass_to_exp)

                    if w_name.startswith('fx') and w_name.endswith('type'):
                        f = 0
                        if '2' in w_name:
                            f = 1
                        self.win.fx_toolBox.setItemText(
                            f, widget.currentText() )
                        self.fx_setup(f + 1)
                        if widget.currentText() != 'bypass':
                            self.win.fx_toolBox.setCurrentIndex(f)
                        if connect:
                            widget.currentIndexChanged.connect(self.fx_switch)

                elif w_type in df.easy_numbers:
                    widget.setValue(allSettings[w_name].normalise_val())
                    if connect:
                        widget.sliderReleased.connect(self.pass_to_exp)
                        if (w_type == 'QDial') or (w_type == 'QSlider'):
                            widget.valueChanged.connect(self.lcd_update)

                elif w_type in df.easy_strings:
                    widget.setText(value)

        if connect:
            self.update_midi_ports()
            self.win.ctrl_midi_update.clicked.connect(self.update_midi_ports)

        self.win.setWindowTitle(allSettings['name'].value+" | Micronux")
        self.win.output_level.setFocus()

        self.loaded = True
