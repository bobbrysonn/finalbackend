""" Custom email templates for djoser. """

from djoser import email


class CustomActivationEmail(email.ActivationEmail):
    """Custom activation email template."""

    template_name = "djoser/email/activation.html"
