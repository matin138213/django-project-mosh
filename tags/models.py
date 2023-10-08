from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models

# Create your models here.


from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class TagItemManager(models.Manager):
    def get_tags_for(self, obj_type, obj_id):
        content_type = ContentType.objects.get_for_model(obj_type)
        queryset = TagItem.objects.select_related('tag').filter(
            content_type=content_type,
            object_id=obj_id
        )


class Tag(models.Model):
    label = models.CharField(max_length=255)

    def __str__(self):
        return self.label


class TagItem(models.Model):
    objects = TagItemManager()
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')  # Specify the related_query_name

    def __str__(self):
        return f"{self.tag.label} - {self.content_object}"  # Optional, for better representation
