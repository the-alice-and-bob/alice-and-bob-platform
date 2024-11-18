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

from .decorators import authorize


@csrf_exempt
@authorize
def new_signup(request):
    """
    This webhook is triggered when a new user signs up.
    """
    return JsonResponse({'message': 'New Signup Webhook'})


@csrf_exempt
@authorize
def new_product_enrollment(request):
    """
    This webhook is triggered when a user enrolls in a FREE product.
    """
    return JsonResponse({'message': 'New Product Enrollment Webhook'})


@csrf_exempt
@authorize
def new_sale(request):
    """
    This webhook is triggered when a user enrolls in a PAID product.
    """
    return JsonResponse({'message': 'New Sale Webhook'})


@csrf_exempt
@authorize
def course_completed(request):
    """
    This webhook is triggered when a user completes a course.
    """
    return JsonResponse({'message': 'Course Completed Webhook'})


@csrf_exempt
@authorize
def chapter_completed(request):
    """
    This webhook is triggered when a user completes a chapter.
    """
    return JsonResponse({'message': 'Chapter Completed Webhook'})


@csrf_exempt
@authorize
def quiz_completed(request):
    """
    This webhook is triggered when a user completes a quiz.
    """
    return JsonResponse({'message': 'Quiz Completed Webhook'})


@csrf_exempt
@authorize
def lesson_completed(request):
    """
    This webhook is triggered when a user completes a lesson.
    """
    return JsonResponse({'message': 'Lesson Completed Webhook'})


__all__ = (
    'new_signup', 'new_product_enrollment', 'new_sale', 'course_completed', 'chapter_completed', 'quiz_completed', 'lesson_completed'
)
