# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models

from odoo.addons.ssi_decorator import ssi_decorator


class Commission(models.Model):
    _name = "commission"
    _inherit = [
        "mixin.transaction_cancel",
        "mixin.transaction_done",
        "mixin.transaction_open",
        "mixin.transaction_confirm",
        "mixin.localdict",
        "mixin.transaction_date_due",
        "mixin.transaction_date_duration",
        "mixin.transaction_account_move_with_field",
        "mixin.account_move_single_line_with_field",
        "mixin.company_currency",
        "mixin.many2one_configurator",
        "mixin.currency",
        "mixin.transaction_untaxed_with_field",
        "mixin.transaction_tax_with_field",
        "mixin.transaction_total_with_field",
        "mixin.transaction_residual_with_field",
    ]
    _description = "Commission"

    _exchange_date_field = "date"

    # Multiple Approval Attribute
    _approval_from_state = "draft"
    _approval_to_state = "open"
    _approval_state = "confirm"
    _after_approved_method = "action_open"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True

    # Attributes related to add element on form view automatically
    _automatically_insert_multiple_approval_page = True
    _automatically_insert_open_policy_fields = False
    _automatically_insert_open_button = False
    _automatically_insert_done_policy_fields = False
    _automatically_insert_done_button = False

    _statusbar_visible_label = "draft,confirm,open,done"
    _policy_field_order = [
        "confirm_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "cancel_ok",
        "restart_ok",
        "manual_number_ok",
    ]
    _header_button_order = [
        "action_confirm",
        "action_approve_approval",
        "action_reject_approval",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "action_restart",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_confirm",
        "dom_reject",
        "dom_open",
        "dom_done",
        "dom_cancel",
        "dom_terminate",
    ]

    # Sequence attribute
    _create_sequence_state = "open"

    _normal_amount = "credit"

    _amount_currency_field_name = "amount_total"

    # Tax computation
    _tax_lines_field_name = "tax_ids"
    _tax_on_self = False
    _tax_source_recordset_field_name = "detail_ids"
    _price_unit_field_name = "price_unit"
    _quantity_field_name = "uom_quantity"
    _partner_id_field_name = "partner_id"

    date = fields.Date(
        string="Date",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    salesperson_id = fields.Many2one(
        string="Salesperson",
        comodel_name="res.users",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    partner_id = fields.Many2one(
        string="Partner",
        comodel_name="res.partner",
        compute="_compute_partner_id",
        store=True,
    )
    all_salesperson_ids = fields.Many2many(
        string="All Salesperson",
        comodel_name="res.users",
        compute="_compute_all_salesperson_ids",
        store=False,
    )
    type_id = fields.Many2one(
        string="Type",
        comodel_name="commission_type",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    move_line_ids = fields.Many2many(
        string="Source Journal Items",
        comodel_name="account.move.line",
        relation="rel_commission_2_aml",
        column1="commission_id",
        column2="line_id",
        readonly=True,
    )
    item_ids = fields.One2many(
        string="Commission Items",
        comodel_name="commission.item_computation",
        inverse_name="commission_id",
        readonly=True,
    )
    detail_ids = fields.One2many(
        string="Details",
        comodel_name="commission.detail",
        inverse_name="commission_id",
        readonly=True,
    )
    tax_ids = fields.One2many(
        string="Taxes",
        comodel_name="commission.tax",
        inverse_name="commission_id",
        readonly=True,
    )
    allowed_salesperson_ids = fields.Many2many(
        string="Allowed Salespersons",
        comodel_name="res.users",
        compute="_compute_allowed_salesperson_ids",
        store=False,
    )
    allowed_currency_ids = fields.Many2many(
        string="Allowed Currencies",
        comodel_name="res.currency",
        compute="_compute_allowed_currency_ids",
        store=False,
    )

    @api.depends(
        "salesperson_id",
    )
    def _compute_all_salesperson_ids(self):
        for record in self:
            result = []
            if record.salesperson_id:
                result = record.salesperson_id
                sp = record.salesperson_id
                if sp.sale_team_id:
                    result += sp.sale_team_id.member_ids
            record.all_salesperson_ids = result

    @api.depends(
        "salesperson_id",
    )
    def _compute_partner_id(self):
        for record in self:
            result = False
            if record.salesperson_id:
                if (
                    record.salesperson_id.partner_id.commercial_partner_id
                    == record.salesperson_id.partner_id
                ):
                    result = record.salesperson_id.partner_id
                else:
                    result = record.salesperson_id.partner_id.contact_id
            record.partner_id = result

    @api.depends("type_id")
    def _compute_allowed_salesperson_ids(self):
        for record in self:
            result = False
            if record.type_id:
                result = record._m2o_configurator_get_filter(
                    object_name="res.users",
                    method_selection=record.type_id.user_selection_method,
                    manual_recordset=record.type_id.user_ids,
                    domain=record.type_id.user_domain,
                    python_code=record.type_id.user_python_code,
                )
            record.allowed_salesperson_ids = result

    @api.depends("type_id")
    def _compute_allowed_currency_ids(self):
        for record in self:
            result = False
            if record.type_id:
                result = record._m2o_configurator_get_filter(
                    object_name="res.currency",
                    method_selection=record.type_id.currency_selection_method,
                    manual_recordset=record.type_id.currency_ids,
                    domain=record.type_id.currency_domain,
                    python_code=record.type_id.currency_python_code,
                )
            record.allowed_currency_ids = result

    @api.onchange(
        "type_id",
    )
    def onchange_currency_id(self):
        self.currency_id = False

    @api.onchange(
        "type_id",
    )
    def onchange_salesperson_id(self):
        self.salesperson_id = False

    @api.onchange(
        "type_id",
    )
    def onchange_policy_template_id(self):
        self.policy_template_id = False

    def action_compute(self):
        for record in self.sudo():
            record.detail_ids.unlink()
            record._compute_computation_item()
            record._compute_commission()
            record._recompute_standard_tax()

    def _compute_commission(self):
        self.ensure_one()
        for detail in self.detail_ids:
            detail.onchange_tax_ids()
            detail._compute_commission()

    def _compute_computation_item(self):
        self.ensure_one()
        self.item_ids.unlink()
        CommissionItem = self.env["commission.item_computation"]
        for computation_item in self.type_id.item_ids:
            CommissionItem.create(
                {
                    "commission_id": self.id,
                    "sequence": computation_item.sequence,
                    "item_id": computation_item.item_id.id,
                }
            )
        for computation_item in self.item_ids:
            computation_item._reload_source_ml()
            computation_item._reload_analytic_account_ids()
            computation_item._create_commission_detail()

    @ssi_decorator.post_open_action()
    def _10_create_accounting_entry(self):
        self.ensure_one()

        if self.move_id:
            return True

        self._create_standard_move()  # Mixin
        ml = self._create_standard_ml()  # Mixin
        self.write(
            {
                "move_line_id": ml.id,
            }
        )

        for detail in self.detail_ids:
            line_ml = detail._create_standard_ml()  # Mixin
            detail.write(
                {
                    "move_line_id": line_ml.id,
                }
            )

        for tax in self.tax_ids:
            tax._create_standard_ml()  # Mixin

        self._post_standard_move()  # Mixin

    @ssi_decorator.post_cancel_action()
    def _delete_accounting_entry(self):
        self.ensure_one()
        for detail in self.detail_ids:
            detail.move_line_id.remove_move_reconcile()
        self._delete_standard_move()  # Mixin

    @api.model
    def _get_policy_field(self):
        res = super(Commission, self)._get_policy_field()
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

    @ssi_decorator.insert_on_form_view()
    def _insert_form_element(self, view_arch):
        if self._automatically_insert_view_element:
            view_arch = self._reconfigure_statusbar_visible(view_arch)
        return view_arch
