from datetime import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver

# admin
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('O campo de e-mail é obrigatório'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser deve ter is_staff=True'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser deve ter is_superuser=True'))

        return self.create_user(email, password, **extra_fields)
    
# admin
class CustomUser(AbstractUser):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=150, unique=True, null=False, blank=False, 
                                help_text=_('Opcional. Um apelido único para exibição no site (ex.: @username).')
    )
    first_name = None
    last_name = None
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # Remove username field entirely
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    class Meta:
        verbose_name = _('usuário')
        verbose_name_plural = _('usuários')

    def __str__(self):
        return self.username
    
# admin
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

# admin/user
class Poll(models.Model):
    creator = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='polls')
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=150, unique=True, blank=True)
    image = models.ImageField(upload_to='poll_images/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='polls')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    is_flagged = models.BooleanField(default=False)
    flag_reason = models.TextField(null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.end_date <= self.start_date:
            raise ValidationError("A data de término deve ser posterior à data de início.")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def total_votes(self):
        return sum(option.votes for option in self.options.all())

    def __str__(self):
        return self.title

    class Meta:
        indexes = [models.Index(fields=['created_at'])]
        verbose_name = "Poll"
        verbose_name_plural = "Polls"

# admin/user
class Option(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=100)
    votes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.text

    class Meta:
        indexes = [models.Index(fields=['poll'])]
        verbose_name = "Option"
        verbose_name_plural = "Options"

# admin/user
class Vote(models.Model):
    user = models.ForeignKey('api.CustomUser', on_delete=models.SET_NULL, null=True, related_name='votes')
    poll = models.ForeignKey(Poll, on_delete=models.SET_NULL, null=True, related_name='votes')
    option = models.ForeignKey(Option, on_delete=models.SET_NULL, null=True, related_name='vote_set')
    voted_at = models.DateTimeField(auto_now_add=True)
    is_updated = models.BooleanField(default=False)
    updated_at = models.DateTimeField(null=True, blank=True)

    def clean(self):
        if self.option and self.poll:
            if self.option.poll != self.poll:
                raise ValidationError("A opção selecionada não pertence à votação especificada.")
            if not self.poll.is_active:
                raise ValidationError("Esta votação não está ativa.")
            if not (self.poll.start_date <= timezone.now() <= self.poll.end_date):
                raise ValidationError("Esta votação não está no período de votação.")

    def __str__(self):
        return f"Voto de {self.user} em {self.option}"

    class Meta:
        unique_together = ('user', 'poll')
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['option']),
            models.Index(fields=['poll']),
        ]
        verbose_name = "Vote"
        verbose_name_plural = "Votes"

# admin
class Flag(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='flags')
    user = models.ForeignKey('api.CustomUser', on_delete=models.SET_NULL, null=True, related_name='flags')
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Flag em {self.poll.title} por {self.reason}"

    class Meta:
        verbose_name = "Flag"
        verbose_name_plural = "Flags"

@receiver(post_save, sender=Vote)
def update_option_votes(sender, instance, created, **kwargs):
    if created and instance.option:
        instance.option.votes += 1
        instance.option.save()

