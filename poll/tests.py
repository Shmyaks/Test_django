from django.test import TestCase
from django.contrib.auth import get_user_model
from django.test import RequestFactory
from .models import Poll
import requests
# Create your tests here.

User = get_user_model()


class TestsDjango(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = requests

    def test_start(self) -> None:
        c = self.factory
        c.post('http://localhost:8000/api/poll',
               data={'title': 'Первый опрос', 'description': 'Хороший опрос'})
        c.post('http://localhost:8000/api/poll',
               data={'title': 'Второй опрос', 'description': 'Хороший-средний опрос'})
        c.post('http://localhost:8000/api/poll',
               data={'title': 'Третий опрос', 'description': 'Хороший-отличный опрос'})

        c.put('http://localhost:8000/api/poll/3',
              data={'title': 'Замена опрос', 'description': 'Замена опрос'})

        response = c.get('http://localhost:8000/api/poll')

        for i in range(5):
            c.post('http://localhost:8000/api/questions',
                   json={"type": 1, "text": ["а опрос"], "poll_id": 1})

        for i in range(5):
            c.post('http://localhost:8000/api/questions',
                   json={"type": 2, "text": ["б опрос", "i love", "dsadsa"], "poll_id": 2})

        for i in range(5):
            c.post('http://localhost:8000/api/questions',
                   json={"type": 3, 'text': [" опрос текст вф выф выф выф фы фыв"], "poll_id": 3})

        response = c.get('http://localhost:8000/api/questions/3')

        response = c.get('http://localhost:8000/api/questions/5')

        response = c.get('http://localhost:8000/api/questions/10')

        response = c.put('http://localhost:8000/api/questions/13',
                         json={'type': 1, 'text': ['100 опрос'], 'poll_id': 1})

        response = c.delete('http://localhost:8000/api/questions/5')

        response = c.post('http://localhost:8000/api/report/start',  # Нужно начального юзера (Admin)
                          data={'owner': '1', 'poll_id': '1'})

        response = c.post('http://localhost:8000/api/report/start',
                          data={'poll_id': '2'})

        response = c.post(
            'http://localhost:8000/api/report/start', data={'poll_id': '2'})

        response = c.get('http://localhost:8000/api/report/2')

        response = c.delete('http://localhost:8000/api/report/3')

        response = c.get("http://localhost:8000/api/user/1/report")

        response = c.patch(
            "http://localhost:8000/api/answer/1", data={'ans': '12345'})

        response = c.put('http://localhost:8000/api/poll/1/close')
