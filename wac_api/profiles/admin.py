from django.contrib import admin

from profiles.models import Profile


@admin.register(Profile)
class UserAdmin(admin.ModelAdmin):
    """User admin."""

    list_display = ('pk', 'email', 'first_name',)
    list_display_links = ('pk', 'email',)

    search_fields = (
        'email',
        'first_name',
        'last_name',
    )

    list_filter = (
        'is_active',
        'is_staff',
        'date_joined',
        'modified',
    )

    readonly_fields = ('date_joined', 'modified',)

    def save_model(self, request, obj, form, change):
        if obj.pk:
            orig_obj = Profile.objects.get(pk=obj.pk)
            if obj.password != orig_obj.password:
                obj.set_password(obj.password)
        else:
            obj.set_password(obj.password)
        obj.save()