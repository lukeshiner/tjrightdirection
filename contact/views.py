"""Views for the contact app."""

import logging

from django.shortcuts import redirect, render

from .forms import ContactForm

logger = logging.getLogger(__name__)


def contact(request):
    """View for the contact page."""
    form = ContactForm()
    if request.method == "POST":
        form = ContactForm(data=request.POST)
        if form.is_valid():
            try:
                form.send_mail()
            except Exception as e:
                logger.exception(e)
                return redirect("contact:failure")
            form = ContactForm()
            return redirect("contact:success")
    return render(request, "contact/contact.html", {"form": form})


def success(request):
    """View for successful messages."""
    form = ContactForm()
    return render(request, "contact/success.html", {"form": form})


def failure(request):
    """View for failed messages."""
    form = ContactForm()
    return render(request, "contact/failure.html", {"form": form})
