import django.contrib
import django.contrib.auth
import django.contrib.auth.admin
from django import forms
from django.contrib import admin
from django.contrib.auth.forms import UserChangeForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import CalendarUser


class CalendarAdminUserCreationForm(forms.ModelForm):

    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
    password2 = forms.CharField(
        label=_("Password confirmation"), widget=forms.PasswordInput
    )

    class Meta:
        model = CalendarUser
        fields = ["first_name", "full_name", "password", "profile_picture"]

    def clean_password2(self):
        """Check that the two password entries match"""
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CalendarAdminUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm.Meta):
        model = CalendarUser
        fields = ["first_name", "full_name", "password", "profile_picture"]


class CalendarUserAdmin(admin.ModelAdmin):

    # list_display = ["first_name", "full_name", "profile_picture"]
    # list_filter = ["is_superuser"]
    fieldsets = [
        ("Usuário", {"fields": ["profile_picture", "first_name"]}),
        (None, {"fields": ["full_name"]}),
    ]
    # add_fieldsets = [
    #    ("Usuário", {"fields": ["profile_picture", "first_name"]}),
    #    (None, {"fields": ["full_name"]}),
    # ]

    # search_fields = ["first_name", "full_name"]
    # ordering = ["full_name"]

    # form = CalendarAdminUserChangeForm
    # add_form = CalendarAdminUserCreationForm


admin.site.register(CalendarUser, CalendarUserAdmin)
