from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import os
import uuid
import datetime

def image_filename(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('images/', filename)
    
class ProfileImage(models.Model):
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=image_filename, blank=True, null=True)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, default='', blank=False)
    HAIR_COLOUR = (
        ('BLACK', 'Black'),
        ('BLONDE', 'Blonde'),
        ('BROWN', 'Brown'),
        ('RED', 'Red'),
        ('GREY', 'Grey'),
        ('BALD', 'Bald'),
        ('BLUE', 'Blue'),
        ('PINK', 'Pink'),
        ('GREEN', 'Green'),
        ('PURPLE', 'Purple'),
        ('OTHER', 'Other'),
    )
    BODY_TYPE = (
        ('THIN', 'Thin'),
        ('AVERAGE', 'Average'),
        ('FIT', 'Fit'),
        ('MUSCULAR', 'Muscular'),
        ('A LITTLE EXTRA', 'A Little Extra'),
        ('CURVY', 'Curvy'),
    )
    LOOKING_FOR = (
        ('MALE', 'Men'),
        ('FEMALE', 'Women'),
        ('BOTH', 'Both'),
    )
    HAIR_LENGTH = (
        ('LONG', 'Long'),
        ('SHOULDER LENGTH', 'Shoulder Length'),
        ('AVERAGE', 'Average'),
        ('SHORT', 'Short'),
        ('SHAVED', 'Shaved')
    )
    RELATIONSHIP_STATUS = (
        ('NEVER MARRIED', 'Never Married'),
        ('DIVORCED', 'Divorced'),
        ('WIDOWED', 'Widowed'),
        ('SEPARATED', 'Separated')
    )
    EDUCATION = (
    ('COLLEGE', 'College'),
    ('BACHELORS DEGREE', 'Bachelors Degree'),
    ('MASTERS', 'Masters'),
    ('PHD / POST DOCTORAL', 'PhD / Post Doctoral'),
    )
    GENDER = (
        ("MALE", "Male"),
        ("FEMALE", "Female"))

    gender = models.CharField(choices=GENDER, default="MALE", max_length=6)
    hair_length = models.CharField(choices=HAIR_LENGTH, default="LONG", blank=False, max_length=100)
    relationship_status = models.CharField(choices=RELATIONSHIP_STATUS, default="NEVER MARRIED", blank=False, max_length=100)
    education = models.CharField(choices=EDUCATION, default="HIGH SCHOOL", blank=False, max_length=100)
    height = models.DecimalField(max_digits=10, default=180.34, decimal_places=2)
    hair_colour = models.CharField(choices=HAIR_COLOUR, default="BLACK", blank=False, max_length=10)
    body_type = models.CharField(choices=BODY_TYPE, default="AVERAGE", blank=False, max_length=15)
    looking_for = models.CharField(choices=LOOKING_FOR, default='BOTH', blank=False, max_length=6)
    children = models.BooleanField(default=False)
    location = models.CharField(max_length=100, default='', blank=False)
    birth_date = models.DateField(null=True, default='1990-01-01', blank=True)
    
    
    
    def age(self):
        return int((datetime.date.today() - self.birth_date).days / 365.25  )

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
    
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(create_user_profile, sender=User)