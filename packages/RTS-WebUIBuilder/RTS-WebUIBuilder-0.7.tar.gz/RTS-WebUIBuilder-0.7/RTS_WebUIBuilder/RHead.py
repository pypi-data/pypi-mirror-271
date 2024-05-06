from RTS_WebUIBuilder import *
from typing import Union
class RHeader:
    def __init__(self):
        self._meta = []
        """"Set with .addMeta(name: str, content: str) -> None"""
        self.charset = "UTF-8"
    
    def addMeta(self, name:str, content:str) -> None:
        """Add a meta tag to the header of the document.

        Args:
            name:str => The name of the meta tag. (REQUIRED)
            content:str => The content of the meta tag. (REQUIRED)
        """
        if name not in ["viewport", "author", "description", "keywords", "robots"]:
            raise ValueError(f'"{name}"could not be recognized as meta tag.\n-> "viewport", "author", "description", "keywords", "robots"')
        metadata = [name, content]
        self._meta.append(metadata)





    def _asm(self) -> str:
        """Not intended for direct use, will be automaticly called during the compilation of the document.\n
        However it can be called for debugging purposes if the compiler generates unexpected content."""
        header = "<head>\n"
        
        for meta in self._meta:
            header += f'    <meta name="{meta[0]}" content="{meta[1]}">\n'

        header += "</head>\n"
        return header

