from odoo import fields, models, api, exceptions, _
from pytz import timezone
from odoo.addons.resource.models.utils import Intervals


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    lunch_start = fields.Datetime('Lunch Start Time')
    lunch_end = fields.Datetime('Lunch End Time')

    @api.depends('check_in', 'check_out', 'lunch_start', 'lunch_end')
    def _compute_worked_hours(self):
        for attendance in self:
            if attendance.check_out and attendance.check_in and attendance.employee_id:
                calendar = attendance._get_employee_calendar()
                resource = attendance.employee_id.resource_id
                tz = timezone(calendar.tz)
                check_in_tz = attendance.check_in.astimezone(tz)
                check_out_tz = attendance.check_out.astimezone(tz)
                lunch_intervals = calendar._attendance_intervals_batch(
                    check_in_tz, check_out_tz, resource, lunch=True)
                attendance_intervals = Intervals([(check_in_tz, check_out_tz, attendance)]) - lunch_intervals[resource.id]
                delta = sum((i[1] - i[0]).total_seconds() for i in attendance_intervals)
                if attendance.lunch_end and attendance.lunch_start:
                    lunch_start_tz = attendance.lunch_start.astimezone(tz)
                    lunch_end_tz = attendance.lunch_end.astimezone(tz)
                    lunch_inters = Intervals([(lunch_start_tz, lunch_end_tz, attendance)])
                    lunch_delta = sum((i[1] - i[0]).total_seconds() for i in lunch_inters)
                    attendance.worked_hours = (delta - lunch_delta) / 3600.0
                else:
                    attendance.worked_hours = delta / 3600.0
            else:
                attendance.worked_hours = False


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    attendance_state = fields.Selection(selection_add=[('lunch_start', 'Lunch Start'),
                                                       ('lunch_end', 'Lunch End')])

    @api.depends('last_attendance_id.check_in', 'last_attendance_id.check_out', 'last_attendance_id')
    def _compute_attendance_state(self):
        for employee in self:
            att = employee.last_attendance_id.sudo()
            if att.check_in and not att.check_out and not att.lunch_start and not att.lunch_end:
                employee.attendance_state = 'checked_in'
            elif att.check_in and not att.check_out and att.lunch_start and not att.lunch_end:
                employee.attendance_state = 'lunch_start'
            elif att.check_in and not att.check_out and att.lunch_start and att.lunch_end:
                employee.attendance_state = 'lunch_end'
            else:
                employee.attendance_state = 'checked_out'

    # Override
    def _attendance_action_change(self, geo_information=None, **post):
        self.ensure_one()
        action_date = fields.Datetime.now()
        state = post.get('state', None)

        if self.attendance_state == 'checked_out':
            if geo_information:
                vals = {
                    'employee_id': self.id,
                    'check_in': action_date,
                    **{'in_%s' % key: geo_information[key] for key in geo_information}
                }
            else:
                vals = {
                    'employee_id': self.id,
                    'check_in': action_date,
                }
            return self.env['hr.attendance'].create(vals)
        attendance = self.env['hr.attendance'].search([('employee_id', '=', self.id), ('check_out', '=', False)],
                                                      limit=1)
        if attendance:
            data = {}
            if state == 'lunch_start':
                data['lunch_start'] = action_date
                attendance.lunch_start = action_date
            elif state == 'lunch_end':
                data['lunch_end'] = action_date
            elif state == 'check_out':
                data['check_out'] = action_date

            print(data,'.data')
            if geo_information:
                data.update({
                    **{'out_%s' % key: geo_information[key] for key in geo_information}
                })
                attendance.write(data)
            else:
                attendance.write(data)
        else:
            raise exceptions.UserError(_(
                'Cannot perform check out on %(empl_name)s, could not find corresponding check in. '
                'Your attendances have probably been modified manually by human resources.',
                empl_name=self.sudo().name))
        return attendance
