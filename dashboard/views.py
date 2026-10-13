from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render
from django.utils import timezone

from classes.models import Class
from payments.models import Payment
from students.models import Student


@login_required
def dashboard_home(request):

    today = timezone.localdate()

    # --------------------------------------------------
    # STUDENTS
    # --------------------------------------------------

    total_students = Student.objects.count()

    active_students = Student.objects.filter(
        status="ACTIVE"
    ).count()

    inactive_students = Student.objects.filter(
        status="INACTIVE"
    ).count()

    # --------------------------------------------------
    # CLASSES
    # --------------------------------------------------

    total_classes = Class.objects.filter(
        is_active=True
    ).count()

    # --------------------------------------------------
    # PAYMENTS THIS MONTH
    # --------------------------------------------------
    # Payment month/year represent the tuition period.
    # This is different from payment_date, which represents
    # the date the payment was actually recorded.

    monthly_payments = Payment.objects.filter(
        payment_year=today.year,
        payment_month=today.month
    ).aggregate(
        total=Sum("amount")
    )["total"] or Decimal("0.00")

    # --------------------------------------------------
    # TOTAL OUTSTANDING
    # --------------------------------------------------
    #
    # We will calculate this from TuitionSetting and
    # student payment records once the tuition setting
    # structure is finalized.
    #
    # For now, keep it at zero rather than calculating
    # from the old Student.tuition_fee field.

    outstanding_payments = Decimal("0.00")

    # --------------------------------------------------
    # RECENT REGISTRATIONS
    # --------------------------------------------------

    recent_students = (
        Student.objects
        .select_related("student_class")
        .order_by(
            "-registration_date",
            "-id"
        )[:5]
    )

    # --------------------------------------------------
    # RECENT PAYMENTS
    # --------------------------------------------------

    recent_payments = (
        Payment.objects
        .select_related(
            "student",
            "recorded_by"
        )
        .order_by(
            "-payment_date",
            "-created_at"
        )[:5]
    )

    # --------------------------------------------------
    # CONTEXT
    # --------------------------------------------------

    context = {
        "today": today,

        "total_students": total_students,
        "active_students": active_students,
        "inactive_students": inactive_students,

        "total_classes": total_classes,

        "monthly_payments": monthly_payments,
        "outstanding_payments": outstanding_payments,

        "recent_students": recent_students,
        "recent_payments": recent_payments,
    }

    return render(
        request,
        "dashboard/home.html",
        context
    )