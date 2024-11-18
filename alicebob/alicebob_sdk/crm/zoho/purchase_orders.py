from typing import Iterable
from datetime import datetime
from dataclasses import dataclass, field

from .interfaces import *


class PurchaseOrderResponseException(Exception):
    ...


class PurchaseOrderDuplicatedException(Exception):
    ...


class PurchaseOrderNotFoundException(Exception):
    ...


FIELD_MAP = {
    "id": "identifier",
    "ID_EzyCourse": "ezycourse_id",
    "Subject": "subject",
    "Contact_Name": "contact_name",
    "Due_Date": "due_date",
    "Status": "status",
    "PO_Date": "po_date",
    "Purchase_Items": "purchase_items",
}


class PurchaseOrderStatus:
    DRAFT = "Borrador"
    SENT = "Enviado"
    APPROVED = "Aprobado"
    REJECTED = "Rechazado"
    DELIVERED = "Entregado"


@dataclass
class ProductSummary:
    name: str
    identifier: int
    unit_price: float


@dataclass
class PurchaseItem:
    list_price: float
    product: ProductSummary

    tax: float = 0
    quantity: int = 1
    discount: float = 0
    total: float = None
    identifier: int = None
    description: str = None
    created: datetime = None
    modified_time: datetime = None
    total_after_discount: float = None

    def __post_init__(self):
        if not self.created:
            self.created = datetime.now()

        if not self.modified_time:
            self.modified_time = datetime.now()

        if not self.total_after_discount:
            self.total_after_discount = self.total - self.discount

        if not self.total:
            self.total = self.list_price * self.quantity


@dataclass
class Buyer:
    identifier: int
    name: str


@dataclass
class PurchaseOrder:
    subject: str
    ezycourse_id: int
    contact_name: Buyer

    identifier: int = None
    po_date: datetime = None
    due_date: datetime = None
    status: str = PurchaseOrderStatus.DELIVERED
    purchase_items: list[PurchaseItem] = field(default_factory=list)

    def __post_init__(self):
        if not self.po_date:
            self.po_date = datetime.now()

        if not self.due_date:
            self.due_date = datetime.now()

    @staticmethod
    def as_zoho() -> dict:
        return FIELD_MAP


class ZohoPurchaseOrders(BaseModule, ModuleInterface):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _custom_zoho_response(self, data: dict) -> PurchaseOrder:
        obj: PurchaseOrder = super()._map_zoho_response_with_object(data, PurchaseOrder, FIELD_MAP)

        """
        In contact name is:
        {'name': 'Jazmín Saavedra None', 'id': '738692000000680088'}
        
        Transform it to:
        Buyer(identifier=738692000000680088, name='Jazmín Saavedra None')
        """
        if contact := obj.contact_name:
            obj.contact_name = Buyer(identifier=contact.get("id"), name=contact.get("name"))

        # Parse purchase items
        purchase_items = []

        for item in obj.purchase_items:
            product = item.get("Product_Name")
            product_summary = ProductSummary(
                name=product.get("name"), identifier=product.get("id"), unit_price=product.get("unit_price")
            )

            purchase_items.append(
                PurchaseItem(
                    modified_time=item.get("Modified_Time"),
                    description=item.get("Description"),
                    discount=item.get("Discount"),
                    created=item.get("Created_Time"),
                    quantity=item.get("Quantity"),
                    list_price=item.get("List_Price"),
                    identifier=item.get("id"),
                    total=item.get("Total"),
                    total_after_discount=item.get("Total_After_Discount"),
                    tax=item.get("Tax"),
                    product=product_summary
                )
            )

        obj.purchase_items = purchase_items

        return obj

    def get_all(self) -> Iterable[PurchaseOrder]:
        for rec in super()._get_records(
                module_name=self.api_name, return_fields=FIELD_MAP.keys()
        ):
            yield self._custom_zoho_response(rec)

    def get_by_email(self, email: str) -> PurchaseOrder | PurchaseOrderNotFoundException:

        try:
            if found := self._search_by_email(email=email, module_name=self.api_name, return_fields=FIELD_MAP.keys()):
                yield self._custom_zoho_response(found)
        except ModuleRecordNotFound:
            raise PurchaseOrderNotFoundException(f"PurchaseOrder with email {email} not found")

    def get_by_id(self, record_id: int) -> PurchaseOrder | PurchaseOrderNotFoundException:
        try:
            if found := self._search_by_id(record_id=record_id, module_name=self.api_name, return_fields=FIELD_MAP.keys()):
                return self._custom_zoho_response(found)
        except ModuleException as e:
            raise PurchaseOrderNotFoundException(e)

    @staticmethod
    def _dump_for_update_or_create(purchase_order: PurchaseOrder) -> dict:
        return {
            "ID_EzyCourse": purchase_order.ezycourse_id,
            "Subject": purchase_order.subject,
            "Contact_Name": {
                "name": purchase_order.contact_name.name,
                "id": purchase_order.contact_name.identifier
            },
            "Status": purchase_order.status,
            "Due_Date": purchase_order.due_date.strftime("%Y-%m-%d"),
            "PO_Date": purchase_order.po_date.strftime("%Y-%m-%d"),
            "Purchase_Items": [
                {
                    "Description": item.description,
                    "Discount": item.discount,
                    "Quantity": item.quantity,
                    "List_Price": item.list_price,
                    "Total": item.total,
                    "Total_After_Discount": item.total_after_discount,
                    "Tax": item.tax,
                    "Product_Name": {
                        "name": item.product.name,
                        "id": item.product.identifier,
                        "unit_price": item.product.unit_price
                    }
                }
                for item in purchase_order.purchase_items
            ]
        }

    def create(self, purchase_order: PurchaseOrder) -> bool | PurchaseOrderResponseException | PurchaseOrderDuplicatedException:
        purchase_order_dict = self._dump_for_update_or_create(purchase_order)

        try:
            self._create_record(module_name=self.api_name, data=purchase_order_dict)
        except ModuleRecordDuplicatedException as e:
            raise PurchaseOrderDuplicatedException(e)

        except ModuleException as e:
            raise PurchaseOrderResponseException(e)

        return True

    def update(self, record_id: int, purchase_order: PurchaseOrder) -> bool | PurchaseOrderResponseException | PurchaseOrderNotFoundException:
        purchase_order_dict = self._dump_for_update_or_create(purchase_order)

        try:
            self._update_record(module_name=self.api_name, record_id=record_id, data=purchase_order_dict)
        except ModuleRecordDuplicatedException as e:
            raise PurchaseOrderNotFoundException(e)

        except ModuleException as e:
            raise PurchaseOrderResponseException(e)

        return True

    def delete(self, record_id: int) -> bool | PurchaseOrderNotFoundException:
        try:
            self._delete_record(module_name=self.api_name, record_id=record_id)
        except ModuleRecordNotFound:
            raise PurchaseOrderNotFoundException(f"PurchaseOrder with id {record_id} not found")

        return True


__all__ = ("ZohoPurchaseOrders", "PurchaseOrder", "PurchaseOrderNotFoundException", "PurchaseOrderDuplicatedException",
           "PurchaseOrderResponseException", "PurchaseOrderStatus", "ProductSummary", "PurchaseItem", "Buyer")
