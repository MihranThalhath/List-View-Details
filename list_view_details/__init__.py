from . import models


def uninstall_hook(env):
    param = (
        env["ir.config_parameter"]
        .sudo()
        .get_param("list_view_details.sample_data_loaded")
    )
    if param:
        env.cr.execute(
            "DELETE FROM ir_config_parameter WHERE key = %s",
            ("list_view_details.sample_data_loaded",),
        )
