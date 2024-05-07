"""main gust module"""

import asyncio
import functools
import inspect
import logging
from typing import Any, List

from tornado.web import Application

from . import context
from .configs import WebConfig
from .web import web
from .web_handler import WebHandler
from .websocket import Websocket

log = logging.getLogger(__name__)


class Gust(Application):
    """A minimal sub-class of tornado.web.Application"""

    def __init__(self, routes: List = None, port: int = 8080, **kwargs):
        self.port = port
        # routes = routes if routes else []
        # for path, cfg in web.route_map.items():
        #     handler = (
        #         WebHandler if isinstance(cfg, (WebConfig,)) else Websocket
        #     )
        #     routes.append((rf'{path}', handler, {'method_settings': cfg}))
        # routes.sort(reverse=True)
        # web.broadcaster = self
        super().__init__(routes, **kwargs)
        web.install(self)

    async def perform(self, user, func: callable, *args, **kwargs) -> Any:
        """await a function or call in a thread_pool, better yet call redis"""
        if inspect.iscoroutinefunction(func):
            log.debug('aperform: %s', func)
            with context.gust(self, user):
                result = await func(*args, **kwargs)
        else:
            log.debug('perform: %s', func)
            partial = functools.partial(
                self.call_in_context, user, func, args, kwargs
            )
            result = await asyncio.to_thread(partial)
        return result

    def call_in_context(self, user, func, args, kwargs):
        """set the context and call function"""
        with context.gust(self, user):
            return func(*args, **kwargs)

    @classmethod
    def broadcast(cls, path, message, client_ids):
        """pass through, maybe point for redis gust"""
        Websocket.broadcast(path, message, client_ids)

    async def _run_(self):  # pragma: no cover
        """listen on self.port and run io_loop"""
        if self.port:
            self.listen(self.port)
            log.info('listening on port: %s', self.port)
        else:
            log.warning("No 'port' in settings")

        if self.settings.get('debug') is True:
            log.info('running in debug mode')

        try:
            await asyncio.Event().wait()
        except (KeyboardInterrupt, SystemExit):
            # graceful shutdown
            pass

    def run(self):  # pragma: no cover
        asyncio.run(self._run_())
