from django.urls import path, include


from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views

from api.views import CommentViewSet, GroupViewSet, PostViewSet

app_name = 'api'


router = DefaultRouter()

router.register('posts', PostViewSet, basename='post')
router.register('groups', GroupViewSet, basename='group')
router.register(r'posts/(?P<post_id>\d+)/comments', CommentViewSet, basename='comment')


urlpatterns = [
    path('api-token-auth/', views.obtain_auth_token),
    path('', include(router.urls)), 
]