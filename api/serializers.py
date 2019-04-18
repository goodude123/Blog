from rest_framework import serializers
from django.contrib.auth.models import User
from cms.models import Article


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('id', 'title', 'content', 'author', 'pub_date')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        
        try:
            user.first_name = validated_data['first_name']
        except KeyError:
            pass

        try:
            user.first_name = validated_data['last_name']
        except KeyError:
            pass

        user.set_password(validated_data['password'])
        user.save()

        return user
