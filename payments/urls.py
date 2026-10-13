
from django.urls import path

from . import views


urlpatterns = [
    path(
        "",
        views.payment_list,
        name="payment_list",
    ),
    path(
        "record/",
        views.payment_create,
        name="payment_create",
    ),
    path(
        "monthly-report/",
        views.monthly_payment_report,
        name="monthly_payment_report",
    ),
    path(
        "monthly-report/export/excel/",
        views.export_monthly_report_excel,
        name="export_monthly_report_excel",
    ),
    path(
        "monthly-report/export/pdf/",
        views.export_monthly_report_pdf,
        name="export_monthly_report_pdf",
    ),
    path(
        "<int:pk>/",
        views.payment_detail,
        name="payment_detail",
    ),
]
