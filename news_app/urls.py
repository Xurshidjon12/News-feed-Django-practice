from django.urls import path
from .views import NewsUpdateView, news_detail, news_list, homePageView, ContactFormView,HomePageView, \
    LocalNewsView, ForeignNewsView, SportNewsView, TechnologyView, \
    NewsUpdateView, NewsDeleteView, NewsCreateView, admin_page, SearchResultsList


urlpatterns = [
    path('', HomePageView.as_view(), name='home_page'),
    path('news/', news_list, name='all_news_list'),
    path('news/create/', NewsCreateView.as_view(), name='news_create'),
    path('news/<slug:news>/', news_detail, name='news_detail'),
    path('news/<slug>/edit/', NewsUpdateView.as_view(), name='news_update'),
    path('news/<slug>/delete/', NewsDeleteView.as_view(), name='news_delete'),
    path('contact-us/', ContactFormView.as_view(), name='contact_page'),
    path('local-news/', LocalNewsView.as_view(), name='local_news_page'),
    path('foreign-news/', ForeignNewsView.as_view(), name='foreign_news_page'),
    path('sport-news/', SportNewsView.as_view(), name='sport_news_page'),
    path('technology-news/', TechnologyView.as_view(), name='technology_news_page'),
    path('admin-page/', admin_page, name='admin_page'),
    path('searchresult/', SearchResultsList.as_view(), name='search_results'), 
] 
