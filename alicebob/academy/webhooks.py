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

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from celery_app import app as background_tasks

from .decorators import *
from .background_tasks.ezycourse_webhooks import *


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
    background_tasks.send_task('task_ezycourse_new_signup', args=(request.json,))

    return JsonResponse({'message': 'New Signup Webhook'})


@csrf_exempt
@require_http_methods(['POST'])
@authorize
@ensure_json
def new_product_enrollment(request):
    """
    This webhook is triggered when a user enrolls in a FREE product.
    """
    background_tasks.send_task('task_ezycourse_new_product_enrollment', args=(request.json,))

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
    background_tasks.send_task('task_ezycourse_new_sale', args=(request.json,))

    return JsonResponse({'message': 'New Sale Webhook'})


@csrf_exempt
@require_http_methods(['POST'])
@authorize
@ensure_json
def course_completed(request):
    """
    This webhook is triggered when a user completes a course.
    """

    background_tasks.send_task("task_ezycourse_course_completed", args=(request.json,))

    return JsonResponse({'message': 'Course Completed Webhook'})


@csrf_exempt
@require_http_methods(['POST'])
@authorize
@ensure_json
def chapter_completed(request):
    """
    This webhook is triggered when a user completes a chapter.
    """
    background_tasks.send_task("task_ezycourse_chapter_completed", args=(request.json,))

    return JsonResponse({'message': 'Chapter Completed Webhook'})


@csrf_exempt
@require_http_methods(['POST'])
@authorize
@ensure_json
def lesson_completed(request):
    """
    This webhook is triggered when a user completes a lesson.
    """
    background_tasks.send_task("task_ezycourse_lesson_completed", args=(request.json,))

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


__all__ = (
    'new_signup', 'new_product_enrollment', 'new_sale', 'course_completed', 'chapter_completed', 'quiz_completed', 'lesson_completed'
)
