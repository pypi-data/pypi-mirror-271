def rgba(r:int,g:int,b:int,a:float)->str:
    """rgba(r:int,g:int,b:int,a:float) -> str
    r: int -> red value (0-255)
    g: int -> green value (0-255)
    b: int -> blue value (0-255)
    a: float -> alpha value (0.0-1.0)\n
    Returns a string that can be used in as a color value."""
    for value, name, limit in [(r, "Red", 255), (g, "Green", 255), (b, "Blue", 255), (a, "Alpha", 1)]:
        if not 0 <= value <= limit:
            raise ValueError(f"{name} value must be between 0 and {limit if name != 'Alpha' else 1.0}.")
    return f"rgba({r},{g},{b},{a})"



def rgb(r:int,g:int,b:int)->str:	
    """rgb(r:int,g:int,b:int) -> str
    r: int -> red value (0-255)
    g: int -> green value (0-255)
    b: int -> blue value (0-255)\n
    Returns a string that can be used as a color value."""
    for value, name, limit in [(r, "Red", 255), (g, "Green", 255), (b, "Blue", 255)]:
        if not 0 <= value <= limit:
            raise ValueError(f"{name} value must be between 0 and {limit}.")
    return f"rgb({r},{g},{b})"