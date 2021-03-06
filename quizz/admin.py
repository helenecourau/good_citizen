from django.contrib import admin
from .models import (
    Category,
    Quizz,
    Question,
    Answer,
    Result,
    QuestionsAnswers,
    User,
)

admin.site.register(Category)
admin.site.register(Quizz)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Result)
admin.site.register(QuestionsAnswers)
admin.site.register(User)
