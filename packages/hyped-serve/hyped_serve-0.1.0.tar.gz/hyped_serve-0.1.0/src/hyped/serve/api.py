"""Hyped API."""
from __future__ import annotations

from datasets import Features
from fastapi import FastAPI, Response
from fastapi.routing import APIRoute
from hyped.data.pipe import DataPipe

from hyped.serve.router import HypedAPIRouter


class HypedAPI(FastAPI):
    """Hyped API serving data pipes."""

    def __init__(self, **kwargs) -> None:
        """Constuctor.

        For more information on arguments, please refer to the fastapi
        documentation.
        """
        super(HypedAPI, self).__init__(
            routes=[
                APIRoute("/health", self.health, methods=["GET"]),
            ]
            + list(kwargs.pop("routes", [])),
            **kwargs,
        )

    def serve_pipe(
        self, pipe: DataPipe, features: Features, **kwargs
    ) -> HypedAPI:
        """Serve a data pipeline.

        Shorthand for creating a `HypedAPIRouter` instance from the
        given data pipe and features and including the router in the
        api.

        Arguments:
            pipe (DataPipe):
                data pipeline to serve
            features (Features):
                input features to be processed by the data pipe
            **kwargs (dict[str, Any]):
                keyword arguments passed to the base constructor. For more
                information check the FastAPIRouter documentation.

        Returns:
            api (HypedAPI):
                self
        """
        # create and include router
        router = HypedAPIRouter(pipe, features, **kwargs)
        self.include_router(router)
        # return self
        return self

    async def health(self) -> Response:
        """Health check."""
        return Response(content="ok", status_code=200)
