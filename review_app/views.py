from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Title, Comment, CustomUser
from .forms import CommentForm, CustomUserCreationForm, UserAuthForm, UserProfileForm
from django.contrib.auth import login, logout, authenticate

def anime(request):
    titles = Title.objects.order_by('title')
    return render(request, 'review_app/anime.html', {'titles': titles})

def anime_detail(request, pk):
    title = get_object_or_404(Title, pk=pk)
    return render(request, 'review_app/anime_detail.html', {'title': title})

def add_comment(request, pk):
    user = get_object_or_404(CustomUser, username=request.user.username)
    title = get_object_or_404(Title, pk=pk) 
    if request.method == 'POST':
        form = CommentForm(request.POST) # pass the user which requested this form
        if form.is_valid():
            comment = form.save(commit=False)
            comment.title = title  
            comment.author = user 
            comment.save()
            return redirect('anime_detail', pk=title.pk)
    else:
        form = CommentForm()
    return render(request, 'review_app/add_comment.html', {'form': form, 'user': user})

def comment_not_found(request):
    return render(request, 'review_app/comment_not_found.html')

def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('anime_detail', pk=comment.title.pk)

def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    try:
        comment.delete()
        return redirect(reverse('anime_detail', kwargs={'pk': comment.title.pk}))
    except Comment.DoesNotExist:
        # Handle the case where the comment does not exist
        return render(request, 'review_app/comment_not_found.html')

from django.contrib.auth import login

def sign_up(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            print("Form is valid!")
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            print(username, "\n", password)
            user = authenticate(request, username=username, password=password) 
            if user is not None:
                login(request, user)
                print("User created and logged in successfully!")
                return redirect('anime')
            else:
                print("User authentication failed.")
        else:
            print("Form errors:", form.errors)
    else:
        form = CustomUserCreationForm()
    return render(request, 'review_app/sign_up.html', {'form': form})

def log_in(request):
    if request.method == 'POST':
        form = UserAuthForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data['username_or_email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username_or_email, password=password)
            if user is not None:
                login(request, user)
                return redirect('anime')
    else:
        form = UserAuthForm()
    return render(request, 'review_app/log_in.html', {'form': form})

def log_out(request):
    logout(request)
    return redirect('anime')

def view_profile(request, username):
    user = get_object_or_404(CustomUser, username=username)
    return render(request, 'review_app/profile.html', {'user': user})

def edit_profile(request, username):
    user = get_object_or_404(CustomUser, username=username)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)  
        if form.is_valid():
            form.save()
            return redirect('view_profile', username=username)
    else:
        form = UserProfileForm(instance=user)
    return render(request, 'review_app/edit_profile.html', {'user': user, 'form': form})
    