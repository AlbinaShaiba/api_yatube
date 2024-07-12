from django.shortcuts import get_object_or_404
from rest_framework import viewsets 
from rest_framework.response import Response
from rest_framework import status

from posts.models import Group, Post
from .serializers import  CommentSerializer, GroupSerializer, PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def update(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != self.request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().update(request)

    def destroy(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != self.request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class =  GroupSerializer 


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class =  CommentSerializer
    
    def get_queryset(self):
        post = Post.objects.get(id=self.kwargs['post_id'])
        return post.comments

    def perform_create(self, serializer):
        post = Post.objects.get(id=self.kwargs['post_id'])
        serializer.save(author=self.request.user,
                        post=post) 
        
    def update(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.author != self.request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().update(request)
        
    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.author != self.request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request)
