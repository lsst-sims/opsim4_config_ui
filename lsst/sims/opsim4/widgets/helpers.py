from PyQt5 import QtGui, QtWidgets

__all__ = ["get_widget_by_type"]

def get_widget_by_type(widget_type):
    """Get a widget based on specified type.

    Parameters
    ----------
    widget_type : str
        The key name for the type of the QWidget.

    Returns
    -------
    QWidget
        The specific QWidget instance based on the requested type.
    str
        The signal name from the QWidget that informs when the widget is changed.
    """
    switcher = {
        'Str': lineedit_widget,
        'StringList': lineedit_widget,
        'Float': float_widget,
        'FloatList': lineedit_widget,
        'Int': int_widget,
        'Bool': bool_widget,
        'File': file_widget
    }

    func = switcher.get(widget_type, default_widget)
    return func()

def default_widget():
    return (QtWidgets.QWidget(), None)

def float_widget():
    widget = QtWidgets.QLineEdit("0.0")
    widget.setValidator(QtGui.QDoubleValidator())
    return (widget, "editingFinished")

def lineedit_widget():
    return (QtWidgets.QLineEdit(" "), "editingFinished")

def int_widget():
    widget = QtWidgets.QLineEdit("0")
    widget.setValidator(QtGui.QIntValidator())
    return (widget, "editingFinished")

def bool_widget():
    widget = QtWidgets.QCheckBox()
    return (widget, "stateChanged")

def file_widget():
    widget = QtWidgets.QPushButton()
    widget.setCheckable(False)
    return (widget, "clicked")
