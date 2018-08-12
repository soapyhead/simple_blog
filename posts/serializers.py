from rest_framework import serializers
from .models import Post, Like


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


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
