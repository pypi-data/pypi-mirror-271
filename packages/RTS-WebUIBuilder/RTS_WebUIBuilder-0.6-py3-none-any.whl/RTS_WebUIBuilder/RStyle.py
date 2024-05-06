
class RStyle():
    """RStyle contains the most common Styling attributes for HTML elements.
    
    Args:
        none"""
    def __init__(self):
        self._position = None
        self._width = None
        self._height = None
        self._color = None
        self._margin = None
        self._padding = None
        self._border = ""
        self._alignment = None
        self._justify = None
        self._display = None
        self._borderRD = None
        self._font = None
        self._origin = None
        self._backgroundImage = None
        self._overflow = None
        self._ident = None


    def backgroundImage(self, url:str, repeat:str="no-repeat", size:str="cover", position:str="center") -> None:
        if not isinstance(url, str):
            raise ValueError("URL must be a string.")
        if repeat not in ["no-repeat", "repeat", "repeat-x", "repeat-y"]:
            raise ValueError(f'"{repeat}" could not be recognized as repeat type.\n-> "no-repeat", "repeat", "repeat-x", "repeat-y"')
        if size not in ["cover", "contain", "auto"]:
            raise ValueError(f'"{size}" could not be recognized as size type.\n-> "cover", "contain", "auto"')
        if position not in ["center", "top", "right", "bottom", "left"]:
            raise ValueError(f'"{position}" could not be recognized as position type.\n-> "center", "top", "right", "bottom", "left"')
        self._backgroundImage = f"background-image: url('{url}'); background-repeat: {repeat}; background-size: {size}; background-position: {position};"
        self._hasStyle = True
        pass

    def importFonts(self, fontlist:list[tuple]) -> str:
        string = "<style>\n"
        for font in fontlist:
            string += r'@font-face {'
            string += f'\nfont-family: "{font[0]}";\n'
            string += f'src: url("{font[1]}");\n'
            string += '}\n'
        string += "</style>"
        return string

    def font(self, fontName:str=None, size:int=None):
        self._font = ""
        
        
        if fontName:
            self._font += f"font-family: '{fontName}'; "
        if size:
            if not isinstance(size, int):
                raise ValueError("Size must be an integer.")
            elif size < 0:
                raise ValueError("Size must be greater than 0. A size of 0 makes no sense.")
            else:
                self._font += f'font-size: {size}px;'
        self._hasStyle = True


    def setOrigin(self,originX:any=0, originY:any=0) -> None:
        if isinstance(originX, int):
            originX = f"{originX}px"
        if isinstance(originY, int):
            originY = f"{originY}px"
        self._origin = f"transform: translate({originX}, {originY});"
        self._hasStyle = True

    def border(self,width:any=0, style:str="solid", color:str="black", affected_sides:str="all"):
        if width < 0:
            raise ValueError("Border width cannot be negative.")
        if style not in ["solid", "dotted", "dashed", "double", "groove", "ridge", "inset", "outset", "none", "hidden"]:
            raise ValueError(f'"{style}" could not be recognized as border style.\n-> "solid", "dotted", "dashed", "double", "groove", "ridge", "inset", "outset", "none", "hidden')
        
        if affected_sides not in ["all", "top", "right", "bottom", "left"]:
            raise ValueError(f'"{affected_sides}" could not be recognized as affected sides.\n-> "all", "top", "right", "bottom", "left')
        
        
        if isinstance(width, float) or isinstance(width, int):
            width = f"{str(width)}px"
        if not isinstance(color, str):
            raise ValueError("Color must be a string, rgb(r,g,b) or rgba(r,g,b,a).\n-> rgba(r,g,b,a), rgb(r,g,b), '#hexcode', 'colorname'")
        
        if affected_sides == "all":
            self._border = f'border: {width} {style} {color};'
        else:
            self._border += f'border-{affected_sides}: {width} {style} {color};'
        self._hasStyle = True

    def roundCorners(self, topright:int=0, topleft:int=0, bottomright:int=0, bottomleft:int=0, all:int=None ) -> None:
        """setting "all" overrides all the other parameters."""
        if topright < 0 or topleft < 0 or bottomright < 0 or bottomleft < 0:
            raise ValueError("Radius cannot be negative.")
        self._borderRD = ''
        if all is None:
            self._borderRD += 'border-radius: '#
            if isinstance(topleft, int):
                self._borderRD += f'{topleft}px '

            if isinstance(topright, int):
                self._borderRD += f'{topright}px '
            
            if isinstance(bottomright, int):
                self._borderRD += f'{bottomright}px '
            if isinstance(bottomleft, int):
                self._borderRD += f'{bottomleft}px '
            self._borderRD += ';'
        
        if isinstance(all, int):
            self._borderRD += f'border-radius: {all}px; '
        self._borderRD += ''
        self._hasStyle = True

    def margin(self,top:int=0, right:int=0, bottom:int=0, left:int=0) -> None:
        if top < 0 or right < 0 or bottom < 0 or left < 0:
            raise ValueError("Margin cannot be negative.")
        self._margin = f'margin: {top}px {right}px {bottom}px {left}px;'
        self._hasStyle = True
    
    def padding(self,top:int=0, right:int=0, bottom:int=0, left:int=0) -> None:
        if top < 0 or right < 0 or bottom < 0 or left < 0:
            raise ValueError("Padding cannot be negative.")
        self._padding = f'padding: {top}px {right}px {bottom}px {left}px;'
        self._hasStyle = True

    def overflow(self, X="auto", Y="auto"):
        if X not in ["auto", "hidden", "visible", "scroll"]:
            raise ValueError(f'"{X}" could not be recognized as overflow type.\n-> "auto", "hidden", "visible", "scroll"')
        if Y not in ["auto", "hidden", "visible", "scroll"]:
            raise ValueError(f'"{Y}" could not be recognized as overflow type.\n-> "auto", "hidden", "visible", "scroll"')
        self._overflow = f'overflow-x: {X}; overflow-y: {Y};'
        self._hasStyle = True


    def colorize(self, color:str=None, background:str=None):
        colorString = ""
        if color and isinstance(color, str):
            colorString += f'color: {color}; '
        if background and isinstance(background, str):
            colorString += f'background-color: {background}; '
        self._color = colorString
        self._hasStyle = True

    def draw(self,moveX:any=None, moveY:any=None, flipX:bool=False, flipY:bool=False,width:any=None, height:any=None, position:str="absolute")->None:
        if isinstance(moveX, int):
            moveX = f"{moveX}px"
        if isinstance(moveY, int):
            moveY = f"{moveY}px"
        if isinstance(width, int):
            width = f"{width}px"
        if isinstance(height, int):
            height = f"{height}px"
        if position not in ["absolute", "relative", "fixed", "sticky"]:
            raise ValueError(f'"{position}" could not be recognized as position type.\n-> "absolute", "relative", "fixed", "sticky"')
        self._position = f"position: {position};"
        if flipX and moveX:
            self._position += f"right: {moveX};"
        elif moveX:
            self._position += f"left: {moveX};"
        if flipY and moveY:
            self._position += f"bottom: {moveY};"
        elif moveY:
            self._position += f"top: {moveY};"


        if height:
            self._height = f"height: {height};"
        if width:
            self._width = f"width: {width};"
        self._hasStyle = True

    def alignment(self, align:str="center", justify:str="center", alignType:str="items", justifyType:str="content") -> None:
        if align not in ["center", "left", "right"]:
            raise ValueError(f'"{align}" could not be recognized as alignment type.\n-> "center", "left", "right"')
        if align and alignType not in ["items", "content"]:
            raise ValueError(f'"{alignType}" could not be recognized as alignment type.\n-> "items", "content"')
        if justify not in ["center", "start", "end", "space-between", "space-around", "space-evenly", "stretch", "flex-start", "flex-end", "baseline"]:
            raise ValueError(f'"{justify}" could not be recognized as justification type.\n-> "center", "left", "right"')
        if justify and justifyType not in ["items", "content"]:
            raise ValueError(f'"{justifyType}" could not be recognized as justification type.\n-> "items", "content"')
        
        if align:
            self._alignment = f'align-{alignType}: {align};'
            self._display = 'flex'
        if justify:
            self._justify = f'justify-{justifyType}: {justify};'
            self._display = 'flex'
        self._hasStyle = True

    def _asm(self) -> str:
        """Not intended for direct use, will be automaticly called during the compilation of the document.\n
        However it can be called for debugging purposes if the compiler generates unexpected content."""
        string = f'style="'
        if self._origin:
            string += f'{self._origin} '
        if self._position:
            string += f'{self._position} '
        if self._width:
            string += f'{self._width} '
        if self._height:
            string += f'{self._height} '
        if self._color:
            string += f'{self._color} '
        if self._margin:
            string += f'{self._margin} '
        if self._padding:
            string += f'{self._padding} '
        if self._border:
            string += f'{self._border} '
        if self._borderRD:
            string += f'{self._borderRD} '
        if self._alignment:
            string += f'{self._alignment} '
        if self._overflow:
            string += f'{self._overflow} '
        if self._justify:
            string += f'{self._justify} '
        if self._font:
            string += f'{self._font} '
        if self._backgroundImage:
            string += f'{self._backgroundImage} '
        if self._display:
            string += f'display: {self._display}; '
        string += '"'
        if string == 'style=""':
            return None
        return string