from django.urls import path, include
from second_buy.web.views import *
from django.contrib.auth import views


urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('login/', Login.as_view(), name='login'),
    path('register/', Register.as_view(), name='register'),
    path('logout/', Logout.as_view(), name='logout'),
    path('view-profile/<int:user_id>/', ViewProfile.as_view(), name='view profile'),
    path('edit-profile/<int:user_id>/', EditProfile.as_view(), name='edit profile'),
    path('my-items/<int:user_id>/', ItemsList.as_view(), name='my items'),
    path('create-item/<int:user_id>/', CreateItem.as_view(), name='create item'),
    path('all-items/', AllItems.as_view(), name='all items'),
    path('view-item/<int:item_id>/', ViewItem.as_view(), name='view item'),
    path('edit-item/<int:item_id>/', EditItem.as_view(), name='edit item'),
    path('delete-item/<int:pk>/', DeleteItem.as_view(), name='delete item'),
    path('send-inquiry/<int:user_id>/<int:item_id>/', SendInquiry.as_view(), name='send inquiry'),
    path('my-discussions/<int:user_id>/', DiscussionsList.as_view(), name='my discussions'),
    path('create-discussion/<int:user_id>/', CreateDiscussion.as_view(), name='create discussion'),
    path('view-discussion/<int:discussion_id>/', ViewDiscussion.as_view(), name='view discussion'),
    path('edit-discussion/<int:discussion_id>/', EditDiscussion.as_view(), name='edit discussion'),
    path('delete-discussion/<int:pk>/', DeleteDiscussion.as_view(), name='delete discussion'),
    path('send-comment/<int:user_id>/<int:discussion_id>/', SendComment.as_view(), name='comment'),
    path('all-discussions/', AllDiscussions.as_view(), name='all discussions'),
]
