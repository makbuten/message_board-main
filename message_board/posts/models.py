from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from froala_editor.fields import FroalaField


class Post(models.Model):
    TANK = 'TN'
    HEAL = 'HL'
    DD = 'DD'
    TRADER = 'TR'
    GUILD_MASTER = 'GM'
    QUEST_GIVER = 'QG'
    BLACKSMITH = 'BS'
    TANNER = 'TN'
    POTIONS_MASTER = 'PM'
    SPELL_MASTER = 'SM'

    CATEGORY_CHOICE = [
        (TANK, 'Танк'),
        (HEAL, 'Хил'),
        (DD, 'ДД'),
        (TRADER, 'Торговец'),
        (GUILD_MASTER, 'Гилдмастер'),
        (QUEST_GIVER, 'Квестгивер'),
        (BLACKSMITH, 'Кузнец'),
        (TANNER, 'Кожевник'),
        (POTIONS_MASTER, 'Зельевар'),
        (SPELL_MASTER, 'Мастер заклинаний'),
    ]
    post_header = models.TextField()
    post_text = FroalaField()
    post_author = models.ForeignKey(User, on_delete=models.CASCADE)
    post_category = models.CharField(max_length=2, choices=CATEGORY_CHOICE)
    post_creation_time = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('post', args=[str(self.id)])

    def __str__(self):
        return self.post_header


class Response(models.Model):
    response_text = models.TextField()
    response_author = models.ForeignKey(User, on_delete=models.CASCADE)
    response_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    response_creation_time = models.DateTimeField(auto_now_add=True)
    response_accepted = models.BooleanField(default=False)
