from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import json
import datetime

from .forms import AccountForm
from .models import User, Quizz, Question, QuestionsAnswers, Result


def page_not_found_view(request, exception):
    return render(request, "core/404.html")


def page_server_not_found(request):
    return render(request, "core/500.html")


def account_create(request):
    if not request.user.is_authenticated:
        form = AccountForm(request.POST or None)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            mail = form.cleaned_data["mail"]
            password = form.cleaned_data["password"]
            try:
                username_test = User.objects.get(username=username)
                messages.add_message(
                    request,
                    messages.WARNING,
                    "Un compte existe déjà avec ce nom d'utilisateur.\
                                      Merci d'en choisir un autre.",
                )
            except User.DoesNotExist:
                user = User.objects.create_user(username, mail, password)
                user.first_name, user.last_name = first_name, last_name
                user.save()
                login(request, user)
                return redirect("account")
    else:
        return redirect("account")

    return render(request, "account/account_create.html", locals())


@login_required(login_url="/connexion")
def account(request):

    if request.method == "POST":
        user_id = request.user.id
        user = User.objects.get(pk=user_id)
        user.delete()
        logout(request)
        return redirect("/connexion")

    return render(request, "account/account.html", locals())


def quizz(request):
    category = request.GET.get("category")
    if category:
        quizz_list = Quizz.objects.filter(category=category)
    else:
        quizz_list = Quizz.objects.all()
    if not quizz_list:
        messages.add_message(request, messages.WARNING, "Pas de quizz.")

    return render(request, "quizz/quizz.html", locals())


def unique_quizz(request, id_quizz):
    total_result = 0
    quizz = Quizz.objects.get(pk=id_quizz)
    questions = Question.objects.filter(quizz__pk=id_quizz).order_by("id")
    right_answers = QuestionsAnswers.objects.filter(
        question__in=questions, right_answer=True
    )
    if request.is_ajax and request.method == "POST":
        answer_user_id = eval(request.POST.getlist("answer_id")[0])
        for elt in answer_user_id:
            result = None
            question_answer = QuestionsAnswers.objects.filter(question__id=elt["key"])
            right_answer = list(
                question_answer.filter(right_answer=True).values_list(
                    "answer__pk", flat=True
                )
            )
            right_answer.sort()
            elt["value"].sort()
            if elt["value"] == right_answer:
                result = True
                total_result += 1
            else:
                result = False
        if total_result >= len(question_answer) / 2:
            final_result = True

        else:
            final_result = False
        response_data = {}
        final_right_answer = {}
        for answer in right_answers:
            if answer.question.pk not in final_right_answer.keys():
                final_right_answer[answer.question.pk] = [answer.answer.pk]
            else:
                final_right_answer[answer.question.pk].append(answer.answer.pk)

        result, created = Result.objects.update_or_create(
            user=request.user,
            quizz=quizz,
            defaults={
                "score": total_result,
                "last_date": datetime.datetime.now(),
                "success": final_result,
            },
        )

        response_data["right_answers"] = final_right_answer
        response_data["total_result"] = total_result
        response_data["final_result"] = final_result
        return HttpResponse(json.dumps(response_data),
                            content_type="application/json")

    return render(request, "quizz/unique_quizz.html", locals())


def results(request):
    if request.user.is_authenticated:
        results = Result.objects.filter(user=request.user)\
                 .order_by("-last_date")

    return render(request, "quizz/results.html", locals())
