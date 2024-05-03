# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class BillOfServicePricelistTask(models.Model):
    _name = "bill_of_service_pricelist_task"
    _description = "Bill of Service To Pricelist Task"
    _inherit = [
        "mixin.product_line_price",
    ]

    bos_pricelist_id = fields.Many2one(
        string="# BoS To Pricelist",
        comodel_name="bill_of_service_pricelist",
        required=True,
        ondelete="cascade",
    )
