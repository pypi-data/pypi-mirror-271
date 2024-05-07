"""
Tests for the serializer module.
"""
# pylint: disable=redefined-outer-name
# pylint: disable=line-too-long
# pylint: disable=protected-access
# pylint: disable=missing-function-docstring

import tempfile
import zipfile
import pandas as pd
import pytest
from cell_typist.core.serializer import ResultSerializer
from cell_typist.core.datatypes import Result


@pytest.fixture
def result_data():
    df = pd.DataFrame(
        {
            "group1": ["A", "B", "A", "B"],
            "group2": ["X", "X", "Y", "Y"],
            "measurement1": [1, 2, 3, 4],
            "measurement2": [5, 6, 7, 8],
        }
    )
    return Result(
        name="Test Result",
        experiment="Test Experiment",
        groupby=["group1", "group2"],
        measurements=["measurement1", "measurement2"],
        data=df,
    )


def test_result_serializer_load(result_data):
    with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as tmp:
        ResultSerializer().save(result_data, tmp.name)
        loaded_result = ResultSerializer.load(tmp.name)
        pd.testing.assert_frame_equal(result_data.data, loaded_result.data)


def test_result_serializer_load_non_zip_file():
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tmp:
        with pytest.raises(ValueError, match="Path must be a zip file"):
            ResultSerializer.load(tmp.name)


def test_result_serializer_load_missing_files():
    with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as tmp:
        with zipfile.ZipFile(tmp.name, "w") as zip_file:
            zip_file.writestr("dummy.txt", "dummy content")
        with pytest.raises(
            ValueError,
            match="Zip file must contain 'result.json' and 'result.csv' files",
        ):
            ResultSerializer.load(tmp.name)
