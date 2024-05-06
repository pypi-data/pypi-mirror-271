from RTS_WebUIBuilder.RStyle import RStyle
class RLabel:
    def __init__(self, transformTo:str="p"):
        if transformTo not in ["p", "span", "i", "pre", "b"]:
            raise ValueError(f'"{transformTo}" could not be recognized as a valid HTML element.\n-> "p", "span","i", "pre"')
        self.transformTo = transformTo
        self.displaytext = ""
        self._text = None
        self.style = RStyle()

    

    def _asm(self):
        string = f'<{self.transformTo} '
        if not self.style._asm() is None:
            string += self.style._asm()
        if isinstance(self.displaytext, str):
            string += f'>{self.displaytext}'
        string+=f'</{self.transformTo}>'
        return string

# $abbr<abbreviation>(abbr) 
# $bdo<rtl>(text)
# $q(fajöc,jrkm)
#
#
#
#
#
#
#
#
#
#   