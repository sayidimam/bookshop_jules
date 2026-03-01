from django.test import TestCase
from django.utils.text import slugify
from .models import Book

class BookSlugTestCase(TestCase):
    def test_slug_generation(self):
        """Test that a slug is automatically generated from the title."""
        book = Book.objects.create(
            title="Test Book",
            regular_price=100.00
        )
        self.assertEqual(book.slug, slugify("Test Book"))

    def test_unique_slug_generation(self):
        """Test that multiple books with the same title get unique slugs."""
        book1 = Book.objects.create(title="Duplicate Title", regular_price=100.00)
        book2 = Book.objects.create(title="Duplicate Title", regular_price=100.00)
        book3 = Book.objects.create(title="Duplicate Title", regular_price=100.00)

        base_slug = slugify("Duplicate Title")
        self.assertEqual(book1.slug, base_slug)
        self.assertEqual(book2.slug, f"{base_slug}-1")
        self.assertEqual(book3.slug, f"{base_slug}-2")

    def test_manual_slug(self):
        """Test that providing a slug manually prevents auto-generation."""
        custom_slug = "my-custom-slug"
        book = Book.objects.create(
            title="Test Book",
            slug=custom_slug,
            regular_price=100.00
        )
        self.assertEqual(book.slug, custom_slug)

    def test_slug_stability(self):
        """Test that updating a book's title does not change its existing slug."""
        book = Book.objects.create(title="Original Title", regular_price=100.00)
        original_slug = book.slug

        book.title = "Updated Title"
        book.save()

        self.assertEqual(book.slug, original_slug)

    def test_non_ascii_title_slug(self):
        """Test slug generation with non-ASCII characters (e.g., Bangla)."""
        # Django's default slugify returns an empty string for non-ASCII if allow_unicode=False
        title = "বই"
        book1 = Book.objects.create(title=title, regular_price=100.00)

        # If slugify("বই") is "", slug will be ""
        # If we create another one, it should be "-1"
        book2 = Book.objects.create(title=title, regular_price=100.00)

        self.assertNotEqual(book1.slug, book2.slug)
        self.assertTrue(book2.slug.startswith(book1.slug))
