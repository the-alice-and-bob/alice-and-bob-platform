from django.db import models
from model_utils.models import TimeStampedModel
from simple_history.models import HistoricalRecords

from academy.models import Student, Product, CourseProgress, Tag, Sells


class ZohoOAuth(models.Model):
    client_id = models.CharField(max_length=255, unique=True)
    client_secret = models.CharField(max_length=255, unique=True)
    grant_token = models.CharField(max_length=255, unique=True)
    refresh_token = models.CharField(max_length=255, unique=True)
    access_token = models.CharField(max_length=255, unique=True)
    expiry_time = models.BigIntegerField()
    api_domain = models.CharField(max_length=255)
    redirect_uri = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    history = HistoricalRecords()

    def __str__(self):
        return f"Client ID: {self.client_id} - {self.api_domain}"

    class Meta:
        verbose_name = "Zoho OAuth"
        verbose_name_plural = "Zoho OAuth"
        db_table = "zoho_oauth"
        # composed indexes
        indexes = [
            models.Index(fields=['access_token', 'refresh_token']),
        ]


class ZohoTag(TimeStampedModel, models.Model):
    zoho_id = models.CharField(max_length=255, null=True, db_index=True)
    tag = models.OneToOneField(Tag, on_delete=models.CASCADE)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.tag.name} - {self.tag.color}"

    class Meta:
        verbose_name = "Zoho Tag"
        verbose_name_plural = "Zoho Tags"
        db_table = "zoho_tags"


class ZohoLead(TimeStampedModel, models.Model):
    zoho_id = models.CharField(max_length=255, null=True, db_index=True)
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    tags = models.ManyToManyField(ZohoTag, related_name='leads_tags', blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.student.name} - {self.student.email}"

    class Meta:
        verbose_name = "Zoho Lead"
        verbose_name_plural = "Zoho Leads"
        db_table = "zoho_leads"


class ZohoContact(TimeStampedModel, models.Model):
    zoho_id = models.CharField(max_length=255, null=True, db_index=True)
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    tags = models.ManyToManyField(ZohoTag, related_name='contacts_tags', blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.student.name} - {self.student.email}"

    class Meta:
        verbose_name = "Zoho Contact"
        verbose_name_plural = "Zoho Contacts"
        db_table = "zoho_contacts"


class ZohoProduct(TimeStampedModel, models.Model):
    zoho_id = models.CharField(max_length=255, null=True, db_index=True)
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    tags = models.ManyToManyField(ZohoTag, related_name='products_tags', blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.product.product_name} - {self.product.ezy_id}"

    class Meta:
        verbose_name = "Zoho Product"
        verbose_name_plural = "Zoho Products"
        db_table = "zoho_products"


class ZohoPurchaseOrders(TimeStampedModel, models.Model):
    zoho_id = models.CharField(max_length=255, null=True, db_index=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    sell = models.OneToOneField(Sells, on_delete=models.CASCADE, null=True)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.student.name} - {self.product.product_name}"

    class Meta:
        verbose_name = "Zoho Purchase Order"
        verbose_name_plural = "Zoho Purchase Orders"
        db_table = "zoho_purchase_orders"
        indexes = [
            models.Index(fields=['student', 'product', 'sell']),
        ]
        unique_together = ('student', 'product', 'sell')


class ZohoCourseProgress(TimeStampedModel, models.Model):
    zoho_id = models.CharField(max_length=255, null=True, db_index=True)

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    course_progress = models.OneToOneField(CourseProgress, on_delete=models.CASCADE)

    history = HistoricalRecords()

    def __str__(self):
        return f"{self.student.name} - {self.product.product_name}"

    class Meta:
        verbose_name = "Zoho Course Progress"
        verbose_name_plural = "Zoho Courses Progress"
        db_table = "zoho_course_progress"
        indexes = [
            models.Index(fields=['student', 'product']),
        ]
        unique_together = ('student', 'product', 'course_progress')
