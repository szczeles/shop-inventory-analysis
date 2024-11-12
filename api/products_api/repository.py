import os

from sqlalchemy import create_engine, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session, joinedload, sessionmaker
from sqlalchemy.sql.elements import BinaryExpression

from products_api.models import Product, ProductAlternate


class ProductsRepository:
    def __init__(self, session: Session):
        self._session: Session = session

    def get_by_upc_of_product_or_alternate(self, upc: str) -> Product | None:
        try:
            return self.get_product_by_upc(upc)
        except NoResultFound:
            try:
                return self.get_product_by_alternate_upc(upc)
            except NoResultFound:
                return None

    def get_product_by_alternate_upc(self, upc: str) -> Product:
        alternate = self.get_alternate_by_upc(upc)
        return self.get_product_by_id(alternate.product_id)

    def get_product_by_upc(self, upc: str) -> Product:
        return self._get_product_by_condition(Product.upc == upc)

    def get_product_by_id(self, id: int) -> Product:
        return self._get_product_by_condition(Product.product_id == id)

    def _get_product_by_condition(self, condition: BinaryExpression) -> Product:
        query = (
            select(Product)
            .filter(condition)
            .options(joinedload(Product.product_alternates))
        )
        return self._session.scalars(query).unique().one()

    def get_alternate_by_upc(self, upc: str) -> ProductAlternate:
        query = select(ProductAlternate).filter(ProductAlternate.upc == upc)
        return self._session.scalars(query).one()


def get_products_repository() -> ProductsRepository:
    engine = create_engine(os.environ["SQLALCHEMY_DATABASE_URI"])
    Session = sessionmaker(engine)

    with Session.begin() as session:
        yield ProductsRepository(session)
