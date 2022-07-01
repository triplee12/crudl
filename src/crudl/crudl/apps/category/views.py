from django.shortcuts import render
from django.views.generic import ListView
from .models import Category


class IdeaCategoryListView(ListView):
    model = Category
    template_name = "categories/category_list.html"
    context_object_name = "categories"
