


def Apply_AMOLED_Style(self):
    style = open('./themes/AMOLED.qss', 'r')
    style = style.read()
    self.setStyleSheet(style)


def Apply_Aqua_Style(self):
    style = open('./themes/Aqua.qss', 'r')
    style = style.read()
    self.setStyleSheet(style)


def Apply_Classic_Style(self):
    style = open('./themes/Classic.qss', 'r')
    style = style.read()
    self.setStyleSheet(style)

def Apply_Console_Style(self):
    style = open('./themes/Console.qss', 'r')
    style = style.read()
    self.setStyleSheet(style)

def Apply_DarkBlue_Style(self):
    style = open('./themes/DarkBlue.qss', 'r')
    style = style.read()
    self.setStyleSheet(style)

def Apply_DarkGray_Style(self):
    style = open('./themes/DarkGray.qss', 'r')
    style = style.read()
    self.setStyleSheet(style)

def Apply_DarkOrange_Style(self):
    style = open('./themes/DarkOrange.qss', 'r')
    style = style.read()
    self.setStyleSheet(style)


def Apply_ElegantDark_Style(self):
    style = open('./themes/ElegantDark.qss', 'r')
    style = style.read()
    self.setStyleSheet(style)


def Apply_MacOS_Style(self):
    style = open('./themes/MacOS.qss', 'r')
    style = style.read()
    self.setStyleSheet(style)


def Apply_ManjaroMix_Style(self):
    style = open('./themes/ManjaroMix.qss', 'r')
    style = style.read()
    self.setStyleSheet(style)


def Apply_MaterialDark_Style(self):
    style = open('./themes/MaterialDark.qss', 'r')
    style = style.read()
    self.setStyleSheet(style)


def Apply_NeonButtons_Style(self):
    style = open('./themes/NeonButtons.qss', 'r')
    style = style.read()
    self.setStyleSheet(style)


def Apply_Ubuntu_Style(self):
    style = open('./themes/Ubuntu.qss', 'r')
    style = style.read()
    self.setStyleSheet(style)


def Theme_Handler(self):
    self.actionAMOLED.triggered.connect(lambda: self.Apply_AMOLED_Style())
    self.actionAqua.triggered.connect(lambda: self.Apply_Aqua_Style())
    self.actionClassic.triggered.connect(lambda: self.Apply_Classic_Style())
    self.actionConsole.triggered.connect(lambda: self.Apply_Console_Style())
    self.actionDarkBlue.triggered.connect(lambda: self.Apply_DarkBlue_Style())
    self.actionDarkGray.triggered.connect(lambda: self.Apply_DarkGray_Style())
    self.actionDarkOrange.triggered.connect(lambda: self.Apply_DarkOrange_Style())
    self.actionElegantDark.triggered.connect(lambda: self.Apply_ElegantDark_Style())
    self.actionMacOS.triggered.connect(lambda: self.Apply_MacOS_Style())
    self.actionManjaroMix.triggered.connect(lambda: self.Apply_ManjaroMix_Style())
    self.actionMaterialDark.triggered.connect(lambda: self.Apply_MaterialDark_Style())
    self.actionNeonButtons.triggered.connect(lambda: self.Apply_NeonButtons_Style())
    self.actionUbuntu.triggered.connect(lambda: self.Apply_Ubuntu_Style())