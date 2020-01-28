from django.db import models
from django.utils import timezone

class Sentence(models.Model):
    sentence_id = models.PositiveIntegerField()
    text = models.TextField(max_length=250)
    word = models.CharField(max_length=30)
    word_id = models.PositiveSmallIntegerField(
         blank=True, null=True)
    Text_index = models.PositiveSmallIntegerField()
    atr = models.PositiveSmallIntegerField(
         blank=True, null=True)
    trans_word = models.CharField(
         max_length=30,blank=True, null=True)

    def __str__(self):
        return self.text
