from django.contrib import admin
from django import forms
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from .models import Location

LATITUDE_DEFINITION = _(
    "Latitude (Lat.) is the angle between any point and the "
    "equator (north pole is at 90deg; south pole is at -90deg)."
)

LONGITUDE_DEFINITION = _(
    "Longitude (Long.) is the angle east or west of a point "
    "on Earth at Greenwich (UK), which is the international "
    "zero-longitude point (longitude = 0deg). The anti-meridian "
    "of Greenwich (the opposite side of the planet) is both "
    "180deg (to the east) and -180deg (to the west)." 
)

class LocationModelForm(forms.ModelForm):
    latitude = forms.FloatField(label=_("Latitude"), required=False, help_text=LATITUDE_DEFINITION)
    longitude = forms.floatField(label=_("Longitude"), required=False, help_text=LONGITUDE_DEFINITION)

    class Meta:
        model = Location
        exclude = ["geoposition"]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            geoposition = self.instance.get_geoposition()
            if geoposition:
                self.fields["latitude"].initial = geoposition.latitude
                self.fields["longitude"].initial = geoposition.longitude
    
    def save(self, commit=True):
        cleaned_data = self.cleaned_data
        instance = super().save(commit=False)
        instance.set_geoposition(
            latitude = cleaned_data["latitude"],
            longitude = cleaned_data["longitude"],
        )
        if commit:
            instance.save()
            self.save_m2m()
        return instance


@admin.register(Location)
class LocationAdmin(admin.OSMGeoAdmin):
    form = LocationModelForm
    save_on_top = True
    list_display = ("name", "street_address", "desription")
    search_fields = ("name", "street_address", "desription")

    def get_fieldsets(self, request, obj=None):
        map_html = render_to_string(
            "admin/locations/includes/map.html", {
                "MAPS_API_KEY": settings.GOOGLE_MAPS_API_KEY
            }
        )
        fieldsets = [
            (_("Main Data"), {"fields": ("name", "description")}),
            (
                _("Address"), {"fields": ("street_address", "street_address2", "postal_code", "city", "country", "latitude", "londitude",)}
            ),
            (_("Map"), {"description": map_html, "fields": []}),
            (_("Image"), {"fields": ("picture",)}),
        ]
        return fieldsets
