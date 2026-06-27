from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

ACCESS_TYPE = (
    ('free', 'free'),
    ('subscription', 'subscription'),
    ('rent', 'rent'),
)

FILM_LANGUAGE = (
    ('kyrgyz', 'kyrgyz'),
    ('russian', 'russian'),
    ('other', 'other'),
)

class UserProfile(AbstractUser):
    avatar = models.ImageField(upload_to='profile_images', null=True, blank=True)
    phone_number = PhoneNumberField(null=True, blank=True)
    date_register = models.DateField(auto_now_add=True)
    STATUS_CHOICES = (
    ('Free', 'Free'),
    ('VIP', 'VIP')
    )
    subscription_status = models.CharField(max_length=5, choices=STATUS_CHOICES, default='Free')
    subscription_end = models.DateTimeField(null=True, blank=True)


    def __str__(self):
        return self.username

class Genre(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='person_image')
    ROLE_CHOICES = (
    ('actor', 'actor'),
    ('director', 'director'),
    ('both', 'both'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f'{self.first_name} - {self.last_name}, {self.role}'

class Country(models.Model):
    country = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.country

class Film(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    poster = models.ImageField(upload_to='film_image')
    year = models.PositiveSmallIntegerField()
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    language = models.CharField(max_length=15, choices=FILM_LANGUAGE)
    duration = models.PositiveIntegerField()
    video = models.FileField(upload_to='film_video')
    trailer_url = models.URLField()
    genres = models.ManyToManyField(Genre, related_name='film_genre')
    persons = models.ManyToManyField(Person, related_name='film_person')
    access_type = models.CharField(max_length=20, choices=ACCESS_TYPE)
    rent_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_published = models.BooleanField(default=False)
    views_count = models.PositiveIntegerField()
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_avg_rating(self):
        rating = self.film_rating.all()
        if rating.exists():
            return  sum([i.stars for i in rating]) / rating.count()
        return 0

    def get_count_people(self):
        return self.film_rating.count()


class Season(models.Model):
    season_number = models.PositiveIntegerField()
    title = models.CharField(max_length=100)
    year = models.PositiveIntegerField()

    def __str__(self):
        return f'Season: {self.season_number}, {self.title}'

class Series(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='season_series')
    title = models.CharField(max_length=30)
    description = models.TextField(null=True, blank=True)
    poster = models.ImageField(upload_to='seria_image/')
    year = models.PositiveIntegerField()
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    language = models.CharField(max_length=15, choices=FILM_LANGUAGE)
    trailer_url = models.URLField()
    video = models.FileField(upload_to='seria_video')
    genres = models.ManyToManyField(Genre)
    persons = models.ManyToManyField(Person)
    access_type = models.CharField(max_length=20, choices=ACCESS_TYPE)
    is_published = models.BooleanField(default=False)
    views_count = models.PositiveIntegerField(default=0)
    created_date = models.DateField(auto_now_add=True)



class Cartoon(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    poster = models.ImageField(upload_to='cartoon_image')
    year = models.PositiveIntegerField()
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    language = models.CharField(max_length=15, choices=FILM_LANGUAGE)
    duration  = models.PositiveIntegerField()
    video_url = models.FileField(upload_to='cartoon_video')
    trailer_url = models.URLField()
    AGE_CHOICES = (
    ('0+', '0+'),
    ('6+', '6+'),
    ('12+', '12+'),
    ('16+', '16+'),
    ('18+', '18+'),
    )
    age_rating = models.CharField(max_length=4, choices=AGE_CHOICES)
    genres = models.ManyToManyField(Genre)
    access_type = models.CharField(max_length=20, choices=ACCESS_TYPE)
    is_published = models.BooleanField(default=False)
    views_count = models.PositiveIntegerField()
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

class Subscription(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    PLAN_CHOICES = (
    ('daily', 'daily'),
    ('monthly', 'monthly'),
    ('yearly', 'yearly'),
    )
    plan = models.CharField(max_length=10, choices=PLAN_CHOICES, null=True, blank=True)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    is_active = models.BooleanField(default=False)
    price = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} - {self.plan}'

class Favorite(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username}- favorite_list'

class FavoriteItem(models.Model):
    watchlist = models.ForeignKey(Favorite, on_delete=models.CASCADE, related_name='favorite_item')
    film = models.ForeignKey(Film, on_delete=models.CASCADE, null=True, blank=True)
    series = models.ForeignKey(Series, on_delete=models.CASCADE, null=True, blank=True)
    cartoon = models.ForeignKey(Cartoon, on_delete=models.CASCADE, null=True, blank=True)
    added_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.film.title} - {self.watchlist}'

class Review(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    film = models.ForeignKey(Film, on_delete=models.CASCADE, null=True, blank=True, related_name='film_rating')
    series = models.ForeignKey(Series, on_delete=models.CASCADE, null=True, blank=True)
    cartoon = models.ForeignKey(Cartoon, on_delete=models.CASCADE, null=True, blank=True)
    stars = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 11)], null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} comment, rating: {self.stars}⭐'