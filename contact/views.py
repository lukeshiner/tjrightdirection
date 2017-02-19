from django.shortcuts import render, redirect
from . forms import ContactForm


def contact(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(data=request.POST)
        if form.is_valid():
            try:
                form.send_mail()
            except:
                return redirect('contact:failure')
            form = ContactForm()
            return redirect('contact:success')
    return render(request, 'contact/contact.html', {'form': form})


def success(request):
    form = ContactForm()
    return render(request, 'contact/success.html', {'form': form})


def failure(request):
    form = ContactForm()
    return render(request, 'contact/success.html', {'form': form})
