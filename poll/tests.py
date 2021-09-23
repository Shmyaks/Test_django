from django.test import TestCase
from django.contrib.auth import get_user_model
import requests
import random
# Create your tests here.

User = get_user_model()


class TestsDjango(TestCase):
    """После тестирования у нас будет:
        3 опроса (2 закрытых)
        5 юзеров
        15 вопросов (3 вопроса будут удалены)
        7 отчётов (5 от юзеров) (2 анонимных) (1 анонимный выполнен)
        20 ответов на опросы
    """

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = requests

    def test_a_create_user(self) -> None:
        """Создание 5 юзеров"""

        self.factory.post('http://localhost:8000/api/user',
                          json={'username': 'anton', 'password': '123456'})
        self.factory.post('http://localhost:8000/api/user',
                          json={'username': 'maxin', 'password': '123456'})
        self.factory.post('http://localhost:8000/api/user',
                          json={'username': 'dima', 'password': '123456'})
        self.factory.post('http://localhost:8000/api/user',
                          json={'username': 'egot', 'password': '123456'})
        self.factory.post('http://localhost:8000/api/user',
                          json={'username': 'leha', 'password': '123456'})

    def test_b_create_polls(self) -> None:
        '''Создание 3 опросов и изменение последнего на tilte - Четвёртый опрос'''

        self.factory.post('http://localhost:8000/api/poll',
                          data={'title': 'Первый опрос', 'description': 'Хороший опрос'})
        self.factory.post('http://localhost:8000/api/poll',
                          data={'title': 'Второй опрос', 'description': 'Хороший-средний опрос'})
        self.factory.post('http://localhost:8000/api/poll',
                          data={'title': 'Третий опрос', 'description': 'Хороший-отличный опрос'})
        self.factory.put('http://localhost:8000/api/poll/3',
                         data={'title': 'Четвёртый опрос', 'description': 'отличный опрос'})

    def test_c_create_questions(self) -> None:
        """Создание 5  в каждом опросе
           в первом один выбор.
           второй с двумя выборами
           3 рандомный текст
        """
        list_type = [1, 2, 3]

        random_words = ['Хорошо', 'Классно', 'Олично',
                        'Большие слова', 'Ещё один выбор', 'Второй выбор']
        for i in range(5):
            self.factory.post('http://localhost:8000/api/questions',
                              json={"type": 1, "chooses": [random_words[random.randint(0, len(random_words)-1)]], "poll_id": 1, 'question': requests.get("https://fish-text.ru/get").json()['text']})

        for i in range(5):
            self.factory.post('http://localhost:8000/api/questions',
                              json={"type": 2, "chooses": [random_words[random.randint(0, len(random_words)-1)],
                                                           random_words[random.randint(0, len(random_words)-1)]], "poll_id": 2, 'question': requests.get("https://fish-text.ru/get").json()['text']})

        for i in range(5):
            self.factory.post('http://localhost:8000/api/questions',
                              json={"type": 3, 'chooses': [" "], "poll_id": 3, 'question': requests.get("https://fish-text.ru/get").json()['text']})

    def test_d_delete_questions(self) -> None:
        """Удаление одного вопроса в каждом опроснике"""
        for i in range(1, 4):
            self.factory.delete(f'http://localhost:8000/api/questions/{i*5}')

    def test_e_start_report(self) -> None:
        """Создание начало опроса
           Каждый юзер начнёт по одному рандомному опросу.
           Последние два будут анонимно
           В сумме 7 отчётов
        """

        random_polls = [1, 2, 3]

        self.factory.post('http://localhost:8000/api/report/start',
                          json={'owner': '1', 'poll_id': random_polls[random.randint(0, len(random_polls)-1)]})
        self.factory.post('http://localhost:8000/api/report/start',
                          json={'owner': '2', 'poll_id': random_polls[random.randint(0, len(random_polls)-1)]})
        self.factory.post('http://localhost:8000/api/report/start',
                          json={'owner': '3', 'poll_id': random_polls[random.randint(0, len(random_polls)-1)]})
        self.factory.post('http://localhost:8000/api/report/start',
                          json={'owner': '4', 'poll_id': random_polls[random.randint(0, len(random_polls)-1)]})
        self.factory.post('http://localhost:8000/api/report/start',
                          json={'owner': '5', 'poll_id': random_polls[random.randint(0, len(random_polls)-1)]})
        self.factory.post('http://localhost:8000/api/report/start',
                          json={'poll_id': random_polls[random.randint(0, len(random_polls)-1)]})
        self.factory.post('http://localhost:8000/api/report/start',
                          json={'poll_id': random_polls[random.randint(0, len(random_polls)-1)]})

    def test_f_close_report(self) -> None:
        """Один анонимный пользователь закончит проходить опрос"""
        self.factory.patch('http://localhost:8000/api/report/6',
                           json={"completed": True})

    def test_g_answer_to_report(self) -> None:
        """Каждый юзер ответит на свои вопросы"""
        for i in range(1, 8):
            response = self.factory.get(
                f'http://localhost:8000/api/user/{i}/report').json()

            # Получаем все ответы
            answers = [answer
                       for answer in response['reports'][0]['answers']]

            questions = [answer['question']
                         for answer in answers]

            for j in range(0, len(answers)):
                words = [word['words'] for word in questions[j]['chooses']]
                id = answers[j]['id']
                word = words[random.randint(0, len(
                    words)-1)] if questions[j]['type'] == 1 or questions[j]['type'] == 2 else requests.get("https://fish-text.ru/get").json()['text']
                self.factory.put(
                    f'http://localhost:8000/api/answer/{id}', json={'ans': word})

    def test_h_close_poll(self) -> None:
        """Закроем 2 опроса из 3"""
        self.factory.put('http://localhost:8000/api/poll/1/close')
        self.factory.put('http://localhost:8000/api/poll/2/close')
