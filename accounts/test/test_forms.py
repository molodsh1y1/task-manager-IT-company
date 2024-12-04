from django.test import TestCase
from accounts.forms import RegisterForm
from accounts.models import Worker, Position


class RegisterFormTests(TestCase):
    def setUp(self):
        self.valid_data = {
            "first_name": "John",
            "last_name": "Doe",
            "username": "johndoe",
            "email": "johndoe@example.com",
            "password1": "SecurePassword123",
            "password2": "SecurePassword123",
        }

    def test_form_with_valid_data(self):
        form = RegisterForm(data=self.valid_data)
        self.assertTrue(
            form.is_valid(),
            "The form should be valid with correct data."
        )
        self.assertEqual(
            form.cleaned_data["first_name"],
            "John"
        )
        self.assertEqual(
            form.cleaned_data["last_name"],
            "Doe"
        )
        self.assertEqual(
            form.cleaned_data["email"],
            "johndoe@example.com"
        )

    def test_form_with_invalid_email(self):
        invalid_data = self.valid_data.copy()
        invalid_data["email"] = "invalid-email"
        form = RegisterForm(data=invalid_data)
        self.assertFalse(
            form.is_valid(),
            "The form should be invalid with an invalid email."
        )
        self.assertIn(
            "Enter a valid email address.",
            form.errors["email"],
            "The form should have an error for an invalid email."
        )

    def test_form_missing_required_fields(self):
        invalid_data = self.valid_data.copy()
        invalid_data.pop("first_name")
        form = RegisterForm(data=invalid_data)
        self.assertFalse(
            form.is_valid(),
            "The form should be invalid if required fields are missing."
        )
        self.assertIn(
            "first_name", form.errors,
            "The error should mention the missing 'first_name' field."
        )
