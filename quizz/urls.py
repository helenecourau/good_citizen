from django.conf.urls import url
from django.views.generic import TemplateView
from django.urls import path , reverse_lazy
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', TemplateView.as_view(template_name='core/home.html'),
         name="home"),
    path('accueil',  TemplateView.as_view(template_name='core/home.html'),
        name="home"),
    path('creer-compte', views.account_create, name="account_create"),
    path('connexion',
        auth_views.LoginView.as_view(template_name='connect.html', redirect_authenticated_user=True), 
        name='login'),
    path('changer-mdp',
        auth_views.PasswordChangeView.as_view(template_name='change_pwd.html', success_url='connexion'),
        name='pwd_change'),
    path('reset-mdp',
        auth_views.PasswordResetView.as_view(template_name='reset_pwd.html', email_template_name='reset_email.html'),
        name='reset_pwd'),
    path('reset-mdp-envoye',
        auth_views.PasswordResetDoneView.as_view(template_name='reset_pwd_sent.html'),
        name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name='reset_pwd_confirm.html'),
        name='password_reset_confirm'),
    path('reset-mdp-termine',
        auth_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete'),
    path('deconnexion', auth_views.LogoutView.as_view(), name='deconnexion'),
    path('mon-compte', views.account, name='account'),
    url('mentions-legales',
        TemplateView.as_view(template_name='legal.html')),
    url(r'^quizz/$', views.quizz, name='quizz'),
    path('quizz/<int:id_quizz>', views.unique_quizz, name='quizz_page'),
    ]