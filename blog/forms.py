from django import forms
from django.contrib.auth.models import User
from .models import Post

#class PostForm(forms.Form):
#    title = forms.CharField(max_length=200, label="Заголовок")
#    text = forms.CharField(widget=forms.Textarea, label="Текст объявления")
#    author = forms.ModelChoiceField(queryset=User.objects.all(), label="Автор")
#    image = forms.ImageField(required=False, label="Изображение")

class PostForm(forms.ModelForm):
    # дополняем конструктор родительского класса
    def __init__ (self, *args, **kwargs):
        # получаем author из именованных аргументов (его передали во views)
        author = kwargs.pop('author', None)
        # вызываем конмтруктор родительского
        super().__init__(*args, **kwargs)
        # устанавливаем начальное значение поля author
        self.fields['author'].initial = author
        # отключаем видимость этого поля в форме
        self.fields['author'].disable = True
        self.fields['author'].widget = forms.HiddenInput()
    class Meta:
        model = Post
        fields = ('title', 'text', 'image', 'author')

        labels = {
            'title': 'Загловок',
            'text': 'Текст объявления',
            'image': 'Изображение',
            # 'price': 'Цена'
        }
class FilterForm(forms.Form):
    author = forms.ModelChoiceField(queryset=User.objects.all(), label='Автор',required=False)
    created_at = forms.DateField(label='Дата публикации',
                                 widget=forms.DateInput(attrs={'type': 'date'}),
                                 input_formats=["%Y-%m-%d"],
                                 required=False)