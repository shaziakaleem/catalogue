from django.db import models
from django.utils.timezone import now
import uuid
from users.models import User

from mongoengine import (
    BooleanField,
    DateTimeField,
    Document,
    EmbeddedDocument,
    EmbeddedDocumentField,
    ListField,
    ObjectIdField,
    ReferenceField,
    StringField,
)


# Create your models here.
class Category(Document):
    _id = ObjectIdField(required=True, default=lambda: ObjectId())
    category_name = StringField(max_length=256, blank=True, null=True)
    date_created = DateTimeField(default=now)
    date_updated = DateTimeField(auto_now=True)
    date_deleted = DateTimeField(default=None, null=True, blank=True)
    created_by = StringField(required=True)
    updated_by = StringField()


class Product(Document):
    _id = ObjectIdField(required=True, default=lambda: ObjectId())
    product_name = StringField(max_length=256, blank=True, null=True)
    tags = ListField()
    features = ListField()
    price = StringField(max_length=256, blank=True, null=True)
    MRP = StringField(max_length=256, blank=True, null=True)
    currency = StringField(max_length=256, blank=True, null=True)
    isactive = BooleanField(default=True)
    date_created = DateTimeField(default=now)
    date_updated = DateTimeField(auto_now=True)
    date_deleted = DateTimeField(default=None, null=True, blank=True)
    created_by = StringField(required=True)
    updated_by = StringField()


class ProductCategory(Document):
    product = ReferenceField("Product", required=True)
    category =ReferenceField("Category", required=True)
    date_created = DateTimeField(default=now)
    date_updated = DateTimeField(auto_now=True)
    date_deleted = DateTimeField(default=None, null=True, blank=True)
    created_by = StringField(required=True)
    updated_by = StringField()

class Currency(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=255)
    date_deleted = models.DateTimeField(default=None, null=True, blank=True)
    date_created = models.DateTimeField(default=now)
    date_updated = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        to_field="id",
        related_name="%(class)s_created_by",
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        to_field="id",
        default=None,
        null=True,
        blank=True,
        related_name="%(class)s_updated_by",
    )

