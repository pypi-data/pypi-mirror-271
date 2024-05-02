# Hyped Serve

Hyped Serve is a lightweight add-on for [hyped](https://github.com/open-hyped/hyped) designed to streamline the serving process of a hyped data pipeline.

## Installation

You can install the add-on directly from PyPI using pip:

```bash
pip install hyped-serve
```

## Getting Started

Hyped Serve leverages the power of [FastAPI](https://fastapi.tiangolo.com) to create a robust serving environment.

To get started, simply define your data pipeline and its expected input features in a Python script, and then serve it using `hyped.serve`.

Here's a basic example:

```python
# app.py
from hyped.serve import HypedAPI
from hyped.data.pipe import DataPipe
from datasets import Features

# Define your data pipeline and its expected input features
pipe = DataPipe([...])
features = Features({...})

# Create the app to be served
app = HypedAPI().serve_pipe(pipe, features, prefix="/")
```

Once you've defined your app, you can serve it using uvicorn:

```bash
uvicorn app:app --host 0.0.0.0 --port 80
```
This will start the server, allowing you to interact with your data pipeline via HTTP requests.

## Endpoints

The Hyped Serve API provides the following endpoints for interacting with your data pipeline:

| Endpoint   | Method | Description                                                                                            |
|------------|--------|--------------------------------------------------------------------------------------------------------|
| /health    | GET    | Simple health check always returns "ok" and code 200.                                                  |
| \<prefix\>/ready | GET    | Readiness check to determine if the server is ready to receive requests.                               |
| \<prefix\>/apply | POST   | Process a single example using the data pipeline. Expects a single example in JSON format matching the specified features. |
| \<prefix\>/batch | POST   | Process a batch of examples using the data pipeline. Expects a list of examples.                   |

Additionally, a Swagger UI API documentation is available at /docs.

## Serving multiple Data Pipes

The serving environment also supports serving multiple data pipes simultaneously. You can configure this by providing multiple data pipes and their respective features.

```python
# app.py

app = (
    HypedAPI()
    .serve_pipe(pipe_one, features_one, prefix="/one")
    .serve_pipe(pipe_two, features_two, prefix="/two")
)
```

This example demonstrates serving two different data pipes (pipe_one and pipe_two) with their corresponding features, each accessible via different prefixes (/one and /two).

## Running Tests

Hyped Serve includes a suite of tests to ensure its functionality. You can run these tests using pytest:

```bash
pytest tests
```

Ensure that you have pytest installed in your environment. You can install it via pip:

```bash
pip install pytest
```

Running the tests will execute various test cases to validate the behavior of Hyped Serve.

## License

Hyped Serve is licensed under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0). See the [`LICENSE`](/LICENSE) file for details.
