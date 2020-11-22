from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("quizz.urls")),
]

handler404 = "quizz.views.page_not_found_view"
handler500 = "quizz.views.page_server_not_found"
