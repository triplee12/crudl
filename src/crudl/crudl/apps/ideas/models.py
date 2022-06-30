import uuid
import contextlib
import os
from django.db import models
from django.urls import reverse
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.timezone import now as timezone_now
from django.utils.translation import gettext_lazy as _
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill
from crudl.apps.core.model_fields import TranslatedField
from crudl.apps.core.models import (
    object_relation_base_factory as generic_relation,
    CreationModificationDateBase, UrlBase
)
from crudl.apps.core.processors import WatermarkOverlay
# from crudl.apps.core.model_fields import (
#     MultilingualTextField,
#     MultilingualCharField,
#     TranslatedField
# )

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

FavoriteObjectBase = generic_relation(
    is_required = True,
)

OwnerBase = generic_relation(
    prefix="owner",
    prefix_verbose = _("Owner"),
    is_required = True,
    add_related_name = True,
    limit_content_type_choices_to = {
        "model__in": ("user", "group",)
    }
)

class Like(OwnerBase):
    class Meta:
        verbose_name = _("Like")
        verbose_name_plural = _("Likes")
    
    def __str__(self):
        return _("{owner} likes {object}").format(
            owner=self.owner_content_object,
            object=self.content_object
        )


class IdeaTranslations(models.Model):
    idea = models.ForeignKey(
        Idea,
        verbose_name = _("Idea"),
        on_delete = models.CASCADE,
        related_name = "translations",
    )
    language = models.CharField(_("Language"), max_length=7)
    title = models.CharField(_("Title"), max_length=200,)
    content = models.TextField(_("Content"))
    
    class Meta:
        verbose_name = _("Idea Translations")
        verbose_name_plural = _("Idea Translations")
        ordering = ["language"]
        unique_together = [["idea", "language"]]
    
    def __str__(self):
        return self.title