from django.urls import path
from .views import (
    CreateUser,
    LoginUser,
    PasswordResetRequestView,
    PasswordResetView,
    # VideoUploadPageView,
    VideoUploadView,
    VideoViewer,
)

urlpatterns = [
    path("signup/", CreateUser.as_view(), name="signup"),
    path("login/", LoginUser.as_view(), name="login"),
    path(
        "request-password-reset/",
        PasswordResetRequestView.as_view(),
        name="request-password-reset",
    ),
    path("reset-password/", PasswordResetView.as_view(), name="reset-password"),
    path("upload-video/", VideoUploadView.as_view(), name="upload-video"),
    # path("upload/", VideoUploadPageView.as_view(), name="upload"),
    path('video/', VideoViewer.as_view(), name='video-viewer'),
    path('video/<int:id>/', VideoViewer.as_view(), name='video-viewer'),
]
