from django.contrib.auth.models import User
from django.test import TestCase

from second_buy.web.forms import ItemForm, InquiryForm, DiscussionForm, CommentForm
from second_buy.web.models import Profile, Category


class ItemFormTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.category = Category.objects.create(name='Test Category')

    def test_item_form_valid_data(self):
        form = ItemForm(data={
            'category': self.category,
            'name': 'Smartphone',
            'description': 'A high-end smartphone',
            'price': 999.99,
            'item_photo': '/image/test.png'
        })
        self.assertTrue(form.is_valid())

    def test_item_form_invalid_data(self):
        form = ItemForm(data={})
        self.assertFalse(form.is_valid())


class InquiryFormTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.profile = Profile.objects.create(user=self.user, phone_number='1234567890', email='test@example.com')

    def test_inquiry_form_valid_data(self):
        form = InquiryForm(data={
            'message': 'I am interested in the item.',
            'phone_number': self.profile.phone_number,
            'email_address': self.profile.email,
        }, user_id=self.profile.user_id)
        self.assertTrue(form.is_valid())

    def test_inquiry_form_invalid_data(self):
        form = InquiryForm(data={})
        self.assertFalse(form.is_valid())


class DiscussionFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.category = Category.objects.create(name='Test Category')

    def test_discussion_form_valid_data(self):
        form = DiscussionForm(data={
            'category': self.category.id,
            'title': 'Test Discussion',
            'context': 'This is a test discussion.',
        })
        self.assertTrue(form.is_valid())

    def test_discussion_form_invalid_data(self):
        # Testing the form with missing data
        form = DiscussionForm(data={})
        self.assertFalse(form.is_valid())

    def test_discussion_form_save(self):
        form = DiscussionForm(data={
            'category': self.category.id,
            'title': 'Test Discussion',
            'context': 'This is a test discussion.',
        })

        # Check if the form is valid and can save the data
        self.assertTrue(form.is_valid())
        form.instance.profile = self.user
        discussion = form.save()

        # Check if the discussion object is saved correctly
        self.assertEqual(discussion.title, 'Test Discussion')
        self.assertEqual(discussion.context, 'This is a test discussion.')
        self.assertEqual(discussion.category, self.category)


class CommentFormTest(TestCase):
    def test_comment_form_valid_data(self):
        form = CommentForm(data={
            'message': 'This is a comment.',
        })
        self.assertTrue(form.is_valid())

    def test_comment_form_invalid_data(self):
        form = CommentForm(data={})
        self.assertFalse(form.is_valid())
