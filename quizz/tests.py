from django.test import TestCase, Client
from django.urls import reverse
from .models import User, Quizz, Question, Answer, QuestionsAnswers, Result


class SetUp(TestCase):
    def setUp(self):

        user = User.objects.create_user("helene",
                                        "helene@test.com",
                                        "helenecouraupwd")

        quizz = Quizz.objects.create(id=1, name="Quizz")
        Quizz.objects.create(id=2, name="Quizz2")

        question = Question.objects.create(
            id=1, name="Question 1", question_text="Lorem ipsum"
        )
        answer1 = Answer.objects.create(id=1,
                                        name="Answer1",
                                        answer_text="Lorem ipsum")
        QuestionsAnswers.objects.create(
            question=question, answer=answer1, right_answer=True
        )
        answer2 = Answer.objects.create(id=2,
                                        name="Answer2",
                                        answer_text="Lorem ipsum")
        QuestionsAnswers.objects.create(
            question=question, answer=answer2, right_answer=False
        )
        question.quizz.add(quizz)

        question2 = Question.objects.create(
            id=2, name="Question 2", question_text="Lorem ipsum"
        )
        answer3 = Answer.objects.create(id=3,
                                        name="Answer3",
                                        answer_text="Lorem ipsum")
        QuestionsAnswers.objects.create(
            question=question2, answer=answer3, right_answer=True
        )
        answer4 = Answer.objects.create(id=4,
                                        name="Answer4",
                                        answer_text="Lorem ipsum")
        QuestionsAnswers.objects.create(
            question=question2, answer=answer4, right_answer=False
        )
        question2.quizz.add(quizz)

        Result.objects.create(
            id=1, user=user,
            quizz=quizz,
            score=2,
            last_date="2020-01-01",
            success=True
        )


class HomePageTestCase(TestCase):
    def test_home_page(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)


class ConnectPageTestCase(SetUp):
    def test_displays_connect_page(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)

    def test_connect_page_redirects_after_connexion(self):
        c = Client()
        response = c.post(
            "/connexion", {"username": "helene", "password": "helenecouraupwd"}
        )
        response = c.get("/mon-compte", follow=True)
        self.assertEqual(response.status_code, 200)

    def test_connect_page_returns_302_if_connected(self):
        c = Client()
        response = c.post(
            "/connexion", {"username": "helene", "password": "helenecouraupwd"}
        )
        self.assertEqual(response.status_code, 302)

    def test_connect_page_returns_200_if_not_valid_username(self):
        c = Client()
        response = c.post(
            "/connexion",
            {"username": "helene2",
             "password": "helenecouraupwd"}
        )
        self.assertEqual(response.status_code, 200)

    def test_connect_page_returns_200_if_not_valid_password(self):
        c = Client()
        response = c.post(
            "/connexion",
            {"username": "helene",
             "password": "helenecouraupwd2"}
        )
        self.assertEqual(response.status_code, 200)


class CreateAccountPageTestCase(SetUp):
    def test_display_register_page(self):
        c = Client()
        response = c.get("/creer-compte")
        self.assertEqual(response.status_code, 200)

    def test_register_page_returns_302_if_connected(self):
        c = Client()
        response = c.post(
            "/connexion", {"username": "helene", "password": "helenecouraupwd"}
        )
        self.assertEqual(response.status_code, 302)

    def test_register_page_returns_200_if_not_valid_mail(self):
        c = Client()
        response = c.post(
            "/creer-compte",
            {
                "first_name": "helene2",
                "last_name": "courau2",
                "username": "helene2",
                "mail": "courau2",
                "password": "helenecouraupwd2",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(first_name="helene2").exists())

    def test_register_page_returns_200_if_user_already_exists(self):
        c = Client()
        response = c.post(
            "/creer-compte",
            {
                "first_name": "helene2",
                "last_name": "courau",
                "username": "helene",
                "mail": "helene@test.com",
                "password": "helenecouraupwd",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(first_name="helene2").exists())

    def test_register_success_create_new_user_in_db(self):
        c = Client()
        c.post(
            "/creer-compte",
            {
                "first_name": "helene3",
                "last_name": "courau3",
                "username": "helene3",
                "mail": "helene3@test.com",
                "password": "helenecouraupwd",
            },
        )
        user = User.objects.get(username="helene3")
        self.assertEqual(user.username, "helene3")


class AccountPageTestCase(SetUp):
    def test_account_page_if_connected(self):
        c = Client()
        response = c.post(
            "/connexion", {"username": "helene", "password": "helenecouraupwd"}
        )
        response = c.get("/mon-compte")
        self.assertEqual(response.status_code, 200)

    def test_account_page_if_not_connected(self):
        response = self.client.get(reverse("account"))
        self.assertEqual(response.status_code, 302)

    def test_delete_account(self):
        c = Client()
        user = User.objects.get(username="helene")
        c.post("/connexion",
               {"username": "helene",
                "password": "helenecouraupwd"})
        c.post("/mon-compte", {"id": user.id})
        self.assertFalse(User.objects.filter(pk=user.id).exists())


class QuizzPageTestCase(SetUp):
    def test_quizz_page_not_connected(self):
        c = Client()
        response = c.get("/quizz/")
        self.assertEqual(response.status_code, 200)

    def test_quizz_page_connected(self):
        c = Client()
        c.post("/connexion",
               {"username": "helene",
                "password": "helenecouraupwd"})
        response = c.get("/quizz/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["quizz_list"]), 2)


class UniqueQuizzPageTestCase(SetUp):
    def test_quizz_page_not_connected(self):
        c = Client()
        response = c.get("/quizz/1")
        self.assertEqual(response.status_code, 200)

    def test_quizz_page_connected(self):
        c = Client()
        c.post("/connexion",
               {"username": "helene",
                "password": "helenecouraupwd"})
        response = c.get("/quizz/1")
        self.assertEqual(response.status_code, 200)

    def test_good_answer(self):
        c = Client()
        c.post("/connexion",
               {"username": "helene",
                "password": "helenecouraupwd"})
        response = c.post(
            "/quizz/1", {"answer_id":
                         ['[{"key":1,"value":[1]},{"key":2,"value":[3]}]']}
        )
        user_id = User.objects.get(username="helene").id
        result = Result.objects.get(user=user_id, quizz=1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["total_result"], 2)
        self.assertEqual(response.json()["final_result"], True)
        self.assertEqual(result.score, 2)

    def test_one_bad_answer(self):
        c = Client()
        c.post("/connexion",
               {"username": "helene",
                "password": "helenecouraupwd"})
        response = c.post(
            "/quizz/1",
            {"answer_id": ['[{"key":1,"value":[1,2]},{"key":2,"value":[3]}]']},
        )
        user_id = User.objects.get(username="helene").id
        result = Result.objects.get(user=user_id, quizz=1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["total_result"], 1)
        self.assertEqual(response.json()["final_result"], True)
        self.assertEqual(result.score, 1)

    def test_all_bad_answer(self):
        c = Client()
        c.post("/connexion",
               {"username": "helene",
                "password": "helenecouraupwd"})
        response = c.post(
            "/quizz/1", {"answer_id":
                         ['[{"key":1,"value":[2]},{"key":2,"value":[4]}]']}
        )
        user_id = User.objects.get(username="helene").id
        result = Result.objects.get(user=user_id, quizz=1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["total_result"], 0)
        self.assertEqual(response.json()["final_result"], False)
        self.assertEqual(result.score, 0)


class ResultTestCase(SetUp):
    def test_quizz_page_not_connected(self):
        c = Client()
        response = c.get("/resultats")
        self.assertEqual(response.status_code, 200)

    def test_quizz_page_connected(self):
        c = Client()
        c.post("/connexion",
               {"username": "helene",
                "password": "helenecouraupwd"})
        response = c.get("/resultats")
        self.assertEqual(response.status_code, 200)

    def test_good_answer(self):
        c = Client()
        c.post("/connexion",
               {"username": "helene",
                "password": "helenecouraupwd"})
        response = c.get("/resultats")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["results"]), 1)
