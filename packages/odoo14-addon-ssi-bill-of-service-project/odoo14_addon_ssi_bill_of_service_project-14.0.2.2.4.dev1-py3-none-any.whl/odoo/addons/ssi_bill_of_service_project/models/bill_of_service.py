# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class BillOfService(models.Model):
    _name = "bill_of_service"
    _inherit = ["bill_of_service"]

    task_ids = fields.One2many(
        string="Tasks",
        comodel_name="bill_of_service.task",
        inverse_name="bos_id",
        copy=True,
    )
    all_task_ids = fields.Many2many(
        string="All Tasks",
        comodel_name="bill_of_service.task",
        compute="_compute_all_task_ids",
        store=False,
    )
    total_work_estimation = fields.Float(
        string="Total Work Estimation",
        compute="_compute_total_work_estimation",
        store=True,
    )

    def _compute_all_task_ids(self):
        for record in self:
            result = self.task_ids
            for parent in record.all_structure_ids:
                result += parent.all_task_ids

            for component in record.component_ids:
                result += component.all_task_ids
            record.all_task_ids = result

    @api.depends(
        "task_ids.work_estimation",
    )
    def _compute_total_work_estimation(self):
        for record in self:
            result = 0.0
            for task in record.task_ids:
                result += task.total_work_estimation
            record.total_work_estimation = result
