import pytest
from products_api.models import Base, Product, ProductAlternate
from products_api.repository import ProductsRepository
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(engine)

    with Session.begin() as session:
        yield session


def test_get_product_by_main_upc(session):
    # given
    upc = "0" * 14
    session.add(Product(upc=upc))

    # when
    product = ProductsRepository(session).get_by_upc_of_product_or_alternate(upc)

    # then
    assert product is not None
    assert product.upc == upc


def test_get_product_by_alternate_upc(session):
    # given
    main_upc = "1" * 14
    upc = "0" * 14
    session.add(Product(upc=main_upc, product_alternates=[ProductAlternate(upc=upc)]))

    # when
    product = ProductsRepository(session).get_by_upc_of_product_or_alternate(upc)

    # then
    assert product is not None
    assert product.upc == main_upc
    assert len(product.product_alternates) == 1
    assert product.product_alternates[0].upc == upc


def test_return_none_if_product_or_alternate_does_not_exist(session):
    # when
    product = ProductsRepository(session).get_by_upc_of_product_or_alternate("0" * 14)

    # then
    assert product is None
