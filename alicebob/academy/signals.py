from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import Student, Sells, Product, Tag


@receiver(post_save, sender=Sells)
def user_buy_a_product(sender, instance: Sells, created, **kwargs):
    if created:
        # Add product tags
        for tag in instance.product.tags.all():
            instance.student.tags.add(tag)

        # Update student scores
        instance.student.update_purchase_score(instance.product, instance, auto_save=False)

    # Actualizar scores de engagement
    instance.student.update_score()
