# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import fields, models


class ResPartner(models.AbstractModel):
    _name = "res.partner"
    _inherit = [
        "res.partner",
    ]

    type = fields.Selection(
        selection_add=[
            ("tax", "Tax Address"),
        ],
    )
