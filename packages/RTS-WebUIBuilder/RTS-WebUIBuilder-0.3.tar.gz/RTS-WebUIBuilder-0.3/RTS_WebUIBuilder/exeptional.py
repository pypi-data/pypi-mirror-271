class ErrDynamicASM(Exception):
    def __init__(self):
        self.message = "Do not use asm() on a dynamic document. Use RDocument().compileDocument() instead."

class ErrStaticCompile(Exception):
    def __init__(self):
        self.message = "Do not use compileDocument() on a static document. Use RDocument().asm() instead."

class ErrHeadOrBodyOverwritten(Exception):
    def __init__(self):
        self.message = "Document could not be compiled. Please check if the you didn't overwote RDocument().body or RDocument().head with a different object.\nNote that .body and .head are already preset as their respective classes and can be accessed directly."

class ErrReservedPath(Exception):
    def __init__(self, message, functouse):
        self.message = f"Can not use {message} as a route, due to it being a reserved route. Use {functouse} to add a to this route."