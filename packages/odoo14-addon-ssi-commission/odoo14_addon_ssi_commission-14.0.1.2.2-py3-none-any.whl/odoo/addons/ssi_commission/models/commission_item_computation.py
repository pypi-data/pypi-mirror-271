# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class CommissionItemComputation(models.Model):
    _name = "commission.item_computation"
    _description = "Commission - Item Computation"
    _inherit = [
        "mixin.many2one_configurator",
    ]
    _order = "commission_id, sequence, id"

    commission_id = fields.Many2one(
        string="# Commission",
        comodel_name="commission",
        required=True,
        ondelete="cascade",
    )
    sequence = fields.Integer(
        string="Sequence",
        default=10,
        required=True,
    )
    item_id = fields.Many2one(
        string="Item",
        comodel_name="commission_item",
        required=True,
        ondelete="restrict",
    )
    move_line_ids = fields.Many2many(
        string="Source Journal Items",
        comodel_name="account.move.line",
        relation="rel_commission_item_computation_2_aml",
        column1="commission_id",
        column2="line_id",
        readonly=True,
    )
    analytic_account_ids = fields.Many2many(
        string="Analytic Accounts",
        comodel_name="account.analytic.account",
        relation="rel_commission_computation_item_2_aa",
        column1="computation_id",
        column2="analytic_account_id",
    )
    allowed_currency_ids = fields.Many2many(
        string="Allowed Currencies",
        comodel_name="res.currency",
        compute="_compute_allowed_currency_ids",
        store=False,
    )
    allowed_account_ids = fields.Many2many(
        string="Allowed Accounts",
        comodel_name="account.account",
        compute="_compute_allowed_account_ids",
        store=False,
    )
    allowed_journal_ids = fields.Many2many(
        string="Allowed Journals",
        comodel_name="account.journal",
        compute="_compute_allowed_journal_ids",
        store=False,
    )

    @api.depends("commission_id")
    def _compute_allowed_currency_ids(self):
        for record in self:
            result = False
            if record.commission_id and record.commission_id.type_id:
                result = record._m2o_configurator_get_filter(
                    object_name="res.currency",
                    method_selection=record.commission_id.type_id.currency_selection_method,
                    manual_recordset=record.commission_id.type_id.currency_ids,
                    domain=record.commission_id.type_id.currency_domain,
                    python_code=record.commission_id.type_id.currency_python_code,
                )
            record.allowed_currency_ids = result

    @api.depends("commission_id")
    def _compute_allowed_account_ids(self):
        for record in self:
            result = False
            if record.commission_id and record.commission_id.type_id:
                result = record._m2o_configurator_get_filter(
                    object_name="account.account",
                    method_selection=record.commission_id.type_id.account_selection_method,
                    manual_recordset=record.commission_id.type_id.account_ids,
                    domain=record.commission_id.type_id.account_domain,
                    python_code=record.commission_id.type_id.account_python_code,
                )
            record.allowed_account_ids = result

    @api.depends("commission_id")
    def _compute_allowed_journal_ids(self):
        for record in self:
            result = False
            if record.commission_id and record.commission_id.type_id:
                result = record._m2o_configurator_get_filter(
                    object_name="account.journal",
                    method_selection=record.commission_id.type_id.journal_selection_method,
                    manual_recordset=record.commission_id.type_id.journal_ids,
                    domain=record.commission_id.type_id.journal_domain,
                    python_code=record.commission_id.type_id.journal_python_code,
                )
            record.allowed_journal_ids = result

    def _reload_analytic_account_ids(self):
        self.ensure_one()
        if not self.item_id.group_aa_ok:
            return True

        self.write(
            {
                "analytic_account_ids": [
                    (6, 0, self.move_line_ids.mapped("analytic_account_id").ids)
                ],
            }
        )

    def _reload_source_ml(self):
        self.ensure_one()
        self.write(
            {
                "move_line_ids": [(6, 0, [])],
            }
        )
        criteria = self._prepare_source_ml_criteria()
        Line = self.env["account.move.line"]
        lines = Line.search(criteria)
        self.write(
            {
                "move_line_ids": [(6, 0, lines.ids)],
            }
        )

    def _prepare_source_ml_criteria(self):
        self.ensure_one()
        result = [
            ("account_id", "in", self.allowed_account_ids.ids),
            ("journal_id", "in", self.allowed_journal_ids.ids),
            ("currency_id", "in", self.allowed_currency_ids.ids),
            ("date", ">=", self.commission_id.date_start),
            ("date", "<=", self.commission_id.date_end),
            ("credit", ">", 0.0),
            ("move_id.state", "=", "posted"),
        ]
        if self.item_id.include_team_ok:
            result += [
                (
                    "move_id.invoice_user_id",
                    "in",
                    self.commission_id.all_salesperson_ids.ids,
                ),
            ]
        else:
            result += [
                ("move_id.invoice_user_id", "=", self.commission_id.salesperson_id.id),
            ]

        if self.item_id.group_aa_ok:
            result += [
                ("analytic_account_id", "!=", False),
            ]
        return result

    def _create_commission_detail(self):
        self.ensure_one()
        CommissionDetail = self.env["commission.detail"]
        if self.analytic_account_ids:
            for aa in self.analytic_account_ids:
                CommissionDetail.create(self._prepare_create_commission_detail(aa))
        else:
            CommissionDetail.create(self._prepare_create_commission_detail())

    def _prepare_create_commission_detail(self, aa=False):
        self.ensure_one()
        account = self.item_id.product_id._get_product_account(
            usage_code=self.item_id.usage_id.code
        )
        return {
            "commission_id": self.commission_id.id,
            "computation_item_id": self.id,
            "product_id": self.item_id.product_id.id,
            "name": self.item_id.name,
            "usage_id": self.item_id.usage_id.id,
            "account_id": account.id,
            "analytic_account_id": aa and aa.id or False,
            "uom_quantity": 1.0,
            "uom_id": self.item_id.product_id.uom_id.id,
            "price_unit": 0.0,
        }
