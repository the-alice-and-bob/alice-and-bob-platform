from enum import Enum

from django.db import models
from model_utils.models import TimeStampedModel
from simple_history.models import HistoricalRecords


class Tag(models.Model):
    name = models.CharField(max_length=150, unique=True)
    color = models.CharField(max_length=50, default='blue')
    color_code = models.CharField(max_length=50, default='#0000FF')

    class Meta:
        db_table = 'tags'
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.name


class PaymentGateway(Enum):
    STRIPE = "STRIPE"
    MANUAL = "MANUAL"


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
    EVENT = 'event'


class UserType(Enum):
    STUDENT = "student"
    TEACHER = "teacher"
    ADMIN = "admin"


class CourseStatus(Enum):
    PUBLISHED = "PUBLISHED"
    DRAFT = "DRAFT"


class UserStatus(Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    SUSPENDED = "SUSPENDED"
    DELETED = "DELETED"


class Product(TimeStampedModel, models.Model):
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
    ezy_id = models.IntegerField(unique=True)
    product_type = models.CharField(max_length=50, choices=[(tag.name, tag.value) for tag in ProductTypes], default=ProductTypes.COURSE)
    product_name = models.CharField(max_length=100)
    price = models.FloatField(default=0)
    tags = models.ManyToManyField(Tag, related_name='products_tags', blank=True)

    published_date = models.DateTimeField(null=True)

    description = models.TextField(null=True, blank=True)
    image = models.URLField(null=True, max_length=500, default=None)
    language = models.CharField(max_length=20, null=True, default='Español')
    extra_data = models.JSONField(null=True, default=dict, blank=True)

    status = models.CharField(
        max_length=50, null=True, choices=[(tag.name, tag.value) for tag in CourseStatus], default=CourseStatus.PUBLISHED
    )

    history = HistoricalRecords()

    class Meta:
        db_table = 'products'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return f"{self.product_name}"


class Student(TimeStampedModel, models.Model):
    """
    id	Id of the student.
    first_name	First name of the student.
    last_name	Last name of the student.
    name	Name of the student. Value should be 3 to 50 characters long.
    email	Email of the student. Value should be 50 characters long.
    """
    ezy_id = models.IntegerField(unique=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=800, unique=True)
    tags = models.ManyToManyField(Tag, related_name='students_tags', blank=True)

    created_date = models.DateTimeField(auto_now_add=True, null=True)
    last_login = models.DateTimeField(null=True)

    user_type = models.CharField(max_length=50, null=True, choices=[(tag, tag.value) for tag in UserType], default=UserType.STUDENT)
    user_status = models.CharField(max_length=50, null=True, choices=[(tag, tag.value) for tag in UserStatus], default=UserStatus.ACTIVE)

    history = HistoricalRecords()

    class Meta:
        db_table = 'students'
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.full_name} ({self.email})"


class Sells(TimeStampedModel, models.Model):
    subject = models.CharField(max_length=400, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='sells')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sells')
    gateway = models.CharField(max_length=100, choices=[(tag.name, tag.value) for tag in PaymentGateway], default=PaymentGateway.STRIPE)
    sell_price = models.FloatField(default=0)

    date = models.DateTimeField(auto_now_add=True, help_text='Date when the product was sold')

    history = HistoricalRecords()

    class Meta:
        unique_together = ('student', 'product')
        db_table = 'sells'
        verbose_name = 'Sell'
        verbose_name_plural = 'Sells'

    def __str__(self):
        return f"{self.student.email} - {self.product.product_name}"


class CourseProgress(TimeStampedModel, models.Model):
    progress = models.FloatField(default=0)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Product, on_delete=models.CASCADE)

    current_chapter = models.CharField(max_length=300, null=True)
    current_lesson = models.CharField(max_length=300, null=True)

    completed_date = models.DateTimeField(null=True, help_text='Date when the course was completed')
    started_date = models.DateTimeField(null=True, help_text='Date when the course was started')
    last_visit = models.DateTimeField(null=True, help_text='Last visit to the course')

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
