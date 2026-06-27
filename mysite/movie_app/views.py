from django.contrib.auth.models import AnonymousUser
from rest_framework import viewsets, generics, permissions, status
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from .filters import FilmFilter
from .pagination import FilmPagination
from .permissions import CheckSubscription, CheckUser


from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CustomLoginView(generics.GenericAPIView):
    serializer_class = CustomLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            refresh_token = serializer.validated_data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response({'detail': 'Невалидный токен'}, status=status.HTTP_400_BAD_REQUEST)



class UserProfileListAPIView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileListSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)


class UserProfileDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileDetailSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)


class GenreAPIView(generics.ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class GenreDetailAPIView(generics.RetrieveAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreDetailSerializer


class PersonListAPIView(generics.ListAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


class PersonDetailAPIView(generics.RetrieveAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonDetailSerializer


class CountryListAPIView(generics.ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class CountryDetailAPIView(generics.RetrieveAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

class FilmListAPIView(generics.ListAPIView):
    queryset = Film.objects.all()
    serializer_class = FilmListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = FilmFilter
    pagination_class = FilmPagination


class FilmDetailAPIView(generics.RetrieveAPIView):
    queryset = Film.objects.all()
    serializer_class = FilmDetailSerializer
    permission_classes = [permissions.IsAuthenticated, CheckSubscription]



class SeasonListAPIView(generics.ListAPIView):
    queryset = Season.objects.all()
    serializer_class = SeasonListSerializer


class SeasonDetailAPIView(generics.RetrieveAPIView):
    queryset = Season.objects.all()
    serializer_class = SeasonDetailSerializer
    permission_classes = [permissions.IsAuthenticated, CheckSubscription]



class CartoonListAPIView(generics.ListAPIView):
    queryset = Cartoon.objects.all()
    serializer_class = CartoonListSerializer


class CartoonDetailAPIView(generics.RetrieveAPIView):
    queryset = Cartoon.objects.all()
    serializer_class = CartoonDetailSerializer
    permission_classes = [permissions.IsAuthenticated, CheckSubscription]

class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

class FavoriteAPIView(generics.RetrieveAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)


    def retrieve(self, request, *args, **kwargs):
        favorite, created = Favorite.objects.get_or_create(user=self.request.user)
        serializer = self.get_serializer(favorite)
        return Response(serializer.data)


class FavoriteItemViewSet(viewsets.ModelViewSet):
    queryset = FavoriteItem.objects.all()
    serializer_class = FavoriteItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if isinstance(self.request.user, AnonymousUser):
            return FavoriteItem.objects.none()

        return FavoriteItem.objects.filter(watchlist__user=self.request.user)

    def perform_create(self, serializer):
        watchlist, created = Favorite.objects.get_or_create(user=self.request.user)

        film = serializer.validated_data.get('film')
        series = serializer.validated_data.get('series')
        cartoon = serializer.validated_data.get('cartoon')

        filters = {'watchlist': watchlist}
        if film:
            filters['film'] = film
        if series:
            filters['series'] = series
        if cartoon:
            filters['cartoon'] = cartoon

        if FavoriteItem.objects.filter(**filters).exists():
            raise serializers.ValidationError('Уже добавлено в избранное')

        serializer.save(watchlist=watchlist)

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, CheckUser]
