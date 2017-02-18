from django import forms
from django.core.mail import EmailMessage
from tjrightdirection import settings
import re


NO_EMAIL_ADDRESS_MESSAGE = "Please supply a return email address"
INVALID_EMAIL_ADDRESS_MESSAGE = "Please provide a valid email address"
NO_NAME_MESSAGE = "Please enter your name"
NO_SUBJECT_MESSAGE = "Please provide a subject for your message"
INVALID_PHONE_MESSAGE = "Please provide a valid phone number or leave blank"
NO_CONTENT_MESSAGE = "Please provide a message"


class ContactForm(forms.Form):
    return_email = forms.EmailField(
        required=True, error_messages={
            'required': NO_EMAIL_ADDRESS_MESSAGE,
            'invalid': INVALID_EMAIL_ADDRESS_MESSAGE},
        widget=forms.fields.EmailInput(
            attrs={
                'placeholder': 'Your email address',
                'class': 'contact_form_input'}))

    contact_name = forms.CharField(
        required=True, error_messages={'required': NO_NAME_MESSAGE},
        widget=forms.fields.TextInput(attrs={
            'placeholder': 'Your name',
            'class': 'contact_form_input'}))

    message_subject = forms.CharField(
        required=True, error_messages={'required': NO_SUBJECT_MESSAGE},
        widget=forms.fields.TextInput(attrs={
            'placeholder': 'Message subject',
            'class': 'contact_form_input'}))

    contact_phone = forms.CharField(
        required=False, widget=forms.fields.TextInput(attrs={
            'placeholder': 'Your phone number (optional)',
            'class': 'contact_form_input'}))

    message_content = forms.CharField(
        required=True, error_messages={'required': NO_CONTENT_MESSAGE},
        widget=forms.Textarea(attrs={
            'placeholder': 'Your message',
            'class': 'contact_form_input'}))

    def clean_contact_phone(self):
        phone_regex = re.compile('^\+?1?\d{9,15}$')
        number = self.cleaned_data['contact_phone']
        if len(number) > 0 and phone_regex.match(number) is None:
            raise forms.ValidationError(INVALID_PHONE_MESSAGE, code='invalid')
        return number

    def make_message(self):
        data = self.cleaned_data
        message = '\n'.join([
            'From: {}'.format(data['contact_name']),
            'eMail: {}'.format(data['return_email']),
            'Phone: {}'.format(data['contact_phone']),
            'Message: ',
            data['message_content']])
        return message

    def make_email(self):
        data = self.cleaned_data
        subject = 'Contact Form message from {} Re: {}'.format(
            data['contact_name'], data['message_subject'])
        return_address = data['return_email']
        message = self.make_message()
        from_address = settings.EMAIL_HOST_USER
        to_address = settings.CONTACT_FORM_TARGET_ADDRESS
        message = EmailMessage(
            subject, message, from_address, [to_address],
            reply_to=[return_address])
        return message

    def send_mail(self):
        email = self.make_email()
        email.send(fail_silently=False)
