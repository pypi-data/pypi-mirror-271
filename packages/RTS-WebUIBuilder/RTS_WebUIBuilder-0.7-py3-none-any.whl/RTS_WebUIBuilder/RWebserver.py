from aiohttp import web
import os
import asyncio, threading, time
from threading import Thread



class RWebserver:
    def __init__(self, host:str='localhost', port:int=8080) -> None:
        from .cache import rtswuib_cache
        if not rtswuib_cache.MAIN_WEBSERVER is None:
            raise ValueError('It is best practice to only have one webserver running at a time. Please stop the current webserver before starting a new one.')
        self.host:str = host
        self.port:int = port
        self.bannedRoutes:set = set()
        self.loop:asyncio = asyncio.get_event_loop()
        self.app:web.Application = web.Application()
        self.runner:web.AppRunner = web.AppRunner(self.app)
        self.site = None
        self._srcFolders:set = set()

    async def __start(self) -> None:
        from .cache import rtswuib_cache
        if not rtswuib_cache.MAIN_WEBSERVER is None:
            raise ValueError('It is best practice to only have one webserver running at a time. Please stop the current webserver before starting a new one.')
        rtswuib_cache.MAIN_WEBSERVER = self
       
        
        await self.runner.setup()
        self.site = web.TCPSite(self.runner, self.host, self.port)
        await self.site.start()
        print(f'Server started at http://{self.host}:{self.port}')
        

    async def stop(self):
        from .cache import rtswuib_cache
        await self.site.stop()
        await self.runner.cleanup()
        rtswuib_cache.MAIN_WEBSERVER = None
        print('Server stopped')

    def disableSourceRoute(self, route:str):
        self._srcFolder.remove(route)
        
    def enableSourceRoute(self, srcFolder:str) -> None:
        print(f"Enabling source route: {srcFolder}")
        self._srcFolders.add(srcFolder)

    async def serve_file(self, request) -> web.FileResponse:
        print("Serving file")
        path = request.match_info.get('path', "")
        sanitized_path = os.path.normpath(path.lstrip('/'))
        for srcFolder in self._srcFolders:
            safe_path = os.path.join(srcFolder, sanitized_path)
            if os.path.commonprefix((os.path.realpath(safe_path), os.path.realpath(srcFolder))) != os.path.realpath(srcFolder):
                continue
            if os.path.isfile(safe_path):
                return web.FileResponse(safe_path)
        raise web.HTTPNotFound()

    def init_routes(self):
        self.app.router.add_route('GET', '/src/{path:.*}', self.serve_file)

    def __proceed(self,launch, *args, **kwargs):
        time.sleep(2)
        if launch:
            launch(*args, **kwargs)


    def run(self, proceedWithFunction, *args, **kwargs) -> None:
        Thread(target=self.__proceed, args=(proceedWithFunction, *args), kwargs=kwargs).start()

        self.init_routes()
        self.automountGet()
        
        self.loop.run_until_complete(self.__start())
        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            self.loop.run_until_complete(self.stop())

    def bannDynamicroutesFromAutomount(self, routes:any) -> None:
        if isinstance(routes, list):
            for route in routes:
                self.bannedRoutes.add(route)
        elif isinstance(routes, str):
            self.bannedRoutes.add(routes)
        else:
            raise ValueError("routes must be a list or a string.")

    def add_route(self,*, method:str='GET', path:str, handler:any) -> None:
        self.bannedRoutes.add(path)
        if method.upper() == 'GET':
            self.app.router.add_get(path, handler)
        elif method.upper() == 'POST':
            self.app.router.add_post(path, handler)
        elif method.upper() == 'PUT':
            self.app.router.add_put(path, handler)
        elif method.upper() == 'DELETE':
            self.app.router.add_delete(path, handler)
        else:
            raise ValueError(f"Unsupported method: {method}")


    def automountGet(self):
        from html import escape
        from .cache import rtswuib_cache
        async def handle(request):
            path = escape(request.path)
            htmlasm = None
            # Suchen Sie die Seite in ASSAMBLED_PAGES
            html = next((html for route, html in rtswuib_cache.ASSAMBLED_PAGES if route == path), None)

            #Raw RDocument
            if path in rtswuib_cache.RAW_PAGES and path in self.bannedRoutes:

                raise web.HTTPNotFound(text='rtswuib_cache.RAW_PAGES.get("/error/bannedDynamic").compileDocument()')
            if path in rtswuib_cache.RAW_PAGES and path not in self.bannedRoutes:
                htmlasm = rtswuib_cache.RAW_PAGES.get(path)
                
            if html is not None:
                return web.Response(text=str(html), content_type='text/html')
            elif htmlasm is not None:
                return web.Response(text=htmlasm.compileDocument(), content_type='text/html')
            else:
                raise web.HTTPNotFound()
            


        self.app.router.add_get('/{path:.*}', handler=handle)

    def add_websocket_route(self, path: str, handler: any) -> None:
        from .cache import rtswuib_cache as tmp
        async def websocket_handler(request):
            ws = web.WebSocketResponse()
            await ws.prepare(request)

            async for msg in ws:
                if msg.type == web.WSMsgType.TEXT:
                    if msg.data == 'close':
                        await ws.close()
                    else:
                        processed_data = await handler(msg.data)
                        await ws.send_str(processed_data)
                elif msg.type == web.WSMsgType.ERROR:
                    print('ws connection closed with exception %s' % ws.exception())

            print('websocket connection closed')
            tmp.WEBSOCKETS.remove((path, websocket_handler))

            return ws

        self.app.router.add_route('GET', path, websocket_handler)
        tmp.WEBSOCKETS.append((path, websocket_handler))