from .RStyle import RStyle
from typing import Union

class RFrame():
    """This is a IFrame element. 
    Suportet Methods: 
    .style -> is a RStyle instance, can be overwriten with a new RStyle instance or used directly to change the style of the element'
    .loadLazy -> bool -> If True the frame will only load when it is in the viewport
    .dimensions(width: int, height: int) -> Set the dimensions of the IFrame
    """
    def __init__(self,*, src: str) -> None:
        """src: str -> The URL to load, is REQUIRED"""

        self.src :str = src
        """.src is best set during the initialization of the IFrame"""

        self.loadLazy : bool = False
        """.loadLazy ->If True the frame will only load when it is in the viewport"""

        self._dimensions :str = None
        """Set the Dimensions with the .dimensions() method"""

        self.style: RStyle = RStyle()
        """Access the style settings directly or overwrite the style with an existing RStyle instance
        
        Methods:
            read docks of RStyle() for more information"""

    def dimensions(self, width: int = None, height: int = None) -> None:
        """Set the dimensions of the IFrame
        width: int -> The width of the IFrame
        height: int -> The height of the IFrame"""
        self._dimensions = ""
        if not width is None:
            self._dimensions += f"width='{width}' "
        if not height is None:
            self._dimensions += f"height='{height}' "

    def setTitle(self, title: str) -> None:
        """
        Set the title of the frame.

        Args:
            title: str > The title to set.
        """
        self.title = title


    def _asm(self) -> str:
        """Not intended for direct use, will be automaticly called during the compilation of the document.\n
        However it can be called for debugging purposes if the compiler generates unexpected content."""

        string = "<iframe "
        string += f"src='{self.src}' "
        if self.loadLazy:
            string += " loading='lazy' "
        if not self._dimensions is None:
            string += self._dimensions
        if not self.style is None:
            string += self.style._asm()
        string += "/>"
        return string