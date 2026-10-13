from decimal import Decimal

from django.db.models import Sum

from .models import Payment, TuitionSetting


def get_monthly_tuition():

    setting = (
        TuitionSetting.objects
        .order_by("-effective_from", "-id")
        .first()
    )

    if not setting:
        return Decimal("0.00")

    return setting.monthly_fee


def get_student_monthly_payment(
    student,
    month,
    year
):

    monthly_fee = get_monthly_tuition()

    total_paid = (
        Payment.objects
        .filter(
            student=student,
            payment_month=month,
            payment_year=year,
        )
        .aggregate(
            total=Sum("amount")
        )["total"]
        or Decimal("0.00")
    )

    balance = max(
        monthly_fee - total_paid,
        Decimal("0.00")
    )

    if monthly_fee <= 0:
        status = "FEE NOT SET"

    elif total_paid >= monthly_fee:
        status = "PAID"

    elif total_paid > 0:
        status = "PARTIALLY PAID"

    else:
        status = "UNPAID"

    return {
        "monthly_fee": monthly_fee,
        "total_paid": total_paid,
        "balance": balance,
        "status": status,
    }