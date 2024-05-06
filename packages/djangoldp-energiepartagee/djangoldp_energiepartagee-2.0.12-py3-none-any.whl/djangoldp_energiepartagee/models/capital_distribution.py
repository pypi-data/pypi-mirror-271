from django.db import models
from django.utils.translation import gettext_lazy as _
from djangoldp.models import Model
from djangoldp.permissions import InheritPermissions

from djangoldp_energiepartagee.models.actor import Actor

class CapitalDistribution(Model):
    actor = models.ForeignKey(
        Actor,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name="Acteur",
        related_name="capital_distributions",
    )
    individuals_count = models.IntegerField(
        blank=True, null=True, verbose_name="Nombre d'actionnaires personnes physiques"
    )
    individuals_capital = models.DecimalField(
        max_digits=30, decimal_places=2, blank=True, null=True, verbose_name="Montant en capital personnes physiques"
    )
    other_funds_capital = models.DecimalField(
        max_digits=30, decimal_places=2, blank=True, null=True, verbose_name="Autres fonds propres personnes physiques"
    )
    individuals_count_resident = models.IntegerField(
       blank=True, null=True, verbose_name="Nombre d'actionnaires résidents"
    )
    other_ess_orgs_capital = models.DecimalField(
        max_digits=30, decimal_places=2, blank=True, null=True, verbose_name="Montant en capital ESS"
    )
    other_ess_orgs_other_funds = models.DecimalField(
        max_digits=30, decimal_places=2, blank=True, null=True, verbose_name="Autres fonds propres ESS"
    )
    communities_count = models.IntegerField(
        blank=True, null=True, verbose_name="Nombre de collectivités"
    )
    communities_capital = models.DecimalField(
        max_digits=30, decimal_places=2, blank=True, null=True, verbose_name="Montant en capital collectivités"
    )
    communities_other_funds = models.DecimalField(
        max_digits=30, decimal_places=2, blank=True, null=True, verbose_name="Autres fonds propres collectivités"
    )
    neighboring_communities_count = models.IntegerField(
        blank=True, null=True, verbose_name="Nombre de collectivités résidentes"
    )
    other_private_orgs_capital = models.DecimalField(
        max_digits=30, decimal_places=2, blank=True, null=True,verbose_name="Montant en capital autres acteurs"
    )
    other_private_orgs_other_funds = models.DecimalField(
        max_digits=30, decimal_places=2, blank=True, null=True, verbose_name="Autres fonds propres autres acteurs"
    )

    class Meta(Model.Meta):
        ordering = ["pk"]
        permission_classes = [InheritPermissions]
        inherit_permissions = ["actor"]
        rdf_type = "energiepartagee:capital_distribution"
        serializer_fields = [
            "actor",
            "individuals_count",
            "individuals_capital",
            "other_funds_capital",
            "individuals_count_resident",
            "other_ess_orgs_capital",
            "other_ess_orgs_other_funds",
            "communities_count",
            "communities_capital",
            "communities_other_funds",
            "neighboring_communities_count",
            "other_private_orgs_capital",
            "other_private_orgs_other_funds",
            "shareholders",
        ]
        nested_fields = ["shareholders"]
        verbose_name = _("Distribution du capital")
        verbose_name_plural = _("Distribution des capitaux")
        depth = 2

    def __str__(self):
        return self.urlid
