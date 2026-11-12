from django.urls import path
from .views import news_detail, news_list, homePageView, ContactFormView,HomePageView, LocalNewsView, ForeignNewsView, SportNewsView, TechnologyView

urlpatterns = [
    path('', HomePageView.as_view(), name='home_page'),
    path('news/', news_list, name='all_news_list'),
    path('detail/<slug:news>/', news_detail, name='news_detail'),
    path('contact-us/', ContactFormView.as_view(), name='contact_page'),
    path('local-news/', LocalNewsView.as_view(), name='local_news_page'),
    path('foreign-news/', ForeignNewsView.as_view(), name='foreign_news_page'),
    path('sport-news/', SportNewsView.as_view(), name='sport_news_page'),
    path('technology-news/', TechnologyView.as_view(), name='technology_news_page')
]
