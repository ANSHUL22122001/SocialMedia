from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import UpdateView, DeleteView

from .models import Post, Comment, UserProfile, Notification
from .forms import PostForm, CommentForm


# Create your views here.
class PostListView(View):
    def get(self, request, *args, **kwargs):
        # if User.is_authenticated:

        profile = UserProfile.objects.get(user=request.user)
        bio = profile.bio
        followers = profile.followers.all()
        number_of_followers = len(followers)
        number_of_post = Post.objects.filter(author=request.user)
        posts = Post.objects.all().order_by('-created_on')
        form = PostForm()

        context = {
            'id': profile.pk,
            'profile_pic': profile.picture,
            'bio': bio,
            'nof': number_of_followers,
            'nop': len(number_of_post),
            'post_list': posts,
            'form': form,
        }
        return render(request, 'media/post_list.html', context)

    def post(self, request, *args, **kwargs):
        if User.is_authenticated:

            # if User.is_authenticated:
            profile = UserProfile.objects.get(user=request.user)
            followers = profile.followers.all()
            number_of_post = Post.objects.filter(author=request.user)

            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                new_post = form.save(commit=False)
                new_post.author = request.user
                new_post.save()
            posts = Post.objects.all().order_by('-created_on')

            context = {
                'id': profile.pk,
                'profile_pic': profile.picture,
                'bio': profile.bio,
                'nof': len(followers),
                'nop': len(number_of_post),
                'post_list': posts,
                'form': form,
            }
            return render(request, 'media/post_list.html', context)
        else:
            return redirect('account_login')


class PostDetailView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = CommentForm()
        comments = Comment.objects.filter(post=post).order_by('-created_on')
        profile = UserProfile.objects.get(user=request.user)
        followers = profile.followers.all()
        number_of_post = Post.objects.filter(author=request.user)

        context = {
            'id': profile.pk,
            'profile_pic': profile.picture,
            'bio': profile.bio,
            'nof': len(followers),
            'nop': len(number_of_post),
            'post': post,
            'form': form,
            'comments': comments,
        }

        return render(request, 'media/post_detail.html', context)

    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = CommentForm(request.POST)
        profile = UserProfile.objects.get(user=request.user)
        followers = profile.followers.all()
        number_of_post = Post.objects.filter(author=request.user)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()

        comments = Comment.objects.filter(post=post).order_by('-created_on')

        context = {
            'id': profile.pk,
            'profile_pic': profile.picture,
            'bio': profile.bio,
            'nof': len(followers),
            'nop': len(number_of_post),
            'post': post,
            'form': form,
            'comments': comments,
        }

        return render(request, 'media/post_detail.html', context)


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'media/comment_delete.html'

    def get_success_url(self):
        pk = self.kwargs['post_pk']
        return reverse_lazy('post-detail', kwargs={'pk': pk})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author


class ProfileView(View):
    def get(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        user = profile.user
        posts = Post.objects.filter(author=user).order_by('-created_on')
        number_of_post = Post.objects.filter(author=request.user)
        followers = profile.followers.all()

        is_following = False
        if len(followers) == 0:
            is_following = False

        for follower in followers:
            if follower == request.user:
                is_following = True
                break
            else:
                is_following = False

        number_of_followers = len(followers)

        context = {
            'user': user,
            'profile': profile,
            'posts': posts,
            'number_of_followers': number_of_followers,
            'is_following': is_following,
            'nop': len(number_of_post)
        }
        return render(request, 'media/profile.html', context)


class ProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = UserProfile
    fields = ['name', 'bio', 'birth_date', 'location', 'picture']
    template_name = 'social/profile_edit.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('profile', kwargs={'pk': pk})

    def test_func(self):
        profile = self.get_object()
        return self.request.user == profile.user


class AddFollower(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        profile.followers.add(request.user)

        return redirect('profile', pk=profile.pk)


class RemoveFollower(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        profile.followers.remove(request.user)

        return redirect('profile', pk=profile.pk)


class AddLike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)

        is_like = False

        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break

        if not is_like:
            post.likes.add(request.user)

        if is_like:
            post.likes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)


class ListFollowers(View):
    def get(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        followers = profile.followers.all()
        number_of_post = Post.objects.filter(author=request.user)

        context = {
            'id': profile.pk,
            'profile_pic': profile.picture,
            'bio': profile.bio,
            'nof': len(followers),
            'nop': len(number_of_post),
            'profile': profile,
            'followers': followers
        }
        print(followers.values())
        return render(request, 'media/followers_list.html', context)


class PostNotification(View):
    def get(self, request, notification_pk, post_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        post = Post.objects.get(pk=post_pk)

        notification.user_has_seen = True
        notification.save()

        return redirect('post-detail', pk=post_pk)


class FollowNotification(View):
    def get(self, request, notification_pk, profile_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        profile = UserProfile.objects.get(pk=profile_pk)

        notification.user_has_seen = True
        notification.save()

        return redirect('profile', pk=profile_pk)


class RemoveNotification(View):
    def delete(self, request, notification_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)

        notification.user_has_seen = True
        notification.save()

        return HttpResponse('Success', content_type='text/plain')
