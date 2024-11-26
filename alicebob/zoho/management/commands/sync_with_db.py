from django.core.management.base import BaseCommand

from academy.models import Student, Tag, Product, Sells, CourseProgress, Tag, Student, Product, CourseProgress
from zoho.models import ZohoLead, ZohoTag, ZohoContact, ZohoProduct, ZohoPurchaseOrders


class Command(BaseCommand):
    help = 'Sync Zoho DB with Academy DB'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Syncing Zoho DB with Academy DB..."))

        # Sync Tags
        self.stdout.write(self.style.SUCCESS("Syncing Tags..."))
        for tag in Tag.objects.all():
            ZohoTag.objects.get_or_create(tag=tag)

        # Sync Students
        self.stdout.write(self.style.SUCCESS("Syncing Students..."))
        for student in Student.objects.prefetch_related('tags', 'sells'):

            sells = student.sells.all()
            price_over_zero = sells.filter(product__price__gt=0).exists()

            if price_over_zero:
                for sell in sells:
                    zoho_contact, created = ZohoContact.objects.get_or_create(
                        student=student
                    )

                    # Get tags
                    zoho_tags = ZohoTag.objects.filter(
                        tag__in=sell.product.tags.all()
                    )

                    zoho_contact.tags.add(*zoho_tags)

            else:
                for sell in sells:
                    zoho_lead, created = ZohoLead.objects.get_or_create(
                        student=student
                    )

                    # Get tags
                    zoho_tags = ZohoTag.objects.filter(
                        tag__in=sell.product.tags.all()
                    )

                    zoho_lead.tags.add(*zoho_tags)

        # Sync Products
        self.stdout.write(self.style.SUCCESS("Syncing Products..."))
        for product in Product.objects.prefetch_related('tags'):
            zoho_product, created = ZohoProduct.objects.get_or_create(
                product=product
            )

            zoho_tags = ZohoTag.objects.filter(
                tag__in=product.tags.all()
            )

            zoho_product.tags.add(*zoho_tags)

        # Sync Sells
        self.stdout.write(self.style.SUCCESS("Syncing Sells..."))
        for sell in Sells.objects.prefetch_related('product', 'student'):
            ZohoPurchaseOrders.objects.get_or_create(
                student=sell.student,
                product=sell.product,
                sell=sell
            )
