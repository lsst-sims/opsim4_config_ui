from PyQt5 import QtWidgets

__all__ = ["ListLineEdit"]

class ListLineEdit(QtWidgets.QLineEdit):
    """Wrap a QLineEdit to handle list information.
    """

    def __init__(self, input_text, parent=None):
        """Initialize the class.

        Parameters
        ----------
        input_text : str
            Default text for line edit widget.
        parent : QWidget, optional
            The parent widget of this one.
        """
        QtWidgets.QLineEdit.__init__(self, input_text, parent=parent)

    def text(self, force_list=False):
        """Append a comma on lists.

        Parameters
        ----------
        force_list : bool, optional
            A flag to append a comma on the contents.

        Returns
        -------
        str
            The contents with a comma at the end.
        """
        value = QtWidgets.QLineEdit.text(self)
        if force_list:
            value += ','
        return value
