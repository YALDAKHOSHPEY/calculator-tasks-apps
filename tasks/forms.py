from django import forms

class TaskForm(forms.Form):
    # فیلدهای فرم شما
    title = forms.CharField(
        label='Task Title',
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter task title'
        })
    )
    
    # یا اگر از ModelForm استفاده می‌کنید:
    class Meta:
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea'}),
        }