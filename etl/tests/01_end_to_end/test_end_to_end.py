import os
import shutil
from pathlib import Path

import pandas as pd
import papermill
import pytest


@pytest.fixture
def chdir(tmp_path):
    lwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        yield
    finally:
        os.chdir(lwd)


def test_end_to_end(chdir, tmp_path):
    # given
    inputs_dir = tmp_path / "inputs"
    inputs_dir.mkdir()
    outputs_dir = tmp_path / "outputs"
    outputs_dir.mkdir()
    inputs = [
        "coding_challenge_inventory.csv",
        "coding_challenge_meta.csv",
        "coding_challenge_prices.csv",
    ]
    for input_file in inputs:
        shutil.copy(Path(__file__).parent / input_file, inputs_dir / input_file)

    # when
    papermill.execute_notebook(
        Path(__file__).parents[2] / "InventoryETL.ipynb",
        outputs_dir / "output.ipynb",
    )

    # then
    generated_products = pd.read_csv(outputs_dir / "products.csv")
    expected_products = pd.read_csv(Path(__file__).parent / "expected_products.csv")
    assert generated_products.compare(expected_products).empty

    generated_alternates = pd.read_csv(outputs_dir / "product_alternates.csv")
    expected_alternates = pd.read_csv(
        Path(__file__).parent / "expected_product_alternates.csv"
    )
    assert generated_alternates.compare(expected_alternates).empty
