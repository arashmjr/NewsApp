import hashlib
import uuid

import magic
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from src.apps.storage.models.media_type import MediaType


class MediaModel(models.Model):
    def file_path(instance, filename):
        file_name = filename.split(".")[-1]
        return "{}/{}.{}".format(
            instance.mime_type, str(uuid.uuid4()), file_name
        )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(upload_to=file_path, verbose_name=_("file"))
    mime_type = models.ForeignKey(
        "storage.MediaType",
        on_delete=models.SET_NULL,
        verbose_name=_("mime type"),
        null=True,
        blank=True,
    )
    alt = models.CharField(max_length=50, verbose_name=_("alt description"))
    checksum = models.CharField(
        max_length=40, verbose_name=_("checksum"), blank=True
    )
    created_at = models.DateField(
        auto_now_add=True, verbose_name=_("created at")
    )
    updated_at = models.DateField(auto_now=True, verbose_name=_("updated at"))


@receiver(pre_save, sender=MediaModel)
def create_media_type(sender, instance, **kwargs):
    mim = magic.from_buffer(instance.file.read(), mime=True)
    media_type_object, _ = MediaType.objects.get_or_create(media_type=mim)
    instance.mime_type = media_type_object


@receiver(pre_save, sender=MediaModel)
def create_checksum(sender, instance, **kwargs):
    sha1_hash = hashlib.sha1()
    content = instance.file.read()
    sha1_hash.update(content)
    digest = sha1_hash.hexdigest()
    instance.checksum = digest
