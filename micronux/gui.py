# module: gui.py
#
# user interface


import sys
from PySide2 import QtWidgets
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile, Qt, QTimer, QCoreApplication
from PySide2.QtGui import QIcon

from micronux import midi, exporter, qlogdial
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
        loader.registerCustomWidget(qlogdial.QLogDial)
        self.win = loader.load(ui_file)
        ui_file.close()

        self.win.setWindowTitle('Micronux')
        self.win.setWindowIcon(QIcon('micronux/icon.png'))

        self.lcdV = self.win.display_setting_value
        self.lcdU = self.win.display_setting_unit
        self.lcdN = self.win.display_setting_name

        self.button_groups = df.get_button_groups(self.win)

        # Re-initialize QLogDial widgets
        logDials = self.win.findChildren(qlogdial.QLogDial)
        for logDial in logDials:
            logDial.initNatural()

        self.loaded = False

    def col(self, obj, col):
        line = 'color:'+col
        obj.setStyleSheet(line)

    color_off = '#555'
    color_on = '#bbb'


    def osc_mute(self):
        '''Visual feedback when osc * level at 0'''
        sw = self.win
        fw = self.app.focusWidget()
        osc_labels = self.get_osc_labels(fw.objectName())
        if fw.value() == 0:
            for w in osc_labels:
                self.col(w, self.color_off)
        else:
            for w in osc_labels:
                self.col(w, self.color_on)

    def get_osc_labels(self, name):
        sw = self.win
        if '1' in name:
            osc_labels = [sw.osc_1_label, sw.label_pre_mix_osc1]
        elif '2' in name:
            osc_labels = [sw.osc_2_label, sw.label_pre_mix_osc2]
        elif '3' in name:
            osc_labels = [sw.osc_3_label, sw.label_pre_mix_osc3]
        return osc_labels


    def filter_mute(self):
        '''Visual feedback when filter * level at 0'''
        sw = self.win
        fw = self.app.focusWidget()
        filter_labels = self.get_filter_labels(fw.objectName())
        if fw.value() == 0:
            for w in filter_labels:
                self.col(w, self.color_off)
        else:
            for w in filter_labels:
                self.col(w, self.color_on)

    def get_filter_labels(self, name):
        sw = self.win
        if '1' in name:
            filter_labels = [sw.filter_1_label, sw.label_post_mix_filter_1]
        elif '2' in name:
            filter_labels = [sw.filter_2_label, sw.label_post_mix_filter_2]
        return filter_labels


    def fx_switch(self):
        '''Update fx toolBox tab focus on fx change'''
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


    def fx_sync_param(self):
        '''Find and toggle fx param when synced'''
        sw = self.win
        # fx param c synced related widgets
        fpc = [sw.fx_param_c, sw.label_fx_param_c]
        fpcm = sw.fx_param_c_synced # multiplier comboBox
        # fx param a
        fpa = [sw.fx2_param_a, sw.label_fx2_param_a]
        fpam = sw.fx2_param_a_synced
        fx1 = sw.fx_type.currentText()
        fx2 = sw.fx2_type.currentText()
        if fx1 in df.fx_synced:
            switch = sw.fx_param_f
            if fx1 == 'super phaser':
                switch = sw.fx_param_g
            if switch.value():
                self.sync_switch(False, fpc, fpcm)
            else:
                self.sync_switch(True, fpc, fpcm)
        else:
            self.sync_switch(True, fpc, fpcm)
        if fx2 in df.fx_synced:
            switch = sw.fx2_param_d
            if switch.value():
                self.sync_switch(False, fpa, fpam)
            else:
                self.sync_switch(True, fpa, fpam)
        else:
            self.sync_switch(True, fpa, fpam)

    def sync_switch(self, toggle, fp, mult):
        if toggle:
            for w in fp:
                w.setEnabled(True)
            self.col(mult, self.color_off)
            mult.setEnabled(False)
        else:
            for w in fp:
                w.setEnabled(False)
            self.col(mult, self.color_on)
            mult.setEnabled(True)


    def fx_setup(self, fx_num):
        '''Update fx param labels and widgets' min/max'''
        if fx_num == 1:
            fx_group = self.win.fx_1
            fx_sel = self.win.fx_type.currentText()
            fx_sync_w = self.win.fx_param_c_synced
        elif fx_num == 2:
            fx_group = self.win.fx_2
            fx_sel = self.win.fx2_type.currentText()
            fx_sync_w = self.win.fx2_param_a_synced

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
        if fx_sel not in df.fx_synced:
            fx_sync_w.hide()
        else:
            fx_sync_w.show()
        self.fx_sync_param()

    def pass_to_exp(self):
        if self.loaded:
            exporter.setting_changed(self)


    def pop_down(self):
        self.win.pop.hide()


    def pop_up(self):
        self.win.pop.show()
        self.win.pop.raise_()


    def rename_dialogue(self):
        cur_name = self.allSettings['name'].value
        new_name, okPressed = QtWidgets.QInputDialog.getText(self.win,
            "Rename Program",
            "Any program with the same name\non the Micron will be overwritten.",
            QtWidgets.QLineEdit.Normal, cur_name)
        if okPressed and new_name != '':
            if not new_name == cur_name:
                self.allSettings['name'].value = new_name
                self.win.name.setText(new_name)


    def lcd_update(self):
        '''update display with value, unit and label'''
        if self.loaded:
            focused = self.app.focusWidget()
            cur_name = focused.objectName()
            t = type(focused).__name__
            label = ''
            if 'waveform' in cur_name:
                cur_name = df.rm_last_word(cur_name)
                label = self.allSettings[cur_name].label
            else:
                cur_widget = self.allSettings[cur_name]
                label = cur_widget.label
            val = ''
            unit = ''
            # changing fx param min/max changes
            # values even tho they're not focused
            if t == 'QDial' or t == 'QLogDial' or t == 'QSlider':
                value = focused.naturalValue if t == 'QLogDial' else focused.value()
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
                    if label in df.param_disp:
                        val = df.param_disp[label][int(val)]

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
        style = start_style+self.color_off+'}'
        sel_preset = self.win.tracking_preset.currentText()
        sel_num = self.win.tracking_numpoints.currentText()
        if sel_preset == 'custom':
            style = start_style+self.color_on+'}'
        group = self.win.tracking_groupBox
        track_sliders = group.findChildren(QtWidgets.QSlider)
        etp = df.get_edge_track_points(self.win)
        for widget in track_sliders:
            if sel_num == '12' and widget in etp:
                widget.setStyleSheet(start_style+self.color_off+'}')
            else:
                widget.setStyleSheet(style)


    def map_widgets(self, allSettings, startup=False):
        self.allSettings = allSettings
        self.loaded = False
        sw = self.win
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
            if w_name in allSettings:
                w_type = type(widget).__name__
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
                    if startup:
                        widget.currentIndexChanged.connect(self.pass_to_exp)
                        widget.currentIndexChanged.connect(self.lcd_update)
                        # Fill in inputs from definitions
                        if w_name == 'sh_input':
                            widget.addItems(df.sh_inputs)
                        if w_name == 'tracking_input':
                            widget.addItems(df.tracking_inputs)
                        if w_name.startswith('mod_'):
                            if w_name.endswith('_source'):
                                widget.addItems(df.mod_inputs)
                            elif w_name.endswith('_dest'):
                                widget.addItems(df.mod_dests)
                        if 'synced' in w_name:
                            widget.addItems(df.sync_mult)
                        if w_name.startswith('knob_'):
                            widget.addItems(df.knobs_assign)
                    # Display better dropdown choices
                    keyword = allSettings[w_name].trim_val
                    if value in df.nicer_names:
                        keyword = df.nicer_names[value]
                    new_index = widget.findText(keyword)
                    widget.setCurrentIndex(new_index)

                    if w_name == 'tracking_numpoints' or w_name == 'tracking_preset':
                        self.set_track_points()
                        if startup:
                            widget.currentIndexChanged.connect(self.set_track_points)
                    # focus fx tabs
                    if w_name.startswith('fx') and w_name.endswith('type'):
                        f = 0
                        if '2' in w_name:
                            f = 1
                        sw.fx_toolBox.setItemText(
                            f, widget.currentText() )
                        self.fx_setup(f + 1)
                        if widget.currentText() != 'bypass':
                            sw.fx_toolBox.setCurrentIndex(f)
                        if startup:
                            widget.currentIndexChanged.connect(self.fx_switch)


                elif w_type == 'QDial' or w_type == 'QLogDial' or w_type == 'QSlider':
                    norm_val = allSettings[w_name].normalise_val()
                    widget.setValue(norm_val)
                    val, unit = allSettings[w_name].disp_val(norm_val)
                    tool_tip = allSettings[w_name].label+'<br>'+val+unit
                    widget.setToolTip(tool_tip)
                    if startup:
                        widget.valueChanged.connect(self.pass_to_exp)
                        widget.valueChanged.connect(self.lcd_update)
                        if w_name in df.sync_switches:
                            widget.valueChanged.connect(self.fx_sync_param)
                    # Show when osc and filter are muted by dimming label
                    if w_name.startswith('osc_') and w_name.endswith('_level'):
                        osc_labels = self.get_osc_labels(w_name)
                        for w in osc_labels:
                            if norm_val == 0:
                                self.col(w, self.color_off)
                            else:
                                self.col(w, self.color_on)
                        if startup:
                            widget.valueChanged.connect(self.osc_mute)
                    if w_name.startswith('filter_') and w_name.endswith('_level'):
                        filter_labels = self.get_filter_labels(w_name)
                        for w in filter_labels:
                            if norm_val == 0:
                                self.col(w, self.color_off)
                            else:
                                self.col(w, self.color_on)
                        if startup:
                            widget.valueChanged.connect(self.filter_mute)


                elif w_type == 'QLabel' or w_type == 'QLineEdit' or w_type == 'QPushButton':
                    widget.setText(value)

        if startup:
            self.update_midi_ports()
            sw.ctrl_midi_update.clicked.connect(self.update_midi_ports)

        sw.setWindowTitle(allSettings['name'].value+" | Micronux")
        sw.output_level.setFocus()

        self.loaded = True
