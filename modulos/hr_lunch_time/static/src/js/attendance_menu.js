/* @odoo-module */

import { patch } from "@web/core/utils/patch";
import { ActivityMenu } from "@hr_attendance/components/attendance_menu/attendance_menu";
import { rpc } from "@web/core/network/rpc";

patch(ActivityMenu.prototype, {
    setup(){
        super.setup();
    },

    async searchReadEmployee(){
        await super.searchReadEmployee();
        if (this.employee.id) {
            this.state.checkedIn = this.employee.attendance_state !== "checked_out";
            this.state.emp_state = this.employee.attendance_state;
        }
    },

    async signInOut(state) {
        navigator.geolocation.getCurrentPosition(
            async ({coords: {latitude, longitude}}) => {
                await rpc("/hr_attendance/systray_check_in_out", {
                    latitude,
                    longitude,
                    state,
                })
                await this.searchReadEmployee()
            },
            async err => {
                await rpc("/hr_attendance/systray_check_in_out", {
                    state
                })
                await this.searchReadEmployee()
            }
        )
    }
});