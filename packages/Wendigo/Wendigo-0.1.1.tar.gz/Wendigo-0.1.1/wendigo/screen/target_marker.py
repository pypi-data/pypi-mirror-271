from collections.abc import Callable
from wendigo import Area, Colors, Keys
from wendigo.logger import Logger
from wendigo.device.core import FormKeys
from wendigo.screen.dll import TargetMarker as DllTargetMarker, TargetMarkEventHandler
from wendigo.screen.target_form import TargetForm
from wendigo.system import Rectangle

class TargetMarker(DllTargetMarker):
    """
    Target marker.
    """
    @classmethod
    def mark(cls, area: Area, border_width: int=None, border_color: Colors=None) -> TargetForm:
        """
        Mark an area.

        Parameters
        ----------
        area: Area.
        border_width: Border width.
        border_color: Border color.

        Returns
        -------
        target: Target.
        """
        return TargetForm(cls.Mark(Rectangle(area.x, area.y, area.width, area.height), border_width, border_color))

    @classmethod
    def get_event_handler(cls, event_handler: Callable[[list[TargetForm]], None]) -> TargetMarkEventHandler:
        """
        Get an event handler.

        Parameters
        ----------
        event_handler: Event handler.

        Returns
        -------
        target_mark_event_handler: Target mark event handler.
        """
        def wrapper(event_args):
            try:
                event_handler([TargetForm(target) for target in event_args.Targets])
            except:
                Logger.exception("An exception raised in event hadler")
        return TargetMarkEventHandler(wrapper)

    @classmethod
    def mark_by_drag(cls, event_handler: Callable[[list[TargetForm]], None],
        keys: list[Keys]=None, n: int=1, border_width: int | list[int]=None, border_color: Colors | list[Colors]=None):
        """
        Mark areas by drag.

        Parameters
        ----------
        event_handler: Event handler.
        keys: Keys.
        n: Number of targets.
        border_width: Border width(s).
        border_color: Border color(s).
        """
        cls.MarkByDrag(cls.get_event_handler(event_handler), FormKeys(keys), n, border_width, border_color)