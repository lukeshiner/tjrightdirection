from django import forms


class GalleryImageAdminForm(forms.ModelForm):

    images = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}))
