from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    quizz_done = models.ManyToManyField('Quizz', through='Result')

    class Meta:
        verbose_name = "User"

    def __str__(self):

        return self.username

class Category(models.Model):
    name = models.CharField(max_length=150, unique=True)

    class Meta:
        verbose_name = "Catégorie"

    def __str__(self):

        return self.name

class Quizz(models.Model):
    name = models.CharField(max_length=255, unique=True)
    create_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "Quizz"

    def __str__(self):

        return self.name

class Question(models.Model):
    name = models.CharField(max_length=255, unique=True)
    question_text = models.TextField()
    create_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    quizz = models.ManyToManyField(Quizz)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "Question"

    def __str__(self):

        return self.name

class Answer(models.Model):
    name = models.CharField(max_length=255, unique=True)
    answer_text = models.TextField()
    question = models.ManyToManyField(Question, through='QuestionsAnswers')

    class Meta:
        verbose_name = "Answer"

    def __str__(self):

        return self.name

class LittleStory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    story_text = models.TextField()
    create_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "Little Story"

    def __str__(self):

        return self.name

class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    quizz = models.ForeignKey(Quizz, on_delete=models.SET_NULL, null=True)
    score = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name = "UserQuizz"

    def __str__(self):

        return f'Score de {self.user.name} sur le quizz {self.quizz.name}'

class QuestionsAnswers(models.Model):
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True)
    answer = models.ForeignKey(Answer, on_delete=models.SET_NULL, null=True)
    right_answer = models.BooleanField()

    class Meta:
        verbose_name = "QuestionsAnswers"

    def __str__(self):

        return f'{self.question} {self.answer}'        


