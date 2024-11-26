from django.urls import path

from .webhooks import *

urlpatterns = [
    path('new-signup/', new_signup, name='new-signup'),
    path('new-enrollment/', new_product_enrollment, name='new-enrollment'),
    path('new-sale/', new_sale, name='new-sale'),
    path('course-completed/', course_completed, name='course-completed'),
    path('chapter-completed/', chapter_completed, name='chapter-completed'),
    path('quiz-completed/', quiz_completed, name='quiz-completed'),
    path('lesson-completed/', lesson_completed, name='lesson-completed'),
]
