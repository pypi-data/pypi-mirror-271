"""Hyped API Router."""
from datasets import Features
from datasets.iterable_dataset import _batch_to_examples, _examples_to_batch
from fastapi import Response
from fastapi.routing import APIRoute, APIRouter
from hyped.data.io.datasets.typed_json import pydantic_model_from_features
from hyped.data.pipe import DataPipe


class HypedAPIRouter(APIRouter):
    """Hyped API Router serving a data pipe."""

    def __init__(self, pipe: DataPipe, features: Features, **kwargs) -> None:
        """Initialize the API Router.

        Arguments:
            pipe (DataPipe):
                data pipeline to serve
            features (Features):
                input features to be processed by the data pipe
            **kwargs (dict[str, Any]):
                keyword arguments passed to the base constructor. For more
                information check the FastAPIRouter documentation.
        """
        self.pipe = pipe
        # prepare data pipe
        out_features = self.pipe.prepare(features)
        # build pydantic request and response models from
        # the input and output features
        in_model = pydantic_model_from_features(features)
        out_model = pydantic_model_from_features(out_features)

        async def batch_apply_pipe(
            examples: list[in_model],
        ) -> list[out_model]:
            """Apply the data pipeline to a batch of examples."""
            index = list(range(len(examples)))
            batch = _examples_to_batch([e.model_dump() for e in examples])
            batch = self.pipe.batch_process(batch, index=index, rank=0)
            return list(_batch_to_examples(batch))

        async def apply_pipe(example: in_model) -> out_model:
            """Apply the data pipeline to an example."""
            return (await batch_apply_pipe([example]))[0]

        super(HypedAPIRouter, self).__init__(
            routes=[
                APIRoute("/ready", self.ready, methods=["GET"]),
                APIRoute("/apply", apply_pipe, methods=["POST"]),
                APIRoute("/batch", batch_apply_pipe, methods=["POST"]),
            ]
            + list(kwargs.pop("routes", [])),
            **kwargs,
        )

    async def ready(self) -> Response:
        """Readiness check."""
        # check if pipeline is prepared
        if not self.pipe.is_prepared:
            return Response(content="pipe not prepared", status_code=503)
        # ready for usage
        return Response(content="ok", status_code=200)
