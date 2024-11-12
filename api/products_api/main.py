from datetime import datetime
from decimal import Decimal
from typing import Annotated, List

from fastapi import Depends, FastAPI, Path
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from products_api.repository import ProductsRepository, get_products_repository


class Variant(BaseModel):
    upc: str = Field(title="Either a secondary product UPC (for variant) or a case UPC")
    type: str = Field(title='Type of alternate - this is either "variant" or "case"')
    case_pack: float | None = Field(
        title='If alternate_type is "case", then the number of units contained in a case'
    )


class Product(BaseModel):
    name: str
    upc: str
    item_number: int = Field(title="Customer's internal identifier for this product")
    price: Decimal = Field(title="Current price")
    supplier: str = Field(title="Name of supplier for a product")
    inventory_level: int = Field(title="Current level of inventory of a product")
    inventory_updated_at: datetime = Field(
        title="Timestamp when inventory was last updated"
    )
    variants: List[Variant] = Field(title="Alternates of the product")


class Message(BaseModel):
    message: str


app = FastAPI()


@app.get(
    "/v1/product/{upc}", response_model=Product, responses={404: {"model": Message}}
)
def get_product(
    upc: Annotated[str, Path(title="UPC of the product", regex="^[0-9]{14}$")],
    repository: ProductsRepository = Depends(get_products_repository),
) -> Product | JSONResponse:
    """
    Retrieve product information for given UPC. The UPC value
    can be an identifier of product or any of its alternates.

    Parameters:
    - **upc**: UPC in GTIN-14 format (14 digits)

    Example:

    ```http
    GET /v1/product/00007127957158 HTTP/1.1

    HTTP/1.1 200 OK
    Content-Type: application/json

    {
      "name": "Gracious Hungry Clarke",
      "upc": "00007127930100",
      "item_number": 30257880,
      "price": "13.76",
      "supplier": "Fresh Express Mid-Atl #16Efx#",
      "inventory_level": 15,
      "inventory_updated_at": "2024-11-04T20:00:16",
      "variants": [
        {
          "upc": "00005114137289",
          "type": "variant",
          "case_pack": null
        },
        {
          "upc": "00007127957158",
          "type": "case",
          "case_pack": 6
        }
      ]
    }
    ```
    """
    product = repository.get_by_upc_of_product_or_alternate(upc)
    if product is None:
        return JSONResponse(status_code=404, content={"message": "Product not found"})
    return Product(
        name=product.name,
        upc=product.upc,
        item_number=product.item_number,
        price=product.price,
        supplier=product.supplier,
        inventory_level=product.inventory_level,
        inventory_updated_at=product.inventory_updated_at,
        variants=[
            Variant(
                upc=alternate.upc,
                type=alternate.alternate_type,
                case_pack=alternate.case_pack,
            )
            for alternate in product.product_alternates
        ],
    )
