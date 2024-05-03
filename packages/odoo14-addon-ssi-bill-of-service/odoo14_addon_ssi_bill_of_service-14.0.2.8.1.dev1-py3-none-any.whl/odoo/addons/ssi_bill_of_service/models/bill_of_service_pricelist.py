# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, tools

from odoo.addons.ssi_decorator import ssi_decorator


class BillOfServicePricelist(models.Model):
    _name = "bill_of_service_pricelist"
    _description = "Bill of Service To Pricelist"
    _inherit = [
        "mixin.transaction_confirm",
        "mixin.transaction_done",
        "mixin.transaction_cancel",
        "mixin.date_duration",
    ]

    # Multiple Approval Attribute
    _approval_from_state = "draft"
    _approval_to_state = "done"
    _approval_state = "confirm"
    _after_approved_method = "action_done"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True
    _automatically_insert_multiple_approval_page = True
    _automatically_insert_done_button = False
    _automatically_insert_done_policy_fields = False

    # Mixin duration attribute
    _date_start_readonly = True
    _date_end_readonly = True
    _date_start_required = False
    _date_end_required = False
    _date_start_states_list = ["draft"]
    _date_start_states_readonly = ["draft"]
    _date_end_states_list = ["draft"]
    _date_end_states_readonly = ["draft"]

    _statusbar_visible_label = "draft,confirm,done"

    _policy_field_order = [
        "confirm_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "cancel_ok",
        "restart_ok",
        "done_ok",
        "manual_number_ok",
    ]

    _header_button_order = [
        "action_confirm",
        "action_approve_approval",
        "action_reject_approval",
        "action_done",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "action_restart",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_confirm",
        "dom_reject",
        "dom_done",
        "dom_cancel",
    ]

    # Sequence attribute
    _create_sequence_state = "done"

    date = fields.Date(
        string="Date",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    bos_id = fields.Many2one(
        string="Bill of Service",
        comodel_name="bill_of_service",
        required=True,
        ondelete="restrict",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    product_tmpl_id = fields.Many2one(
        string="Product Template",
        comodel_name="product.template",
        related="bos_id.product_tmpl_id",
        store=True,
    )
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
        related="bos_id.product_id",
        store=True,
    )
    product_category_id = fields.Many2one(
        string="Product Category",
        comodel_name="product.category",
        related="bos_id.product_category_id",
        store=True,
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        required=True,
        ondelete="restrict",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    pricelist_id = fields.Many2one(
        string="Target Pricelist",
        comodel_name="product.pricelist",
        required=True,
        ondelete="restrict",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    pricelist_item_id = fields.Many2one(
        string="Target Pricelist Item",
        comodel_name="product.pricelist.item",
        readonly=True,
        ondelete="restrict",
    )
    price_round = fields.Float(
        string="Price Round",
        required=True,
        readonly=True,
        default=0.0,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    margin = fields.Float(
        string="Margin",
        required=True,
        readonly=True,
        default=100.00,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    amount_good = fields.Monetary(
        string="Amount Good",
        compute="_compute_amount_good",
        store=True,
        currency_field="currency_id",
    )
    amount_service = fields.Monetary(
        string="Amount Service",
        compute="_compute_amount_service",
        store=True,
        currency_field="currency_id",
    )
    amount_total = fields.Monetary(
        string="Amount Total",
        compute="_compute_amount_total",
        store=True,
        currency_field="currency_id",
    )
    amount_after_margin = fields.Monetary(
        string="Amount After Margin",
        compute="_compute_amount_total",
        store=True,
        currency_field="currency_id",
    )
    amount_final = fields.Monetary(
        string="Amount Final",
        compute="_compute_amount_total",
        store=True,
        currency_field="currency_id",
    )

    state = fields.Selection(
        string="State",
        default="draft",
        selection=[
            ("draft", "Draft"),
            ("confirm", "Waiting for Approval"),
            ("done", "Done"),
            ("cancel", "Cancelled"),
            ("reject", "Rejected"),
        ],
        readonly=True,
    )

    def _compute_amount_service(self):
        for record in self:
            result = 0.0
            record.amount_service = result

    def _compute_amount_good(self):
        for record in self:
            result = 0.0
            record.amount_good = result

    @api.depends(
        "margin",
        "price_round",
    )
    def _compute_amount_total(self):
        for record in self:
            result = 0.0
            for field_name in self._get_amount_field():
                result += getattr(record, field_name)
            record.amount_total = result
            record.amount_after_margin = record.amount_final = result * (
                (record.margin + 100.00) / 100.00
            )
            if record.price_round:
                record.amount_final = tools.float_round(
                    record.amount_after_margin, precision_rounding=record.price_round
                )

    @api.model
    def _get_amount_field(self):
        return [
            "amount_good",
            "amount_service",
        ]

    @api.model
    def _get_policy_field(self):
        res = super(BillOfServicePricelist, self)._get_policy_field()
        policy_field = [
            "confirm_ok",
            "approve_ok",
            "done_ok",
            "cancel_ok",
            "reject_ok",
            "restart_ok",
            "restart_approval_ok",
            "manual_number_ok",
        ]
        res += policy_field
        return res

    @ssi_decorator.post_done_action()
    def _create_update_pricelist_item(self):
        self.ensure_one()
        if not self.pricelist_item_id:
            self._create_pricelist_item()
        else:
            self.pricelist_item_id.write(self._prepare_pricelist_item())

    def _create_pricelist_item(self):
        self.ensure_one()
        PricelistItem = self.env["product.pricelist.item"]
        item = PricelistItem.create(self._prepare_pricelist_item())
        self.write(
            {
                "pricelist_item_id": item.id,
            }
        )

    def _prepare_pricelist_item(self):
        self.ensure_one()
        result = {
            "pricelist_id": self.pricelist_id.id,
            "fixed_price": self.amount_final,
            "compute_price": "fixed",
        }
        if self.bos_id.product_id:
            result.update(
                {
                    "product_id": self.bos_id.product_id.id,
                    "applied_on": "0_product_variant",
                }
            )
        else:
            result.update(
                {
                    "product_tmpl_id": self.bos_id.product_tmpl_id.id,
                    "applied_on": "1_product",
                }
            )
        if self.date_start and self.date_end:
            result.update(
                {
                    "date_start": self.date_start,
                    "date_end": self.date_end,
                }
            )
        return result
