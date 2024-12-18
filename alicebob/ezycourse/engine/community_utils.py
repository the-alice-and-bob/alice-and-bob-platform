from typing import Iterable

from awesome_ezycourse.sdk import Communities
from academy.models import Product, ProductTypes

from .auth import ezycourse_instance


def populate_communities() -> Iterable[Product]:

    communities = Communities(auth=ezycourse_instance())

    for community in communities.list():

        try:
            product = Product.objects.get(ezy_id=community.identifier)
            already_exists = True
        except Product.DoesNotExist:
            already_exists = False
            product = Product.objects.create(
                ezy_id=community.identifier,
                product_type=ProductTypes.COMMUNITY,
                product_name=community.title,
                price=community.pricing,
                description=community.short_description,
                image=community.cover
            )

        if already_exists:
            continue

        yield product


__all__ = ('populate_communities',)
