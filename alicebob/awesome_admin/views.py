from django.shortcuts import render
from academy.models import Student, Sells
from news.models import News


def dashboard_callback(request, context: dict):
    students_count = Student.objects.count()
    sales_count = Sells.objects.count()
    news_count = News.objects.count()

    latest_students_enrolled = {
        "headers": ["Nombre", "Apellido", "Email", "Fecha de registro"],
        "rows": [
            [
                student.first_name,
                student.last_name,
                student.email,
                student.created
            ]
            for student in Student.objects.order_by('-created')[:5]
        ]
    }

    latest_sales = {
        "headers": ["Nombre", "Apellido", "Email", "Fecha de compra", "Producto", "Precio"],
        "rows": [
            [
                sl.student.first_name,
                sl.student.last_name,
                sl.student.email,
                sl.created,
                sl.product.product_name,
                sl.product.price
            ]
            for sl in Sells.objects.order_by('-created')[:10]
        ]
    }

    # Datos para las gráficas
    context.update({
        'students_count': students_count,
        'sales_count': sales_count,
        'news_count': news_count,
        'latest_students': latest_students_enrolled,
        'latest_sales': latest_sales
    })

    return context
