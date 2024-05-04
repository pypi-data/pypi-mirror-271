from dataclasses import dataclass, field

from typing import Union, Tuple
@dataclass 
class RTSCache():
    from RTS_WebUIBuilder.RDocument import RDocument, RHTML
    ASSAMBLED_PAGES:list[list[Tuple[str,RHTML]]] = field(default_factory=list)
    RAW_PAGES:dict[str:RDocument] = field(default_factory=dict)
    MAIN_WEBSERVER = None

rtswuib_cache = RTSCache()