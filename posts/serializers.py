from django.conf import settings
from rest_framework import serializers
from blog_backend.tools import upload_file
from accounts.serializers import UserSerializer
from .models import Post, Like, MediaFile, Link


class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Like
        exclude = ('id', 'active', )


class MediaFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaFile
        fields = '__all__'


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    likes = LikeSerializer(many=True, read_only=True,
                           source='get_likes')
    media_files = MediaFileSerializer(many=True, read_only=True)
    links = LinkSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = '__all__'


class CreatePostSerializer(serializers.ModelSerializer):
    media_files = serializers.ListField(
        child=serializers.FileField(max_length=64),
        required=False,
    )
    links = serializers.ListField(
        child=serializers.CharField(max_length=255),
        required=False
    )

    class Meta:
        model = Post
        fields = ('text', 'media_files', 'links')

    def validate_media_files(self, media_files):
        for file in media_files:
            fname, file_ext = file.name.split('.')
            if file_ext.lower() not in settings.ALLOWED_MEDIA_FORMATS:
                raise serializers.ValidationError(
                    f"{file_ext} - not allowed media format"
                )
        return media_files

    @staticmethod
    def handle_uploaded_file(file, post):
        try:
            upload_file(file, str(post.id))
            post.media_files.create(file=file, filename=file.name)
        except Exception as e:
            raise e

    def create(self, validated_data):
        request = self.context.get('request', None)
        if not request:
            raise Exception("No 'request' in context")
        if not hasattr(request, 'user'):
            raise Exception("No 'user' in request")
        user = request.user
        instance = Post.objects.create(user=user, text=validated_data['text'])

        # TODO: do this async with Celery
        files = validated_data['media_files']
        if files:
            for file in files:
                instance.media_files.create(file=file, filename=file.name)
        links = validated_data['links']
        if links:
            for link in links:
                instance.links.create(link=link)
        return instance

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
            # like already exists, so just reverse active it
            like.active = not like.active
            like.save()
        return like
