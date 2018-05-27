"""Forms for the gallery app."""

from django import forms


class GalleryImageAdminForm(forms.ModelForm):
    """Admin form for the gallery app."""

    images = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}))
