from odoo import api, models, fields, _
from odoo.exceptions import ValidationError


class ListViewDetails(models.Model):
    _name = "list.view.details"
    _description = "List View Record Details Configuration"

    model_id = fields.Many2one(
        "ir.model",
        string="Model",
        required=True,
        ondelete="cascade",
        copy=False,
    )
    model_name = fields.Char(
        related="model_id.model",
        string="Model Name",
        store=True,
        readonly=True,
        index=True,
        copy=False,
    )
    qweb_view = fields.Text(
        string="QWeb View",
        compute="_compute_qweb_view",
    )
    view_id = fields.Many2one(
        "ir.ui.view",
        string="QWeb View Reference",
        domain=[("type", "=", "qweb")],
        help="Reference to the QWeb view used for rendering record details.",
        ondelete="cascade",
        copy=False,
    )
    active = fields.Boolean(default=True, copy=False)

    def _compute_qweb_view(self):
        for record in self:
            record.qweb_view = record.view_id.arch if record.view_id else ""

    @api.constrains("model_id")
    def _check_unique_model(self):
        for record in self:
            existing = self.search_count(
                [("model_id", "=", record.model_id.id), ("id", "!=", record.id)]
            )
            if existing:
                raise ValidationError(
                    _(
                        f"A configuration for the model '{record.model_id.name}' "
                        "already exists."
                    )
                )

    @api.model
    def _action_load_sale_data(self):
        sale_model = (
            self.env["ir.model"].sudo().search([("model", "=", "sale.order")], limit=1)
        )
        if not sale_model:
            return
        param = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("list_view_details.sample_data_loaded")
        )
        if param:
            return
        # WARNING: The following qweb code was generated with the help of Gemini
        qweb_template = """
<t t-name="sale_order.list_view_details">
    <!-- WARNING: The following qweb code was generated with the help of Gemini -->
    <style type="text/css">
        .o_sale_order_details_table {
            width: 100%;
            border-collapse: collapse;
            margin: 16px 0;
            font-family: -apple-system, BlinkMacSystemFont,
                "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            border-radius: 5px;
            overflow: hidden;
        }

        /* ---------------------------------------------------- */
        /* HEADER STYLES (Blue with White Text) */
        /* ---------------------------------------------------- */
        .o_sale_order_details_table thead tr {
            background-color: #3498db; /* Odoo-like Blue */
            color: #ffffff;
            font-weight: 600;
        }

        .o_sale_order_details_table th,
        .o_sale_order_details_table td {
            padding: 12px 15px;
            text-align: center;
        }

        /* ---------------------------------------------------- */
        /* ROW STRIPING (Zebra Effect) - Light Grey */
        /* ---------------------------------------------------- */
        .o_sale_order_details_table tbody tr:nth-of-type(even) {
            background-color: #f3f3f3; /* Very light grey for even rows */
        }

        /* Adds a nice hover effect for data rows */
        .o_sale_order_details_table tbody tr:hover {
            background-color: #eaf2f8; /* A light blue hover */
        }

        /* ---------------------------------------------------- */
        /* COLUMN STRIPING - New Feature! */
        /* A subtle off-white for the first column */
        /* ---------------------------------------------------- */
        .o_sale_order_details_table td:nth-child(1) {
            background-color: rgba(0, 0, 0, 0.05);
            /* Slightly darker shade for the first column */
            font-weight: 500; /* Makes the first column data slightly stand out */
        }

        /* Ensure the even-numbered rows maintain the column color */
        .o_sale_order_details_table tbody tr:nth-of-type(even) td:nth-child(1) {
             /* Slightly darker shade on the grey row */
             background-color: rgba(0, 0, 0, 0.1);
        }

        /* Final cleanup */
        .o_sale_order_details_table tbody tr {
            border-bottom: 1px solid #dddddd;
        }
        .o_sale_order_details_table tbody tr:last-of-type {
            border-bottom: none;
        }

    </style>

    <table class="o_sale_order_details_table">
        <thead>
            <tr>
                <th>Name</th>
                <th>Quantity</th>
                <th>Unit</th>
                <th>Unit Price</th>
                <th>Tax Incl.</th>
            </tr>
        </thead>
        <tbody>
            <t t-foreach="record.order_line" t-as="line">
                <tr>
                    <td><t t-esc="line.name"/></td>
                    <td><t t-esc="line.product_uom_qty"/></td>
                    <td><t t-esc="line.product_uom_id.name"/></td>
                    <td><t t-esc="line.price_unit"/></td>
                    <td><t t-esc="line.price_total"/></td>
                </tr>
            </t>
        </tbody>
    </table>
</t>
        """
        list_view_details_id = (
            self.env["list.view.details"]
            .sudo()
            .create(
                {
                    "model_id": sale_model.id,
                }
            )
        )
        list_view_details_id.view_id.write({"arch": qweb_template})
        self.env["ir.config_parameter"].sudo().set_param(
            "list_view_details.sample_data_loaded", "true"
        )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            model_name = self.env["ir.model"].sudo().browse(vals.get("model_id")).model
            qweb_view = (
                self.env["ir.ui.view"]
                .sudo()
                .create(
                    {
                        "name": f"list.view.details.{model_name}",
                        "key": f"list.view.details.{model_name}",
                        "type": "qweb",
                        "arch": "",
                        "xml_id": f"list.view.details.{model_name}",
                    }
                )
            )
            vals["view_id"] = qweb_view.id
        return super().create(vals_list)

    def unlink(self):
        for record in self:
            if record.sudo().view_id:
                record.sudo().view_id.unlink()
        return super().unlink()

    def action_open_related_view(self):
        self.ensure_one()
        return {
            "name": _("QWeb View"),
            "type": "ir.actions.act_window",
            "res_model": "ir.ui.view",
            "view_mode": "form",
            "res_id": self.view_id.id,
            "target": "current",
        }

    @api.model
    def action_render_qweb_view(self, model_name, record_id):
        record = self.env[model_name].browse(record_id)
        list_view_record = self.search([("model_name", "=", model_name)], limit=1)
        if not list_view_record:
            return ""
        try:
            rendered_html = self.env["ir.qweb"]._render(
                list_view_record.sudo().view_id.name, {"record": record}
            )
        except Exception as e:
            rendered_html = (
                f"<div class='alert alert-danger'>Error rendering view: {e}</div>"
            )
        return rendered_html
