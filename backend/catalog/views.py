from rest_framework import views, status, generics, permissions, filters
from rest_framework.response import Response
from django.core.files.base import ContentFile
import requests
from .models import Book, Author, Publisher, Category
from .services.scraper import WafilifeScraper
from .serializers import BookSerializer, BookDetailSerializer

class ScrapeProductView(views.APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        url = request.data.get('url')
        if not url:
            return Response({'error': 'URL is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            scraper = WafilifeScraper()
            data = scraper.scrape(url)

            # 1. Handle Publisher
            publisher = None
            if data['publisher']:
                publisher, _ = Publisher.objects.get_or_create(name=data['publisher'])

            # 2. Handle Authors
            authors = []
            for auth_name in data['authors']:
                author, _ = Author.objects.get_or_create(name=auth_name)
                authors.append(author)

            # 3. Handle Categories
            categories = []
            for cat_name in data['categories']:
                category, _ = Category.objects.get_or_create(name=cat_name)
                categories.append(category)

            # 4. Create/Update Book
            book, created = Book.objects.update_or_create(
                title=data['title'],
                defaults={
                    'description': data['description'],
                    'publisher': publisher,
                    'regular_price': data['regular_price'] or 0,
                    'sale_price': data['sale_price'] or 0,
                    'page_count': data['page_count'],
                    'edition': data['edition'],
                    'language': data['language'],
                    'is_active': True
                }
            )

            book.authors.set(authors)
            book.categories.set(categories)

            # 5. Handle Image
            if data['image_url']:
                img_resp = requests.get(data['image_url'])
                if img_resp.status_code == 200:
                    book.cover_image.save(
                        f"{book.slug}.jpg",
                        ContentFile(img_resp.content),
                        save=True
                    )

            return Response(BookDetailSerializer(book).data)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class BookListView(generics.ListAPIView):
    queryset = Book.objects.filter(is_active=True)
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'authors__name', 'publisher__name', 'categories__name']
    ordering_fields = ['sale_price', 'created_at']

class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.filter(is_active=True)
    serializer_class = BookDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'
