from django import forms
from .models import Student


class StudentForm(forms.ModelForm):

    class Meta:
        model = Student

        fields = [
            "full_name",
            "gender",
            "date_of_birth",
            "parent_guardian_name",
            "parent_phone",
            "student_class",
            "status",
        ]

        widgets = {
            "full_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter student's full name",
                }
            ),

            "gender": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "date_of_birth": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "parent_guardian_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter parent/guardian name",
                }
            ),

            "parent_phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter parent phone number",
                }
            ),

            "student_class": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "tuition_fee": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Optional",
                    "min": "0",
                    "step": "0.01",
                }
            ),

            "status": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
        }

        labels = {
            "full_name": "Full Name",
            "gender": "Gender",
            "date_of_birth": "Date of Birth",
            "parent_guardian_name": "Parent / Guardian Name",
            "parent_phone": "Parent Phone Number",
            "student_class": "Class",
            "status": "Status",
        }

        