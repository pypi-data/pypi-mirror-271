from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {'packages': [],
                 'excludes': ['tkinter',
                              'PyQt5',
                              'PyQt5.QtCore',
                              'PyQt5.QtGui',
                              'PyQt5.QtWidgets',
                              'PyQt5.QtQml',
                              'PyQt5.QtBluetooth',
                              'PyQt5.QtQuickWidgets',
                              'PyQt5.QtSensors',
                              'PyQt5.QtSerialPort',
                              'PyQt6.QtSql',
                              'PyQt6.QtQml',
                              'PyQt6.QtBluetooth',
                              'PyQt6.QtQuickWidgets',
                              'PyQt6.QtSensors',
                              'PyQt6.QtSerialPort',
                              'PyQt6.QtSql',
                              'PyQt6.QtQuick',
                              'PyQt6.QtQuick3D',
                              'PyQt6.QtQuickWidgets',
                              'PyQt6.QtDesigner',
                              'PyQt6.QtPdf',
                              'PyQt6.QtPdfWidgets',
                              'PyQt6.QtSensors',
                              'PyQt6.QtTest',
                              'PyQt6.QtTextToSpeech',
                              ]}


import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('sound_source_id\\__main__.py',
               base=base,
               target_name = 'sound_source_id',
               icon='icons/point-right.ico')
]

setup(name='sound_source_id',
    version="0.2.3",
      description = '',
      options = {'build_exe': build_options},
      executables = executables)
