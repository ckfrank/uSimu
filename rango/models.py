import datetime
from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


class Category(models.Model):
    NAME_MAX_LEN = 128
    name = models.CharField(max_length=NAME_MAX_LEN, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Page(models.Model):
    TITLE_MAX_LEN = 128
    URL_MAX_LEN = 200
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=TITLE_MAX_LEN)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    # link UserProfile to a User model instance
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # additional attr to incl
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username


# Start of self defined models:

class CPU_Family(models.Model):
    NAME_MAX_LEN = 512
    LOC_MAX_LEN = 512
    name = models.CharField(max_length=NAME_MAX_LEN, unique=True)

    def __str__(self):
        return self.name


class CPU(models.Model):
    NAME_MAX_LEN = 512
    LOC_MAX_LEN = 512
    name = models.CharField(max_length=NAME_MAX_LEN, unique=True)
    reg_count = models.IntegerField(blank=False)  # must have
    mem_count = models.IntegerField(blank=False)  # must have
    reg_bits = models.IntegerField(blank=False)
    mem_bits = models.IntegerField(blank=False)
    family = models.ForeignKey(CPU_Family, on_delete=models.CASCADE)

    # further implementation can include slug for CPU description
    # slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Submission(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=128)
    content = models.TextField(blank=False)
    result = models.TextField(blank=False)
    result_detail = models.TextField(blank=True)
    cpu = models.ForeignKey(CPU, on_delete=models.CASCADE, related_name='submission_cpu')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submission_owner')

    # feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE, related_name='submission_feedback')
    class Meta:
        ordering = ['date']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super(Submission, self).save()


class Feedback(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    content = models.TextField(max_length=99999)
    referring_submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='referring_submission')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedback_owner')

    class Meta:
        ordering = ['date']

    def __str__(self):
        return 'Feedback for submission {} from {}'.format(self.referring_submission_id, self.owner)

    def save(self, *args, **kwargs):
        super(Feedback, self).save()