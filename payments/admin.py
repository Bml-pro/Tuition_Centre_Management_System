from django.contrib import admin

from .models import Payment, TuitionSetting


@admin.register(TuitionSetting)
class TuitionSettingAdmin(admin.ModelAdmin):

    list_display = (
        "monthly_fee",
        "effective_from",
        "updated_at",
    )

    ordering = (
        "-effective_from",
        "-id",
    )


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):

    list_display = (
        "student",
        "amount",
        "payment_month",
        "payment_year",
        "payment_date",
        "payment_method",
        "recorded_by",
    )

    list_filter = (
        "payment_month",
        "payment_year",
        "payment_method",
    )

    search_fields = (
        "student__full_name",
        "student__student_id",
    )

    ordering = (
        "-payment_year",
        "-payment_month",
        "-payment_date",
    )