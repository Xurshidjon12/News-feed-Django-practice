from django.http import HttpResponse
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, UpdateView, DeleteView, CreateView

from news_app.custom_permissions import OnlyLoggedSuperUser
from .models import Comment, News, Category
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from .forms import CommentForm, ContactForm
from django.contrib.auth.decorators import login_required, user_passes_test
from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountMixin


# Create your views here.
def news_list(request):
    #news_list = News.objects.filter(status=News.Status.PUBLISH)
    news_list = News.published.all()  # PublishedManager manageri ishlatiladi
    context ={
        "news_list": news_list
    }
    
    return render(request, "news/news_list.html", context)



def news_detail(request, news):
    news = get_object_or_404(News, slug=news, status=News.Status.PUBLISH)
    context = {}
    hit_count = get_hitcount_model().objects.get_for_object(news)
    hits = hit_count.hits
    hitcontext =context['hitcount'] = {'pk': hit_count.pk}
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    if hit_count_response.hit_counted:
        hits += 1
        hitcontext['hit_counted'] = hit_count_response.hit_counted
        hitcontext['hit_message'] = hit_count_response.hit_message
        context['hits'] = hits



    comments = news.comments.filter(active=True)
    new_comment = None
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.news = news
            new_comment.user = request.user
            new_comment.save() 
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()


    context = {
        "news": news,
        "comments": comments,
        "new_comment": new_comment,
        "comment_form": comment_form,
        "comments_count": news.comments.count()
    }
    
    return render(request, "news/news_detail.html", context)

def homePageView(request):
    news_list = News.published.all().order_by('-publish_time')[:10]
    categories = Category.objects.all()
    local_one = News.published.filter(category__name__iexact="Mahalliy").order_by('-publish_time')[:1]
    local_news = News.published.filter(category__name__iexact="Mahalliy").order_by('-publish_time')[1:5]

    context = {
        'news_list': news_list,
        'categories': categories,
        'local_news': local_news,
        'local_one': local_one
    }
    return render(request, 'news/home.html', context)


class HomePageView(ListView):
    model = News
    template_name = 'news/home.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['news_list'] = News.published.all().order_by('-publish_time')[:4]
        context['mahalliy_xabarlar'] = News.published.all().filter(category__name__iexact="Mahalliy").order_by('-publish_time')[:5]
        context['xorij_xabarlar'] = News.published.all().filter(category__name__iexact="Xorij").order_by('-publish_time')[:5]
        context['sport'] = News.published.all().filter(category__name__iexact="Sport").order_by('-publish_time')[:5]
        context['texnalogiyalar'] = News.published.filter(
            category__name__iexact="Texnalogiya"
        ).order_by('-publish_time')[:5]
        

        return context


# def contact_page(request): #bu function view orqali contact formani ishlatishimiz mumkin
#     print(request.POST)
#     form = ContactForm(request.POST or None)
#     if form.is_valid() and request.method == "POST":
#         form.save()
#         return HttpResponse("<h2> Biz bilan bog'langanguz uchun tashakkur!")
#     context = {
#         "form": form
#     }
#     return render(request, 'news/contact.html', context)


class ContactFormView(TemplateView): #bu class view orqali contact formani ishlatishimiz mumkin
    
    template_name = 'news/contact.html'

    def get(self, request, *args, **kwargs):
        form = ContactForm()
        context = {
            "form": form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if request.method == 'POST' and form.is_valid():
            form.save()
            return HttpResponse("<h2> Biz bilan bog'langanguz uchun tashakkur!")
        context = {
            "form": form
        }
        return render(request, self.template_name, context)


class LocalNewsView(ListView):
    model = News
    template_name = 'news/mahalliy.html' 
    context_object_name = 'mahalliy_yangiliklar'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name__iexact="Mahalliy")
        return news


class ForeignNewsView(ListView):
    model = News
    template_name = 'news/xorij.html' 
    context_object_name = 'xorij_yangiliklar'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name__iexact="Xorij")
        return news

class SportNewsView(ListView):
    model = News
    template_name = 'news/sport.html' 
    context_object_name = 'sport_yangiliklar'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name__iexact="Sport")
        return news

class TechnologyView(ListView):
    model = News
    template_name = 'news/texnalogiya.html' 
    context_object_name = 'texnalogiya_yangiliklar'

    def get_queryset(self): 
        news = self.model.published.all().filter(category__name__iexact="Texnalogiya")
        return news

class NewsUpdateView(OnlyLoggedSuperUser,UpdateView):
    model = News
    fields = ['title', 'slug', 'body', 'image', 'category', 'status']
    template_name = 'crud/news_edit.html'


class NewsDeleteView(OnlyLoggedSuperUser,DeleteView):
    model = News
    template_name = 'crud/news_delete.html'
    success_url = reverse_lazy('home_page')  # bu yerda delete qilingandan keyin qaysi page ga redirect qilinishini belgilaymiz


class NewsCreateView(OnlyLoggedSuperUser, CreateView):
    model = News
    template_name = 'crud/news_create.html'
    fields = ['title', 'slug', 'body', 'image', 'category', 'status']

    success_url = reverse_lazy('home_page')  # bu yerda create qilingandan keyin qaysi page ga redirect qilinishini belgilaymiz



@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_page(request):
    admin_users = User.objects.filter(is_superuser=True)
    context = {
        "admin_users": admin_users
    }
    return render(request, 'pages/admin_page.html', context)



class SearchResultsList(ListView):
    model = News
    template_name = 'news/search_results.html'
    context_object_name = 'barcha_yangiliklar'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return News.objects.filter(
            Q(title__icontains=query) | Q(body__icontains=query)

        )


