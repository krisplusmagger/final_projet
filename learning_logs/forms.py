from django import forms

from .models import Topic, Entry 

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic #根据模型创造表单
        fields = ['text'] #只包含字段text
        labels = {'text': ''} #不要为字段text生成标签
class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = [ 'text' ]
        lables = { 'text': ' '}
        widgets = {'text': forms.Textarea(attrs={'cols':80})}        