from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from .models import Post
from django.http import HttpResponseRedirect
from .forms import CommentForm
from django.views.generic.edit import UpdateView, DeleteView


class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by("-created_on")
    template_name = "blog.html"
    paginate_by = 6


class PostDetail(View):
    def get(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by("-created_on")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True
            
        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": False,
                "liked": liked,
                "comment_form": CommentForm()
            },
        )

    def post(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=False).order_by("-created_on")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
        else:
            comment_form = CommentForm()

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": False,
                "liked": liked,
                "comment_form": CommentForm()
            },
        )


class PostLikes(View):
    def post(self, request, slug, *args, **kwargs):
            post = get_object_or_404(Post, slug=slug)
            if post.likes.filter(id=request.user.id).exists():
                post.likes.remove(request.user)
            else:
                post.likes.add(request.user)

            return HttpResponseRedirect(reverse('post_detail', args=[slug]))


#
# @login_required
# def delete_own_comment(request, message_id):
#   comment = get_object_or_404(comments.get_model(), pk=message_id,
#            site__pk=settings.SITE_ID)
#    if comment.user == request.user:
#        comment.is_removed = True
#        comment.save()


class EditComment(UpdateView):
    model = Post
    field = ['body']
    template_name = 'edit-comment.html'


class DeleteComment(DeleteView):
    model = Post
    template_name = 'delete-comment.html'


def home(response):
    return render(response, 'home.html')


def nutrition(response):
    return render(response, 'nutrition.html')

    
def exercises(response):
    return render(response, 'exercises.html')