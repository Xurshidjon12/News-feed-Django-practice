from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import Category, Contact, News


class ContactFormSubmissionTests(TestCase):
    def test_contact_form_submission_is_saved(self):
        response = self.client.post(
            reverse("contact_page"),
            {
                "name": "Test visitor",
                "email": "visitor@example.com",
                "message": "I would like to get in touch.",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Contact.objects.count(), 1)
        self.assertEqual(Contact.objects.get().email, "visitor@example.com")


class HomePageTests(TestCase):
    def test_published_news_from_admin_is_shown_on_homepage(self):
        category = Category.objects.create(name="Technology")
        image = SimpleUploadedFile(
            "news.jpg", b"file contents", content_type="image/jpeg"
        )
        News.objects.create(
            title="Admin news",
            slug="admin-news",
            body="News body",
            image=image,
            category=category,
            status=News.Status.PUBLISH,
        )

        response = self.client.get(reverse("home_page"))

        self.assertContains(response, "Admin news")

    def test_published_mahalliy_news_is_shown_in_local_section(self):
        category = Category.objects.create(name="mahalliy")
        image = SimpleUploadedFile(
            "local-news.jpg", b"file contents", content_type="image/jpeg"
        )
        News.objects.create(
            title="Local admin news",
            slug="local-admin-news",
            body="Local news body",
            image=image,
            category=category,
            status=News.Status.PUBLISH,
        )

        response = self.client.get(reverse("home_page"))

        self.assertContains(response, "Local admin news")

    def test_published_technology_news_is_shown_in_technology_section(self):
        category = Category.objects.create(name="Texnalogiya")
        image = SimpleUploadedFile(
            "technology-news.jpg", b"file contents", content_type="image/jpeg"
        )
        News.objects.create(
            title="Technology admin news",
            slug="technology-admin-news",
            body="Technology news body",
            image=image,
            category=category,
            status=News.Status.PUBLISH,
        )

        response = self.client.get(reverse("home_page"))

        self.assertContains(response, "Technology admin news")
