from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import StudentForm
from .models import Student
from payments.models import TuitionSetting


@login_required
def student_list(request):

    query = request.GET.get("q", "").strip()

    students = Student.objects.select_related(
        "student_class"
    ).all()

    if query:
        students = students.filter(
            Q(student_id__icontains=query)
            | Q(full_name__icontains=query)
            | Q(parent_guardian_name__icontains=query)
            | Q(parent_phone__icontains=query)
        )

    context = {
        "students": students,
        "query": query,
    }

    return render(
        request,
        "students/student_list.html",
        context
    )


@login_required
def student_create(request):

    if request.method == "POST":
        form = StudentForm(request.POST)

        if form.is_valid():
            student = form.save()

            messages.success(
                request,
                f"Student {student.student_id} registered successfully."
            )

            return redirect(
                "student_detail",
                pk=student.pk
            )

    else:
        form = StudentForm()

    return render(
        request,
        "students/student_form.html",
        {
            "form": form,
            "page_title": "Register Student",
        }
    )


@login_required
def student_detail(request, pk):

    student = get_object_or_404(
        Student.objects.select_related("student_class"),
        pk=pk
    )

    payments = student.payments.select_related(
        "recorded_by"
    ).all()

    context = {
        "student": student,
        "payments": payments,
    }

    return render(
        request,
        "students/student_detail.html",
        context
    )


@login_required
def student_update(request, pk):

    student = get_object_or_404(
        Student,
        pk=pk
    )

    if request.method == "POST":
        form = StudentForm(
            request.POST,
            instance=student
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Student information updated successfully."
            )

            return redirect(
                "student_detail",
                pk=student.pk
            )

    else:
        form = StudentForm(
            instance=student
        )

    return render(
        request,
        "students/student_form.html",
        {
            "form": form,
            "student": student,
            "page_title": "Edit Student",
        }
    )