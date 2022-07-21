from os import stat
import re
from urllib import response
from django.test import TestCase
from django.urls import reverse
from requests import delete
from rest_framework import status
from rest_framework.test import APITestCase
from crudl.apps.accounts.models import User
from .models import Song

class SongTests(APITestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.superuser = User.objects.create_superuser(
            username="admin", password="admin", email="admin@example.com"
        )
        cls.song = Song.objects.create(
            artist="Lana Del Rey",
            title="Video Games - Remastered",
            url="https://open.spotify.com/track/5UOo694cVvjcPFqLFiNWGU?si=maZ7JCJ7Rb6WzESLXg1Gdw",
        )
        cls.song_to_delete = Song.objects.create(
            artist="Milky Chance",
            title="Stolen Dance",
            url="https://open.spotify.com/track/3miMZ2IlJiaeSWo1DohXlN?si=g-xMM4m9S_yScOm02C2MLQ",
        )
    
    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()
        cls.song.delete()
        cls.superuser.delete()
    
    def test_list_songs(self):
        url = reverse('rest_song_list')
        data = {}
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], Song.objects.count())
    
    def test_get_song(self):
        url = reverse('rest_song_detail', kwargs={"pk": self.song.pk})
        data = {}
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["uuid"], str(self.song.pk))
        self.assertEqual(response.data["artist"], self.song.artist)
        self.assertEqual(response.data["title"], self.song.title)
        self.assertEqual(response.data["url"], self.song.url)
    
    def test_create_song_allowed(self):
        # Login
        self.client.force_authenticate(user=self.superuser)
        url = reverse("rest_song_list")
        data = {
            "artist": "Capital Cities",
            "title": "Safe And Sound",
            "url": "https://open.spotify.com/track/40Fs0YrUGuwLNQSaHGVfqT?si=2OUawusIT-evyZKonT5GgQ",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        song = Song.objects.filter(pk=response.data["uuid"])
        self.assertEqual(song.count(), 1)
        # Logout
        self.client.force_authenticate(user=None)
    
    def test_create_song_restricted(self):
        # Make sure the user is logged out
        self.client.force_authenticate(user=None)
        url = reverse('rest_song_list')
        data = {
            "artist": "Men I Trust",
            "title": "Tailwhip",
            "url": "https://open.spotify.com/track/2DoO0sn4SbUrz7Uay9ACTM?si=SC_MixNKSnuxNvQMf3yBBg",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_change_song_allowed(self):
        # Login
        self.client.force_authenticate(user=self.superuser)
        url = reverse('rest_song_detail', kwargs={"pk": self.song.pk})
        # Change only title
        data = {
            "artist": "Men I Trust",
            "title": "Tailwhip",
            "url": "https://open.spotify.com/track/2DoO0sn4SbUrz7Uay9ACTM?si=SC_MixNKSnuxNvQMf3yBBg",
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["uuid"], str(self.song.pk))
        self.assertEqual(response.data["artist"], self.song.artist)
        self.assertEqual(response.data["title"], self.song.title)
        self.assertEqual(response.data["url"], self.song.url)
        # Logout
        self.client.force_authenticate(user=None)
    
    def test_change_song_restricted(self):
        # Make sure the user is logged out
        self.client.force_authenticate(user=None)
        url = reverse('rest_song_detail', kwargs={"pk": self.song.pk})
        # Change only title
        data = {
            "artist": "Capital Cities",
            "title": "Safe And Sound",
            "url": "https://open.spotify.com/track/40Fs0YrUGuwLNQSaHGVfqT?si=2OUawusIT-evyZKonT5GgQ",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_delete_song_restricted(self):
        # Make sure the user is logged out
        self.client.force_authenticate(user=None)
        url = reverse("rest_song_detail", kwargs={"pk": self.song.pk})
        data = {}
        response = self.client.delete(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_delete_song_allowed(self):
        # Login
        self.client.force_authenticate(user=self.superuser)
        url = reverse('rest_song_detail', kwargs={'pk': self.song.pk})
        data = {}
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Logout
        self.client.force_authenticate(user=None)

