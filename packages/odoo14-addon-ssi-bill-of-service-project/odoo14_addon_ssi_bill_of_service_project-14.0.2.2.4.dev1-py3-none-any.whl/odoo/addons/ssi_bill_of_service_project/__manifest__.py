# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Bill of Service - Project Integration",
    "version": "14.0.2.2.3",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "ssi_bill_of_service",
        "ssi_task_work_log",
        "ssi_work_log_cost",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/bill_of_service_views.xml",
        "views/bill_of_service_pricelist_views.xml",
    ],
    "demo": [],
    "images": [],
}
