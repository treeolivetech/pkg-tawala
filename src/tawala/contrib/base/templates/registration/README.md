# Registration Templates

This directory contains the HTML templates expected by `django.contrib.auth` views.

## Template Files

| Template File                  | View                        | Description                                        |
| ------------------------------ | --------------------------- | -------------------------------------------------- |
| `login.html`                   | `LoginView`                 | User login page                                    |
| `logged_out.html`              | `LogoutView`                | Page shown after logout                            |
| `password_change_form.html`    | `PasswordChangeView`        | Form to change password (authenticated users)      |
| `password_change_done.html`    | `PasswordChangeDoneView`    | Confirmation after password change                 |
| `password_reset_form.html`     | `PasswordResetView`         | Form to request a password reset email             |
| `password_reset_done.html`     | `PasswordResetDoneView`     | Confirmation that reset email was sent             |
| `password_reset_confirm.html`  | `PasswordResetConfirmView`  | Form to enter a new password via reset link        |
| `password_reset_complete.html` | `PasswordResetCompleteView` | Confirmation after password has been reset         |
| `password_reset_email.html`    | —                           | Email body sent during password reset (not a page) |
| `password_reset_subject.txt`   | —                           | Email subject line for password reset (`.txt`)     |

## URL Configuration

To use these templates, include the auth URLs in your project's `urls.py`:

```python
from django.urls import path, include

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
]
```

This will register all auth views under `/accounts/` (e.g., `/accounts/login/`, `/accounts/logout/`, etc.).
