from django.db import models
from classes.models import Class


class Student(models.Model):

    STATUS_CHOICES = [
        ("ACTIVE", "Active"),
        ("INACTIVE", "Inactive"),
    ]

    GENDER_CHOICES = [
        ("MALE", "Male"),
        ("FEMALE", "Female"),
        ("OTHER", "Other"),
    ]

    student_id = models.CharField(
        max_length=20,
        unique=True,
        editable=False
    )

    full_name = models.CharField(
        max_length=200
    )

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True
    )

    parent_guardian_name = models.CharField(
        max_length=200
    )

    parent_phone = models.CharField(
        max_length=30
    )

    student_class = models.ForeignKey(
        Class,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="students"
    )

    registration_date = models.DateField(
        auto_now_add=True
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="ACTIVE"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-registration_date", "full_name"]

    def save(self, *args, **kwargs):

        if not self.student_id:

            last_student = Student.objects.order_by("-id").first()

            if last_student:
                number = last_student.id + 1
            else:
                number = 1

            self.student_id = f"STU-{number:05d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student_id} - {self.full_name}"