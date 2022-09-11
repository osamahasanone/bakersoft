from django.db import models


class BaseModel(models.Model):
    class Meta:
        abstract = True
        ordering = (
            "-created_at",
            "-updated_at",
        )

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
