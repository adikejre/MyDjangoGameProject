from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class AllMyScores(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    game_title=models.CharField(max_length=20)
    latest_score=models.IntegerField(default=0)
    max_score=models.IntegerField(default=0)
    #leaderboard_position?

    def __str__(self):
        return self.game_title

    class Meta:
        ordering=['max_score']
