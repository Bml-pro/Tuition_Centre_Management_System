from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):

    list_display = (
        "student_id",
        "full_name",
        "student_class",
        "gender",
        "parent_phone",
        "payment_status_display",
        "balance_display",
        "status",
        "registration_date",
    )

    list_filter = (
        "status",
        "gender",
        "student_class",
        "registration_date",
    )

    search_fields = (
        "student_id",
        "full_name",
        "parent_guardian_name",
        "parent_phone",
    )

    readonly_fields = (
        "student_id",
        "registration_date",
        "created_at",
        "updated_at",
    )

    ordering = (
        "-registration_date",
    )

    @admin.display(
        description="Payment Status"
    )
    def payment_status_display(self, obj):
        return obj.payment_status

    @admin.display(
    description="Balance"
)
    def balance_display(self, obj):
     if obj.balance is None:
        return "Not Set"

     return f"TSh {obj.balance:,.2f}"