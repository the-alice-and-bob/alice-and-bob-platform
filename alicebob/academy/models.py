from enum import Enum

from django.db import models
from simple_history.models import HistoricalRecords


class ProductTypes(Enum):
    COURSE = 'course'
    BUNDLE_COURSE = 'bundle_course'
    PRIVATE_CHAT = 'private_chat'
    COMMUNITY = 'community'
    GROUP = 'group'
    DIGITAL_PRODUCT = 'digital_product'
    PHYSICAL_PRODUCT = 'physical_product'
    VIDEO_LIBRARY = 'video_library'
    MEMBERSHIP = 'membership'
    ORGANIZATION = 'organization'


class Student(models.Model):
    """
    id	Id of the student.
    first_name	First name of the student.
    last_name	Last name of the student.
    name	Name of the student. Value should be 3 to 50 characters long.
    email	Email of the student. Value should be 50 characters long.
    """
    zoho_id = models.BigIntegerField(unique=True, null=True)
    zoho_is_lead = models.BooleanField(default=True)
    ezy_id = models.IntegerField(unique=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=800, unique=True)
    tags = models.JSONField(null=True, default=list)

    # This tag is used to store the tags from Zoho. Zoho tags contains some properties, like: id, name or color
    zoho_tags = models.JSONField(null=True, default=list)

    history = HistoricalRecords()

    class Meta:
        db_table = 'students'
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"EzyCourse ID: {self.ezy_id} - {self.first_name} {self.last_name}"


class Product(models.Model):
    """
    id	Id of the student.
    first_name	First name of the student.
    last_name	Last name of the student.
    name	Name of the student. Value should be 3 to 50 characters long.
    email	Email of the student. Value should be 50 characters long.
    product_id	Product id will be the id of the product. Value will be integer. This is required when product_type is not 'private_chat'.
    product_type	Product type will be one of the following: 'course', 'bundle_course', 'private_chat', 'community', 'group',
    'digital_product', 'physical_product', 'video_library', 'membership','organization'.
    product_name	Name of the product
    price	Price of the sold product.
    gateway	Payment gateway of the sold product.
    """
    zoho_id = models.BigIntegerField(unique=True, null=True)
    ezy_id = models.IntegerField(unique=True)
    product_type = models.CharField(max_length=50, choices=[(tag, tag.value) for tag in ProductTypes])
    product_name = models.CharField(max_length=100)
    price = models.FloatField(default=0)
    tags = models.JSONField(null=True, default=list)

    # This tag is used to store the tags from Zoho. Zoho tags contains some properties, like: id, name or color
    zoho_tags = models.JSONField(null=True, default=list)

    history = HistoricalRecords()


    class Meta:
        db_table = 'products'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return f"EzyCourse ID: {self.ezy_id} - {self.product_name}"


class Sells(models.Model):
    subject = models.CharField(max_length=400, null=True)
    zoho_id = models.BigIntegerField(null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    gateway = models.CharField(max_length=100)
    sell_price = models.FloatField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    history = HistoricalRecords()

    class Meta:
        unique_together = ('student', 'product', 'zoho_id')
        db_table = 'sells'
        verbose_name = 'Sell'
        verbose_name_plural = 'Sells'

    def __str__(self):
        return f"{self.student.email} - {self.product.product_name}"


class CourseProgress(models.Model):

    zoho_id = models.BigIntegerField(null=True)

    progress = models.FloatField(default=0)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Product, on_delete=models.CASCADE)

    current_chapter = models.CharField(max_length=300, null=True)
    current_lesson = models.CharField(max_length=300, null=True)

    completed_date = models.DateTimeField(null=True)
    started_date = models.DateTimeField(null=True)
    last_visit = models.DateTimeField(null=True)

    @property
    def is_completed(self):
        return self.progress == 100

    def __str__(self):
        return f"{self.student.full_name} - {self.course.product_name}"

    class Meta:
        db_table = 'course_progress'
        verbose_name = 'Course Progress'
        verbose_name_plural = 'Courses Progress'
        unique_together = ('student', 'course')
