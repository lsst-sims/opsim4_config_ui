from PyQt4 import QtGui

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
        'Float': float_widget
    }

    func = switcher.get(widget_type, default_widget)
    return func()

def default_widget():
    return (QtGui.QWidget(), None)

def float_widget():
    widget = QtGui.QLineEdit("0.0")
    widget.setValidator(QtGui.QDoubleValidator())
    return (widget, "editingFinished")

def lineedit_widget():
    return (QtGui.QLineEdit(" "), "editingFinished")
