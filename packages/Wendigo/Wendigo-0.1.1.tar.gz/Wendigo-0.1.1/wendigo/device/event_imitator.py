from wendigo import Keys
from wendigo.device.core import FormKeys
from wendigo.device.dll import EventImitator as DllEventImitator

class EventImitator():
    """
    Event imitator.
    """
    @classmethod
    def record(cls, path: str, start_keys: list[Keys], stop_keys: list[Keys]):
        """
        Record device events.
        Key events for start_keys and stop_keys are ignored.

        Parameters
        ----------
        path: File path.
        start_keys: Keys to start recording.
        stop_keys: Keys to stop recording.
        """
        DllEventImitator.Record(path, FormKeys(start_keys), FormKeys(stop_keys))

    @classmethod
    def play(cls, path: str, start_keys: list[Keys], stop_keys: list[Keys]):
        """
        Play device events.

        Parameters
        ----------
        path: File path.
        start_keys: Keys to start playing.
        stop_keys: Keys to stop playing.
        """
        DllEventImitator.Play(path, FormKeys(start_keys), FormKeys(stop_keys))