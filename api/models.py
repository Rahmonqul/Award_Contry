from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from ckeditor.fields import RichTextField

class Partner(AbstractUser, PermissionsMixin):
    full_name = models.CharField(max_length=255, verbose_name="Full Name")
    image = models.ImageField(upload_to='partners/', null=True, blank=True, verbose_name="Image")
    biography = RichTextField(null=True, blank=True, verbose_name="Biography")
    position = models.CharField(max_length=255, null=True, blank=True, verbose_name="Position")

    class Meta:
        verbose_name = "Partner"
        verbose_name_plural = "Partners"

    def __str__(self):
        return self.username  # Используем стандартное поле username для идентификации

class Decision(models.Model):
    name = models.CharField(max_length=255, verbose_name="Name")
    link = models.URLField(verbose_name="Link")

    def __str__(self):
        return self.name


# Award Model
class Award(models.Model):
    name = models.CharField(max_length=255, verbose_name="Name")
    description = RichTextField(null=True, blank=True, verbose_name="Description")
    image = models.ImageField(upload_to='awards/', null=True, blank=True, verbose_name="Image")
    code = models.CharField(max_length=50, null=True, blank=True, verbose_name="Code")
    docs = models.FileField(upload_to='documents/', null=True, blank=True, verbose_name="Documents")
    partners = models.ManyToManyField(
        Partner, through='AwardPartner', related_name='awards', verbose_name="Partners"
    )

    def __str__(self):
        return self.name


# AwardPartner Model (through model)
class AwardPartner(models.Model):
    award = models.ForeignKey(Award, on_delete=models.CASCADE, related_name="award_partners")
    decision = models.ForeignKey(Decision, on_delete=models.CASCADE, related_name="award_partners")
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name="award_partners")
    date = models.DateField(verbose_name="Date")

    def __str__(self):
        return f"{self.award.name} - {self.partner.full_name}"


# SocialLink Model
class SocialLink(models.Model):
    name = models.CharField(max_length=255, verbose_name="Name")
    link = models.URLField(null=True, blank=True, verbose_name="Link")
    icon = models.ImageField(upload_to='social_icons/', null=True, blank=True, verbose_name="Icon")

    def __str__(self):
        return self.name

class AboutCountryAward(models.Model):
    text=RichTextField()

    def __str__(self):
        return f'Davlat Mukofotlari Reestri'



