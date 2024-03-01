from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Title, Comment
from .forms import CommentForm

def anime(request):
    titles = Title.objects.order_by('title')
    return render(request, 'review_app/anime.html', {'titles': titles})

def anime_detail(request, pk):
    title = get_object_or_404(Title, pk=pk)
    return render(request, 'review_app/anime_detail.html', {'title': title})

def add_comment(request, pk):
    title = get_object_or_404(Title, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.title = title
            comment.save()
            return redirect('anime_detail', pk=title.pk)
    else:
        form = CommentForm()
    return render(request, 'review_app/add_comment.html', {'form': form})

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