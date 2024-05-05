# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class MarketingCommissionTax(models.Model):
    _name = "marketing_commission.tax"
    _description = "Marketing Commission - Tax"
    _inherit = ["mixin.tax_line"]

    # account.move.line
    _partner_id_field_name = "partner_id"
    _analytic_account_id_field_name = "analytic_account_id"
    _label_field_name = "name"
    _amount_currency_field_name = "tax_amount"
    _normal_amount = "debit"

    commission_id = fields.Many2one(
        comodel_name="marketing_commission",
        string="# Commission",
        required=True,
        ondelete="cascade",
    )
    move_id = fields.Many2one(related="commission_id.move_id")
    currency_id = fields.Many2one(related="commission_id.currency_id")
    company_id = fields.Many2one(related="commission_id.company_id")
    company_currency_id = fields.Many2one(related="commission_id.company_currency_id")
    partner_id = fields.Many2one(
        related="commission_id.partner_id",
    )
    date = fields.Date(related="commission_id.date")
    # Additional
    account_move_line_id = fields.Many2one(
        string="Journal Item",
        comodel_name="account.move.line",
        copy=False,
    )
