import uuid

from asgiref.sync import sync_to_async
from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(db_index=True)
    updated_at = models.DateTimeField(db_index=True)

    class Meta:
        abstract = True
        get_latest_by = "created_at"
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.__class__.__name__.lower()}:{str(self.uuid)[:6]}"

    def save(self, *args, **kwargs):
        force_updated_at = kwargs.pop("force_updated_at", False)
        force_created_at = kwargs.pop("force_created_at", False)
        now = timezone.now()
        if (not force_created_at or not self.created_at) and self._state.adding:
            self.created_at = now
        if not (force_updated_at and self.updated_at):
            self.updated_at = now
        return super().save(*args, **kwargs)

    @sync_to_async
    def asave(self, *args, **kwargs):
        return self.save(*args, **kwargs)

    @sync_to_async
    def arefresh_from_db(self, *args, **kwargs):
        return self.refresh_from_db(*args, **kwargs)

    @sync_to_async
    def adelete(self, *args, **kwargs):
        return self.delete(*args, **kwargs)
