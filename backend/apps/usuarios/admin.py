from django.contrib import admin
from django import forms
from .models import Perfil, Plan, PROFILE_FIELD_CHOICES


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ("usuario", "es_prestador", "plan", "onboarding_completed")
    list_filter = ("es_prestador", "plan", "onboarding_completed")
    search_fields = ("usuario__username", "usuario__email", "ciudad", "provincia")


class PlanAdminForm(forms.ModelForm):
    fields_enabled = forms.MultipleChoiceField(
        choices=[(f, f) for f in PROFILE_FIELD_CHOICES],
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Plan
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        initial = self.instance.fields_enabled if self.instance and isinstance(self.instance.fields_enabled, list) else []
        self.fields['fields_enabled'].initial = initial

    def clean_fields_enabled(self):
        data = self.cleaned_data.get('fields_enabled') or []
        return list(data)


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    form = PlanAdminForm
    list_display = ("code", "name", "price_text", "precio_mensual", "max_images", "max_videos", "is_active", "order")
    list_filter = ("is_active",)
    search_fields = ("code", "name")
    ordering = ("order", "id")
    list_editable = ("precio_mensual", "max_images", "max_videos", "is_active", "order")


