from django.db import models


class EzyCourseAuth(models.Model):
    email = models.EmailField(max_length=255, unique=True, default=None)
    site = models.CharField(max_length=255)
    session_cookie = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.site} - {self.email}"

    class Meta:
        verbose_name = "EzyCourse Auth"
        verbose_name_plural = "EzyCourse Auth"
        db_table = "ezycourse_auth"
