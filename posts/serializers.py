from rest_framework import serializers
from accounts.serializers import UserSerializer
from .models import Post, Like


class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Like
        exclude = ('active', )


class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    likes = LikeSerializer(many=True, read_only=True,
                           source='get_likes')

    class Meta:
        model = Post
        fields = '__all__'


class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('text', )

    def create(self, validated_data):
        request = self.context.get('request', None)
        if not request:
            raise Exception("No 'request' in context")
        if not hasattr(request, 'user'):
            raise Exception("No 'user' in request")
        user = request.user
        return Post.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        instance.text = validated_data.get('text', instance.text)
        instance.save()
        return instance


class LikePostSerializer(serializers.Serializer):
    post_id = serializers.IntegerField(required=True)

    def validate_post_id(self, value):
        if not Post.objects.filter(pk=value).exists():
            raise serializers.ValidationError('Unknown id')
        return value

    def create(self, validated_data):
        request = self.context.get('request', None)
        if not request:
            raise Exception("No 'request' in context")
        if not hasattr(request, 'user'):
            raise Exception("No 'user' in request")
        user = request.user
        post = Post.objects.get(pk=validated_data['post_id'])
        like, created = post.likes.get_or_create(user=user)
        if not created:
            # like already exists, so just reverse activate it
            like.active = not like.active
            like.save()
        return like
