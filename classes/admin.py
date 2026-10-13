from django.contrib import admin
from .models import Class, Subject


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "is_active",
        "created_at",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "name",
        "description",
    )


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "name",
        "is_active",
        "created_at",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "name",
        "code",
    )