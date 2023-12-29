import json


class ControlBaseListener:
    """Base class for ControlListeners.

    Attributes:
        events_data (list): A list to store control events.
        m_listener (object): The underlying listener object.
        filepath (str): The path to the file to save control events.
    """

    events_data = []
    m_listener = None

    def __init__(self, filepath: str, **kwargs):
        """Initialize the listener.

        Args:
            filepath (str): The path to the file to save control events.
        """
        self.filepath = filepath

    def start(self):
        """Start the listener.

        This method is responsible for starting the underlying listener object.
        """
        self.m_listener.start()

    def stop(self):
        """Stop the listener.

        This method is responsible for stopping the underlying listener object.
        """
        self.m_listener.stop()

    def save(self):
        """Save the control events to a file.

        This method iterates through the `events_data` list and saves the events to a JSON file.
        """

        events_data_copy = self.events_data.copy()
        self.events_data = []

        with open(self.filepath, 'a+') as file:
            jd = json.dumps(events_data_copy)
            file.write(f"{jd}\n")
            file.flush()
