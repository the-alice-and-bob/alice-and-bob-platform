from django.conf import settings

from news.models import News
from campaigns.models import EmailCampaigns
from academy.models import Student, Sells


def dashboard_callback(request, context: dict):
    students_count = Student.objects.count()
    sales_count = Sells.objects.count()
    # news_count = News.objects.count()
    emails_count = EmailCampaigns.objects.count()

    latest_students_enrolled = {
        "headers": ["Nombre", "Apellido", "Email", "Fecha de registro"],
        "rows": [
            [
                student["first_name"],
                student["last_name"],
                student["email"],
                student["created"]
            ]
            for student in Student.objects.values(
                "first_name", "last_name", "email", "created"
            ).order_by('-created')[:5]
        ]
    }

    latest_sales = {
        "headers": ["Nombre", "Apellido", "Email", "Fecha de compra", "Producto", "Precio"],
        "rows": [
            [
                sl["student__first_name"],
                sl["student__last_name"],
                sl["student__email"],
                sl["created"],
                sl["product__product_name"],
                sl["sell_price"]
            ]
            for sl in Sells.objects.prefetch_related("student", "product").values(
                "student__first_name", "student__last_name", "student__email", "created", "product__product_name", "sell_price"
            ).order_by('-created')[:5]
        ]
    }

    table_engagement = {
        "headers": ["Nombre", "Apellido", "Email", "Score total", "Score de compras"],
        "rows": [
            [
                student["first_name"],
                student["last_name"],
                student["email"],
                student["total_score"],
                student["purchase_score"]
            ]
            for student in Student.objects.values(
                "first_name", "last_name", "email", "purchase_score", "total_score"
            ).order_by("-total_score")[:5]
        ]
    }

    # Datos para las gráficas
    context.update({
        'students_count': students_count,
        'sales_count': sales_count,
        # 'news_count': news_count,
        'emails_count': emails_count,
        'latest_students': latest_students_enrolled,
        'latest_sales': latest_sales,
        'table_engagement': table_engagement
    })

    # -------------------------------------------------------------------------
    # Engagement de los usuarios
    # -------------------------------------------------------------------------
    # Query para usuarios con mayor engagement pagado considerando scoring total y de compras

    return context


def environment_callback(request):
    if settings.DEBUG:
        return ["Development", "info"]
    else:
        return ["Production", "danger"]

# -------------------------------------------------------------------------
# Sidebar callbacks
# -------------------------------------------------------------------------
