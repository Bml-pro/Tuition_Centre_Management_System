from django.db import models
from django.contrib.auth.models import User

from students.models import Student


class TuitionSetting(models.Model):

    monthly_fee = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    effective_from = models.DateField()

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = "Tuition Setting"
        verbose_name_plural = "Tuition Settings"

    def __str__(self):
        return (
            f"TSh {self.monthly_fee:,.2f} "
            f"from {self.effective_from}"
        )


class Payment(models.Model):

    PAYMENT_METHOD_CHOICES = [
        ("CASH", "Cash"),
    ]

    MONTH_CHOICES = [
        (1, "January"),
        (2, "February"),
        (3, "March"),
        (4, "April"),
        (5, "May"),
        (6, "June"),
        (7, "July"),
        (8, "August"),
        (9, "September"),
        (10, "October"),
        (11, "November"),
        (12, "December"),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.PROTECT,
        related_name="payments"
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    payment_month = models.PositiveSmallIntegerField(
    choices=MONTH_CHOICES
 )

    payment_year = models.PositiveIntegerField()

    payment_date = models.DateField()

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default="CASH"
    )

    recorded_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="recorded_payments"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = [
            "-payment_year",
            "-payment_month",
            "-payment_date",
            "-created_at",
        ]

    def __str__(self):
        return (
            f"{self.student.student_id} - "
            f"{self.get_payment_month_display()} "
            f"{self.payment_year} - "
            f"TSh {self.amount:,.2f}"
        )