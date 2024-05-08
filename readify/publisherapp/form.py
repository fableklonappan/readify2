from django import forms
from libraryapp.models import AddBook, AudioBook

class AddBookForm(forms.ModelForm):
    class Meta:
        model = AddBook
        fields = '__all__'  # You can specify specific fields if needed

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if AddBook.objects.filter(title=title).exists():
            raise forms.ValidationError("A book with this title already exists.")
        return title
    

class AudioBookForm(forms.ModelForm):
    class Meta:
        model = AudioBook
        fields = ('title', 'author','duration','narrator','cover_image','audio_file','publication_date')

    def clean_title(self):
        title = self.cleaned_data.get('title') # Debugging statement
        if AddBook.objects.filter(title=title).exists():
            raise forms.ValidationError("A book with this title already exists.")
        return title