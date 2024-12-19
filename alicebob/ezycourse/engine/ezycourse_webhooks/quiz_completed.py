# import logging
#
# from django.db.transaction import atomic
#
# from academy.models import Student,
#
# from .models import QuizCompleted
# from .helpers import get_or_create_student
#
# db_logger = logging.getLogger("db")
#
#
# def ezycourse_quiz_completed(data: dict):
#     """
#     This webhook is triggered when a user completes a quiz.
#     Stores the quiz attempt in the database and updates student progress.
#     """
#     try:
#         obj = QuizCompleted.from_json(data)
#     except Exception as e:
#         db_logger.error(f"Invalid data while processing quiz completion: {e}")
#         raise ValueError(f"Invalid data: {e}")
#
#     with atomic():
#         try:
#             # Get or create student
#             student = get_or_create_student(obj)
#
#             # Get lesson containing the quiz
#             try:
#                 lesson = Lesson.objects.get(ezy_id=obj.lesson_id)
#             except Lesson.DoesNotExist:
#                 db_logger.error(f"Lesson {obj.lesson_id} not found while processing quiz completion")
#                 raise ValueError(f"Lesson {obj.lesson_id} not found")
#
#             # Record quiz attempt
#             QuizAttempt.objects.create(
#                 student=student,
#                 lesson=lesson,
#                 total_questions=obj.how_many_qu,
#                 correct_answers=obj.correct_answer,
#                 wrong_answers=obj.wrong_answer,
#                 total_marks=obj.total_mark,
#                 completion_date=obj.date
#             )
#
#             db_logger.info(f"Recorded quiz completion for student {student.name} in lesson {lesson.name}")
#
#         except Exception as e:
#             db_logger.error(f"Error processing quiz completion: {e}")
#             raise
#
#
# __all__ = ("ezycourse_quiz_completed",)
