from django.core.exceptions import PermissionDenied

from rest_framework import viewsets 
from rest_framework.response import Response
from rest_framework import status

from api.serializers import  CommentSerializer, GroupSerializer, PostSerializer
from posts.models import Group, Post


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied(PermissionError)
        super().perform_update(serializer)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied(PermissionError)
        return super().perform_destroy(instance)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class =  GroupSerializer 


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class =  CommentSerializer
    
    def get_queryset(self):
        return Post.objects.get(id=self.kwargs['post_id']).comments

    def perform_create(self, serializer):
        post = Post.objects.get(id=self.kwargs['post_id'])
        serializer.save(author=self.request.user,
                        post=post) 
        
    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied(PermissionError)
        super().perform_update(serializer)
        
    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied(PermissionError)
        return super().perform_destroy(instance)
