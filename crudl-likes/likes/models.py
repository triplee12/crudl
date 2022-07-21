import uuid
import contextlib
import os
from urllib.parse import urlparse, urlunparse
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.timezone import now as timezone_now
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.exceptions import FieldError
from django.utils import translation
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill
from pilkit.lib import Image


class TranslatedField(object):
    def __init__(self, field_name):
        self.field_name = field_name
    
    def __get__(self, instance, owner):
        lang_code = translation.get_language()
        if lang_code == settings.LANGUAGE_CODE:
            # The fields of the default language are in the manin model
            return getattr(instance, self.field_name)
        else:
            # The fields of the orther languages are in the translation
            # Model, but falls back to the main model
            translations = instance.translations.filter(
                language = lang_code,
            ).first() or instance
            return getattr(translations, self.field_name)


class WatermarkOverlay(object):
    def __init__(self,watermark_image):
        self.watermark_image = watermark_image
    
    def process(self, img):
        original = img.convert('RGBA')
        overlay = Image.open(self.watermark_image)
        img = Image.alpha_composite(original, overlay).convert('RGB')
        return img

class CreationModificationDateBase(models.Model):
    """
    Abstract base class with a creation and modification date and time
    """
    created = models.DateTimeField(_("Creation Date and Time"), auto_now_add=True,)
    modified = models.DateTimeField(_("Modification Date and Time"), auto_now=True)

    class Meta:
        abstract = True


class UrlBase(models.Model):
    """
    A replacement for get_absolute_url()

    Args:
        models (mixix): Models extending this mixin should have either get_url or 
        get_url_path implemented.
    """
    class Meta:
        abstract = True
    
    def get_url(self):
        if hasattr(self.get_url_path, "dont_recurse"):
            raise NotImplementedError
        try:
            path = self.get_url_path()
        except NotImplementedError:
            raise
        return settings.WEBSITE_URL + path
    get_url.dont_recurse = True
    
    def get_url_path(self):
        if hasattr(self.get_url, "dont_recurse"):
            raise NotImplementedError
        try:
            url = self.get_url()
        except NotImplementedError:
            raise
        bits = urlparse(url)
        return urlunparse(("", "") + bits[2:])
    get_url_path.dont_recurse = True
    
    def get_absolute_url(self):
        return self.get_url()


def object_relation_base_factory(prefix=None, prefix_verbose=None, add_related_name=False, limit_content_type_choices_to=None, is_required=False):
    """
    Returns a mixin class for generic foreign keys using
    "Content type - object ID" with dynamic field names.
    This function is just a class generator.

    Parameters:
    prefix: a prefix, which is added in front of the fields

    prefix_verbose: a verbose name of the prefix, used to
                    generate a title for the field column
                    of the content object in the Admin
    
    add_related_name: a boolean value indicating, that a
                    related name for the generated content
                    type foreign key should be added. This
                    value should be true, if you use more than
                    one ObjectRelationBase in your model.

    The model fields are created using this naming scheme:
        <<prefix>>_content_type
        <<prefix>>_object_id
        <<prefix>>_content_object
    """
    p = ""
    if prefix:
        p = f"{prefix}_"
        prefix_verbose = prefix_verbose or _("Related object")
        limit_content_type_choices_to = limit_content_type_choices_to or {}
        content_type_field = f"{p}content_type"
        object_id_field = f"{p}object_id"
        content_object_field = f"{p}content_object"

        class TheClass(models.Model):
            class Meta:
                abstract = True
        
        if add_related_name:
            if not prefix:
                raise FieldError("if add_related_name is set to " "True, a prefix must be given")
            related_name = prefix
        else:
            related_name = None
        
        optional = not is_required
        ct_verbose_name = _(f"{prefix_verbose}'s type (model)")
        content_type = models.ForeignKey(
            ContentType,
            verbose_name=ct_verbose_name,
            related_name=related_name,
            blank=optional,
            null=optional,
            help_text = _("Please select the type (model) " "for the relation, you want to build."),
            limit_choices_to=limit_content_type_choices_to,
            on_delete=models.CASCADE
        )
        fk_verbose_name = prefix_verbose
        
        object_id = models.CharField(
            fk_verbose_name,
            blank=optional,
            null=False,
            help_text=_("Please enter the ID of the related object."),
            max_length=255,
            default=""
        )
        
        content_object = GenericForeignKey(
            ct_field=content_type_field,
            fk_field=object_id_field
        )
        
        TheClass.add_to_class(content_type_field, content_type)
        TheClass.add_to_class(object_id_field, object_id)
        TheClass.add_to_class(content_object_field, content_object)
    
        return TheClass


def upload_to(instance, filename):
    now = timezone_now()
    base, extension = os.path.splitext(filename)
    extension = extension.lower()
    return f"ideas/{now:%Y/%m}/{instance.pk}{extension}"

RATING_CHOICES = (
    (1, "★☆☆☆☆"),
    (2, "★★☆☆☆"),
    (3, "★★★☆☆"),
    (4, "★★★★☆"),
    (5, "★★★★★"),
)


class Idea(CreationModificationDateBase, UrlBase):
    uuid = models.UUIDField(
        primary_key = True, default = uuid.uuid4, editable = False
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name = _("Author"),

        on_delete=models.SET_NULL,
        blank = True,
        null = True,
        related_name = "authored_ideas"
    )
    title = models.CharField(
        _('Title'),
        max_length = 200,
    )
    content = models.TextField(
        _('Content')
    )
    picture = models.ImageField(_("Picture"), upload_to=upload_to)
    watermarked_picture_large = ImageSpecField(
        source="picture", processors=[
            ResizeToFill(800, 400), WatermarkOverlay(
                watermark_image=os.path.join(settings.STATIC_ROOT, 'site', 'img', 'watermark.png'),
            )
        ],
        format="PNG"
    )
    picture_social = ImageSpecField(source="picture", processors=[ResizeToFill(1024, 512)], format="JPEG", options={"quality": 100},)
    picture_large = ImageSpecField(source="picture", processors=[ResizeToFill(800, 400)], format="PNG")
    picture_thumbnail = ImageSpecField(source="picture", processors=[ResizeToFill(728,250)], format="PNG")
    categories = models.ManyToManyField(
        "category.Category",
        verbose_name = _("Categories"),
        related_name="category_ideas",
    )
    rating = models.PositiveIntegerField(
        _("Rating"), choices = RATING_CHOICES, blank=True, null=True
    )
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    # Use translateField if you don't want to keep migrating model every time you change language'
    translated_title = TranslatedField("title")
    translated_content = TranslatedField("content")
    translated_categories = TranslatedField("categories")
    
    class Meta:
        verbose_name = _("Idea")
        verbose_name_plural = _("Ideas")
        constraints = [
            models.UniqueConstraint(
                fields = ["title"],
                condition = ~models.Q(author = None),
                name = "unique_titles_for_each_author"
            ),
            models.CheckConstraint(
                check = models.Q(
                    title__iregex = r"^\S.*\S$"
                    # starts with non-whitespace characters,
                    # ends with non-whitespace characters,
                    # anything in the middle
                ),
                name = "title_has_no_leading_and_trailing_whitespaces",
            )
        ]
    
    def clean(self):
        import re
        if self.author and Idea.objects.exclude(pk=self.pk).filter(
            author = self.author,
            title = self.title,
        ).exists():
            raise ValidationError(
                _("Each idea of the same user should have a unique title.")
            )
        if not re.match(r"^\S.*\S$", self.title):
            raise ValidationError(
                _("The title cannot start or end with a whitespace.")
            )
    
    def __str__(self):
        return self.title
    
    def get_url_path(self):
        return reverse("ideas:idea_detail", kwargs={"pk":self.pk})
    
    def delete(self, *args, **kwargs):
        from django.core.files.storage import default_storage
        if self.picture:
            with contextlib.supress(FileNotFoundError):
                default_storage.delete(
                    self.picture_social.path
                )
                default_storage.delete(
                    self.picture_large.path
                )
                default_storage.delete(
                    self.picture_thumbnail.path
                )
            self.picture.delete()
        super().delete(*args, **kwargs)
    
    @property
    def structured_data(self):
        from django.utils.translation import get_language
        
        lang_code = get_language()
        data = {
            "@type": "CreativeWork",
            "name": self.translated_title,
            "description": self.translated_content,
            "unLanguage": lang_code,
        }
        if self.author:
            data["author"] = {
                "@type": "Person",
                "name": self.author.get_full_name() or self.author.username,
            }
        if self.picture:
            data["image"] = self.picture_social.url
        return data

LikeableObject = object_relation_base_factory(is_required=True)


class Like(CreationModificationDateBase):
    class Meta:
        verbose_name = _('Like')
        verbose_name_plural = _('Likes')
        ordering = ('-created',)
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    def __str__(self):
        return _("{user} likes {obj}").format(user=self.user, obj=self.content_object)
