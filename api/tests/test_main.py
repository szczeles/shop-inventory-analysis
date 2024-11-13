from datetime import datetime, timezone
from decimal import Decimal
from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient
from products_api.main import app, get_products_repository
from products_api.models import Product, ProductAlternate


@pytest.fixture
def products_repository():
    return Mock()


@pytest.fixture
def test_client(products_repository):
    app.dependency_overrides[get_products_repository] = lambda: products_repository
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_404_on_getting_non_existing_product(products_repository, test_client):
    # given
    products_repository.get_by_upc_of_product_or_alternate.return_value = None

    # when
    response = test_client.get("/v1/product/" + "0" * 14)

    # then
    assert response.status_code == 404
    assert response.json() == {"message": "Product not found"}


def test_disallow_invalid_upcs(test_client):
    # when
    response = test_client.get("/v1/product/1234")

    # then
    assert response.status_code == 422


def test_return_product_in_expected_format(products_repository, test_client):
    # given
    product = Product(
        name="Milk",
        upc="1" * 14,
        item_number=100,
        price=Decimal("2.99"),
        supplier="Mariusz's Farm",
        inventory_level=42,
        inventory_updated_at=datetime(2024, 11, 13, tzinfo=timezone.utc),
        product_alternates=[
            ProductAlternate(
                upc="2" * 14,
                alternate_type="case",
                case_pack=12,
            )
        ],
    )
    products_repository.get_by_upc_of_product_or_alternate.return_value = product

    # when
    response = test_client.get("/v1/product/" + "1" * 14)

    # then
    assert response.status_code == 200
    assert response.json() == {
        "name": "Milk",
        "upc": "11111111111111",
        "item_number": 100,
        "price": "2.99",
        "supplier": "Mariusz's Farm",
        "inventory_level": 42,
        "inventory_updated_at": "2024-11-13T00:00:00Z",
        "variants": [{"upc": "22222222222222", "type": "case", "case_pack": 12.0}],
    }
