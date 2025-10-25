from odoo import models


class IrHttp(models.AbstractModel):
    _inherit = "ir.http"

    def session_info(self):
        res = super().session_info()
        list_view_details_records = self.env["list.view.details"].sudo().search([])
        allowed_models = list_view_details_records.mapped("model_name")
        res["allowed_models"] = allowed_models
        return res
