from django.urls import path
from .views import ScrapeProductView, BookListView, BookDetailView

urlpatterns = [
    path('scrape/', ScrapeProductView.as_view(), name='scrape-product'),
    path('books/', BookListView.as_view(), name='book-list'),
    path('books/<slug:slug>/', BookDetailView.as_view(), name='book-detail'),
]
