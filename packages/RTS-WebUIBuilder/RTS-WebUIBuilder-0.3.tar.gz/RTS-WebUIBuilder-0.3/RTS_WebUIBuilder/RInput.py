from .RStyle import RStyle

class RTextInput:
    def __init__(self) -> None:
        self._hasStyle = False
        self._type = None
        self._id = None
        self._class = None
        self._min = 0
        self._max = 0
        self._placeholder = None
        
        self.style = RStyle()

    def placeholder(self, text:str) -> None:
        if not isinstance(text, str):
            raise ValueError("Placeholder must be a string.") 
        self._placeholder = text


    def _asm(self) -> str:
        if not self._type:
            print("WARNING: RTextInput Type not set. Defaulting to text. \n .inputPlainText(),\n .inputPassword(),\n .inputEmail(),\n .inputNumber(),\n .inputDate(),\n .inputTime()\n to set the type.")
            self._type = "text"


        string = f'<input type="{self._type}"'
        if self._id: 
            string += f'id="{self._id} "'
        if self._class:
            string += f'class="{self._class} "'
        if self._min and not self._min == 0:
            string += f'minlength="{self._min} "'
        if self._max and not self._max == 0:
            string += f'maxlength="{self._max} "'
        if self._placeholder:
            string += f'placeholder="{self._placeholder} "'
        if not self.style._asm() == 'style=""':
            string += self.style._asm()
        string += '>\n'
            
        
        return string

    


    def setMinMaxLength(self, min:int=0, max:int=0):
        if min < 0 or max < 0:
            raise ValueError("Neither Min nor Max length can be negative.")
        if min > max:
            raise ValueError("Min length cannot be greater than Max length.")

        self._min = min
        self._max = max

    

    def setIdentifier(self, identType:str, ident:str) -> None:
        if identType not in ["id", "class"]:
            raise ValueError(f'"{identType}" could not be recognized as identifier type.\n-> "id", "class"')
        
        if identType == "id":
            self._id = ident

        if identType == "class":
            self._class = ident


    def inputPlainText(self) -> None:
        if not self._type:
            self._type = "text"
    
    def inputPassword(self) -> None:
        if not self._type:
            self._type = "password"

    def inputEmail(self) -> None:
        if not self._type:
            self._type = "email"
    
    def inputNumber(self) -> None:
        if not self._type:
            self._type = "number"
    
    def inputDate(self) -> None:
        if not self._type:
            self._type = "date"
    
    def inputTime(self) -> None:
        if not self._type:
            self._type = "time"
