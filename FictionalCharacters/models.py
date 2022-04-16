from django.db import models

# Create your models here.
# Creating choices for model fields
GENDERS = (
    ('F', 'Female'),
    ('M', 'Male'),
    ('NB', 'Non-Binary'),
    ('O', 'Other'),
)

ALIGNMENT = (
    ('Lawful Good', 'Lawful Good'),
    ('Neutral Good', 'Neutral Good'),
    ('Chaotic Good', 'Chaotic Good'),
    ('Lawful Neutral', 'Lawful Neutral'),
    ('True Neutral', 'True Neutral'),
    ('Chaotic Neutral', 'Chaotic Neutral'),
    ('Lawful Evil', 'Lawful Evil'),
    ('Neutral Evil', 'Neutral Evil'),
    ('Chaotic Evil', 'Chaotic Evil'),
)

TYPES = (
    ('ANI', 'Anime'),
    ('BOOK', 'Book'),
    ('CMC', 'Comic'),
    ('FILM', 'Movie'),
    ('TV', 'Television Series'),
    ('VG', 'Video Game'),
    ('OTH', 'Other'),
)

# Declaring a new model named Series
class Series(models.Model):
    # Model fields
    name = models.CharField(max_length=150)
    type = models.CharField(max_length=20, choices=TYPES)
    creator = models.CharField(max_length=100, blank=True, null=True)

    objects = models.Manager()

    # Rename instances of model with their name
    def __str__(self):
        return self.name

# Declaring a new model named Characters
class Characters(models.Model):
    # Model fields
    name = models.CharField(max_length=100)
    age = models.IntegerField(default='')
    gender = models.CharField(max_length=15, choices=GENDERS)
    species = models.CharField(max_length=50)
    skill = models.CharField(max_length=100)
    alignment = models.CharField(max_length=19, choices=ALIGNMENT, blank=True, null=True)
    series = models.ForeignKey(Series, on_delete=models.CASCADE)
    notes = models.CharField(max_length=500, blank=True, null=True)

    objects = models.Manager()

    # Rename instances of model with their name
    def __str__(self):
        return self.name

