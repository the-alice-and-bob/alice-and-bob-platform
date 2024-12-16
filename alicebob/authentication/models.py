from enum import Enum

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class UserRoles:
    USER = "user"
    RRSS = "rrss"
    MANAGER = "manager"
    PLATFORM_ADMIN = "platform_admin"


class AliceBobUser(AbstractUser):
    roles = models.JSONField(default=list, db_default=[UserRoles.USER], db_index=True)

    engagement_score = models.IntegerField(default=0)
    recency_score = models.IntegerField(default=0)
    interaction_score = models.IntegerField(default=0)
    loyalty_score = models.IntegerField(default=0)

    # Nuevas métricas
    email_open_rate = models.FloatField(default=0.0)  # Porcentaje de apertura
    email_click_rate = models.FloatField(default=0.0)  # Porcentaje de clics
    community_activity_score = models.IntegerField(default=0)  # Puntaje de actividad

    @property
    def total_score(self):
        """Suma ponderada de los scores individuales."""
        return (
                self.engagement_score * 0.3 +
                self.recency_score * 0.2 +
                self.interaction_score * 0.2 +
                self.loyalty_score * 0.1 +
                self.community_activity_score * 0.1 +
                (self.email_open_rate + self.email_click_rate) * 0.1
        )
