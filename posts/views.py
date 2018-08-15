from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Post
from .serializers import (
    PostSerializer, CreatePostSerializer, LikePostSerializer
)


class PostPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'


class ActionBasedPermission(AllowAny):
    """
    Grant or deny access to a view, based on a mapping in view.action_permissions
    """
    def has_permission(self, request, view):
        for klass, actions in getattr(view, 'action_permissions', {}).items():
            if view.action in actions:
                return klass().has_permission(request, view)
        return False


class PostModelViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = PostPagination

    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        IsAuthenticated: ['create', 'update', 'partial_update', 'destroy'],
        AllowAny: ['list', 'retrieve']
    }

    def list(self, request, *args, **kwargs):
        """
        Return list of post with pagination. (default page_size=10)
        """
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        Get detail post instance by id.
        """
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
        Create new post.
        """
        serializer = CreatePostSerializer(data=request.data,
                                          context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(self.serializer_class(instance).data,
                        status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """
        Update post. Allowed only by post's owner.
        """
        instance = self.get_object()
        if instance.user == request.user:
            serializer = CreatePostSerializer(instance=instance,
                                              data=request.data)
            serializer.is_valid(raise_exception=True)
            updated_instance = serializer.update(instance,
                                                 serializer.validated_data)
            return Response(self.serializer_class(updated_instance).data,
                            status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, **kwargs):
        """
        Delete post. Allowed only by post's owner.
        """
        instance = self.get_object()
        if instance.user == request.user:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)

    @action(methods=['post'], detail=True, permission_classes=[IsAuthenticated],
            url_path='like', url_name='like_post')
    def like(self, request, pk=None):
        """
        Like a post.
        """
        serializer = LikePostSerializer(data={'post_id': pk},
                                        context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED)
