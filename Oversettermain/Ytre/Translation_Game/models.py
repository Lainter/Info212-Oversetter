from django.db import models
# Create your models here.

class Language(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name
class Word(models.Model):
    word = models.CharField(max_length=255)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag', related_name='words', blank=True)

    def __str__(self):
        return self.word

class Translation(models.Model):
    source_word = models.ForeignKey(Word, on_delete=models.CASCADE, related_name="translations_from")
    target_word = models.ForeignKey(Word, on_delete=models.CASCADE, related_name="translations_to")

    def __str__(self):
        return f"{self.source_word} → {self.target_word}"
