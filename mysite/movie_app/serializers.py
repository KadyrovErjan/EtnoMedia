from rest_framework import serializers
from .models import *

from rest_framework_simplejwt.tokens import RefreshToken

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('email', 'username', 'phone_number', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        if UserProfile.objects.filter(email=value).exists():
            raise serializers.ValidationError("Пользователь с таким email уже существует")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        email = validated_data.pop('email')
        username = validated_data.pop('username')
        user = UserProfile(email=email, username=username, **validated_data)
        user.set_password(password)
        user.save()
        return user

class CustomLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        try:
            user = UserProfile.objects.get(email=email)
        except UserProfile.DoesNotExist:
            raise serializers.ValidationError({"email": "Пользователь с таким email не найден"})

        if not user.check_password(password):
            raise serializers.ValidationError({"password": "Неверный пароль"})



        self.context['user'] = user
        return data

    def to_representation(self, instance):
        user = self.context['user']
        refresh = RefreshToken.for_user(user)

        return {
            'user': {
                'username': user.username,
                'email': user.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        token = attrs.get('refresh')
        try:
            RefreshToken(token)
        except Exception:
            raise serializers.ValidationError({"refresh": "Невалидный токен"})
        return attrs



class UserProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'first_name', 'last_name', 'avatar']


class UserProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'first_name', 'last_name', 'email', 'avatar', 'phone_number']


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'country']


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['id', 'first_name', 'last_name', 'photo', 'role']


class PersonDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['id', 'first_name', 'last_name', 'photo', 'role', 'film_person']


class FilmListSerializer(serializers.ModelSerializer):
    country = CountrySerializer()
    genres = GenreSerializer(many=True)
    get_avg_rating = serializers.SerializerMethodField(read_only=True)
    get_count_people = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Film
        fields = ['id', 'title', 'poster', 'year',
                  'access_type', 'is_published',
                  'country', 'genres', 'get_avg_rating', 'get_count_people']

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

    def get_count_people(self, obj):
        return obj.get_count_people()


class FilmDetailSerializer(serializers.ModelSerializer):
    country = CountrySerializer()
    genres = GenreSerializer(many=True)
    persons = PersonSerializer(many=True)

    class Meta:
        model = Film
        fields = ['id', 'title', 'description', 'poster', 'year',
                  'language', 'duration', 'video', 'trailer_url',
                  'access_type', 'rent_price', 'is_published',
                  'views_count', 'created_date',
                  'country', 'genres', 'persons']


class GenreDetailSerializer(serializers.ModelSerializer):
    film_genre = FilmListSerializer(many=True)

    class Meta:
        model = Genre
        fields = ['id', 'name', 'film_genre']



class SeriesListSerializer(serializers.ModelSerializer):
    country = CountrySerializer()
    genres = GenreSerializer(many=True)

    class Meta:
        model = Series
        fields = ['id', 'title', 'poster', 'year',
                  'language', 'access_type', 'is_published',
                  'country', 'genres']


class SeriesDetailSerializer(serializers.ModelSerializer):
    country = CountrySerializer()
    genres = GenreSerializer(many=True)
    persons = PersonSerializer(many=True)

    class Meta:
        model = Series
        fields = ['id', 'title', 'description', 'poster', 'year',
                  'language', 'video', 'trailer_url',
                  'access_type', 'is_published', 'views_count', 'created_date',
                  'country', 'genres', 'persons']

class SeasonListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Season
        fields = ['id', 'season_number', 'title', 'year']


class SeasonDetailSerializer(serializers.ModelSerializer):
    season_series = SeriesDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Season
        fields = ['id', 'season_number', 'title', 'year', 'season_series']



class CartoonListSerializer(serializers.ModelSerializer):
    country = CountrySerializer()
    genres = GenreSerializer(many=True)

    class Meta:
        model = Cartoon
        fields = ['id', 'title', 'poster', 'year',
                  'language', 'age_rating', 'access_type',
                  'is_published', 'country', 'genres']


class CartoonDetailSerializer(serializers.ModelSerializer):
    country = CountrySerializer()
    genres = GenreSerializer(many=True)

    class Meta:
        model = Cartoon
        fields = ['id', 'title', 'description', 'poster', 'year',
                  'language', 'duration', 'video_url', 'trailer_url',
                  'age_rating', 'access_type', 'is_published',
                  'views_count', 'created_date', 'country', 'genres']

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'

class FavoriteItemSerializer(serializers.ModelSerializer):
    film = FilmListSerializer(read_only=True)
    film_id = serializers.PrimaryKeyRelatedField(
        queryset=Film.objects.all(), write_only=True, required=False,
        allow_null=True, source='film'
    )

    series = SeriesListSerializer(read_only=True)
    series_id = serializers.PrimaryKeyRelatedField(
        queryset=Series.objects.all(), write_only=True, required=False,
        allow_null=True, source='series'
    )

    cartoon = CartoonListSerializer(read_only=True)
    cartoon_id = serializers.PrimaryKeyRelatedField(
        queryset=Cartoon.objects.all(), write_only=True, required=False,
        allow_null=True, source='cartoon'
    )

    class Meta:
        model = FavoriteItem
        fields = ['id', 'film', 'film_id', 'series', 'series_id',
                  'cartoon', 'cartoon_id', 'added_date']

    def validate(self, attrs):
        film = attrs.get('film')
        series = attrs.get('series')
        cartoon = attrs.get('cartoon')

        provided = [x for x in (film, series, cartoon) if x is not None]
        if len(provided) != 1:
            raise serializers.ValidationError(
                'Укажите ровно один объект: film_id, series_id или cartoon_id'
            )
        return attrs

class FavoriteSerializer(serializers.ModelSerializer):
    favorite_item = FavoriteItemSerializer(read_only=True, many=True)

    class Meta:
        model = Favorite
        fields = ['id', 'user', 'favorite_item']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

