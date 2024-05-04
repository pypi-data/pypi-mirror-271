class DummyClass:
    pass
from .RStyle import RStyle
from .RFrame import RFrame
from .RLabel import RLabel
from .RInput import RTextInput
from .RBox import RBox
from .RGroupStyle import RGroupStyle
try:
    from RTS_WebUIBuilder.RQuickScripts import RQuickScripts
except ImportError:
    RQuickScripts = DummyClass
from .RTitle import RTitle
from typing import Union

class RBody:
    def __init__(self):
        self.elements = {}
        self.style = RStyle()
        self._scrollbar = True
        self._fontimport = None
    

    def __setattr__(self, name, value):
        if isinstance(value, (RBox, RFrame, RLabel, RTextInput,RTitle, RGroupStyle,RQuickScripts)) and name not in ['elements', 'style', '_id', '_class',"_scrollbar","_fontimport"]:
            self.elements[name] = value
        elif name in ['elements', 'style', '_id', '_class','_scrollbar','_fontimport']:
            super().__setattr__(name, value)
        else:
            raise ValueError("Can not add an unrecognized element to the box. Given type: "+str(type(value)))
        
    def __getattr__(self, name):
        if name in self.elements:
            return self.elements[name]
        else:
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

    def removeScrollbar(self):
        self._scrollbar = False
    def _asm(self):
        string = "<body"
        if not self.style._asm() is None:
            string += f' {self.style._asm()}'
        if self._scrollbar is False:
            string += r'-ms-overflow-style: none; scrollbar-width: none; '
        string += ">\n"    
        if self._scrollbar is False:
            string += r'<style>body::-webkit-scrollbar {display: none;}</style>'
        if self._fontimport:
            string += self.style.importFonts(self._fontimport)
        for _, element in self.elements.items():
            if isinstance(element, RQuickScripts):
                string += f'    {element.get()}'
                continue
            asm = f'    {element._asm()}'
            asm_lines = asm.splitlines()
            asm_tabbed = "\n    ".join(asm_lines)
            string += f'    {asm_tabbed}'
        string += "\n</body>\n"
        return string