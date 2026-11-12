from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, TemplateView
from .models import News, Category
from .forms import ContactForm


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
    context = {
        "news": news
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