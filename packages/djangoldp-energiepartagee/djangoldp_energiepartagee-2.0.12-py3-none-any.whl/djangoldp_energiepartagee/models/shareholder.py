from django.db import models
from django.utils.translation import gettext_lazy as _
from djangoldp.models import Model
from djangoldp.permissions import InheritPermissions

from djangoldp_energiepartagee.models.actor import Actor
from djangoldp_energiepartagee.models.capital_distribution import CapitalDistribution

class Shareholder(Model):
    actor = models.ForeignKey(
        Actor,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name="Acteur",
        related_name="shareholders",
    )
    capital_distribution = models.ForeignKey(
        CapitalDistribution,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name="Capital",
        related_name="shareholders",
    )
    capital_amount = models.DecimalField(
        max_digits=30, decimal_places=2, blank=True, null=True, verbose_name="Montant capital"
    )
    other_funds_amount = models.DecimalField(
        max_digits=30, decimal_places=2, blank=True, null=True,  verbose_name="Montant autres fonds"
    )
    relay_investment = models.DecimalField(
        max_digits=30, decimal_places=2, blank=True, null=True, 
        verbose_name="Investissement relais",
        default=False,
    )

    class Meta(Model.Meta):
        ordering = ["pk"]
        permission_classes = [InheritPermissions]
        inherit_permissions = ["actor"]
        rdf_type = "energiepartagee:shareholder"
        serializer_fields = [
            "actor",
            "capital_amount",
            "other_funds_amount",
            "relay_investment",
        ]
        nested_fields= ["actor"]
        verbose_name = _("Actionnaire")
        verbose_name_plural = _("Actionnaires")

        def __str__(self):
            return self.structure_name
        

