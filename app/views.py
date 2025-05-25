from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from app.models import Article
from app.forms import CreateArticleForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView


def home(request):
    articles = Article.objects.all()
    return render(request, "app/home.html", {"articles": articles})


def create_article(request):
    if request.method == "POST":
        form = CreateArticleForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            new_article = Article(
                title=form_data["title"],
                status=form_data["status"],
                content=form_data["content"],
                word_count=form_data["word_count"],
                twitter_post=form_data["twitter_post"],
            )
            new_article.save()

            return redirect("home")
    else:
        form = CreateArticleForm()
    return render(request, "app/article_create.html", {"form": form})


class ArticleListView(ListView):
    template_name = "app/home.html"
    model = Article
    context_object_name = "articles"


class ArticleCreateView(CreateView):
    template_name = "app/article_create.html"
    model = Article
    fields = ["title", "status", "content", "twitter_post"]
    success_url = reverse_lazy("home")

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.creator = self.request.user
        return super().form_valid(form)


class ArticleUpdateView(UpdateView):
    template_name = "app/article_update.html"
    model = Article
    fields = ["title", "status", "content", "twitter_post"]
    success_url = reverse_lazy("home")
    context_object_name = "article"


class ArticleDeleteView(DeleteView):
    template_name = "app/article_delete.html"
    model = Article
    success_url = reverse_lazy("home")
    context_object_name = "article"
