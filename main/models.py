from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyUserManager(BaseUserManager):
    def create_user(self, email, name, lastname, age, password=None):
        if not email:
            raise ValueError("User must have an email.")
        if not name:
            raise ValueError("User must have a name.")
        if not lastname:
            raise ValueError("User must have a lastname.")
        if not age:
            raise ValueError("You must provide your age.")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            lastname=lastname,
            age=age,
        )

        user.is_active = False
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, lastname, age, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            name=name,
            lastname=lastname,
            password=password,
            age=age,
        )

        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    MANAGER = 1
    WORKER = 2
    SEO = 3

    ROLE_CHOICES = (
        (SEO, 'SEO'),
        (MANAGER, 'Manager'),
        (WORKER, 'Worker'),
    )

    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    organization = models.ForeignKey('Organization', null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    lastname = models.CharField(max_length=256)
    age = models.IntegerField()

    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)

    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(verbose_name='Registration date', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='Last login', auto_now=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'lastname', 'age']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def save(self, *args, **kwargs):
        method_create = self._state.adding
        super().save(*args, **kwargs)
        if method_create:
            Indicators.objects.create(
                user_email=self,
                higher_pressure=0,
                lower_pressure=0,
                heartbeat_rate=0,
                temperature=0,
                is_critical=False,
                timeouts_taken=0,
            )


class Organization(models.Model):
    WorkersCount = (
        (10, '10'),
        (25, '25'),
        (50, '50'),
        (100, '100'),
    )

    name = models.CharField(max_length=256, primary_key=True)
    workers_count = models.IntegerField(choices=WorkersCount)
    registration_date = models.DateField(auto_now_add=True)
    ceo = models.CharField(max_length=256)


class Message(models.Model):
    id = models.AutoField(primary_key=True)
    header = models.CharField(max_length=60)
    text = models.TextField()
    sender = models.ForeignKey('User', related_name='sender', null=True, blank=False, on_delete=models.SET_NULL)
    recipient = models.ForeignKey('User', null=False, blank=False, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now=True)


class Report(models.Model):
    id = models.AutoField(primary_key=True)
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    danger_level = models.PositiveSmallIntegerField()
    report_details = models.TextField()
    recommendation = models.TextField()


class Indicators(models.Model):
    user_email = models.OneToOneField('User', on_delete=models.CASCADE)
    higher_pressure = models.DecimalField(max_digits=5, decimal_places=2)
    lower_pressure = models.DecimalField(max_digits=5, decimal_places=2)
    heartbeat_rate = models.IntegerField()
    temperature = models.DecimalField(max_digits=2, decimal_places=1)
    is_critical = models.BooleanField(default=False)
    timeouts_taken = models.IntegerField(default=0)

    def __str__(self):
        return str(self.user_email)
