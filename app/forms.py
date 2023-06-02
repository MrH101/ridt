from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from .models import User, Blog, Comment
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

class UserForm(UserCreationForm):
    profile_picture = forms.ImageField(required=True)
    phone_number = forms.CharField(max_length=20, required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone_number', 'profile_picture', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-2'
        self.helper.field_class = 'col-md-10'
        self.helper.layout = Layout(
            'username',
            'first_name',
            'last_name',
            'email',
            'profile_picture',
            'phone_number',
            'password1',
            'password2',
            Row(
                Column(Submit('submit', 'Submit', css_class='btn-primary'), css_class='col-md-2'),
                css_class='form-group'
            )
        )

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'content')

    def __init__(self, *args, **kwargs):
        super(BlogForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-2'
        self.helper.field_class = 'col-md-10'
        self.helper.layout = Layout(
            'title',
            'content',
            Row(
                Column(Submit('submit', 'Submit', css_class='btn-primary'), css_class='col-md-2'),
                css_class='form-group'
            )
        )

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-inline'
        self.helper.label_class = 'sr-only'
        self.helper.field_class = 'form-control mb-2 mr-sm-2'
        self.helper.layout = Layout(
            'content',
            Submit('submit', 'Submit', css_class='btn-primary mb-2')
        )