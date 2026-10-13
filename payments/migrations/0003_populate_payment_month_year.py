from django.db import migrations


def populate_payment_periods(apps, schema_editor):
    Payment = apps.get_model("payments", "Payment")

    for payment in Payment.objects.filter(
        payment_month__isnull=True
    ):
        payment.payment_month = payment.payment_date.month
        payment.payment_year = payment.payment_date.year

        payment.save(
            update_fields=[
                "payment_month",
                "payment_year",
            ]
        )


class Migration(migrations.Migration):

    dependencies = [
        (
            "payments",
            "0002_tuitionsetting_alter_payment_options_and_more",
        ),
    ]

    operations = [
        migrations.RunPython(
            populate_payment_periods,
            migrations.RunPython.noop,
        ),
    ]