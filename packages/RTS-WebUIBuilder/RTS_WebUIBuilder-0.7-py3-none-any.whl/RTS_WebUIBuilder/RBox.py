from typing import Union
from .RStyle import RStyle
from .RFrame import RFrame
from .RLabel import RLabel
from .RInput import RTextInput
from .RTitle import RTitle
from .RGroupStyle import RGroupStyle


class RBox:
    def __init__(self):
        self.elements = {}
        """Do NOT modify directly, use .addElement(element) instead"""
        
        self.style = RStyle()
        """.style => Access the style settings directly or overwrite the style with an existing RStyle instance"""

        self._id = None
        """Do NOT modify directly, use .setIdentifier(identType, ident) instead"""

        self._class = None
        """Do NOT modify directly, use .setIdentifier(identType, ident) instead"""

        self._onclick = None

    def __setattr__(self, name, value):
        if isinstance(value, (RBox, RFrame, RLabel, RTextInput, RTitle, RGroupStyle)) and name not in ['elements', 'style', '_id', '_class','_onclick']:
            self.elements[name] = value
        elif name in ['elements', 'style', '_id', '_class','_onclick']:
            super().__setattr__(name, value)
        else:
            raise ValueError("Can not add an unrecognized element to the box. Given type: "+str(type(value)))
        
    def __getattr__(self, name):
        if name in self.elements:
            return self.elements[name]
        else:
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")
        
    def setIdentifier(self,*, identType, ident):

        if identType not in ["id", "class"]:
            raise ValueError(f'"{identType}" could not be recognized as identifier type.\n-> "id", "class"')
        
        if identType == "id":
            self._id = ident

        if identType == "class":
            self._class = ident
        
    def clickEvent(self,tocall:str, *args) -> None:
        self._onclick = f'{tocall}({",".join(args)})'

    def _asm(self):
        """Not intended for direct use, will be automaticly called during the compilation of the document.\n
        However it can be called for debugging purposes if the compiler generates unexpected content."""

        string = f'<div '
        if self._id:
            string += f' id="{self._id}"'
        if self._class:
            string += f' class="{self._class}"'
        if self._onclick:
            string += f' onclick="{self._onclick}"'
        if not self.style._asm()is None:
            string += self.style._asm()
        string += '>\n'
        for _, element in self.elements.items():
            string += f'    {element._asm()}'
        string += f'</div>'
            
        
        return string