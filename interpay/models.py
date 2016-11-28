from django.contrib.auth.base_user import BaseUserManager
from django.core.mail import send_mail
from django.core.validators import RegexValidator, int_list_validator
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db import models
from django.forms import ChoiceField
from django_countries.fields import CountryField
from datetime import datetime
import unicodedata


class Manager(BaseUserManager):
    def create_user(self, USERNAME_FIELD, email, password):
        email = self.normalize_email(email)
        username = self.model.normalize_username(USERNAME_FIELD)
        user = self.model(username=username, email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="UserProfile")
    password = models.CharField(max_length=10, null=False, blank=False)
    picture = models.ImageField(upload_to='userProfiles/', null=True, blank=True)
    date_of_birth = models.DateTimeField(null=False, blank=False)
    date_joined = models.DateTimeField(default=datetime.now())
    country = CountryField(default="Iran")
    national_code = models.CharField(max_length=10, null=False, blank=False)
    mobile_number = models.CharField(max_length=11, null=True, blank=True)
    email = models.EmailField(null=False, blank=False)
    # TODO : this field should not be nullable. fix it.
    national_card_photo = models.ImageField(upload_to='nationalCardScans/', null=True, blank=True)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'

    objects = Manager()

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def __str__(self):
        return '{}'.format(self.user.username)

    def __unicode__(self):
        return self.user.username

        # def __init__(self, *args, **kwargs):
        #     super(UserProfile, self).__init__(*args, **kwargs)
        #     if self.instance:
        #         # we're operating on an existing object, not a new one...
        #         country = self.instance.country
        #         cities = self.fields["new_city"] = ChoiceField(choices=cities)


class CommonUser(models.Model):
    # since we might need to define a Manager model in the future, this model is named as "CommonUser"
    user_ID = models.ForeignKey(UserProfile, null=False, related_name='user_ID')

    def __str__(self):
        return '{} - {}'.format(self.customer_ID, self.user_ID.name)
