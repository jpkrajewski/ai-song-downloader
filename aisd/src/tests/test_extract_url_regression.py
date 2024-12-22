import json
from pathlib import Path

import pytest

from aisd.src.download import extract_url_from_payload

REGRESSION_DIR = Path(__file__).resolve().parent / "regression"


@pytest.mark.parametrize("file", list(REGRESSION_DIR.rglob("*.json")))
def test_transform_regression(file: Path):
    with file.open("r") as f:
        data = json.load(f)
    result = extract_url_from_payload(data)
    assert result is not None
