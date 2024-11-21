import builtins
from datetime import datetime
from time import sleep

from typing import Optional, List, Tuple, Literal

from django.db.transaction import atomic

from awesome_zohocrm import (
    ZohoCRM, ZohoProducts, ProductNotFoundException, Product as ZohoProduct, Tag,
    PurchaseOrder, PurchaseItem, Buyer, PurchaseOrderStatus, ProductSummary, ProductDuplicatedException,
    ZohoLeads, LeadNotFoundException, ZohoContacts, ZohoPurchaseOrders, ContactNotFoundException, PurchaseOrderNotFoundException,
    LeadDuplicatedException, Lead, ZohoCourseProgress, CourseBrief, CourseProgressDuplicatedException,
    CourseProgress as CourseProgressZoho
)

from alicebob_sdk.zoho import zoho_instance
from academy.models import Student, Product, Sells, ProductTypes, CourseProgress

from .models import LessonCompleted, ChapterCompleted, CourseCompleted


class UserCreationException(Exception):
    ...


def merge_tags(tag_list_one: List[Tag], tag_list_two: List[Tag]) -> List[Tag]:
    """
    Merge two lists of tags
    """
    ret = []
    tags_cache = set()

    for tag_list in (tag_list_one, tag_list_two):
        for tag in tag_list:
            if tag.name not in tags_cache:
                tags_cache.add(tag.name)
                ret.append(tag)
                continue

    return ret


def load_module_and_cache(crm: ZohoCRM, module_function: str) -> ZohoLeads | ZohoProducts | ZohoContacts | ZohoPurchaseOrders:
    module_key = f"zoho_instance_{module_function}"

    if getattr(builtins, module_key, None) is None:
        setattr(builtins, module_key, getattr(crm, module_function)())

    return getattr(builtins, module_key)


def check_or_create_student(
        email: str,
        identifier: int,
        first_name: str,
        last_name: str,
        *,
        zoho: Optional[ZohoCRM] = None
) -> Student:
    # Check if the user already exists
    try:
        return Student.objects.get(email=email, ezy_id=identifier)
    except Student.DoesNotExist:

        with atomic():

            # Create the Lead at Zoho
            zoho: ZohoCRM = zoho or zoho_instance()
            zoho_leads: ZohoLeads = zoho.get_leads_module()

            # Check if the lead already exists
            zoho_id = None

            try:
                zoho_id = zoho_leads.get_by_email(email).identifier
            except LeadNotFoundException:
                # Create the lead
                try:
                    zoho_id = zoho_leads.create(
                        Lead(
                            email=email,
                            first_name=first_name,
                            last_name=last_name
                        )
                    )
                except LeadDuplicatedException:
                    print(f"Lead with email {email} already exists or already converted.")

            except Exception as e:
                raise UserCreationException(f"Error creating lead: {e}")

            # Create a new student
            return Student.objects.create(
                zoho_id=zoho_id,
                ezy_id=identifier,
                email=email,
                first_name=first_name,
                last_name=last_name,
            )


def get_or_create_product(
        zoho: ZohoCRM,
        product_id: int,
        product_name: str,
        price: float,
        product_type: ProductTypes,
) -> Product:
    # Get the product ID from DB
    try:
        return Product.objects.get(ezy_id=product_id)
    except Product.DoesNotExist:
        zoho_product_module: ZohoProducts = load_module_and_cache(zoho, "get_products_module")

        print(f"Product {product_id} not found in DB. Creating...")
        # Create in Zoho
        try:
            zoho_product = ZohoProduct(
                ezycourse_id=product_id,
                product_name=product_name,
                unit_price=price,
                product_category=product_type.value,
            )

            zoho_product_module: ZohoProducts = load_module_and_cache(zoho, "get_products_module")
            zoho_product_module.create(zoho_product)

        except ProductDuplicatedException:

            try:
                zoho_product = zoho_product_module.get_by_ezy_id(product_id)
            except ProductNotFoundException:
                print(f"Product {product_id} not found in Zoho")
                return False
            except Exception as e:
                print(f"Error getting product: {e}")
                return False

        # Create the product
        return Product.objects.create(
            zoho_id=zoho_product.identifier,
            ezy_id=product_id,
            product_type=zoho_product.product_category,
            product_name=product_name,
            price=price,
            tags=[
                tag.name for tag in zoho_product.tags
            ],
            zoho_tags=[
                {
                    "id": tag.identifier,
                    "name": tag.name,
                    "color": tag.color
                }
                for tag in zoho_product.tags
            ]
        )


def get_contact_or_lead(email: str, zoho: ZohoCRM) -> Tuple[int | None, bool]:
    """
    This function will get a contact or a lead from Zoho.

    Returns the Zoho ID of the associated record for the email passed.

    If the record is not found, it will return None

    Returns: (zoho_id, is_lead)
    """
    print(f"Getting Zoho ID for {email}...")
    zoho_lead_module: ZohoLeads = load_module_and_cache(zoho, "get_leads_module")

    # Checks if the lead exists
    try:
        zoho_obj = zoho_lead_module.get_by_email(email)
        is_lead = True
    except LeadNotFoundException:
        print(f"Lead {email} not found in Zoho. Creating contact...")

        zoho_contact_module: ZohoContacts = load_module_and_cache(zoho, "get_contacts_module")

        # Checks if Contact exists
        try:
            zoho_obj = zoho_contact_module.get_by_email(email)
            is_lead = False
        except ContactNotFoundException:
            print(f"Contact {email} not found in Zoho")
            is_lead = False
            zoho_obj = None

    if zoho_obj:
        zoho_id = zoho_obj.identifier
    else:
        zoho_id = None

    return zoho_id, is_lead


def get_or_create_purchase_order(
        zoho: ZohoCRM,
        st: Student,
        pd: Product,
        gateway: str | None,
        update_zoho: bool = True
) -> PurchaseOrder:
    sell_subject = pd.product_name

    try:
        Sells.objects.get(student=st, product=pd)
    except Sells.DoesNotExist:
        print(f"Creating sale for {pd.product_name}...")
        sl = Sells.objects.create(
            subject=sell_subject,
            student=st,
            product=pd,
            sell_price=pd.price,
            gateway=gateway
        )

        if update_zoho:
            print(f"Checking Zoho ID for sale {pd.product_name}...")
            zoho_sale: ZohoPurchaseOrders = load_module_and_cache(zoho, "get_purchase_orders_module")

            # Get from Purchase Orders from Zoho
            try:
                zoho_sale_obj_id = zoho_sale.get_first_by_user_id_and_subject(st.zoho_id, sell_subject).identifier
            except PurchaseOrderNotFoundException:
                print(f"Purchase Order for {pd.product_name} not found in Zoho. Creating...")
                order = PurchaseOrder(
                    subject=sell_subject,
                    ezycourse_id=pd.ezy_id,
                    contact_name=Buyer(
                        identifier=st.zoho_id,
                        name=st.full_name
                    ),
                    status=PurchaseOrderStatus.DELIVERED,
                    purchase_items=[
                        PurchaseItem(
                            description=sell_subject,
                            list_price=pd.price,
                            product=ProductSummary(
                                name="301 - Ocultación y ejecución de código Python",
                                identifier=pd.zoho_id,
                                unit_price=pd.price
                            )
                        )
                    ]
                )
                zoho_sale_obj_id = zoho_sale.create(order)

            except Exception as e:
                print(f"Error getting sale: {e}")
                return False

            # Save the sale
            sl.zoho_id = zoho_sale_obj_id
            sl.save()


def update_user_tags(zoho: ZohoCRM, st: Student, pd: Product, lead_or_contact: str = Literal["lead", "contact"]) -> None:
    # Set tags to the product based on the student
    if lead_or_contact == "lead":
        module_name = "get_leads_module"
    elif lead_or_contact == "contact":
        module_name = "get_contacts_module"
    else:
        raise ValueError("Invalid value for lead_or_contact")

    module = load_module_and_cache(zoho, module_name)
    record = module.get_by_email(st.email)

    #
    # Local DB tags
    #
    product_tags_zoho_format = [
        Tag(
            identifier=t["id"],
            name=t["name"],
            color=t["color"]
        ) for t in pd.zoho_tags
    ]

    # Update tags with the new tags from product
    st.tags.extend([tag.name for tag in product_tags_zoho_format])
    st.zoho_tags = [
        {
            "id": tag.identifier,
            "name": tag.name,
            "color": tag.color
        }
        for tag in merge_tags(product_tags_zoho_format, record.tags)
    ]
    st.save()

    # Update tags with the new tags from contact
    module.update_tags(
        record.identifier,
        tags=merge_tags(record.tags, product_tags_zoho_format)
    )


def convert_lead_to_contact(zoho: ZohoCRM, email: str, lead_id: int) -> int | ContactNotFoundException:
    print(f"Converting lead {lead_id} to contact...")
    zoho_lead_module = load_module_and_cache(zoho, "get_leads_module")
    zoho_contact_module = load_module_and_cache(zoho, "get_contacts_module")

    # Convert the lead to a contact
    try:
        zoho_lead_module.convert_lead(lead_id)
    except LeadNotFoundException:
        print(f"It seems that the lead {lead_id} was already converted")

    # Get the contact
    zoho_contact = None

    for _ in range(15):
        try:
            zoho_contact = zoho_contact_module.get_by_email(email)
            break
        except ContactNotFoundException:
            print(f"Contact {email} not found in Zoho. Waiting...")
            sleep(5)

    if not zoho_contact:
        print(f"Contact {email} not found in Zoho")
        raise ContactNotFoundException(f"Contact {email} not found in Zoho")

    return zoho_contact.identifier


def update_course_progress(
    obj: CourseCompleted | ChapterCompleted | LessonCompleted
):
    zoho: ZohoCRM = zoho_instance()

    try:
        st: Student = check_or_create_student(
            email=obj.email,
            identifier=obj.identifier,
            first_name=obj.first_name,
            last_name=obj.last_name,
            zoho=zoho,
        )
    except Exception as e:
        print(f"Error creating student: {e}")
        raise ValueError(f"Error creating student: {e}")

    # For this we need that the student has a Zoho ID and is not a lead
    if st.zoho_id is None or st.zoho_is_lead:
        print(f"Student {st.email} is a lead. Skipping.")
        raise ValueError(f"Student {st.email} is a lead. Skipping.")

    config = {}

    if isinstance(obj, ChapterCompleted):
        config["current_chapter"] = obj.chapter_name

    if isinstance(obj, LessonCompleted):
        config["current_lesson"] = obj.lesson_name

    # TODO: Implement progress
    # if new_progress:
    #     config["progress"] = new_progress

    if isinstance(obj, CourseCompleted):
        # date: now
        config["completed_date"] = datetime.now()

    # Get the course progress
    with atomic():
        zoho_course_progress_module: ZohoCourseProgress = zoho.get_course_progress_module()

        try:
            pg: CourseProgress = CourseProgress.objects.get(student=st, course__ezy_id=course_id)

            #
            # Update
            #
            for key, value in config.items():
                setattr(pg, key, value)

            pg.save()

            # Get course ID
            course = Product.objects.get(ezy_id=obj.course_id)

            # Fix date:
            if "completed_date" in config:
                config["completed_date"] = config["completed_date"].strftime("%Y-%m-%d")

            zoho_course_progress = zoho_course_progress_module.get_by_customer_and_course(st.zoho_id, course.zoho_id)
            zoho_course_progress_module.update(
                zoho_course_progress.identifier,
                **config
            )

        except CourseProgress.DoesNotExist:
            #
            # Create from scratch
            #
            try:
                # Get Course Zoho ID
                try:
                    zoho_course_id: int = Product.objects.get(ezy_id=obj.course_id).zoho_id
                except Product.DoesNotExist:
                    raise ValueError(f"Course {obj.course_id} not found in local DB. Skipping.")

                course_progress = CourseProgressZoho(
                    course=CourseBrief(
                        name=obj.course_name,
                        identifier=zoho_course_id
                    ),
                    customer=Buyer(
                        name=f"{st.first_name} {st.last_name}",
                        identifier=st.zoho_id
                    ),
                    **config
                )

                # Get the course progress
                zoho_course_progress_id = zoho_course_progress_module.create(course_progress)
            except CourseProgressDuplicatedException:
                zoho_course_progress_id = zoho_course_progress_module.get_by_customer_and_course(st.zoho_id, course_id).identifier

            config["zoho_id"] = zoho_course_progress_id
            config["student"] = st
            config["course"] = Product.objects.get(ezy_id=obj.course_id)

            # Create the course progress
            CourseProgress.objects.create(
                **config
            )


__all__ = (
    "check_or_create_student", "UserCreationException", "get_or_create_product", "merge_tags", "load_module_and_cache",
    "get_contact_or_lead", "get_or_create_purchase_order", "update_user_tags", "convert_lead_to_contact", "update_course_progress"
)
