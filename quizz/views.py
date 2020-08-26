from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from django.core.paginator import Paginator, EmptyPage

from .forms import AccountForm
from .models import User, Quizz, Question, Answer, QuestionsAnswers

def account_create(request):
    if not request.user.is_authenticated:
        form = AccountForm(request.POST or None)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            mail = form.cleaned_data['mail']
            password = form.cleaned_data['password']
            try:
                username_test = User.objects.get(username=username)
                messages.add_message(request, messages.WARNING,
                                     "Un compte existe déjà avec ce nom d'utilisateur.\
                                      Merci d'en choisir un autre.")
            except User.DoesNotExist:
                user = User.objects.create_user(username, mail, password)
                user.first_name, user.last_name = first_name, last_name
                user.save()
                login(request, user)
                return redirect('account')
    else:
        return redirect('account')

    return render(request, 'account_create.html', locals())

@login_required(login_url='/connexion')
def account(request):
    
    if request.method == 'POST':
        user_id = request.user.id
        user = User.objects.get(pk=user_id)
        user.delete()
        logout(request)
        return redirect('/connexion')

    return render(request, 'account.html', locals())

def quizz(request):
    category = request.GET.get('category')
    if category:
        quizz_list = Quizz.objects.filter(category=category)
    else:
        quizz_list = Quizz.objects.all()
    if not quizz_list:
        messages.add_message(request, messages.WARNING,
                             "Pas de quizz.")

    return render(request, 'quizz/quizz.html', locals())

def unique_quizz(request, id):
    questions = Question.objects.filter(quizz__pk=id).order_by('id')
    paginator = Paginator(questions, 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    total_result = 0
    if request.method == 'POST':
        answer_user_id = request.POST.getlist('answer_id')
        question_id = page_obj.object_list[0].id
        question_answer = QuestionsAnswers.objects.filter(question__id=question_id)
        answer_user = question_answer.filter(answer__id__in=answer_user_id).values_list('right_answer', flat=True)
        right_answer = question_answer.filter(right_answer=True)
        if False in answer_user:
            result = False
        else:
            result = True
        if result == False:
            messages.add_message(request, messages.WARNING,
                                 ("Aïe! Ce n'était pas tout à fait ça. La bonne réponse est " + right_answer[0].answer.answer_text))
        if result == True:
            total_result += 1
            messages.add_message(request, messages.WARNING,
                                 "Bravo! C'était la bonne réponse !")
    
    return render(request, 'quizz/unique_quizz.html', {'page_obj': page_obj})