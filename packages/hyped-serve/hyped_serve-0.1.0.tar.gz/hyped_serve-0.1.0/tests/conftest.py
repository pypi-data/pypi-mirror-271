from typing import Any

import pytest
from datasets import Features, Value
from datasets.iterable_dataset import _batch_to_examples, _examples_to_batch
from fastapi import FastAPI
from fastapi.testclient import TestClient
from hyped.data.pipe import DataPipe
from hyped.data.processors.features.format import (
    FormatFeatures,
    FormatFeaturesConfig,
)

from hyped.serve.api import HypedAPI


@pytest.fixture
def data_pipe() -> DataPipe:
    return DataPipe(
        [FormatFeatures(FormatFeaturesConfig(output_format={"y": "x"}))]
    )


@pytest.fixture
def features() -> Features:
    return Features({"x": Value("int32")})


@pytest.fixture
def api(data_pipe: DataPipe, features: Features) -> HypedAPI:
    return HypedAPI().serve_pipe(data_pipe, features)


@pytest.fixture
def client(api: FastAPI) -> TestClient:
    return TestClient(api)


@pytest.fixture(params=range(10))
def example(request) -> dict[str, Any]:
    return {"x": request.param}


@pytest.fixture
def out_example(
    data_pipe: DataPipe, features: Features, example: dict[str, Any]
) -> dict[str, Any]:
    data_pipe.prepare(features)
    batch = _examples_to_batch([example])
    batch = data_pipe.batch_process(batch, index=[0])
    return next(_batch_to_examples(batch))
