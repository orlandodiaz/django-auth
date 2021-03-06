"""djangoauth URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path

from users.views import RegisterView, LoginView, PreferencesView, activate, IndexView, SendEmailVerification

urlpatterns = [
    path('admin/', admin.site.urls),
    path('verify_email/', SendEmailVerification.as_view(), name='send-email-verification'),
    path('auth/', include('django.contrib.auth.urls')),
    path('login/', LoginView.as_view(), name='login'),

    # path('logout/', LogoutView.as_view(), name="logout"),
    path('register/', RegisterView.as_view(), name='register'),
    path('preferences/', PreferencesView.as_view(), name='preferences'),
    # path('preferences/update', PreferencesView.as_view(), name='update-profile'),

    path('', IndexView.as_view(), name='home'),

    # path('activate/<uidb64>/<token>', activate, name="activate"),

    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            activate, name='activate'),
]


from django.conf import settings
from django.urls import include, path  # For django versions from 2.0 and up

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),

        # For django versions before 2.0:
        # url(r'^__debug__/', include(debug_toolbar.urls)),

    ] + urlpatterns