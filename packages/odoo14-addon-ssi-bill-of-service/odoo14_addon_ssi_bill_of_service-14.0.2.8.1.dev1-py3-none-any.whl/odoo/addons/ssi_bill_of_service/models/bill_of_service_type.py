# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class BillOfServiceType(models.Model):
    _name = "bill_of_service_type"
    _description = "Bill Of Service Type"
    _inherit = ["mixin.master_data"]

    name = fields.Char(
        help="Bill of Service Type's name",
    )
    code = fields.Char(
        help="Bill of Service Type's code. Duplicate not allowed",
    )
    allowed_product_category_ids = fields.Many2many(
        string="Allowed Product Categories",
        comodel_name="product.category",
        relation="rel_bos_type_2_product_category",
        column1="type_id",
        column2="product_category_id",
    )
    allowed_product_tmpl_ids = fields.Many2many(
        string="Allowed Product Templates",
        comodel_name="product.template",
        relation="rel_bos_type_2_product_template",
        column1="type_id",
        column2="product_template_id",
    )
