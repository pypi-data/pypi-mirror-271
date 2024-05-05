# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class MarketingCommissionItem(models.Model):
    _name = "marketing_commission_item"
    _inherit = [
        "mixin.master_data",
        "mixin.account_account_m2o_configurator",
        "mixin.account_journal_m2o_configurator",
        "mixin.res_currency_m2o_configurator",
    ]
    _description = "Marketing Commission Item"
    _account_account_m2o_configurator_insert_form_element_ok = True
    _account_account_m2o_configurator_form_xpath = "//page[@name='account']"
    _account_journal_m2o_configurator_insert_form_element_ok = True
    _account_journal_m2o_configurator_form_xpath = "//page[@name='account']"
    _res_currency_m2o_configurator_insert_form_element_ok = True
    _res_currency_m2o_configurator_form_xpath = "//page[@name='account']"

    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
        required=True,
    )
    computation_python_code = fields.Text(
        string="Computation Code",
        required=True,
        default="price_unit = uom_quantity = 0.0",
    )
    usage_id = fields.Many2one(
        string="Usage",
        comodel_name="product.usage_type",
        required=True,
    )
