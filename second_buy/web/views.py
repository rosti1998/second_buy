from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import Http404
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth import views
from django.shortcuts import render, get_object_or_404
from django.views.generic import FormView, DetailView, UpdateView, CreateView, ListView, DeleteView

from second_buy.web.forms import ItemForm, InquiryForm, DiscussionForm, CommentForm
from second_buy.web.models import Profile, Item, Category, Inquiry, Discussion, Comment


class UserIsOwnerMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        profile = None
        if 'user_id' in kwargs:
            profile = get_object_or_404(Profile, user_id=kwargs['user_id'])
        if 'item_id' in kwargs:
            item = get_object_or_404(Item, pk=kwargs['item_id'])
            profile = Profile.objects.get(user_id=item.profile.pk)
        if 'discussion_id' in kwargs:
            discussion = get_object_or_404(Discussion, pk=kwargs['discussion_id'])
            profile = Profile.objects.get(user_id=discussion.profile.pk)
        if request.user == profile.user:
            return super().dispatch(request, *args, **kwargs)
        else:
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied


class Index(View):
    template_name = 'index.html'

    def get(self, request):

        return render(request, self.template_name, {"user": request.user})


class Login(views.LoginView):
    success_url = reverse_lazy('/')


class Logout(views.LogoutView):
    pass


class Register(FormView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')  # Replace 'login' with the name of your login URL pattern

    def form_valid(self, form):
        try:
            user = form.save()

            profile = Profile.objects.create(user=user)
            profile.save()

            return super().form_valid(form)
        except Exception as e:
            return render(self.request, 'error.html', {'error_message': str(e)})


class ViewProfile(UserIsOwnerMixin, DetailView):
    model = Profile
    template_name = 'profile/profile_view.html'
    context_object_name = 'profile'

    def test_func(self):
        return self.request.user.pk == self.kwargs['user_id']

    def get_object(self, queryset=None):
        try:
            return get_object_or_404(Profile, user_id=self.kwargs['user_id'])
        except Http404:
            # Handle Http404 exception here
            raise Http404("Profile not found")


class EditProfile(UserIsOwnerMixin, UpdateView):
    model = Profile
    fields = ['phone_number', 'email', 'profile_photo']
    template_name = 'profile/edit_profile.html'

    def test_func(self):
        return self.request.user.pk == self.kwargs['user_id']

    def get_object(self, queryset=None):
        try:
            user_id = self.kwargs['user_id']
            return get_object_or_404(Profile, user_id=user_id)
        except Http404:
            # Handle Http404 exception here
            raise Http404("Profile not found")

    def get_success_url(self):
        return reverse_lazy('view profile', kwargs={'user_id': self.kwargs['user_id']})


class ItemsList(UserIsOwnerMixin, View):
    template_name = 'my_items.html'

    def test_func(self):
        return self.request.user.pk == self.kwargs['user_id']

    def get(self, request, user_id):
        try:
            items = Item.objects.filter(profile_id=user_id)
            return render(request, 'my_items.html', {'items': items, 'user_id': user_id})
        except Exception as e:
            # Handle the exception, you can log it or render an error page
            return render(request, 'error.html', {'error_message': str(e)})


class CreateItem(UserIsOwnerMixin, CreateView):
    model = Item
    form_class = ItemForm
    template_name = 'create_item.html'

    def form_valid(self, form):
        form.instance.profile_id = self.kwargs['user_id']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('my items', kwargs={'user_id': self.kwargs['user_id']})


class AllItems(ListView):
    model = Item
    template_name = 'all_items.html'
    context_object_name = 'items'
    paginate_by = 2  # Number of items per page

    def get_queryset(self):
        queryset = super().get_queryset()
        category_filter = self.request.GET.get('category', None)
        search_query = self.request.GET.get('search', None)
        if category_filter:
            queryset = queryset.filter(category__name=category_filter)

        if search_query:
            queryset = queryset.filter(Q(name__icontains=search_query))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['selected_category'] = self.request.GET.get('category', None)
        context['search_query'] = self.request.GET.get('search', None)
        items = context['items']
        paginator = Paginator(items, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            items_page = paginator.page(page)
        except PageNotAnInteger:
            items_page = paginator.page(1)
        except EmptyPage:
            items_page = paginator.page(paginator.num_pages)

        context['items'] = items_page
        return context


class ViewItem(View):
    template_name = 'item_detail.html'

    def test_func(self):
        item = self.get_object()

        return self.request.user == item.profile

    def get_object(self):
        pk = self.kwargs.get('item_id')
        return get_object_or_404(Item, pk=pk)

    def get(self, request, *args, **kwargs):
        item = self.get_object()
        context = {
            'item': item,
            'isOwner': self.test_func(),
            'user': self.request.user,
            'inquiries': item.inquiries.all()
        }
        return render(request, self.template_name, context)


class EditItem(UserIsOwnerMixin, UpdateView):
    model = Item
    fields = ['name', 'category', 'description', 'price', 'item_photo']
    template_name = 'edit_item.html'

    def get_object(self, queryset=None):
        item_id = self.kwargs['item_id']
        return get_object_or_404(Item, pk=item_id)

    def get_success_url(self):
        return reverse_lazy('view item', kwargs={'item_id': self.kwargs['item_id']})


class DeleteItem(DeleteView):
    model = Item
    template_name = 'delete_item.html'
    success_url = reverse_lazy('all items')


class SendInquiry(LoginRequiredMixin, CreateView):
    model = Inquiry
    form_class = InquiryForm
    template_name = 'create_inquiry.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user_id'] = self.request.user.id
        return kwargs

    def form_valid(self, form):
        form.instance.item_id = self.kwargs['item_id']
        user = User.objects.get(pk=self.kwargs['user_id'])
        form.instance.username = user.username
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('view item', kwargs={'item_id': self.kwargs['item_id']})


class DiscussionsList(UserIsOwnerMixin, View):
    def get(self, request, user_id):
        discussions = Discussion.objects.filter(profile_id=user_id)
        return render(request, 'my_discussions.html', {'discussions': discussions, 'user_id': user_id})


class CreateDiscussion(UserIsOwnerMixin, CreateView):
    model = Discussion
    form_class = DiscussionForm
    template_name = 'create_discussion.html'

    def form_valid(self, form):
        form.instance.profile_id = self.kwargs['user_id']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('my discussions', kwargs={'user_id': self.kwargs['user_id']})


class ViewDiscussion(View):
    template_name = 'discussion_detail.html'

    def test_func(self):
        discussion = self.get_object()
        return self.request.user == discussion.profile

    def get_object(self):
        pk = self.kwargs.get('discussion_id')
        return get_object_or_404(Discussion, pk=pk)

    def get(self, request, *args, **kwargs):
        discussion = self.get_object()
        context = {
            'discussion': discussion,
            'isOwner': self.test_func(),
            'user': self.request.user,
            'comments': discussion.comments.all().order_by('-created_on')
        }
        return render(request, self.template_name, context)


class EditDiscussion(UserIsOwnerMixin, UpdateView):
    model = Discussion
    fields = ['title', 'category', 'context']
    template_name = 'edit_discussion.html'

    def get_object(self, queryset=None):
        discussion_id = self.kwargs['discussion_id']
        return get_object_or_404(Discussion, pk=discussion_id)

    def get_success_url(self):
        return reverse_lazy('view discussion', kwargs={'discussion_id': self.kwargs['discussion_id']})


class DeleteDiscussion(DeleteView):
    model = Discussion
    template_name = 'delete_discussion.html'
    success_url = reverse_lazy('index')


class SendComment(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'create_comment.html'

    def form_valid(self, form):
        form.instance.discussion_id = self.kwargs['discussion_id']
        user = User.objects.get(pk=self.kwargs['user_id'])
        form.instance.username = user.username
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('view discussion', kwargs={'discussion_id': self.kwargs['discussion_id']})


class AllDiscussions(ListView):
    model = Discussion
    template_name = 'all_discussions.html'
    context_object_name = 'discussions'
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        category_filter = self.request.GET.get('category', None)
        search_query = self.request.GET.get('search', None)
        if category_filter:
            queryset = queryset.filter(category__name=category_filter)

        if search_query:
            queryset = queryset.filter(Q(title__icontains=search_query))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['selected_category'] = self.request.GET.get('category', None)
        context['search_query'] = self.request.GET.get('search', None)
        discussions = context['discussions']
        paginator = Paginator(discussions, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            discussions_page = paginator.page(page)
        except PageNotAnInteger:
            discussions_page = paginator.page(1)
        except EmptyPage:
            discussions_page = paginator.page(paginator.num_pages)

        context['discussions'] = discussions_page
        return context