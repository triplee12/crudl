import json
from unittest import mock
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Idea

class JSSetLikeViewTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super(JSSetLikeViewTest, cls).setUpClass()

        cls.idea = Idea.objects.create(
            title = "Ebuka Pops",
            content = "If you want to see something spectacular, come to Barcelona, Catalonia, Spain and visit Park Güell. Located on a hill, Park Güell is a public park with beautiful gardens and organic architectural elements.",
            picture = "ideas/2022/06/6de2c473-72f9-495a-950a-7ac05e6ebaed.jpg"
        )
        cls.content_type = ContentType.objects.get_for_model(Idea)
        cls.superuser = User.objects.create_superuser(username="blockdev", password="blockdev", email="blockdev@crudl.com")
    
    @classmethod
    def tearDownClass(cls) -> None:
        super(JSSetLikeViewTest, cls).tearDownClass()
        cls.idea.delete()
        cls.superuser.delete()
    
    def test_authenticated_json_set_like(self):
        from .views import json_set_like

        mock_request = mock.Mock()
        mock_request.user = self.superuser
        mock_request.method = "POST"
        response = json_set_like(mock_request, self.content_type.pk, self.idea.pk)
        expected_result = json.dumps({"success": True, "action": "add", "count": Idea.objects.count()})
        self.assertJSONEqual(response.content, expected_result)
    
    @mock.patch("django.contrib.auth.models.User")
    def test_anonymous_json_set_like(self, MockUser):
        from .views import json_set_like

        anonymous_user = MockUser()
        anonymous_user.is_authenticated = False
        mock_request = mock.Mock()
        mock_request.user = anonymous_user
        mock_request.method = 'POST'
        response = json_set_like(mock_request, self.content_type.pk, self.idea.pk)
        expected_result = json.dumps({"success": False})
        self.assertJSONEqual(response.content, expected_result)
