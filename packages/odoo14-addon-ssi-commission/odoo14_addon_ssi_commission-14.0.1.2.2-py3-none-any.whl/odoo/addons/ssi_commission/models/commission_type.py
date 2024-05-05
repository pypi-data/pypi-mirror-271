# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class CommissionType(models.Model):
    _name = "commission_type"
    _inherit = [
        "mixin.master_data",
        "mixin.account_account_m2o_configurator",
        "mixin.account_journal_m2o_configurator",
        "mixin.res_currency_m2o_configurator",
        "mixin.res_users_m2o_configurator",
    ]
    _description = "Commission Type"
    _account_account_m2o_configurator_insert_form_element_ok = True
    _account_account_m2o_configurator_form_xpath = "//page[@name='account']"
    _account_journal_m2o_configurator_insert_form_element_ok = True
    _account_journal_m2o_configurator_form_xpath = "//page[@name='account']"
    _res_currency_m2o_configurator_insert_form_element_ok = True
    _res_currency_m2o_configurator_form_xpath = "//page[@name='account']"
    _res_users_m2o_configurator_insert_form_element_ok = True
    _res_users_m2o_configurator_form_xpath = "//page[@name='salesperson']"

    item_ids = fields.One2many(
        string="Items",
        comodel_name="commission_type.item",
        inverse_name="type_id",
    )
