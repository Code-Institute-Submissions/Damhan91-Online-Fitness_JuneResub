from django.shortcuts import render
from django.views import generic
from .models import Post


class Postlist(generic.ListView):
    model = Post
    template_name = 'index.html'
    ordering = ['-created_on']
    paginate_by = 4