import uuid
from django.db import models
from django.urls import reverse
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from crudl.apps.core.model_fields import TranslatedField
from crudl.apps.core.models import (
    object_relation_base_factory as generic_relation,
    CreationModificationDateBase, UrlBase
)
# from crudl.apps.core.model_fields import (
#     MultilingualTextField,
#     MultilingualCharField,
#     TranslatedField
# )

RATING_CHOICES = (
    (1, "★☆☆☆☆"),
    (2, "★★☆☆☆"),
    (3, "★★★☆☆"),
    (4, "★★★★☆"),
    (5, "★★★★★"),
)


class Idea(models.Model):
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
    categories = models.ManyToManyField(
        "category.Category",
        verbose_name = _("Categories"),
        related_name="category_ideas",
    )
    rating = models.PositiveIntegerField(
        _("Rating"), choices = RATING_CHOICES, blank=True, null=True
    )
    # Use translateField if you don't want to keep migrating model every time you change language'
    translated_title = TranslatedField("title")
    translated_content = TranslatedField("content")
    
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