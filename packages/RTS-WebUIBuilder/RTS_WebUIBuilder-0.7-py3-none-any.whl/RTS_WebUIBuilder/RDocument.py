from .RBody import RBody
from .RHead import RHeader
from .RWebserver import RWebserver
from .privatizehead import private
from .exeptional import *
class RDocument:
    def __init__(self,*,documentRoute:str, static:bool=True) -> None:
        
        if documentRoute.startswith("/src"):
            raise ErrReservedPath("/src","RWebserver().enableSourceRoute()")
        if documentRoute.startswith("/docs"):
            pass
            #print("Please consider using /docs only if you are creating a module and want to add local documentation pages for other developers to it.\n For any other documentation purposes, please use a custom route instead.(like /documentation or /doc)")
        
        self._documentRoute = documentRoute
        self._static = static
        """Only set during the initialization of the document"""

        if not self._static:
            from .cache import rtswuib_cache as tmp
            tmp.RAW_PAGES[self._documentRoute] = self
        
        self.body = RBody()
        self.head = RHeader()
        self._fonts = []



        
    def importFonts(self,*,font:str, fontURL:str) -> None:
        self._fonts.append((font,fontURL))
     
   
    def defaultFont(self, font:str) -> None:
        self.body.style.font(font)

    def compileDocument(self) -> str:
        """This Method is needed to be called in a custom route handler (if RDocument(static=True)) to compile the document to html."""
        
        if not self._static:
            self.body._fontimport = self._fonts
            if isinstance(self.body, RBody) and isinstance(self.head, RHeader):
                document = f"<!DOCTYPE html>\n<html>\n{self.head._asm()}{self.body._asm()}</html>"
                return document
            else: 
                raise ErrHeadOrBodyOverwritten()
        else:
            raise ErrStaticCompile()
   
    def asm(self) -> None:
        self.body._fontimport = self._fonts
        """Only call this method if the document is set to be static (RDocument(static=True)) and at the very end of your page file."""
        
        if self._static:
            from .cache import rtswuib_cache
            html = RHTML(self)
            if True:
                for i, (existing_route, _) in enumerate(rtswuib_cache.ASSAMBLED_PAGES):
                    if existing_route == self._documentRoute:
                        rtswuib_cache.ASSAMBLED_PAGES[i] = (self._documentRoute, html)
                        break
                else:
                    if self._documentRoute not in rtswuib_cache.RAW_PAGES:
                        rtswuib_cache.ASSAMBLED_PAGES.append((self._documentRoute, html))
          
        else:
            raise ErrDynamicASM()
@private   
class RHTML:
    def __init__(self,document):
        """This class is not intended for direct use. use RDocument.asm() instead."""
        if isinstance(document.body, RBody) and isinstance(document.head, RHeader):
            self.get = f"<!DOCTYPE html>\n<html>\n{document.head._asm()}{document.body._asm()}</html>"
        else:
            raise ErrHeadOrBodyOverwritten()
    def __str__(self):
        return self.get

    