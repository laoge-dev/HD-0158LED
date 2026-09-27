from django.db import models

# Create your models here.
class Message(models.Model):
    title_text = models.CharField(max_length=200)
    mode_int = models.IntegerField(default=0)
    green_text = models.TextField()
    red_text = models.TextField()
    size_int = models.IntegerField(default=0)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.title_text
