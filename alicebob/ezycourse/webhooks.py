"""
This file defines the EzyCourses webhooks:

- New Signup Webhook
- New Product Enrollment: This is triggered when a user enrolls in FREE product
- New Sale Webhook: This is triggered when a user enrolls in a PAID product
- Course Completed Webhook: This is triggered when a user completes a course
- Chapter Completed Webhook: This is triggered when a user completes a chapter
- Quiz Completed Webhook: This is triggered when a user completes a quiz
- Lesson Completed Webhook: This is triggered when a user completes a lesson
"""
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from ezycourse.engine import *
from alicebob_sdk.decorators import *
from celery_app import app as background_task


@csrf_exempt
@require_http_methods(['POST'])
@authorize
@ensure_json
def new_signup(request):
    """
    This webhook is triggered when a new user signs up.
    ---
    id	Id of the student.
    first_name	First name of the student.
    last_name	Last name of the student.
    name	Name of the student. Value should be 3 to 50 characters long.
    email	Email of the student. Value should be 50 characters long.
    """
    ezycourse_new_signup(request.json)

    return JsonResponse({'message': 'New Signup Webhook'})


@csrf_exempt
@require_http_methods(['POST'])
@authorize
@ensure_json
def new_product_enrollment(request):
    """
    This webhook is triggered when a user enrolls in a FREE product.
    """
    ezycourse_new_product_enrollment(request.json)

    return JsonResponse({'message': 'New Product Enrollment Webhook'})


@csrf_exempt
@require_http_methods(['POST'])
@authorize
@ensure_json
def new_sale(request):
    """
    This webhook is triggered when a user enrolls in a PAID product.
    ---

    JSON Schema:

    id	Id of the student.
    first_name	First name of the student.
    last_name	Last name of the student.
    name	Name of the student. Value should be 3 to 50 characters long.
    email	Email of the student. Value should be 50 characters long.
    product_id	Product id will be the id of the product. Value will be integer. This is required when product_type is not 'private_chat'.
    product_type	Product type will be one of the following: 'course', 'bundle_course', 'private_chat', 'community', 'group', 'digital_product', 'physical_product', 'video_library', 'membership','organization'.
    product_name	Name of the product
    price	Price of the sold product.
    gateway	Payment gateway of the sold product.

    """
    ezycourse_new_sale(request.json)

    return JsonResponse({'message': 'New Sale Webhook'})


@csrf_exempt
@require_http_methods(['POST'])
@authorize
@ensure_json
def course_completed(request):
    """
    This webhook is triggered when a user completes a course.
    """

    ezycourse_course_completed(request.json)

    return JsonResponse({'message': 'Course Completed Webhook'})


@csrf_exempt
@require_http_methods(['POST'])
@authorize
@ensure_json
def chapter_completed(request):
    """
    This webhook is triggered when a user completes a chapter.
    """
    ezycourse_chapter_completed(request.json)

    return JsonResponse({'message': 'Chapter Completed Webhook'})


@csrf_exempt
@require_http_methods(['POST'])
@authorize
@ensure_json
def lesson_completed(request):
    """
    This webhook is triggered when a user completes a lesson.
    """
    ezycourse_lesson_completed(request.json)

    return JsonResponse({'message': 'Lesson Completed Webhook'})


@csrf_exempt
@require_http_methods(['POST'])
@authorize
@ensure_json
def quiz_completed(request):
    """
    This webhook is triggered when a user completes a quiz.
    """
    return JsonResponse({'message': 'Quiz Completed Webhook'})


@csrf_exempt
@require_http_methods(['POST'])
@authorize
@ensure_json
def subscribe_to_email_list(request):
    """
    This webhook is triggered when a user subscribes to an email list.

    Expected data format in request.json:

    {
        'params': {
            'school_id': 794,
            'form_name': 'subscribe-user-to-the-mail-list',
            'response': {
                'Nombre': 'Daniel',
                'Email': 'garcia.garcia.daniel@gmail.com'
            }
        }
    }
    """

    data = request.json

    try:
        name = data['params']['response']['Nombre']
    except KeyError:
        logger.error("Received invalid data from the form")
        return

    try:
        email = data['params']['response']['Email']
    except KeyError:
        logger.error("Received invalid data from the form")
        return

    if settings.DEBUG:
        subscribe_user_to_mail_list(name, email)

    else:
        background_task.send_task("task_subscribe_new_user_to_general_list", args=(name, email))

    return JsonResponse({'message': 'Subscribe to Email List Webhook'})


__all__ = (
    'new_signup', 'new_product_enrollment', 'new_sale', 'course_completed', 'chapter_completed', 'quiz_completed', 'lesson_completed',
    'subscribe_to_email_list'
)
