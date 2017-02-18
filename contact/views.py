from django.shortcuts import render
from . forms import ContactForm


def contact(request):
    form = ContactForm()
    status = None
    if request.method == 'POST':
        form = ContactForm(data=request.POST)
        if form.is_valid():
            try:
                form.send_mail()
            except:
                status = 'failed'
            form = ContactForm()
            status = 'success'
    return render(request, 'contact/contact.html', {
        'form': form, 'status': status})
