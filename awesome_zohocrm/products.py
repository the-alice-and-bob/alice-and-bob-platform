from datetime import datetime
from typing import Iterable, List, Optional
from dataclasses import dataclass, field

from .interfaces import *


class ProductResponseException(Exception):
    ...


class ProductDuplicatedException(Exception):
    ...


class ProductNotFoundException(Exception):
    ...


FIELD_MAP = {
    "id": "identifier",
    "ID_EzyCourse": "ezycourse_id",
    "Product_Name": "product_name",
    "Product_Category": "product_category",
    "Unit_Price": "unit_price",
    "Created_Time": "created_time",
    "Modified_Time": "modified_time",
    "Tag": "tags",
}


@dataclass
class Product(RecordInterface):
    ezycourse_id: int
    product_name: str
    unit_price: float
    product_category: str
    tags: List[Tag] = field(default_factory=list)

    identifier: Optional[int] = None
    created_time: Optional[datetime] = None
    modified_time: Optional[datetime] = None

    @property
    def zoho_map(self) -> dict:
        return FIELD_MAP


class ZohoProducts(BaseModule, ModuleInterface):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def _map_dict(d: dict) -> Product:

        return Product(
            identifier=d["id"],
            ezycourse_id=d["ID_EzyCourse"],
            product_name=d["Product_Name"],
            product_category=d["Product_Category"],
            unit_price=d["Unit_Price"],
            created_time=d["Created_Time"],
            modified_time=d["Modified_Time"],
            tags=[Tag.from_zoho_api(tag) for tag in d["Tag"]]
        )

    def get_all(self) -> Iterable[Product]:
        for rec in super()._get_records(
                module_name=self.api_name, return_fields=FIELD_MAP.keys()
        ):
            yield super()._map_zoho_response_with_object(rec, Product, FIELD_MAP)

    def get_by_email(self, email: str) -> Product | ProductNotFoundException:

        try:
            if found := self._search_by_email(email=email, module_name=self.api_name, return_fields=FIELD_MAP.keys()):
                return super()._map_zoho_response_with_object(found, Product, FIELD_MAP)
        except ModuleRecordNotFound:
            raise ProductNotFoundException(f"Product with email {email} not found")

    def get_by_id(self, product_id: int) -> Product | ProductNotFoundException:
        try:
            if found := self._search_by_id(record_id=product_id, module_name=self.api_name, return_fields=FIELD_MAP.keys()):
                return super()._map_zoho_response_with_object(found, Product, FIELD_MAP)
        except ModuleException as e:
            raise ProductResponseException(e)
        except ModuleRecordNotFound:
            raise ProductNotFoundException(f"Product with id {product_id} not found")

    def get_by_ezy_id(self, ezy_id: int) -> Product | ProductNotFoundException:
        try:
            criteria = [
                ("ID_EzyCourse", "equals", str(ezy_id))
            ]

            if found := self._search_by_field(
                    criteria=criteria,
                    module_name=self.api_name,
                    return_fields=FIELD_MAP.keys()
            ):
                return super()._map_zoho_response_with_object(found, Product, FIELD_MAP)
        except ModuleException as e:
            raise ProductResponseException(f"Error getting product with ezy_id {ezy_id}: {e}")
        except ModuleRecordNotFound:
            raise ProductNotFoundException(f"Product with ezy_id {ezy_id} not found")

    def create(self, product: Product) -> bool | ProductResponseException | ProductDuplicatedException:
        product_dict = product.as_zoho()

        try:
            self._create_record(module_name=self.api_name, data=product_dict)
        except ModuleRecordDuplicatedException as e:
            raise ProductDuplicatedException(e)

        except ModuleException as e:
            raise ProductResponseException(e)

        return True

    def update(self, record_id: int, **kwargs) -> bool | ProductResponseException | ProductNotFoundException:
        product_dict = Product.from_object(FIELD_MAP, kwargs)

        try:
            self._update_record(module_name=self.api_name, record_id=record_id, data=product_dict)
        except ModuleRecordDuplicatedException as e:
            raise ProductNotFoundException(e)

        except ModuleException as e:
            raise ProductResponseException(e)

        return True

    def update_tags(self, record_id: int | str, tags: List[Tag]) -> None | ProductResponseException | ProductNotFoundException:

        try:
            self._update_record_tag(module_name=self.api_name, record_id=record_id, tags=tags)
        except ModuleRecordDuplicatedException as e:
            raise ProductNotFoundException(e)

        except ModuleException as e:
            raise ProductResponseException(e)

    def delete(self, record_id: int) -> bool | ProductNotFoundException:
        try:
            self._delete_record(module_name=self.api_name, record_id=record_id)
        except ModuleRecordNotFound:
            raise ProductNotFoundException(f"Product with id {record_id} not found")

        return True


__all__ = ("ZohoProducts", "Product", "ProductNotFoundException", "ProductDuplicatedException", "ProductResponseException")
