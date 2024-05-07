from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from . import models
from django.shortcuts import get_object_or_404


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password_confirmation = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = models.User
        fields = "__all__"

    def clean_password_confirmation(self):
        # Check that the two password entries match
        password = self.cleaned_data.get("password")
        password_confirmation = self.cleaned_data.get("password_confirmation")
        if password and password_confirmation and password != password_confirmation:
            raise forms.ValidationError("Passwords don't match")
        return password_confirmation

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = models.User
        fields = "__all__"

    def clean_national_code(self):
        return self.cleaned_data["username"]

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class IsSupportTeamMember(admin.SimpleListFilter):
    """
    filter on users who are support team member or not. support team members have permission to edit schools some specs like `members_count_paid_plan` or `max_record_size` ... .also to do so they should be granted as admin user by superuser.
    """

    title = "is a support team member"
    parameter_name = "supp_mem"

    def lookups(self, request, ModelAdmin):
        return ((True, "is a support team member"),)

    def queryset(self, request, queryset):
        if self.value() == "True":
            supp_grp = get_object_or_404(Group, name="support_team")
            queryset = supp_grp.user_set.all()
        return queryset


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = (
        "id",
        "username",
        "is_admin",
        "is_superuser",
        "cellphone",
        "fullname",
        "email",
    )
    list_filter = ("is_superuser",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "username",
                    "password",
                    "id",
                    "cellphone",
                    "fullname",
                    "email",
                )
            },
        ),
        (
            "Personal info",
            {
                "fields": (
                    "created",
                    "modified",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_admin",
                    "is_superuser",
                    "is_deleted",
                    "is_active",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. BaseUserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "password",
                    "password_confirmation",
                    "user_permissions",
                    "groups",
                    "created",
                    "modified",
                    "cellphone",
                    "email",
                ),
            },
        ),
    )
    search_fields = ("username", "cellphone", "email")
    ordering = ("username",)
    filter_horizontal = ("user_permissions", "groups")
    readonly_fields = ["id"]
    list_filter = ["is_superuser", "is_admin", "is_deleted", IsSupportTeamMember]

    def get_form(self, request, obj=None, **kwargs):
        # aim of this method overridation. these fields has null=True. we dont want to rest apis fill these with empty strings also allow admin site to ingnore their requiered. so we cant use blank=True in model layer and i have used this hack.
        form = super().get_form(request, obj, **kwargs)
        if request.user.is_admin and not request.user.is_superuser:
            for field_name, field in form.base_fields.items():
                if field_name in ["username", "cellphone", "fullname", "email"]:
                    continue
                field.disabled = True
        for field in ["cellphone", "email"]:
            form_field = form.base_fields.get(field)
            if form_field:
                # if a user has change perm to this model,he enters this block
                form_field.required = False
        return form


# Now register the new UserAdmin...
admin.site.register(models.User, UserAdmin)
