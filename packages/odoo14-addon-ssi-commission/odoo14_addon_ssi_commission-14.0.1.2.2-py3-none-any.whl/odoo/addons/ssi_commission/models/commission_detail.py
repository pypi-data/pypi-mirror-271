# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval


class CommissionDetail(models.Model):
    _name = "commission.detail"
    _description = "Commission - Detail"
    _inherit = [
        "mixin.product_line_account",
        "mixin.account_move_single_line_with_field",
        "mixin.localdict",
    ]

    # Accounting Entry Mixin
    _move_id_field_name = "move_id"
    _account_id_field_name = "account_id"
    _partner_id_field_name = "partner_id"
    _analytic_account_id_field_name = "analytic_account_id"
    _currency_id_field_name = "currency_id"
    _company_currency_id_field_name = "company_currency_id"
    _amount_currency_field_name = "price_subtotal"
    _company_id_field_name = "company_id"
    _date_field_name = "date"
    _label_field_name = "name"
    _product_id_field_name = "product_id"
    _uom_id_field_name = "uom_id"
    _quantity_field_name = "uom_quantity"
    _price_unit_field_name = "price_unit"
    _normal_amount = "debit"

    commission_id = fields.Many2one(
        comodel_name="commission",
        string="# Commission",
        required=True,
        ondelete="cascade",
    )
    computation_item_id = fields.Many2one(
        string="Computation Item",
        comodel_name="commission.item_computation",
        required=True,
    )
    item_id = fields.Many2one(
        related="computation_item_id.item_id",
        store=True,
    )
    move_line_ids = fields.Many2many(
        string="Source Journal Items",
        comodel_name="account.move.line",
        compute="_compute_move_line_ids",
        store=False,
    )

    # Related to header
    # Needed for convinience

    move_id = fields.Many2one(
        related="commission_id.move_id",
    )
    currency_id = fields.Many2one(
        related="commission_id.currency_id",
    )
    company_id = fields.Many2one(related="commission_id.company_id")
    company_currency_id = fields.Many2one(related="commission_id.company_currency_id")
    # TODO
    partner_id = fields.Many2one(related="commission_id.partner_id")
    date = fields.Date(related="commission_id.date")

    @api.depends(
        "computation_item_id",
    )
    def _compute_move_line_ids(self):
        for record in self:
            if record.analytic_account_id:
                result = record.computation_item_id.move_line_ids.filtered(
                    lambda r: r.analytic_account_id.id == record.analytic_account_id.id
                )
            else:
                result = record.computation_item_id.move_line_ids
            record.move_line_ids = result

    def _compute_commission(self):
        self.ensure_one()
        localdict = self._get_default_localdict()
        try:
            safe_eval(
                self.item_id.computation_python_code,
                localdict,
                mode="exec",
                nocopy=True,
            )
            price_unit = localdict["price_unit"]
            uom_quantity = localdict["uom_quantity"]
        except Exception as error:
            raise UserError(_("Error evaluating conditions.\n %s") % error)
        self.write(
            {
                "price_unit": price_unit,
                "uom_quantity": uom_quantity,
            }
        )

    def _get_default_localdict(self):
        self.ensure_one()
        _super = super(CommissionDetail, self)
        result = _super._get_default_localdict()
        sum_credit = sum_amount_currency = 0.0
        for ml in self.move_line_ids:
            sum_credit += ml.credit
            sum_amount_currency += ml.amount_currency
        result.update(
            {
                "sum_credit": sum_credit,
                "sum_amount_currency": sum_amount_currency,
            }
        )
        return result
