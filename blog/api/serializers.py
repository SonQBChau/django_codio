from rest_framework import serializers
from blog.models import Post, Tag
from blango_auth.models import User

from django.utils.text import slugify


def is_capitalized(value):
    if value[0].lower() == value[0]:
        raise serializers.ValidationError("Value must be capitalized")


# class UserSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     email = serializers.EmailField(required=False)
#     first_name = serializers.CharField(
#         max_length=20, required=False, validators=[is_capitalized]
#     )
#     last_name = serializers.CharField(
#         max_length=20, required=False, validators=[is_capitalized]
#     )
#     password = serializers.CharField(write_only=True, required=False)
#     join_date = serializers.DateTimeField(read_only=True)

#     def create(self, validated_data):
#         return User(**validated_data)

#     def update(self, instance, validated_data):
#         for key, value in validated_data.items():
#             setattr(instance, key, value)
#         return instance

#     def validate_email(self, value):
#         value = value.lower()
#         domain = value.split("@")[
#             1
#         ]  # safe to do since we know value is valid email address
#         if domain != "example.com":
#             raise serializers.ValidationError("domain must be example.com")
#         return value

#     def validate(self, data):
#         if (not data.get("first_name")) != (not data.get("last_name")):
#             raise serializers.ValidationError(
#                 "first_name and last_name must be provided together"
#             )
#         return data


# class PostSerializer(serializers.ModelSerializer):
#     slug = serializers.SlugField(required=False)
#     autogenerate_slug = serializers.BooleanField(
#         required=False, write_only=True, default=False
#     )

#     class Meta:
#         model = Post
#         exclude = ["modified_at", "created_at"]

#     def validate(self, data):
#         if not data.get("slug"):
#             if data.get("autogenerate_slug"):
#                 data["slug"] = slugify(data["title"])
#                 del data["autogenerate_slug"]
#             else:
#                 raise serializers.ValidationError(
#                     "slug is required if autogenerate_slug is not set"
#                 )

#         return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]


class PostSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(
        slug_field="value", many=True, queryset=Tag.objects.all()
    )
    author = serializers.HyperlinkedRelatedField(
        queryset=User.objects.all(), view_name="api_user_detail", lookup_field="email"
    )

    class Meta:
        model = Post
        fields = "__all__"
        readonly = ["modified_at", "created_at"]
