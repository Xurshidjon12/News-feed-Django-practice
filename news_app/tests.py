from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User

from .models import Category, Comment, Contact, News


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


class NewsDetailCommentCountTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="commenter", password="test-password")
        self.news = News.objects.create(
            title="News",
            slug="news",
            body="News body",
            image="news/images/news.jpg",
            category=Category.objects.create(name="Local"),
            status=News.Status.PUBLISH,
        )
        self.url = reverse("news_detail", args=[self.news.slug])

    def test_count_matches_displayed_comments(self):
        self.assertContains(self.client.get(self.url), "Izohlar soni: 0")
        Comment.objects.create(news=self.news, user=self.user, body="Visible")
        Comment.objects.create(news=self.news, user=self.user, body="Inactive", active=False)

        response = self.client.get(self.url)

        self.assertContains(response, "Izohlar soni: 2")
        self.assertContains(response, "Visible")
        self.assertContains(response, "Inactive")

    def test_count_updates_after_submitting_comment(self):
        self.client.force_login(self.user)

        response = self.client.post(self.url, {"body": "New comment"})

        self.assertContains(response, "Izohlar soni: 1")
        self.assertContains(response, "New comment")


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
