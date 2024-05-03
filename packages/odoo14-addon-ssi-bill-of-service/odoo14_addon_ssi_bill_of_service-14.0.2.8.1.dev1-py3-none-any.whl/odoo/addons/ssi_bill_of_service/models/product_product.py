# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductProduct(models.Model):
    _name = "product.product"
    _inherit = [
        "product.product",
    ]

    bos_id = fields.Many2one(
        string="Default BoS",
        comodel_name="bill_of_service",
        ondelete="restrict",
    )
    bos_ids = fields.One2many(
        string="Bill of Services",
        comodel_name="bill_of_service",
        inverse_name="product_id",
    )
