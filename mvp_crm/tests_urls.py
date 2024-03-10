import unittest
from django.urls import reverse, resolve
from django.test import SimpleTestCase
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from users.auth import CustomObtainAuthToken


class TestURLPatterns(SimpleTestCase):
    def test_admin_url_resolves(self):
        url = reverse('admin:index')
        resolved = resolve(url)
        self.assertEqual(resolved.view_name, 'admin:index')
        self.assertEqual(resolved.url_name, 'index')

    def test_api_url_resolves(self):
        url = reverse('api-root')
        resolved = resolve(url)
        self.assertEqual(resolved.url_name, 'api-root')
        self.assertIsNotNone(resolved.func)

    def test_schema_url_resolves(self):
        url = reverse('schema')
        resolved = resolve(url)
        self.assertEqual(resolved.view_name, 'schema')
        self.assertEqual(resolved.func.view_class, SpectacularAPIView)

    def test_docs_url_resolves(self):
        url = reverse('docs')
        resolved = resolve(url)
        self.assertEqual(resolved.view_name, 'docs')
        self.assertEqual(resolved.func.view_class, SpectacularSwaggerView)