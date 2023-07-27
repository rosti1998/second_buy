from django.test import TestCase
from django.contrib.auth.models import User
from second_buy.web.models import Category, Item, Inquiry, Discussion, Comment, Profile


class ModelTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create a test category
        self.category = Category.objects.create(name='Test Category')

        # Create a test item
        self.item = Item.objects.create(
            profile=self.user,
            category=self.category,
            name='Test Item',
            description='This is a test item.',
            price=9.99,
        )

        # Create a test inquiry
        self.inquiry = Inquiry.objects.create(
            message='Test inquiry message',
            username='Test User',
            phone_number='1234567890',
            email_address='test@example.com',
            item=self.item,
        )

        # Create a test discussion
        self.discussion = Discussion.objects.create(
            title='Test Discussion',
            category=self.category,
            context='This is a test discussion.',
            profile=self.user,
        )

        # Create a test comment
        self.comment = Comment.objects.create(
            message='Test comment message',
            username='Test User',
            discussion=self.discussion,
        )

    def test_profile_creation(self):
        profile = Profile.objects.create(user=self.user, phone_number='1234567890', email='test@example.com')
        self.assertEqual(str(profile), 'testuser')

    def test_category_creation(self):
        self.assertEqual(str(self.category), 'Test Category')

    def test_item_creation(self):
        self.assertEqual(str(self.item), 'Test Item')

    def test_inquiry_creation(self):
        self.assertEqual(str(self.inquiry), 'Test User - Test Item')

    def test_discussion_creation(self):
        self.assertEqual(str(self.discussion), 'Test Discussion')

    def test_comment_creation(self):
        self.assertEqual(str(self.comment), 'Test User - Test Discussion')


