from django import forms
from .models import Item, Inquiry, Profile, Discussion, Comment


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['category', 'name', 'description', 'price', 'item_photo']


class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ['message', 'phone_number', 'email_address']

    def __init__(self, *args, user_id=None, **kwargs):
        super(InquiryForm, self).__init__(*args, **kwargs)
        if user_id:
            profile = Profile.objects.get(user_id=user_id)
            self.fields['phone_number'].initial = profile.phone_number
            self.fields['email_address'].initial = profile.email


class DiscussionForm(forms.ModelForm):
    class Meta:
        model = Discussion
        fields = ['category', 'title', 'context']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['message']

