import math
from PySide2.QtWidgets import QDial
from PySide2.QtCore import Signal, Slot

class QLogDial(QDial):

    naturalValue = 0
    naturalValueChanged = Signal(int)
    scale = 1000000

    def __init__(self, parent):
        super().__init__(parent)
        self.valueChanged.connect(self.onValueChanged)

    def initNatural(self):
        self.setRange(math.floor(math.log(self.minimum()) * self.scale), math.ceil(math.log(self.maximum()) * self.scale))
        self.setSingleStep(10000)
        self.setPageStep(500000)

    @Slot(int)
    def onValueChanged(self, value):
        self.naturalValue = round(pow(math.e, value / self.scale))
        self.naturalValueChanged.emit(self.naturalValue)
