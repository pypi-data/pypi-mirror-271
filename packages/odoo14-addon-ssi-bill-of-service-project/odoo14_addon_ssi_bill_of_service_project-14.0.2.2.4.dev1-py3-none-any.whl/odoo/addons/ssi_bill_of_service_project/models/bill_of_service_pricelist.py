# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class BillOfServicePricelist(models.Model):
    _name = "bill_of_service_pricelist"
    _inherit = [
        "bill_of_service_pricelist",
    ]

    task_ids = fields.One2many(
        string="Task",
        comodel_name="bill_of_service_pricelist_task",
        inverse_name="bos_pricelist_id",
        readonly=True,
    )
    amount_task = fields.Monetary(
        string="Amount Task",
        compute="_compute_amount_task",
        store=True,
        currency_field="currency_id",
    )
    task_pricelist_id = fields.Many2one(
        string="Task Pricelist",
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

    @api.depends(
        "task_ids",
        "task_ids.price_subtotal",
    )
    def _compute_amount_task(self):
        for record in self:
            result = 0.0
            for task in record.task_ids:
                result += task.price_subtotal
            record.amount_task = result
            record._compute_amount_total()

    @api.onchange(
        "currency_id",
    )
    def onchange_task_pricelist_id(self):
        self.task_pricelist_id = False

    @api.model
    def _get_amount_field(self):
        _super = super(BillOfServicePricelist, self)
        result = _super._get_amount_field()
        result.append("amount_task")
        return result

    def action_populate_task(self):
        for record in self.sudo():
            record._populate_task()

    def _populate_task(self):
        self.ensure_one()
        Task = self.env["bill_of_service_pricelist_task"]
        self.task_ids.unlink()
        for task in self.bos_id.task_ids:
            result = Task.create(task._prepare_pricelist_data(self))
            result.onchange_price_unit()
            result._compute_price()

        for bos in self.bos_id.all_structure_ids:
            for task in bos.task_ids:
                result = Task.create(task._prepare_pricelist_data(self))
                result.onchange_price_unit()
                result._compute_price()

        self._process_component_task(self.bos_id)

    def _process_component_task(self, bos):
        Task = self.env["bill_of_service_pricelist_task"]
        for component in bos.component_ids:
            for task in component.task_ids:
                result = Task.create(task._prepare_pricelist_data(self))
                result.onchange_price_unit()
                result._compute_price()
            for bos1 in component.all_structure_ids:
                for task in bos1.task_ids:
                    result = Task.create(task._prepare_pricelist_data(self))
                    result.onchange_price_unit()
                    result._compute_price()
            if component.component_ids:
                self._process_component_task(component)
