from django import forms
from django.db.models import Sum
from django.utils import timezone

from .models import Payment, TuitionSetting


class PaymentForm(forms.ModelForm):

    class Meta:
        model = Payment

        fields = [
            "student",
            "amount",
            "payment_month",
            "payment_year",
            "payment_date",
            "payment_method",
        ]

        widgets = {
            "payment_date": forms.DateInput(
                attrs={
                    "type": "date"
                }
            ),

            "payment_year": forms.NumberInput(
                attrs={
                    "min": 2020,
                    "max": 2100
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        today = timezone.localdate()

        # Default to the current month/year
        if not self.initial.get("payment_month"):
            self.initial["payment_month"] = today.month

        if not self.initial.get("payment_year"):
            self.initial["payment_year"] = today.year

        if not self.initial.get("payment_date"):
            self.initial["payment_date"] = today

    def clean(self):

        cleaned_data = super().clean()

        student = cleaned_data.get("student")
        amount = cleaned_data.get("amount")
        month = cleaned_data.get("payment_month")
        year = cleaned_data.get("payment_year")

        if not student or not amount or not month or not year:
            return cleaned_data

        if amount <= 0:
            raise forms.ValidationError(
                "Payment amount must be greater than zero."
            )

        # Get current tuition setting
        tuition_setting = (
            TuitionSetting.objects
            .order_by("-effective_from", "-id")
            .first()
        )

        if not tuition_setting:
            raise forms.ValidationError(
                "Monthly tuition fee has not been configured yet."
            )

        monthly_fee = tuition_setting.monthly_fee

        # Calculate payments already made for this student/month
        existing_paid = (
            Payment.objects
            .filter(
                student=student,
                payment_month=month,
                payment_year=year,
            )
            .exclude(pk=self.instance.pk)
            .aggregate(
               total=Sum("amount")
            )["total"] or 0
        )

        remaining_balance = monthly_fee - existing_paid

        if remaining_balance <= 0:
            raise forms.ValidationError(
                "This student's tuition for this month "
                "has already been fully paid."
            )

        if amount > remaining_balance:
            raise forms.ValidationError(
                f"Maximum payment allowed for this month is "
                f"TSh {remaining_balance:,.2f}."
            )

        return cleaned_data