from rest_framework import viewsets 
from rest_framework.response import Response
from rest_framework import status

from posts.models import Comment, Group, Post
from .exceptions import PermissionDenied
from .serializers import  CommentSerializer, GroupSerializer, PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def update(self, request, pk=None, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        if instance.author != self.request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            self.perform_update(serializer)
            return Response(status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        instance = self.get_object()
        if instance.author != self.request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)



class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class =  GroupSerializer 


class CommentViewSet(viewsets.ModelViewSet):
    pk_url_kwargs = ["post_id", "comment_id"]
    serializer_class =  CommentSerializer
    

    def get_queryset(self):
        post = Post.objects.get(id=self.kwargs['post_id'])
        return post.comments

    def perform_create(self, serializer, pk=None):
        post = Post.objects.get(id=self.kwargs['post_id'])
        serializer.save(author=self.request.user,
                        post=post)
        
    def update(self, request, pk=None, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = Post.objects.get(pk)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        if instance.author != self.request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            self.perform_update(serializer)
            return Response(status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        instance = self.get_object()
        if instance.author != self.request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


