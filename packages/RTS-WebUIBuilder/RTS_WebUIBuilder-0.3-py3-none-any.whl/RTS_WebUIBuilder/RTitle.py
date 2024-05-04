from RTS_WebUIBuilder.RStyle import RStyle
class RTitle:
    def __init__(self, size=1):
        """size:int between 1 and 6"""
        self.displaytext = ""
        self._text = None
        if not isinstance(size, int):
            raise ValueError("Size must be an integer.")
        if size <= 1 or size >= 6:
            self.size = size
        else:
            raise ValueError("Size must be between 1 and 6.")
        self.style = RStyle()

    

    def _asm(self):
        string = f'<h{self.size} '
        if not self.style._asm() == None:
            string += self.style._asm()
        string += f'>{self.displaytext}</h{self.size}>\n'
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