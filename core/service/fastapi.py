# ----------------------------------------------------------------------
# FastAPIService
# ----------------------------------------------------------------------
# Copyright (C) 2007-2021 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
import os
from typing import Optional, Tuple, Dict

# Third-party modules
import uvicorn
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware
from starlette.responses import Response, JSONResponse
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder

# NOC modules
from noc.core.version import version
from noc.core.log import PrefixLoggerAdapter
from noc.core.debug import error_report
from .base import BaseService
from .paths.loader import loader, ServicePathLoader
from .middleware.logging import LoggingMiddleware
from .middleware.span import SpanMiddleware


class FastAPIService(BaseService):
    BASE_OPENAPI_TAGS_DOCS = {
        "internal": "NOC internal API, including healthchecks, monitoring and tooling",
        "JSON-RPC API": "Implemented by JSON-RPC specification 1.0",
    }
    # Additional OpenAPI tags docs, tag -> description
    OPENAPI_TAGS_DOCS: Dict[str, str] = {}

    def __init__(self):
        super().__init__()
        self.app = None

    async def error_handler(self, request: "Request", exc) -> Response:
        """
        Error handler for ServerErrorMiddleware
        :return:
        """
        error_report(logger=self.logger)
        return JSONResponse(
            status_code=500,
            content={
                "error": "internal_error",
                "error_description": f"Internal Server Error: {exc}",
                "error_uri": str(request.url),
            },
        )

    async def request_validation_error_handler(self, request: "Request", exc) -> Response:
        """
        Handle request validation and customize response
        :param request:
        :param exc:
        :return:
        """
        return JSONResponse(
            status_code=400,
            content={
                "error": "invalid_request",
                "error_description": jsonable_encoder(exc.errors()),
                "error_uri": str(request.url),
            },
        )

    async def init_api(self):
        # Build tags docs
        openapi_tags = []
        for tag in self.BASE_OPENAPI_TAGS_DOCS:
            openapi_tags += [{"name": tag, "description": self.BASE_OPENAPI_TAGS_DOCS[tag]}]
        if self.OPENAPI_TAGS_DOCS:
            for tag in self.OPENAPI_TAGS_DOCS:
                openapi_tags += [{"name": tag, "description": self.OPENAPI_TAGS_DOCS[tag]}]
        # Build FastAPI app
        self.app = FastAPI(
            title="NOC '%s' Service API" % (self.name or "unknown"),
            version=version.version,
            openapi_url="/api/%s/openapi.json" % self.name,
            docs_url="/api/%s/docs" % self.name,
            redoc_url="/api/%s/redoc" % self.name,
            openapi_tags=openapi_tags,
            exception_handlers={
                Exception: self.error_handler,
                RequestValidationError: self.request_validation_error_handler,
            },
        )
        self.app.add_middleware(ProxyHeadersMiddleware, trusted_hosts="*")
        self.app.add_middleware(LoggingMiddleware, logger=PrefixLoggerAdapter(self.logger, "api"))
        self.app.add_middleware(SpanMiddleware, service_name=self.name)
        self.server: Optional[uvicorn.Server] = None
        # Initialize routers
        for path in loader.iter_classes():
            self.app.include_router(loader.get_class(path))
        service_paths = ("services", self.name, "paths")
        if os.path.exists(os.path.join(*service_paths)):
            extra_loader = ServicePathLoader()
            extra_loader.base_path = service_paths
            for path in extra_loader.iter_classes():
                kls = extra_loader.get_class(path)
                if kls:
                    self.app.include_router(kls)
        # Get address and port to bind
        addr, port = self.get_service_address()
        # Initialize uvicorn server
        # Reproduce Service.run/.serve method
        uvi_config = uvicorn.Config(
            self.app, host=addr, port=port, lifespan="on", access_log=False, loop="none"
        )
        self.server = uvicorn.Server(config=uvi_config)
        uvi_config.setup_event_loop()
        uvi_config.load()
        self.server.lifespan = uvi_config.lifespan_class(uvi_config)
        await self.server.startup()
        # Get effective listen socket port
        self.address, self.port = self.get_effective_address()
        self.logger.info("Running HTTP APIs at http://%s:%s/", self.address, self.port)
        self.logger.info(
            "Running HTTP APIs Docs at http://%s:%s/api/%s/docs", self.address, self.port, self.name
        )
        self.loop.create_task(self.server.main_loop())

    async def shutdown_api(self):
        await self.server.shutdown()

    def get_effective_address(self) -> Tuple[str, int]:
        for srv in self.server.servers:
            for sock in srv.sockets:
                return sock.getsockname()
