from django import forms

from users.models import User
from blog.models import Post, Comment

class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ('title','content')

class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ('comment_text',)

    def save(self, commit=True):
        comment = super(CommentForm, self).save(commit=False)
        comment.comment_text = self.cleaned_data['comment_text']

        if commit:
            comment.save()
        
        return comment

class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('image',)

