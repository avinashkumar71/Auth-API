from django.urls import path
from .views import (UserRegistrationViews,UserLoginView,UserProfileView,UserPasswordChange,
                    UserPasswordResetView,UserPasswordResetSubmit)
urlpatterns = [
    path('register/',UserRegistrationViews.as_view()),
    path('login/',UserLoginView.as_view()),
    path('profile/',UserProfileView.as_view()),
    path('pwdchange/',UserPasswordChange.as_view()),
    path('pwdreset/',UserPasswordResetView.as_view()),
    path('pwdresetsubmit/<uid>/<token>/',UserPasswordResetSubmit.as_view()),
]