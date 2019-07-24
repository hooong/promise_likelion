from django import forms
from .models import Promise, Promise_Comment
from tempus_dominus.widgets import DateTimePicker
from django.utils import timezone

class PromiseForm(forms.ModelForm):

    class Meta:
        model = Promise
        fields = ['title', 'content']

        labels = {
            'title': '제목',
            'content': '약속내용',
        }
        #form css class, id 입히기
    def __init__(self, *args, **kwargs):
        super(PromiseForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['class'] = 'form-control formInput'
        self.fields['content'].widget.attrs['class'] = 'form-control formInput'

class Promise_CommentForm(forms.ModelForm):
    class Meta:
        model = Promise_Comment
        fields = ['content']

        labels = {
            'content': '댓글내용'
        }