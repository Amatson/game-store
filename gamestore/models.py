from django.contrib.auth.models import User
from django.db import models


class Developer(models.Model):
    """Developer profile (every user has either Player or Developer profile). The profile is used to storing additional
    attributes and permissions for users.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='developer')
    activated = models.BooleanField(default=False)
    user_hash = models.CharField(max_length=255)

    @classmethod
    def create(cls, user):
        return cls(user=user)

    class Meta:
        permissions = (
            ('developer', 'The user is a developer'),
        )


class Player(models.Model):
    """Player profile (every user has either Player or Developer profile). The profile is used to storing additional
    attributes and permissions for users.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='player')
    owned_games = models.ManyToManyField('Game')
    activated = models.BooleanField(default=False)
    user_hash = models.CharField(max_length=255)

    @classmethod
    def create(cls, user):
        return cls(user=user)

    class Meta:
        permissions = (
            ('player', 'The user is a player'),
        )


class Game(models.Model):
    """A model for all games. 'developer' is the one who added the game to the gamestore."""
    name = models.CharField(max_length=255, unique=True)
    category = models.CharField(max_length=225)
    description = models.TextField(max_length=500)
    game_url = models.URLField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    developer = models.ForeignKey(Developer, related_name='added_games')


class Order(models.Model):
    """A model for all game purchases. 'status' indicates if the order has been paid or not."""
    buyer = models.ForeignKey(Player, related_name='orders')
    seller = models.ForeignKey(Developer, related_name='sales')
    game = models.ForeignKey(Game, related_name='orders')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    purchase_time = models.DateTimeField(auto_now_add=True, blank=True)
    status = models.BooleanField(default=False)


class HighScore(models.Model):
    """A model for saved game scores."""
    player = models.ForeignKey(Player, related_name='high_scores')
    game = models.ForeignKey(Game, related_name='high_scores')
    score = models.IntegerField()

    class Meta:
        ordering = ['-score']


class SaveState(models.Model):
    """A model for saving a games state. Used when saving/loading a game."""
    player = models.ForeignKey(Player, related_name='saves')
    game = models.ForeignKey(Game, related_name='saves')
    state = models.CharField(max_length=10000)  # save state in json formatted string
