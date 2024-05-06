# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import api, fields, models


class MixinTransactionTaxAddess(models.AbstractModel):
    _name = "mixin.transaction_tax_address"
    _inherit = [
        "mixin.transaction",
    ]
    _description = "Mixin for Transaction Object With Tax Address"

    partner_id = fields.Many2one(
        string="Partner",
        comodel_name="res.partner",
        domain=[
            ("parent_id", "=", False),
        ],
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )

    @api.depends(
        "partner_id",
    )
    def _compute_allowed_tax_address_ids(self):
        Partner = self.env["res.partner"]
        for record in self:
            result = []
            if record.partner_id:
                criteria = [
                    ("commercial_partner_id", "=", record.partner_id.id),
                    ("id", "!=", record.partner_id.id),
                    ("type", "=", "tax"),
                ]
                result = Partner.search(criteria).ids
            record.allowed_tax_address_ids = result

    allowed_tax_address_ids = fields.Many2many(
        string="Allowed Tax Address",
        comodel_name="res.partner",
        compute="_compute_allowed_tax_address_ids",
        store=False,
    )
    tax_address_id = fields.Many2one(
        string="Tax Address",
        comodel_name="res.partner",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )

    @api.onchange(
        "partner_id",
    )
    def onchange_tax_address_id(self):
        self.tax_address_id = False


class MixinTransactionTaxAddressRequired(models.AbstractModel):
    _name = "mixin.transaction_tax_address_required"
    _inherit = [
        "mixin.transaction_tax_address",
    ]
    _description = "mixin.transaction_tax_address with required contact"

    tax_address_id = fields.Many2one(
        required=True,
    )
