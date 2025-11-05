from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from pos import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Authentication
    path('login/', auth_views.LoginView.as_view(template_name='pos/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='pos/logout_confirm.html', next_page='login'), name='logout'),

    # App routes
    path('', views.index, name='index'),
    path('', include('pos.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)