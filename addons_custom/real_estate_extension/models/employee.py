import base64

from odoo import models, fields, api
from odoo.exceptions import UserError, _logger
import requests
import json
import re
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError
import requests
import urllib.parse

import json as py_json  # Use Python's built-in json module
import logging


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    city = fields.Char()
    zip = fields.Char('Pin Code')
    state_id = fields.Many2one('res.country.state')
    corporate_email = fields.Char()
    mobile = fields.Char()
    pan_number = fields.Char('PAN No.')
    branch = fields.Char('Branch Name')
    joining_date = fields.Date()
    grade = fields.Char()
    ctc = fields.Float('CTC')
    active_status = fields.Boolean()
    private_email = fields.Char(string="Private Email", groups="hr.group_hr_user", store=True, related=False)
    partner_id = fields.Many2one('res.partner')
    location = fields.Char()
    project_ids = fields.Many2many('building', string='Assigned Projects', domain="[('active', '=', True)]")
    # employee_number = fields.Char("Employee Number")

    @api.model
    def _generate_access_token(self):
        """
        Generate a new access token using the Keka token endpoint.
        """
        token_url = "https://login.keka.com/connect/token"
        payload = {
            "grant_type": "kekaapi",
            "scope": "kekaapi",
            "client_id": "b52c8371-b0a1-49f7-b347-d60509e9f245",
            "client_secret": "X5aVGfRIvUaL6eRStt1I",
            "api_key": "znquteKxtZRP5FJKL8lncz9BhKBfnWAIY2BgX7dPp08="
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0"
        }
        try:
            response = requests.post(token_url, data=payload, headers=headers)
            _logger.info("Token generation response status: %s", response.status_code)
            _logger.info("Token generation response content: %s", response.text)
            if response.status_code == 200:
                res_data = response.json()
                new_token = res_data.get("access_token")
                if not new_token:
                    raise Exception("Token not found in response: %s" % response.text)
                expires_in = res_data.get("expires_in", 3600)
                expiry_date = datetime.now() + timedelta(seconds=expires_in)
                config = self.env['ir.config_parameter']
                config.set_param('real_estate_extension.employee_api_token', new_token)
                config.set_param('real_estate_extension.employee_api_token_expiry', expiry_date.strftime("%Y-%m-%d %H:%M:%S"))
                _logger.info("Generated new token valid until: %s", expiry_date)
                return new_token
            else:
                raise Exception("Failed to generate token: %s" % response.text)
        except Exception as e:
            _logger.exception("Error generating access token")
            self.env['api.log'].sudo().create({
                'record': 'Token Generation',
                'code': '',
                'response': str(e),
                'date': fields.Datetime.now(),
                'type': 'token',
                'status': 'failed',
                'name': 'Token Generation Failure',
                'direction': 'out',
                # 'args': json.dumps(payload)
            })
            raise e

    @api.model
    def _cron_update_employee(self):
        return True

    # @api.model
    # def _cron_update_employee(self):
    #     """
    #     This function is called periodically via a scheduled action.
    #     It compares the current time with the stored token expiry.
    #     If the token has expired or is not set, it generates a new token.
    #     """
    #     record = self.search([], limit=1)
    #     config = self.env['ir.config_parameter']
    #     token = config.get_param('real_estate_extension.employee_api_token')
    #     api_token_expiry_time = config.get_param('real_estate_extension.employee_api_token_expiry')
    #
    #     employee_fetching_api = config.get_param('real_estate_extension.employee_fetching_api')
    #     today_date = datetime.now().strftime("%Y-%m-%d")
    #     last_modified_value = f"{today_date}T00:00:00Z"
    #     encoded_last_modified = urllib.parse.quote(last_modified_value)
    #     # custom date 2025-03-06T00:00:00Z  + encoded_last_modified +
    #     if not employee_fetching_api:
    #         employee_fetching_api = (
    #             "https://justopulse.keka.com/api/v1/hris/employees?"
    #             "employmentStatus=Working&inProbation=false&"
    #             "inNoticePeriod=false&lastModified=" + encoded_last_modified +
    #             "&pageSize=200"
    #         )
    #         print("emp api ", employee_fetching_api)
    #
    #     now = datetime.now()
    #     if not api_token_expiry_time or now >= fields.Datetime.from_string(api_token_expiry_time):
    #         _logger.info("Access token is missing or expired; generating a new token.")
    #         token = self._generate_access_token()
    #         config.set_param('real_estate_extension.employee_api_token', token)
    #
    #     else:
    #         _logger.info("Current access token is still valid.")
    #     # print("data")
    #
    #     headers = {
    #         "accept": "application/json",
    #         "authorization": "Bearer " + token
    #     }
    #
    #     try:
    #         # Make the GET request to fetch employee data.
    #         res = requests.get(employee_fetching_api, headers=headers)
    #         if res.status_code != 200:
    #             _logger.error("API call failed with status %s: %s", res.status_code, res.text)
    #             # return {"error": "API call failed with status %s" % res.status_code}
    #             status = 'failed'
    #         else:
    #             status = ''
    #
    #         if not res.text.strip():
    #             _logger.error("Empty response from API at %s", employee_fetching_api)
    #             return {"error": "Empty API response"}
    #         data = res.json()
    #         employees = data.get("data", [])
    #
    #         gender_map = {
    #             1: 'male',
    #             2: 'female',
    #             3: 'other'
    #         }
    #         marital_map = {
    #             0: 'single',
    #             1: 'married',
    #             2: 'cohabitant',
    #             3: 'widower',
    #             4: 'divorced'
    #         }
    #         employee_type_map = {
    #             1: 'employee',
    #             2: 'student',
    #             3: 'trainee',
    #             4: 'contractor',
    #             5: 'freelance'
    #         }
    #         employee_role_map = {
    #             "CRM Operations": 'crm',
    #             "Closing TL": 'closing_tl',
    #             "Closing": 'closing_manager',
    #             "Sourcing TL": 'sourcing_tl',
    #             "Sourcing": 'sourcing_manager',
    #             "Marketing ": 'marketing',
    #             "Business Head": 'business_head',
    #             "Site Head": 'site_head',
    #             "Cluster Head": 'cluster_head',
    #             "Sourcing Head": 'sourcing_head',
    #             "Closing Head": 'closing_head',
    #             # "Operations": 'admin',
    #             "CRM Head": 'crm_head',
    #             "CRM Team Lead": 'crm_team_lead',
    #         }
    #         keka_emp_id = ''
    #
    #         for emp_data in employees:
    #             log_message = ""
    #             update_vals = {}
    #             keka_emp_id = emp_data.get("employeeNumber")
    #             keka_work_email = emp_data.get("email")
    #             display_name = emp_data.get("displayName")
    #
    #             # First, try to find a local record by barcode (which stores the unique id).
    #             local_employee = self.search([('barcode', '=', keka_emp_id)], limit=1)
    #
    #             # Convert countryCode to country_id (Many2one)
    #             country_code = emp_data.get("countryCode")
    #             country = self.env['res.country'].sudo().search([('code', '=', country_code)], limit=1)
    #             country_id = country.id if country else False
    #
    #             job_title_str = emp_data.get("secondaryJobTitle")  # This returns a string such as "Site Head"
    #             job_record = self.env['hr.job'].sudo().search([('name', '=', job_title_str)], limit=1)
    #             job_id_value = job_record.id if job_record else False
    #
    #             groups = emp_data.get("groups", [])
    #             department_name = False
    #             for group in groups:
    #                 if group.get("groupType") == 2:
    #                     department_name = group.get("title")
    #                     break
    #             department_id = False
    #             if department_name:
    #                 dept = self.env['hr.department'].sudo().search([('name', '=', department_name)], limit=1)
    #                 department_id = dept.id if dept else False
    #
    #             # Extract parent information from API response
    #             reports_to = emp_data.get("reportsTo", {})
    #             parent_email = reports_to.get("email", "")
    #
    #             # Look up the parent record in hr.employee using the full name.
    #             # parent_record = self.env['hr.employee'].sudo().search([('name', 'ilike', parent_full_name)], limit=1)
    #             parent_record = self.env['hr.employee'].sudo().search([('work_email', 'ilike', parent_email)], limit=1)
    #             parent_id_value = parent_record.id if parent_record else False
    #
    #             l2_manager_data = emp_data.get("l2Manager", {})
    #             first_name = l2_manager_data.get("firstName", "") or ""
    #             last_name = l2_manager_data.get("lastName", "") or ""
    #             l2_manager_full_name = (first_name + " " + last_name).strip()
    #             user_record = self.env['res.users'].sudo().search([('name', 'ilike', l2_manager_full_name)], limit=1)
    #             user_id_value = user_record.id if user_record else False
    #
    #             api_joining_date = emp_data.get("joiningDate")
    #             if api_joining_date:
    #                 parsed_datetime = datetime.strptime(api_joining_date, "%Y-%m-%dT%H:%M:%SZ")
    #                 join_date_str = parsed_datetime.date()
    #             else:
    #                 join_date_str = False
    #
    #             api_birthday = emp_data.get("dateOfBirth")
    #             if api_birthday:
    #                 parsed_birthday = datetime.strptime(api_birthday,"%Y-%m-%dT%H:%M:%SZ")
    #                 birthday_str = parsed_birthday.date()
    #             else:
    #                 birthday_str = False
    #
    #             # Assume user_id_value has been determined by looking up the manager's full name, etc.
    #             if user_id_value and local_employee:
    #                 # Check if another employee (different from the current one) already has this user_id.
    #                 duplicate_employee = self.search([
    #                     ('user_id', '=', user_id_value),
    #                     ('id', '!=', local_employee.id)  # Exclude the current employee record.
    #                 ], limit=1)
    #                 if duplicate_employee:
    #                     _logger.warning(
    #                         "User %s is already assigned to employee ID %s; skipping update of user_id for employee %s.",
    #                         user_id_value, duplicate_employee.id, emp_data.get("employeeNumber"))
    #                     update_vals.pop("user_id", None)  # Remove user_id from the update values.
    #
    #             branch_value = False
    #             custom_fields = emp_data.get("customFields", [])
    #             for field in custom_fields:
    #                 if field.get("title") == "Branch Name":  # adjust title as needed
    #                     branch_value = field.get("value")
    #                     break
    #
    #             update_vals = {
    #                 "name": emp_data.get("displayName"),
    #                 "work_email": emp_data.get("email"),
    #                 "city": emp_data.get("city"),
    #                 "job_title": emp_data.get("jobTitle", {}).get("title"),
    #                 "zip": (emp_data.get("permanentAddress") or {}).get("zip", ""),
    #                 "location": (emp_data.get("permanentAddress") or {}).get("city", ""),
    #                 "grade": (emp_data.get("payGradeInfo") or {}).get("title", ""),
    #                 "parent_id": parent_id_value,
    #                 "role": employee_role_map.get(emp_data.get("secondaryJobTitle")),
    #                 # "place_of_birth": (emp_data.get("nationality") or {}),
    #                 # "user_id": user_id_value, #duplicate key value violates unique constraint "hr_employee_user_uniq"   DETAIL:  Key (user_id, company_id)=(9, 1) already exists.
    #                 # "job_id": job_id_value,
    #                 "branch": branch_value,
    #                 "gender": gender_map.get(emp_data.get("gender")),
    #                 "department_id": department_id,
    #                 "marital": marital_map.get(emp_data.get("maritalStatus")),
    #                 "joining_date": join_date_str,
    #                 "departure_date": emp_data.get("relievingDate"),
    #                 "employee_type": employee_type_map.get(emp_data.get("employeeType"), 'employee'),
    #                 "country_id": country_id,
    #                 # "image_1920": image_data,
    #                 "birthday": birthday_str,
    #                 "mobile_phone": emp_data.get("mobilePhone"),
    #                 "work_phone": emp_data.get("workPhone"),
    #                 # "phone": emp_data.get(""),
    #                 "emergency_phone": emp_data.get("homePhone"),
    #                 "private_email": emp_data.get("personalEmail"),
    #                 "active_status":  True if emp_data.get("accountStatus") == 1 else False,
    #             }
    #
    #             keka_api_data = {
    #                 "name": emp_data.get("displayName"),
    #                 "work_email": emp_data.get("email"),
    #                 "city": emp_data.get("city"),
    #                 "job_title": emp_data.get("jobTitle", {}).get("title"),
    #                 "zip": (emp_data.get("permanentAddress") or {}).get("zip", ""),
    #                 "location": (emp_data.get("permanentAddress") or {}).get("city", ""),
    #                 "grade": (emp_data.get("payGradeInfo") or {}).get("title", ""),
    #                 "parent_id": parent_id_value,
    #                 "role": employee_role_map.get(emp_data.get("secondaryJobTitle")),
    #                 # "place_of_birth": (emp_data.get("nationality") or {}),
    #                 # "country_of_birth": (emp_data.get("permanentAddress") or {}).get("countryCode", ""),
    #                 # "user_id": user_id_value, #duplicate key value violates unique constraint "hr_employee_user_uniq"   DETAIL:  Key (user_id, company_id)=(9, 1) already exists.
    #                 # "job_id": job_id_value,
    #                 "branch": branch_value,
    #                 "gender": gender_map.get(emp_data.get("gender")),
    #                 "department_id": department_id,
    #                 "marital": marital_map.get(emp_data.get("maritalStatus")),
    #                 "joining_date": join_date_str,
    #                 "departure_date": emp_data.get("relievingDate"),
    #                 "employee_type": employee_type_map.get(emp_data.get("employeeType"), 'employee'),
    #                 "country_id": country_id,
    #                 "birthday": birthday_str,
    #                 "mobile_phone": emp_data.get("mobilePhone"),
    #                 "work_phone": emp_data.get("workPhone"),
    #                 "emergency_phone": emp_data.get("homePhone"),
    #                 "private_email": emp_data.get("personalEmail"),
    #                 # "image_1920": image_data,
    #                 "active_status":  True if emp_data.get("accountStatus") == 1 else False,
    #             }
    #             # Extract the image URL from the Keka API response.
    #             image_info = emp_data.get("image", {})
    #             thumbs = image_info.get("thumbs", {})
    #             image_url = thumbs.get("200x200")
    #             image_data = False
    #
    #             if image_url:
    #                 response = None
    #                 try:
    #                     response = requests.get(image_url)
    #                     if response.status_code == 200:
    #                         image_data = base64.b64encode(response.content).decode('utf-8').strip()
    #                     else:
    #                         _logger.warning("Failed to fetch image from URL: %s (Status Code: %s)", image_url,
    #                                         response.status_code)
    #                 except Exception as e:
    #                     _logger.exception("Error fetching image from URL: %s", image_url)
    #
    #             local_image = getattr(local_employee, "image_1920", None)
    #             if local_image:
    #                 if isinstance(local_image, bytes):
    #                     local_image_str = local_image.decode('utf-8').strip()
    #                 else:
    #                     local_image_str = local_image.strip()
    #             else:
    #                 local_image_str = ""
    #
    #             vals_to_update = {}
    #
    #                     # log_message += "Error updating image. "
    #                     # status = 'failed'
    #             # else:
    #             #     log_message += f"No update needed for employee {keka_emp_id}. "
    #             #     status = 'success'
    #
    #                 # if update_vals:
    #                 #     try:
    #                 #         local_employee.write(update_vals)
    #                 #         # Now, if the write is successful, update the log message.
    #                 #         if "image_1920" in update_vals:
    #                 #             log_message += "Image updated. "
    #                 #         status = 'success'
    #                 #     except Exception as e:
    #                 #         _logger.exception("Error updating employee %s", keka_emp_id)
    #                 #         status = 'failure'
    #
    #             # vals_to_update = {}
    #             keka_api_updated = {}
    #             if local_employee:
    #                 # Compare each field; update only if differences are found.
    #                 log_update_vals = keka_api_data.copy()
    #                 log_update_vals.pop("image_1920", None)
    #
    #                 log_vals_update = vals_to_update.copy()
    #                 log_vals_update.pop("image_1920", None)
    #
    #                 for field_name, new_value in update_vals.items():
    #                     local_value = getattr(local_employee, field_name, None)
    #                     try:
    #                         if local_value.id != new_value:
    #                             vals_to_update[field_name] = new_value
    #                     except:
    #
    #                         if local_value != new_value and new_value is not None:
    #                             vals_to_update[field_name] = new_value
    #
    #                 for field_name2, new_value2 in keka_api_data.items():
    #                     local_value = getattr(local_employee, field_name2, None)
    #                     try:
    #                         if local_value.id != new_value2:
    #                             keka_api_updated[field_name2] = new_value2
    #                     except:
    #                         if local_value != new_value2 and new_value2 is not None:
    #                             keka_api_updated[field_name2] = new_value2
    #                 # print(vals_to_update)
    #
    #                 log_update_vals2 = vals_to_update.copy()
    #                 log_update_vals2.pop("image_1920", None)
    #
    #                 if vals_to_update:
    #                     # print(vals_to_update, "- Before write")
    #                     _logger.info("Updating employee %s with values %s", keka_emp_id, vals_to_update)
    #                     try:
    #                         local_employee.write(vals_to_update)
    #                         log_message += "Employee updated successfully. "
    #                         status = 'success'
    #                     except Exception as e:
    #                         log_message += f"Error updating employee: {str(e)}. "
    #                         status = 'failed'
    #                 else:
    #                     _logger.info("No update needed for employee %s", keka_emp_id)
    #             else:
    #                 # Create a new employee record if no matching record exists.
    #                 # _logger.info("Creating new employee record for employeeNumber %s", keka_emp_id)
    #                 # print(update_vals, "- before create vals_to_update")
    #                 update_vals['barcode'] = keka_emp_id
    #                 update_vals['image_1920'] = image_data
    #
    #                 existing_emp = self.env['hr.employee'].sudo().search([('work_email', '=', keka_work_email)])
    #                 if not existing_emp:
    #                     self.create(update_vals)
    #                     # update_vals['barcode'] = keka_emp_id
    #                     # update_vals['image_1920'] = image_data
    #                     log_message += "Employee created successfully. "
    #                     status = 'success'
    #                     _logger.info("Employee %s created successfully", keka_emp_id)
    #                 else:
    #                     log_message += f"Failed to create employee {keka_emp_id}: Work email {keka_work_email} already exists. "
    #                     # work_email_msg = emp_data.get("email")
    #                     status = 'failed'
    #                     _logger.warning("Employee with work email %s already exists. Skipping creation.", existing_emp.work_email)
    #
    #             # Check if image data is available and different from the current image.
    #             if image_data and local_image_str != image_data:
    #                 vals_to_update["image_1920"] = image_data
    #
    #             # If there are values to update, attempt to write them.
    #             if vals_to_update:
    #                 try:
    #                     local_employee.write(vals_to_update)
    #                     # Re-read the image field after the write.
    #                     updated_image = getattr(local_employee, "image_1920", None)
    #                     if updated_image:
    #                         if isinstance(updated_image, bytes):
    #                             updated_image_str = updated_image.decode('utf-8').strip()
    #                         else:
    #                             updated_image_str = updated_image.strip()
    #                     else:
    #                         updated_image_str = ""
    #
    #                     # Verify the image update.
    #                     if updated_image_str == image_data:
    #                         log_message += "Image updated. "
    #                         status = 'success'
    #                     # else:
    #                     #     log_message += "Image update failed. "
    #                     #     status = 'failed'
    #                 except Exception as e:
    #                     _logger.exception("Error updating employee %s", keka_emp_id)
    #
    #             role_from_api = emp_data.get("secondaryJobTitle")
    #             role_value = employee_role_map.get(emp_data.get("secondaryJobTitle"))
    #             if not role_value:
    #                 log_message += f"Failed to update the role. '{role_from_api}' is invalid. "
    #                 status = 'failed'
    #                 _logger.warning(
    #                     "Role mismatch for employee %s: received role '%s' is invalid or not mapped .",
    #                     keka_emp_id, emp_data.get("secondaryJobTitle")
    #                 )
    #             api_gender = gender_map.get(emp_data.get("gender"))
    #             local_gender = local_employee.gender if local_employee else None
    #             if api_gender and local_gender is not None and local_gender != api_gender:
    #                 log_message += f"Gender mismatch: API value '{api_gender}' vs local value '{local_employee.gender}'. "
    #
    #             api_marital = marital_map.get(emp_data.get("maritalStatus"))
    #             local_marital = local_employee.marital if local_employee else None
    #             if api_marital and local_marital is not None and local_marital != api_marital:
    #                 log_message += f"Marital status mismatch: API value '{api_marital}' vs local value '{local_employee.marital}'. "
    #
    #             api_emp_type = employee_type_map.get(emp_data.get("employeeType"))
    #             local_emp_type = local_employee.employee_type if local_employee else None
    #             if api_emp_type and local_emp_type != api_emp_type:
    #                 log_message += f"Employee type mismatch: API value '{api_emp_type}' vs local value '{local_employee.employee_type}'. "
    #
    #             if ("Employee updated successfully." in log_message or "Employee created successfully." in log_message or "Image updated." in log_message):
    #                 status = 'success'
    #
    #             if log_message:
    #                 self.env['api.log'].sudo().create({
    #                     'record': keka_emp_id,
    #                     'code': 200 if status == 'success' else '',
    #                     'response': log_message,
    #                     'date': fields.Datetime.now(),
    #                     'type': 'employee',
    #                     'status': status,
    #                     'name': f'{display_name}',
    #                     'direction': 'in',
    #                     'args': str(keka_api_updated)
    #                 })
    #         return True
    #
    #     except Exception as e:
    #         # print(update_vals, "- After Exception")
    #         _logger.exception("Error updating employee data: %s", e)
    #         return {"error": str(e)}


    @api.constrains('mobile', 'mobile_phone', 'work_phone', 'emergency_contact', 'emergency_phone')
    def contact_fields_validation(self):
        for record in self:
            # if record.mobile_phone and not re.match(r'^\d{10}$', record.mobile_phone):
            #     raise ValidationError('Work Mobile must be exactly 10 digits.')
            if record.work_phone and not record.work_phone.isdigit():
                raise ValidationError('Work Phone must contain only digits.')
            if record.mobile and not re.match(r'^\d{10}$', record.mobile):
                raise ValidationError('Mobile must be exactly 10 digits.')
            # if record.emergency_contact and not re.match(r'^\d{10}$', record.emergency_contact):
            #     raise ValidationError('Emergency Contact must be exactly 10 digits.')
            if record.emergency_phone and not record.emergency_phone.isdigit():
                raise ValidationError('Emergency Phone must contain only digits.')

    def process_employee_api(self, role=False):
        employee_id = self
        # commented fields - because not in mobile app
        employee_role = employee_id.role or ''
        if role:
            employee_role = role
        params = {
            "name": employee_id.name,
            "employee_id": employee_id.id,
            "pan": employee_id.pan_number or "",
            # "job_position": employee_id.job_title or "",
            "work_mobile": employee_id.mobile_phone or "",
            "work_phone": employee_id.work_phone or "",
            "date_of_birth": employee_id.birthday.strftime('%d/%m/%Y') if employee_id.birthday else "",
            # "department": employee_id.department_id.name or "",
            "manager": employee_id.parent_id.id or "",
            "gender": 1 if employee_id.gender == 'male' else 2 if employee_id.gender == 'female' else 1 if employee_id.gender == 'other' else 1,
            # "joining_date": employee_id.joining_date.strftime('%d/%m/%Y') if employee_id.joining_date else "",
            "city": employee_id.city or "",
            "location": employee_id.location or "",
            # "zip": employee_id.zip or "",
            "email": employee_id.private_email or "",
            "corporate_email": employee_id.corporate_email or "",
            "personal_mobile": employee_id.mobile or "",
            # "marital_status": employee_id.marital or "",
            # "emergency_contact_number": employee_id.emergency_contact or "",
            "active_status": True if employee_id.active_status else False,
            "relieving_date": employee_id.departure_date.strftime('%d/%m/%Y') if employee_id.departure_date else "",
            "role": employee_role,
            # "ctc": employee_id.ctc,,
            'rom': True if employee_id.is_rom and employee_id.role in ('sourcing_tl', 'sourcing_manager') else False
        }
        url = self.env['ir.config_parameter'].sudo().get_param('real_estate_extension.employee_api_url')
        username = self.env['ir.config_parameter'].sudo().get_param(
            'real_estate_extension.employee_api_username')
        password = self.env['ir.config_parameter'].sudo().get_param('real_estate_extension.employee_api_key')

        data = {
            'params': {
                'login': username,
                'password': password,
                'record': params
            }
        }
        code = ''
        try:
            headers = {"Content-Type": "application/json; charset=utf-8"}
            response = requests.post(url, headers=headers, json=data)
            if response.ok:
                res = json.loads(response.text)
                if res.get('status') in (201, 200):
                    code = res.get('status')
                    response = response.content
                    status = 'success'
                    pass
                else:
                    raise ValidationError(str(res))
            else:
                raise ValidationError(str(response.text))
        except Exception as e:
            response = e
            status = 'failed'
            pass
        self.env['api.log'].sudo().create({
            'record': str(employee_id.id),
            'code': code,
            'response': response,
            'date': datetime.now(),
            'type': 'employee',
            'status': status,
            'name': employee_id.barcode,
            'direction': 'out',
            'args': str(data)
        })

    @api.model
    def create(self, vals):
        res = super(HrEmployee, self).create(vals)
        out_api = self.env['ir.config_parameter'].sudo().get_param('real_estate_extension.enable_employee_out_api')
        if out_api and res:
            res.process_employee_api()
        return res

    def write(self, vals):
        res = super(HrEmployee, self).write(vals)
        out_api = self.env['ir.config_parameter'].sudo().get_param('real_estate_extension.enable_employee_out_api')
        if out_api and self:
            self.process_employee_api()
        return res

    @api.constrains('work_email', 'private_email')
    def prevent_email_duplication(self):
        if self.work_email:
            if self.env['hr.employee'].sudo().search([('work_email', '=', self.work_email), ('id', '!=', self.id)]):
                raise UserError('Employee with Work Email already exists!')
        if self.private_email:
            if self.env['hr.employee'].sudo().search([('private_email', '=', self.private_email), ('id', '!=', self.id)]):
                raise UserError('Employee with Email already exists!')

    _sql_constraints = [
        ('unique_name_per_employee', 'UNIQUE (name)', 'Employee name must be unique!'),
        ('unique_corporate_email_per_employee', 'UNIQUE (corporate_email)', 'Employee Corporate Email must be unique!'),
    ]

    def _message_log(self, **kwargs):
        if kwargs.get('body') and "<b>Congratulations!</b> May I recommend you to setup an" in kwargs.get('body'):
            return
        return super(HrEmployee, self._post_author())._message_log(**kwargs)

    @api.model
    def default_get(self, fields_list):
        res = super(HrEmployee, self).default_get(fields_list)
        res['country_id'] = self.env.company.country_id.id
        res['state_id'] = self.env.company.state_id.id
        return res

    @api.onchange('state_id')
    def onchange_state(self):
        self.country_id = self.state_id.country_id
