from django.db import models

class Territory(models.Model):
    territory_name = models.CharField(verbose_name="Territory name", max_length=128, unique=True)
    parent_territory = models.ManyToManyField("self", verbose_name="Parent territory", symmetrical=False,
                                           related_name="territory_parent", blank=True)

    def __str__(self):
        return self.territory_name


class Language(models.Model):
    language_name = models.CharField(verbose_name="Language name", max_length=128)
    language_autonym = models.CharField(verbose_name="Language autonym", max_length=128, blank=True)
    language_code = models.CharField(verbose_name="Language code", max_length=10, unique=True)

    def __str__(self):
        return self.language_name


class WikimediaProject(models.Model):
    wikimedia_project_name = models.CharField(verbose_name="Wikimedia project name", max_length=128)
    wikimedia_project_code = models.CharField(verbose_name="Wikimedia project code", max_length=40, unique=True)

    def __str__(self):
        return self.wikimedia_project_name