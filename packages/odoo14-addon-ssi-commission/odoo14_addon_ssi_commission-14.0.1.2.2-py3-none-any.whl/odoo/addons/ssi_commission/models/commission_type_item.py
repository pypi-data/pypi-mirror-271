# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class CommissionTypeItem(models.Model):
    _name = "commission_type.item"
    _description = "Commission Type - Item"
    _order = "type_id, sequence, id"

    type_id = fields.Many2one(
        string="Type",
        comodel_name="commission_type",
        ondelete="cascade",
        required=True,
    )
    sequence = fields.Integer(
        string="Sequence",
        default=10,
        required=True,
    )
    item_id = fields.Many2one(
        string="Item",
        comodel_name="commission_item",
        ondelete="restrict",
        required=True,
    )
