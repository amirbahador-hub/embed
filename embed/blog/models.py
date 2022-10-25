from django.db import models
from embed.common.models import BaseModel
from embed.users.models  import BaseUser


class Post(BaseModel):

    slug = models.SlugField(
            primary_key=True,
            max_length=100,
    )
    title = models.CharField(
        max_length=100,
        unique=True,
    )
    content = models.CharField(
        max_length=1000,
    )

    def __str__(self):
        return self.title

class Subscription(models.Model):
    subscriber = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name="subs")
    target     = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name="targets")

