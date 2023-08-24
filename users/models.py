from django.db import models
from django.contrib.auth import models as auth_models
from django_countries.fields import CountryField
from PIL import Image


class UserManager(auth_models.BaseUserManager):
    def create_user(
        self,
        first_name: str,
        last_name: str,
        email: str,
        password: str = None,
        is_staff=False,
        is_superuser=False,
    ) -> "User":
        if not email:
            raise ValueError("User must have an email")
        if not first_name:
            raise ValueError("User must have a first name")
        if not last_name:
            raise ValueError("User must have a last name")

        user = self.model(email=self.normalize_email(email))
        user.first_name = first_name
        user.last_name = last_name
        user.set_password(password)
        user.is_active = True
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.save()

        return user

    def create_superuser(
        self, first_name: str, last_name: str, email: str, password: str
    ) -> "User":
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            is_staff=True,
            is_superuser=True,
        )
        user.save()

        return user


class User(auth_models.AbstractUser):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField( max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = None
    display_name = models.CharField(max_length=255)
    avatar = models.ImageField(default='avatar.jpg', upload_to='profile_avatars')
    cover_img = models.ImageField(upload_to='cover_images', null=True, blank=True)
    country = CountryField( null=True, blank=True) 
    Bio = models.TextField(null=True, blank=True)
    follows = models.ManyToManyField(
        "self",
        related_name="followed_by",
        symmetrical="false",
        blank=True
    )

    def __str__(self):
        return f"{self.last_name}'s Profile"
    
    
    def save(self, *args, **kwargs):
        #save profile first
        super().save(*args, **kwargs)

        #resize image
        img = Image.open(self.avatar.path)
        if img.height or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.avatar.path)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["display_mame"]
