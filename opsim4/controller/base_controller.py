__all__ = ["BaseController"]

class BaseController(object):
    """This class handles the basic set of information for the view controllers.
    """

    def __init__(self, name):
        """Initialize the class.

        Parameters
        ----------
        name : str
            The name of tab the controller is responsible for.
        """
        self.name = name
        self.model = None
        self.widget = None

    def get_tab(self):
        """Return the view controller's widget.
        """
        return self.widget
