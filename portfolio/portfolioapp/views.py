from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, TemplateView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Idea_list, Opinion, Profile
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def signupfunc(request):
    if request.method == 'POST':
        username2 = request.POST['username']
        password2 = request.POST['password']
        prefectures2 = request.POST['prefectures']
        works2 = request.POST['works']

        try:
            User.objects.get(username=username2)
            return render(request, 'signup.html', {'error': 'このユーザは登録されています。'})

        except:
            user = User.objects.create_user(username2, '', password2)
            user.profile.prefectures = prefectures2
            user.profile.works = works2
            user.save()
            return redirect('../accounts/login')

        return render(request, 'signup.html')


class Home(TemplateView):
    template_name = 'home.html'


class Ideas_list(LoginRequiredMixin, ListView):
    template_name = 'ideas_list.html'
    model = Idea_list
    paginate_by = 3

    def get_queryset(self):
        q_word = self.request.GET.get('query')

        if q_word:
            object_list = Idea_list.objects.filter(Q(genre__icontains=q_word))
        else:
            object_list = Idea_list.objects.all()
        return object_list


@login_required
def opinion(request, pk):
    idea = Idea_list.objects.get(pk=pk).genre
    if request.method == 'POST':
        author2 = request.POST['author']
        title2 = request.POST['title']
        content2 = request.POST['content']
        Opinion.objects.create(author=author2, title=title2,
                               content=content2, idea_list_id=pk)
        return redirect('main_list', pk=pk)
    return render(request, 'opinion.html', {'object': idea})


@login_required
def main_list(request, pk):
    items = Opinion.objects.filter(idea_list_id=pk)
    paginator = Paginator(items, 5)
    page_num = request.GET.get('page', 1)
    pages = paginator.page(page_num)

    try:
        pages = paginator.page(page_num)

    except PageNotAnInteger:
        pages = paginator.page(1)

    except EmptyPage:
        pages = paginator.page(1)

    d = {
        'page_obj': pages,
        'pk2': pk,
        'main_title': Idea_list.objects.get(pk=pk).genre,
        'is_paginated': pages.has_other_pages,
    }
    return render(request, "main_list.html", d)


@login_required
def goodfunc(request, pk):
    post = Opinion.objects.get(pk=pk)
    pk2 = post.idea_list_id
    post2 = request.user.get_username()
    if post2 in post.goodcheck:
        return redirect('main_list', pk=pk2)
    else:
        post.good += 1
        post.goodcheck = post.goodcheck + '' + post2
        post.save()
        return redirect('main_list', pk=pk2)


@login_required
def branchfunc(request, pk):
    user = request.user.get_username()
    post = Opinion.objects.filter(idea_list_id=pk).filter(author=user)
    if not post:
        return redirect('opinion', pk=pk)
    else:
        return redirect('main_list', pk=pk)


@login_required
def detailfunc(request, author):
    key = User.objects.get(username=author).id
    profile2 = Profile.objects.get(user_id=key)
    opinion2 = Opinion.objects.filter(author=author)
    z = {
        "profile": profile2,
        "opinion": opinion2,
    }
    return render(request, 'detail.html', z)


@login_required
def myfunc(request):
    id = request.user.id
    userinfo = Profile.objects.get(user_id=id)
    name = userinfo.user.username
    ideas = Opinion.objects.filter(author=name)
    paginator = Paginator(ideas, 1)
    page_num = request.GET.get('page', 1)
    pages = paginator.page(page_num)

    try:
        pages = paginator.page(page_num)

    except PageNotAnInteger:
        pages = paginator.page(1)

    except EmptyPage:
        pages = paginator.page(1)

    z = {
        'userinfo': userinfo,
        'page_obj': pages,
        'is_paginated': pages.has_other_pages,
    }
    return render(request, 'my_page.html', z)


class Edit(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = 'edit.html'
    fields = ('prefectures', 'works')
    success_url = reverse_lazy('my_page')


class Idea_edit(LoginRequiredMixin, UpdateView):
    model = Opinion
    template_name = 'idea_edit.html'
    fields = ('title', 'content')
    success_url = reverse_lazy('my_page')


class Delete(LoginRequiredMixin, DeleteView):
    model = Opinion
    template_name = 'delete.html'
    success_url = reverse_lazy('my_page')
