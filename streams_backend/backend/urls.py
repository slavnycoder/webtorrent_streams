from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from knox import views as knox_views
from rest_framework.routers import DefaultRouter

from backend import settings
from common.views.health import health_view
from common.views.settings import ws_settings
from streams.views import on_publish_view, on_publish_done_view
from users.views import ChannelsViewSet, LoginView, UserViewSet, ChannelPanels

if settings.PUBLISHER:
    urlpatterns = [
        path('on_publish/', on_publish_view),
        path('on_publish_done/', on_publish_done_view),
    ]
else:
    router = DefaultRouter()
    router.register('channels', ChannelsViewSet, 'channels')
    router.register('channel-panels', ChannelPanels, 'channel-panels')
    router.register('users', UserViewSet, 'users')
    urlpatterns = [
        path('admin/', admin.site.urls),
        path('api/auth/login/', LoginView.as_view(), name='knox_login'),
        path('api/auth/logout/', knox_views.LogoutAllView.as_view(), name='knox_logout'),
        path('api/settings/', ws_settings),
        path('api/', include(router.urls)),
        path('health/', health_view),
    ]

    if settings.DEBUG:
        import debug_toolbar

        urlpatterns.append(path('api/api-auth/', include('rest_framework.urls', namespace='rest_framework')))
        urlpatterns += staticfiles_urlpatterns()
        urlpatterns = [path('__debug__/', include(debug_toolbar.urls)), *urlpatterns]
