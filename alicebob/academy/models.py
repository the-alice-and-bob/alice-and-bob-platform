from enum import Enum

from django.db import models
from django.utils.text import slugify
from model_utils.models import TimeStampedModel
from simple_history.models import HistoricalRecords


# -------------------------------------------------------------------------
# Scoring values
# -------------------------------------------------------------------------
class PurchaseScore:
    FREE = 15
    PAID = 100


class UserScore:
    """
    - purchase_score:	0.5	- Es el indicador principal de valor económico.
    - engagement_score:	0.2	- Representa el uso activo y sostenido de productos.
    - community_score:	0.1	- Participación social contribuye al ecosistema.
    - retention_score:	0.15 -	Retorno a la plataforma indica lealtad.
    - email_engagement_score:	0.05 - Interacción con correos muestra interés (menos relevante).
    """
    PURCHASE_SCORE = 0.5
    ENGAGEMENT_SCORE = 0.2
    COMMUNITY_SCORE = 0.1
    RETENTION_SCORE = 0.15
    EMAIL_ENGAGEMENT_SCORE = 0.05


# -------------------------------------------------------------------------
# End Scoring values
# -------------------------------------------------------------------------


class Tag(models.Model):
    name = models.CharField(max_length=150, unique=True)
    color = models.CharField(max_length=50, default='blue')
    color_code = models.CharField(max_length=50, default='#0000FF')

    class Meta:
        db_table = 'academy_tags'
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
    product_type = models.CharField(
        max_length=50, choices=[(tag.name, tag.value) for tag in ProductTypes], default=ProductTypes.COURSE.value
    )
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

    engagement_score = models.FloatField(default=20, help_text="Peso adicional para el score del estudiante al comprar este producto.")

    history = HistoricalRecords()

    @property
    def slug_name(self) -> str:
        product_type = self.product_type.lower()

        return f"alicebob-{product_type}-{slugify(self.product_name)}"

    class Meta:
        db_table = 'products'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return f"{self.product_name}"


class Lead(TimeStampedModel, models.Model):
    email = models.EmailField(max_length=800, unique=True)
    ezy_id = models.IntegerField(null=True, db_index=True)
    tags = models.ManyToManyField(Tag, related_name='leads_tags', blank=True)

    history = HistoricalRecords()

    class Meta:
        db_table = 'leads'
        verbose_name = 'Lead'
        verbose_name_plural = 'Leads'


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

    # Scoring metrics
    purchase_score = models.FloatField(default=0, help_text="Score basado en compras realizadas.")
    engagement_score = models.FloatField(default=0, help_text="Score general de actividad y participación.")
    community_score = models.FloatField(default=0, help_text="Score basado en participación en comunidad.")
    retention_score = models.FloatField(default=0, help_text="Score basado en retención y visitas repetidas.")
    email_engagement_score = models.FloatField(default=0, help_text="Score basado en interacción con correos (apertura y clics).")

    total_score = models.FloatField(default=0, help_text="Score total del estudiante.")

    class Meta:
        db_table = 'students'
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.full_name} ({self.email})"

    def update_score(self, auto_save=True):
        self.total_score = (
                self.purchase_score * UserScore.PURCHASE_SCORE +
                self.engagement_score * UserScore.ENGAGEMENT_SCORE +
                self.community_score * UserScore.COMMUNITY_SCORE +
                self.retention_score * UserScore.RETENTION_SCORE +
                self.email_engagement_score * UserScore.EMAIL_ENGAGEMENT_SCORE
        )

        if auto_save:
            self.save()

    # -------------------------------------------------------------------------
    # Scoring functions
    # -------------------------------------------------------------------------
    def update_purchase_score(self, product: Product, sell: "Sells", auto_save=True):
        """
        Actualiza el scoring del estudiante basado en la compra y el engagement del producto
        (solo si el producto es de pago).
        """
        # Scoring base según el precio
        base_score = PurchaseScore.FREE if sell.sell_price == 0 else PurchaseScore.PAID

        # Aplica refuerzo de engagement solo para productos pagos
        if sell.sell_price > 0:
            engagement_multiplier = 1 + (product.engagement_score / 100)
        else:
            engagement_multiplier = 1  # No hay refuerzo para productos gratuitos

        # Calcula el score final
        final_score = base_score * engagement_multiplier
        self.purchase_score += final_score

        # Incrementa el engagement score solo si es un producto de pago
        if sell.sell_price > 0:
            self.engagement_score += product.engagement_score

        if auto_save:
            self.save()

    def update_email_engagement_score(student, event_type, auto_save=True):
        """
        Actualiza el score de 'email_engagement_score' del estudiante basado en eventos de email.
        """
        if event_type == EmailEventType.OPEN:
            score_increment = 0.5  # Define cuánto incrementa por apertura
        elif event_type == EmailEventType.CLICK:
            score_increment = 1.0  # Define cuánto incrementa por clic
        elif event_type in [EmailEventType.COMPLAINT, EmailEventType.HARD_BOUNCE]:
            score_increment = -2.0  # Penalización por quejas o rebotes duros
        else:
            score_increment = 0  # Para otros eventos

        student.email_engagement_score += score_increment

        if auto_save:
            student.update_score()  # Recalcula el total_score


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
