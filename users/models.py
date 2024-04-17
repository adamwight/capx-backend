from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver
from django.utils import timezone
from django.db.models.signals import post_save
from orgs.models import Organization
from skills.models import Skill
from users.submodels import Territory, Language, WikimediaProject
from django.core.validators import RegexValidator


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_("username"), max_length=100, unique=True, help_text=_("100 characters or fewer"))
    first_name = models.CharField(_('first name'), max_length=30, null=True, blank=True)
    middle_name = models.CharField(_("middle name"), max_length=128, null=True, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, null=True, blank=True)
    email = models.EmailField(_('email address'), max_length=255, null=True, blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(_('active'), default=True, help_text=_(
        'Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    user_groups = models.JSONField(null=True, blank=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'


class Profile(models.Model):
    PRONOUNS = (
        ("he-him", _("He/Him")),
        ("she-her", _("She/Her")),
        ("they-them", _("They/Them"))
    )

    CONTACT_METHODS = (
        ("email", _("Email")),
        ("discussion", _("Discussion page")),
        ("wiki", _("Meta-Wiki talk page")),
        ("IRC", _("IRC")),
    )

    # PERSONAL INFORMATION
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, editable=False)
    pronoun = models.CharField(verbose_name=_("Pronoun"), max_length=20, choices=PRONOUNS, blank=True)
    profile_image = models.URLField(verbose_name=_("Profile image"), null=True, blank=True)
    display_name = models.CharField(verbose_name=_("Display name"), max_length=387, blank=True)
    birthday = models.DateField(verbose_name=_("Birthday"), null=True, blank=True)
    about = models.TextField(verbose_name=_("About me"), max_length=2000, blank=True, default="")
    wikidata_qid = models.CharField(verbose_name="Wikidata Qid", max_length=10, blank=True, validators=[RegexValidator(
        regex=r'^Q[1-9]\d*$',
        message="Invalid Wikidata Qid format. The format should be Q12345"
    )])

    # CONTACT
    contact_method = models.CharField(verbose_name=_("Preferred contact method"), max_length=10,
                                      choices=CONTACT_METHODS, blank=True)
    irc = models.CharField(verbose_name=_("IRC"), max_length=128, blank=True)
    wiki_alt = models.CharField(verbose_name=_("Wikimedia alternative account"), max_length=128, blank=True)
    wiki_develop = models.CharField(verbose_name=_("Wikimedia developer account"), max_length=128, blank=True)
    email = models.EmailField(verbose_name=_("Email"), blank=True)

    # LOCALIZATION
    territory = models.ManyToManyField(Territory, verbose_name="Territory", related_name="user_territory", blank=True)
    language = models.ManyToManyField(Language, verbose_name=_("Language"), related_name="user_language", blank=True)
    affiliation = models.ManyToManyField(Organization, verbose_name=_("Affiliation"),
                                         related_name="user_affiliation", blank=True)
    wikimedia_project = models.ManyToManyField(WikimediaProject, verbose_name=_("Wikimedia project"),
                                               related_name="user_wikimedia_project", blank=True)

    # SKILLS
    skills_known = models.ManyToManyField(Skill, verbose_name=_("Skill known"), related_name="user_known_skils", blank=True)
    skills_available = models.ManyToManyField(Skill, verbose_name=_("Available skills"), related_name="user_available_skills", blank=True)
    skills_wanted = models.ManyToManyField(Skill, verbose_name=_("Skill desired"), related_name="user_desired_skils",
                                           blank=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
