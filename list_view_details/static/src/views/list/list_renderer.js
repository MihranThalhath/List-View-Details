/** @odoo-module **/

import {ListRenderer} from "@web/views/list/list_renderer";
import {markup} from "@odoo/owl";
import {patch} from "@web/core/utils/patch";
import {session} from "@web/session";
import {useService} from "@web/core/utils/hooks";

patch(ListRenderer.prototype, {
    setup() {
        super.setup(...arguments);
        this.orm = useService("orm");
    },

    getActiveColumns() {
        const columns = super.getActiveColumns();
        if (!this.isX2Many && this.checkListDetailsExists()) {
            if (!columns.find((col) => col.id === "_expand_details")) {
                columns.unshift({
                    id: "_expand_details",
                    type: "_expand_details",
                    name: "_expand_details",
                });
            }
        }
        return columns;
    },

    checkListDetailsExists() {
        const sessionInfo = session;
        if (
            sessionInfo.allowed_models.includes(
                this.props.list?.model?.config?.resModel || this.props.list?.evalContext?.params?.model
            )
        ) {
            return true;
        }
        return false;
    },
    getRecordDetails(record) {
        let details = "";
        if (record.data.view_record_details) {
            details = markup(record.data.view_record_details);
        }
        return details;
    },
    getExpandedRowColspan() {
        let colspan = this.columns.length;
        if (this.hasSelectors) {
            colspan++;
        }
        if (this.hasActionsColumn) {
            colspan++;
        }
        if (this.hasOpenFormViewColumn) {
            colspan++;
        }
        return colspan;
    },
    async expandRecordDetails(record) {
        if (record.data.view_record_details) {
            delete record.data.view_record_details;
            record.expanded = false;
            return;
        }
        const record_details = await this.orm.call("list.view.details", "action_render_qweb_view", [
            this.props.list?.model?.config?.resModel || this.props.list?.evalContext?.params?.model,
            record.evalContext.id,
        ]);
        record.data.view_record_details = markup(record_details);
        record.expanded = true;
    },
});
