from odoo import http
from odoo.http import request
import datetime
import os


class ProjectTransactionsController(http.Controller):
    @http.route('/project_transactions/download_sample_file', type='http', auth='user')
    def download_sample_file(self):
        # Define the path to the sample file
        module_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(module_path, '../static/src/file/sample_file.xlsx')

        # Check if file exists
        if not os.path.isfile(file_path):
            return request.not_found()

        with open(file_path, 'rb') as file:
            file_data = file.read()

        # Set the headers to download the file
        headers = [
            ('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
            ('Content-Disposition', 'attachment; filename="sample.xlsx"')
        ]

        return request.make_response(file_data, headers=headers)

    @http.route(['/correct_api_affected_employee_data'], type='http', auth="public")
    def correct_api_affected_employee_data(self):
        if request.env.user.has_group('base.group_system'):
            old_data = [
                {'id': 1939, 'name': 'Sonali  Birajdar', 'pan_number': 'CFTPB5387R', 'job_title': 'Assistant Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1992, 6, 17),
                 'department_id': 9, 'parent_id': 689, 'gender': 'female', 'joining_date': datetime.date(2024, 9, 16),
                 'departure_date': None, 'city': 'Mumbai', 'zip': '400087', 'private_email': 'sbirajdar87@gmail.com',
                 'corporate_email': 'sonali.birajdar@justo.co.in', 'work_email': 'sonali.birajdar@justo.co.in',
                 'mobile': '8850755683', 'marital': 'single', 'emergency_contact': '9619246604', 'active_status': True,
                 'ctc': 45833.0, 'location': 'Regional Office_Mumbai', 'barcode': 'JUS708'},
                {'id': 1943, 'name': 'Nikhil Sunil Chavan', 'pan_number': 'ALVPC4105C', 'job_title': 'Senior Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1991, 2, 10),
                 'department_id': 15, 'parent_id': 103, 'gender': 'male', 'joining_date': datetime.date(2024, 9, 23),
                 'departure_date': None, 'city': 'Nerul', 'zip': '400706', 'private_email': 'nikhilchavan555@gmail.com',
                 'corporate_email': 'nikhil.chavan@justo.co.in', 'work_email': 'nikhil.chavan@justo.co.in',
                 'mobile': '9029614023', 'marital': 'married', 'emergency_contact': '8108431792', 'active_status': True,
                 'ctc': 108333.0, 'location': 'Mumbai Western', 'barcode': 'JUS714'},
                {'id': 1966, 'name': 'Akshay Anil Wagh', 'pan_number': 'AEYPW1087R', 'job_title': 'Assistant Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1996, 10, 4),
                 'department_id': 2, 'parent_id': 422, 'gender': 'male', 'joining_date': datetime.date(2024, 10, 3),
                 'departure_date': None, 'city': 'Thane', 'zip': '400608', 'private_email': 'akshaywagh758@gmail.com',
                 'corporate_email': 'akshay.wagh@justo.co.in', 'work_email': 'akshay.wagh@justo.co.in',
                 'mobile': '7208808067', 'marital': 'single', 'emergency_contact': '8454902002', 'active_status': True,
                 'ctc': 45500.0, 'location': 'KDMC', 'barcode': 'JUS718'},
                {'id': 1948, 'name': 'Priti  Vishal Sharma', 'pan_number': 'BNNPS5500C',
                 'job_title': 'Assistant General Manager', 'mobile_phone': '000000000', 'work_phone': '000000',
                 'birthday': datetime.date(1976, 5, 16), 'department_id': 2, 'parent_id': 243, 'gender': 'female',
                 'joining_date': datetime.date(2024, 9, 25), 'departure_date': None, 'city': 'Mumbai', 'zip': '400069',
                 'private_email': 'Pritisakshat2009@gmail.com', 'corporate_email': 'priti.sharma@justo.co.in',
                 'work_email': 'priti.sharma@justo.co.in', 'mobile': '9321110043', 'marital': 'married',
                 'emergency_contact': '9821110042', 'active_status': True, 'ctc': 123500.0,
                 'location': 'Mumbai Western', 'barcode': 'JUS715'},
                {'id': 1952, 'name': 'Mugdha Sanjay Ambawale', 'pan_number': 'DNAPA1791Q', 'job_title': 'Executive',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(2001, 2, 13),
                 'department_id': 18, 'parent_id': None, 'gender': 'female', 'joining_date': datetime.date(2024, 9, 30),
                 'departure_date': None, 'city': 'Pune', 'zip': '412101',
                 'private_email': 'mugdha.ambawale0713@gmail.com', 'corporate_email': 'mugdha.ambawale@justo.co.in',
                 'work_email': 'mugdha.ambawale@justo.co.in', 'mobile': '9309538358', 'marital': 'single',
                 'emergency_contact': '9922888832', 'active_status': True, 'ctc': 31667.0, 'location': 'Pune',
                 'barcode': 'JUS717'},
                {'id': 336, 'name': 'Amarnath Dhone', 'pan_number': 'ASHPD6800G',
                 'job_title': 'Assistant General Manager', 'mobile_phone': '000000000', 'work_phone': '000000',
                 'birthday': datetime.date(1984, 4, 20), 'department_id': 2, 'parent_id': 459, 'gender': 'male',
                 'joining_date': datetime.date(2021, 6, 19), 'departure_date': None, 'city': 'City', 'zip': '000000',
                 'private_email': 'amar3030@gmail.com', 'corporate_email': 'amarnath.dhone@justo.co.in',
                 'work_email': 'amarnath.dhone@justo.co.in', 'mobile': '8080316496', 'marital': 'single',
                 'emergency_contact': '00000000', 'active_status': True, 'ctc': 114666.0, 'location': 'Pune',
                 'barcode': 'JUS0279'},
                {'id': 1941, 'name': 'sakshi Vijay  Natuskar', 'pan_number': 'BVJPN3238G', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(2000, 1, 1),
                 'department_id': 2, 'parent_id': 1043, 'gender': 'female', 'joining_date': datetime.date(2024, 9, 16),
                 'departure_date': None, 'city': 'Mumbai ', 'zip': '401208',
                 'private_email': 'sakshinatuskar27@gmail.com', 'corporate_email': 'sakshi.natuskar@justo.co.in',
                 'work_email': 'sakshi.natuskar@justo.co.in', 'mobile': '7066115586', 'marital': 'single',
                 'emergency_contact': '8169514894', 'active_status': True, 'ctc': 33800.0, 'location': 'Mumbai Western',
                 'barcode': 'JUS710'},
                {'id': 1947, 'name': 'Vivek Vishwamitra Pandey', 'pan_number': 'EDDPP1021A', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1999, 6, 19),
                 'department_id': 2, 'parent_id': 1309, 'gender': 'male', 'joining_date': datetime.date(2024, 9, 18),
                 'departure_date': None, 'city': 'Bhayandar', 'zip': '401101',
                 'private_email': 'pandeyvicky198@gmail.com', 'corporate_email': 'vivek.pandey@justo.co.in',
                 'work_email': 'vivek.pandey@justo.co.in', 'mobile': '9819451750', 'marital': 'single',
                 'emergency_contact': '9702445820', 'active_status': True, 'ctc': 54167.0, 'location': 'Mumbai Western',
                 'barcode': 'JUS711'},
                {'id': 1949, 'name': 'Rohit Patil', 'pan_number': 'EBTPP7861J', 'job_title': 'Assistant Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1998, 8, 10),
                 'department_id': 18, 'parent_id': 696, 'gender': 'male', 'joining_date': datetime.date(2024, 9, 25),
                 'departure_date': None, 'city': 'Dhule', 'zip': '424005', 'private_email': 'rdpatil1096@gmail.com',
                 'corporate_email': 'rohit.p@justo.co.in', 'work_email': 'rohit.p@justo.co.in', 'mobile': '8668928792',
                 'marital': 'single', 'emergency_contact': '9921049111', 'active_status': True, 'ctc': 62500.0,
                 'location': 'Regional Office _ Pune', 'barcode': 'JUS716'},
                {'id': 1962, 'name': 'Aditya Guruling Nagare', 'pan_number': '000000', 'job_title': 'Assistant Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(2006, 1, 5),
                 'department_id': 2, 'parent_id': 304, 'gender': 'male', 'joining_date': datetime.date(2024, 1, 5),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'adityanagare3006@gmail.com',
                 'corporate_email': 'aditya.nagare1@justo.co.in', 'work_email': 'aditya.nagare1@justo.co.in',
                 'mobile': '00000000', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 49779.0, 'location': 'Pune', 'barcode': 'JUS1338'},
                {'id': 1940, 'name': 'Ravi Kumar Dutta', 'pan_number': 'CCYPD9178E', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1996, 10, 13),
                 'department_id': 2, 'parent_id': 854, 'gender': 'male', 'joining_date': datetime.date(2024, 9, 18),
                 'departure_date': None, 'city': 'Mumbai', 'zip': '401105',
                 'private_email': 'ravikumardutta1996@gmail.com', 'corporate_email': 'ravikumar.dutta@justo.co.in',
                 'work_email': 'ravikumar.dutta@justo.co.in', 'mobile': '9702445820', 'marital': 'single',
                 'emergency_contact': '8169064239', 'active_status': True, 'ctc': 65833.0, 'location': 'Mumbai Western',
                 'barcode': 'JUS712'},
                {'id': 2415, 'name': 'Adarsh Kendre', 'pan_number': '000000', 'job_title': 'Management Trainee',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(2001, 4, 23),
                 'department_id': 10, 'parent_id': 841, 'gender': 'male', 'joining_date': datetime.date(2024, 10, 14),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'adarshkendre123@gmail.com',
                 'corporate_email': 'adarsh.kendre@justo.co.in', 'work_email': 'adarsh.kendre@justo.co.in',
                 'mobile': '00000000', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 20000.0, 'location': 'Regional Office _ Pune', 'barcode': 'JUS722'},
                {'id': 1413, 'name': 'Divya Waghela', 'pan_number': 'AFWPW3977K', 'job_title': 'Assistant Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1999, 5, 12),
                 'department_id': 2, 'parent_id': 304, 'gender': 'female', 'joining_date': datetime.date(2023, 1, 6),
                 'departure_date': None, 'city': 'Pune', 'zip': '411027', 'private_email': 'divyawaghela25@gmail.com',
                 'corporate_email': 'divya.waghela@justo.co.in', 'work_email': 'divya.waghela@justo.co.in',
                 'mobile': '9579346517', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 39779.0, 'location': 'Pune', 'barcode': 'JUS1019'},
                {'id': 1302, 'name': 'Devendra Hydrabadkar', 'pan_number': 'AKZPH1185L', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1994, 9, 29),
                 'department_id': 2, 'parent_id': 336, 'gender': 'male', 'joining_date': datetime.date(2023, 2, 7),
                 'departure_date': None, 'city': 'City', 'zip': '000000',
                 'private_email': 'DevendraHydrabadkar@icloud.com',
                 'corporate_email': 'devendra.hydrabadkar@justo.co.in',
                 'work_email': 'devendra.hydrabadkar@justo.co.in', 'mobile': '8983338258', 'marital': 'single',
                 'emergency_contact': '00000000', 'active_status': True, 'ctc': 79779.0, 'location': 'Pune',
                 'barcode': 'JUS1083'},
                {'id': 1618, 'name': 'Aarti  Bhajanlal Bachwani', 'pan_number': 'CFNPB5809Q',
                 'job_title': 'Senior Executive', 'mobile_phone': '000000000', 'work_phone': '000000',
                 'birthday': datetime.date(1997, 5, 7), 'department_id': 2, 'parent_id': 848, 'gender': 'female',
                 'joining_date': datetime.date(2024, 1, 15), 'departure_date': None, 'city': 'tHANE', 'zip': '421002',
                 'private_email': 'aarti.bachwani07@gmail.com', 'corporate_email': 'aarti.bachwani@justo.co.in',
                 'work_email': 'aarti.bachwani@justo.co.in', 'mobile': '7972343421', 'marital': 'single',
                 'emergency_contact': '9284226506', 'active_status': True, 'ctc': 27350.0, 'location': 'KDMC',
                 'barcode': 'JUS1356'},
                {'id': 1491, 'name': 'Akash Thorat', 'pan_number': '000000', 'job_title': 'Assistant Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(2000, 3, 27),
                 'department_id': 2, 'parent_id': 450, 'gender': 'male', 'joining_date': datetime.date(2023, 6, 5),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'akashthorat7474@gmail.com',
                 'corporate_email': 'akash.thorat@justo.co.in', 'work_email': 'akash.thorat@justo.co.in',
                 'mobile': '00000000', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 45278.0, 'location': 'Pune', 'barcode': 'JUS1171'},
                {'id': 59, 'name': 'Akash Ozarkar', 'pan_number': 'AEHPO7939P', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1996, 3, 8),
                 'department_id': 2, 'parent_id': 1732, 'gender': 'male', 'joining_date': datetime.date(2021, 1, 21),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'akashozarkar7@gmail.com',
                 'corporate_email': 'akash.ozarkar@justo.co.in', 'work_email': 'akash.ozarkar@justo.co.in',
                 'mobile': '8668201132', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 54779.0, 'location': 'Pune', 'barcode': 'JUS0214'},
                {'id': 689, 'name': 'Animesh Kumar Dutta', 'pan_number': 'AJOPD3344H',
                 'job_title': 'Deputy General Manager', 'mobile_phone': '000000000', 'work_phone': '000000',
                 'birthday': datetime.date(1981, 4, 5), 'department_id': 9, 'parent_id': 1091, 'gender': 'male',
                 'joining_date': datetime.date(2022, 7, 1), 'departure_date': None, 'city': 'City', 'zip': '000000',
                 'private_email': 'caanimeshmdutta@gmail.com', 'corporate_email': 'animesh.dutta@justo.co.in',
                 'work_email': 'animesh.dutta@justo.co.in', 'mobile': '9967024793', 'marital': 'single',
                 'emergency_contact': '00000000', 'active_status': True, 'ctc': 201333.0, 'location': 'Mumbai - HO',
                 'barcode': 'JUS0822'},
                {'id': 213, 'name': 'Ajinkya Jadhav', 'pan_number': 'BDPPJ7986R', 'job_title': 'Senior Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1991, 3, 1),
                 'department_id': 2, 'parent_id': 1835, 'gender': 'male', 'joining_date': datetime.date(2020, 11, 25),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'sample3@sample.com',
                 'corporate_email': 'ajinkya.jadhav@justo.co.in', 'work_email': 'ajinkya.jadhav@justo.co.in',
                 'mobile': '8007539157', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 64779.0, 'location': 'Pune', 'barcode': 'JUS0163'},
                {'id': 265, 'name': 'Akshay Dupate', 'pan_number': 'APRPD7522G', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1992, 6, 26),
                 'department_id': 2, 'parent_id': 393, 'gender': 'male', 'joining_date': datetime.date(2022, 6, 15),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'akshay.dupae@gmail.com',
                 'corporate_email': 'akshay.dupate@justo.co.in', 'work_email': 'akshay.dupate@justo.co.in',
                 'mobile': '7447794914', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 43890.0, 'location': 'KDMC', 'barcode': 'M0503'},
                {'id': 1106, 'name': 'Amit Ramchandra Jagdale', 'pan_number': 'AKFPJ3285M',
                 'job_title': 'Assistant Manager', 'mobile_phone': '000000000', 'work_phone': '000000',
                 'birthday': datetime.date(1989, 7, 2), 'department_id': 13, 'parent_id': 105, 'gender': 'male',
                 'joining_date': datetime.date(2024, 4, 13), 'departure_date': datetime.date(2024, 6, 18),
                 'city': 'THANE', 'zip': '421306', 'private_email': 'jagdaleamit02@gmail.com',
                 'corporate_email': 'amit.jagdale@justo.co.in', 'work_email': 'amit.jagdale@justo.co.in',
                 'mobile': '9167229959', 'marital': 'married', 'emergency_contact': '9821853542', 'active_status': True,
                 'ctc': 50800.0, 'location': 'Navi Mumbai', 'barcode': 'JUS1496'},
                {'id': 206, 'name': 'Lalit Balu', 'pan_number': 'BBOPR8684P', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1991, 6, 10),
                 'department_id': 2, 'parent_id': 305, 'gender': 'male', 'joining_date': datetime.date(2021, 10, 7),
                 'departure_date': datetime.date(2024, 7, 12), 'city': 'City', 'zip': '000000',
                 'private_email': 'ballupawan@gmail.com', 'corporate_email': 'lalit.balu@justo.co.in',
                 'work_email': 'lalit.balu@justo.co.in', 'mobile': '9096550073', 'marital': 'single',
                 'emergency_contact': '00000000', 'active_status': True, 'ctc': 42800.0, 'location': 'Pune',
                 'barcode': 'JUS0435'},
                {'id': 377, 'name': 'Ashwini Kumar', 'pan_number': 'BJVPK2043L',
                 'job_title': 'Assistant General Manager', 'mobile_phone': '000000000', 'work_phone': '000000',
                 'birthday': datetime.date(1989, 3, 16), 'department_id': 2, 'parent_id': 337, 'gender': 'male',
                 'joining_date': datetime.date(2021, 2, 1), 'departure_date': None, 'city': 'City', 'zip': '000000',
                 'private_email': 'kumarashwini2189@gmail.com', 'corporate_email': 'ashwini.kumar@justo.co.in',
                 'work_email': 'ashwini.kumar@justo.co.in', 'mobile': '7972187496', 'marital': 'single',
                 'emergency_contact': '00000000', 'active_status': True, 'ctc': 109666.0, 'location': 'Pune',
                 'barcode': 'JUS0224'},
                {'id': 391, 'name': 'Aniket Pathade', 'pan_number': 'CLFPP2970Q', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1994, 8, 28),
                 'department_id': 2, 'parent_id': 335, 'gender': 'male', 'joining_date': datetime.date(2021, 9, 14),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'sample3@sample.com',
                 'corporate_email': 'aniket.pathade@justo.co.in', 'work_email': 'aniket.pathade@justo.co.in',
                 'mobile': '8830033600', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 49779.0, 'location': 'Pune - ROM', 'barcode': 'JUS0405'},
                {'id': 1151, 'name': 'Akshay Bagul', 'pan_number': 'ANKPB9211F',
                 'job_title': 'Assistant General Manager', 'mobile_phone': '000000000', 'work_phone': '000000',
                 'birthday': datetime.date(1987, 9, 11), 'department_id': 2, 'parent_id': 848, 'gender': 'male',
                 'joining_date': datetime.date(2024, 5, 1), 'departure_date': None, 'city': 'Kalyan - Dombovili',
                 'zip': '421204', 'private_email': 'rockford_04@yahoo.com',
                 'corporate_email': 'akshay.bagul@justo.co.in', 'work_email': 'akshay.bagul@justo.co.in',
                 'mobile': '7977338299', 'marital': 'married', 'emergency_contact': '9821930905', 'active_status': True,
                 'ctc': 119300.0, 'location': 'Thane', 'barcode': 'JUS594'},
                {'id': 771, 'name': 'Deepak Rangrao Nikam', 'pan_number': 'AIFPG1258H', 'job_title': 'Senior Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1983, 6, 5),
                 'department_id': 10, 'parent_id': 841, 'gender': 'male', 'joining_date': datetime.date(2021, 2, 1),
                 'departure_date': None, 'city': 'Dhayari', 'zip': '411041',
                 'private_email': 'deeptheanimator@gmail.com', 'corporate_email': 'deepak.nikam@justo.co.in',
                 'work_email': 'deepak.nikam@justo.co.in', 'mobile': '9076231056', 'marital': 'single',
                 'emergency_contact': '8356849582', 'active_status': True, 'ctc': 69757.0,
                 'location': 'Regional Office _ Pune', 'barcode': 'JUS0225'},
                {'id': 464, 'name': 'Anant Sawant', 'pan_number': 'KSCPS4210N', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(2000, 5, 24),
                 'department_id': 2, 'parent_id': 100, 'gender': 'male', 'joining_date': datetime.date(2023, 1, 5),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'AnantSawant36211@gmail.com',
                 'corporate_email': 'anant.sawant@justo.co.in', 'work_email': 'anant.sawant@justo.co.in',
                 'mobile': '7045654585', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 41800.0, 'location': 'Navi Mumbai', 'barcode': 'P0370'},
                {'id': 1717, 'name': 'Akash  Surendra  Bachhav', 'pan_number': '000000',
                 'job_title': 'Assistant Manager', 'mobile_phone': '000000000', 'work_phone': '000000',
                 'birthday': datetime.date(1999, 8, 31), 'department_id': 2, 'parent_id': 993, 'gender': 'male',
                 'joining_date': datetime.date(2024, 5, 27), 'departure_date': None, 'city': 'City', 'zip': '000000',
                 'private_email': 'akashbachhav7@gmail.com', 'corporate_email': 'akash.bachhav@justo.co.in',
                 'work_email': 'akash.bachhav@justo.co.in', 'mobile': '00000000', 'marital': 'single',
                 'emergency_contact': '00000000', 'active_status': True, 'ctc': 63800.0, 'location': 'Pune',
                 'barcode': 'JUS607'},
                {'id': 1729, 'name': 'Ajinkya Ashok Bhawar', 'pan_number': 'CNBPB2855G',
                 'job_title': 'Assistant Manager', 'mobile_phone': '000000000', 'work_phone': '000000',
                 'birthday': datetime.date(1997, 10, 25), 'department_id': 7, 'parent_id': 648, 'gender': 'male',
                 'joining_date': datetime.date(2024, 5, 14), 'departure_date': None, 'city': 'Dombivali',
                 'zip': '421202', 'private_email': 'bhawarajinkya7@gmail.com',
                 'corporate_email': 'ajinkya.bhawar@justo.co.in', 'work_email': 'ajinkya.bhawar@justo.co.in',
                 'mobile': '8451817936', 'marital': 'single', 'emergency_contact': '8451817936', 'active_status': True,
                 'ctc': 50000.0, 'location': 'Regional Office _ Pune', 'barcode': 'JUS600'},
                {'id': 491, 'name': 'Aditya Thakare', 'pan_number': 'AVVPT3659C', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1996, 3, 15),
                 'department_id': 2, 'parent_id': 887, 'gender': 'male', 'joining_date': datetime.date(2023, 5, 2),
                 'departure_date': None, 'city': 'City', 'zip': '000000',
                 'private_email': 'AdityaThakare1sjr@gmail.com', 'corporate_email': 'aditya.thakare@justo.co.in',
                 'work_email': 'aditya.thakare@justo.co.in', 'mobile': '00000000', 'marital': 'single',
                 'emergency_contact': '00000000', 'active_status': True, 'ctc': 54317.0, 'location': 'Pune',
                 'barcode': 'JUS1135'},
                {'id': 71, 'name': 'Aaira Ansari', 'pan_number': 'CWZPA4542C', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1998, 1, 20),
                 'department_id': 10, 'parent_id': 841, 'gender': 'female', 'joining_date': datetime.date(2020, 12, 23),
                 'departure_date': datetime.date(2024, 10, 12), 'city': 'City', 'zip': '000000',
                 'private_email': 'sample3@sample.com', 'corporate_email': 'aaira.ansari@justo.co.in',
                 'work_email': 'aaira.ansari@justo.co.in', 'mobile': '8805556108', 'marital': 'single',
                 'emergency_contact': '00000000', 'active_status': False, 'ctc': 73112.0, 'location': 'Pune',
                 'barcode': 'JUS0188'},
                {'id': 1512, 'name': 'Manish  Prem  Auji', 'pan_number': '000000', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(2000, 8, 29),
                 'department_id': 2, 'parent_id': 898, 'gender': 'male', 'joining_date': datetime.date(2024, 6, 10),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'manishauji7@gmail.com',
                 'corporate_email': 'manish.auji@justo.co.in', 'work_email': 'manish.auji@justo.co.in',
                 'mobile': '00000000', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 53800.0, 'location': 'Pune', 'barcode': 'JUS620'},
                {'id': 1422, 'name': 'Samina  Mahebub Mulla', 'pan_number': 'GEWPM7484C', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(2001, 10, 10),
                 'department_id': 2, 'parent_id': 385, 'gender': 'female', 'joining_date': datetime.date(2024, 6, 3),
                 'departure_date': None, 'city': 'pune', 'zip': '411021', 'private_email': 'Saminamulla7866@gmail.com',
                 'corporate_email': 'samina.mulla@justo.co.in', 'work_email': 'samina.mulla@justo.co.in',
                 'mobile': '9422754988', 'marital': 'widower', 'emergency_contact': '9527952608', 'active_status': True,
                 'ctc': 51750.0, 'location': 'Pune', 'barcode': 'JUS615'},
                {'id': 502, 'name': 'Dhondiba Aptekar', 'pan_number': 'ATCPA8843L', 'job_title': 'Senior Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1991, 11, 5),
                 'department_id': 2, 'parent_id': 1732, 'gender': 'male', 'joining_date': datetime.date(2021, 12, 10),
                 'departure_date': None, 'city': 'City', 'zip': '000000',
                 'private_email': 'aptekardhondiba40@gmail.com', 'corporate_email': 'dhondiba.aptekar@justo.co.in',
                 'work_email': 'dhondiba.aptekar@justo.co.in', 'mobile': '9623051313', 'marital': 'single',
                 'emergency_contact': '00000000', 'active_status': True, 'ctc': 64779.0, 'location': 'Pune',
                 'barcode': 'JUS0531'},
                {'id': 1739, 'name': 'Akshay Balu More', 'pan_number': 'CQPPM8117B', 'job_title': 'Assistant Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1995, 10, 17),
                 'department_id': 14, 'parent_id': None, 'gender': 'male', 'joining_date': datetime.date(2024, 6, 1),
                 'departure_date': datetime.date(2024, 6, 8), 'city': 'Panvel', 'zip': '410218',
                 'private_email': 'akshay.more836@gmail.com', 'corporate_email': 'akshay.more@justo.co.in',
                 'work_email': 'akshay.more@justo.co.in', 'mobile': '9619532283', 'marital': 'single',
                 'emergency_contact': '9820723885', 'active_status': True, 'ctc': 31800.0, 'location': 'Navi Mumbai',
                 'barcode': 'JUS610'},
                {'id': 514, 'name': 'Akash Kotwal', 'pan_number': 'DQNPK1866E', 'job_title': 'Assistant Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1996, 3, 24),
                 'department_id': 2, 'parent_id': 305, 'gender': 'male', 'joining_date': datetime.date(2021, 5, 21),
                 'departure_date': None, 'city': 'Pune', 'zip': '411041', 'private_email': 'akashkotwale12@gmail.com',
                 'corporate_email': 'akash.kotwal@justo.co.in', 'work_email': 'akash.kotwal@justo.co.in',
                 'mobile': '8830602720', 'marital': 'married', 'emergency_contact': '8208256773', 'active_status': True,
                 'ctc': 44779.0, 'location': 'Pune', 'barcode': 'JUS0255'},
                {'id': 512, 'name': 'Laxman Nitnaware', 'pan_number': 'AJHPN0926C', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1991, 6, 10),
                 'department_id': 2, 'parent_id': 304, 'gender': 'male', 'joining_date': datetime.date(2022, 12, 21),
                 'departure_date': None, 'city': 'Pune', 'zip': None, 'private_email': 'laxman.nitnaware@justo.co.in',
                 'corporate_email': 'Laxman.Nitnaware@justo.co.in', 'work_email': 'Laxman.Nitnaware@justo.co.in',
                 'mobile': '8830283180', 'marital': 'married', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 51800.0, 'location': None, 'barcode': 'JUS1004'},
                {'id': 1763, 'name': 'Ajinkya Pramod  Gulumkar', 'pan_number': 'CCFPG8758N', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1998, 11, 9),
                 'department_id': 2, 'parent_id': 1824, 'gender': 'male', 'joining_date': datetime.date(2024, 6, 13),
                 'departure_date': None, 'city': 'Baramati', 'zip': '413102',
                 'private_email': 'ajinkya.gulumkar@yahoo.com', 'corporate_email': 'ajinkya.gulumkar@justo.co.in',
                 'work_email': 'ajinkya.gulumkar@justo.co.in', 'mobile': '8600152779', 'marital': 'single',
                 'emergency_contact': '9130503036', 'active_status': True, 'ctc': 51800.0, 'location': 'Pune',
                 'barcode': 'JUS630'},
                {'id': 1823, 'name': 'Ashish  Tulsidas  Katgaye', 'pan_number': '000000', 'job_title': 'Senior Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1992, 1, 15),
                 'department_id': 2, 'parent_id': 887, 'gender': 'male', 'joining_date': datetime.date(2024, 7, 1),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'katgayeashish@gmail.com',
                 'corporate_email': 'ashish.katgaye@justo.co.in', 'work_email': 'ashish.katgaye@justo.co.in',
                 'mobile': '00000000', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 76200.0, 'location': 'Pune', 'barcode': 'JUS657'},
                {'id': 1830, 'name': 'Amyn  Anwar Khoja', 'pan_number': 'APJPK5425K',
                 'job_title': 'Assistant General Manager', 'mobile_phone': '000000000', 'work_phone': '000000',
                 'birthday': datetime.date(1979, 7, 26), 'department_id': 2, 'parent_id': 447, 'gender': 'male',
                 'joining_date': datetime.date(2024, 7, 4), 'departure_date': datetime.date(2024, 10, 11),
                 'city': 'Pune', 'zip': '411006', 'private_email': 'aymynkhoja7@gmail.com',
                 'corporate_email': 'amyn.khoja@justo.co.in', 'work_email': 'amyn.khoja@justo.co.in',
                 'mobile': '9022900788', 'marital': 'widower', 'emergency_contact': '8208413214',
                 'active_status': False, 'ctc': 125000.0, 'location': 'Pune', 'barcode': 'JUS664'},
                {'id': 564, 'name': 'Akshay Timbole', 'pan_number': 'BNDPT8604A', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1999, 1, 1),
                 'department_id': 2, 'parent_id': 56, 'gender': 'male', 'joining_date': datetime.date(2023, 1, 5),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'sample3@sample.com',
                 'corporate_email': 'akshay.timbole@justo.co.in', 'work_email': 'akshay.timbole@justo.co.in',
                 'mobile': '7875504282', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 46800.0, 'location': 'Pune', 'barcode': 'JUS1014'},
                {'id': 1831, 'name': 'Abhijeet  Gaikwad', 'pan_number': 'AYUPG8649P', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1992, 3, 23),
                 'department_id': 5, 'parent_id': 251, 'gender': 'male', 'joining_date': datetime.date(2024, 7, 5),
                 'departure_date': None, 'city': 'Pune', 'zip': '411028', 'private_email': 'gabhijeet400@gmail.com',
                 'corporate_email': 'abhijeet.gaikwad@justo.co.in', 'work_email': 'abhijeet.gaikwad@justo.co.in',
                 'mobile': '7020423750', 'marital': 'married', 'emergency_contact': '8767976126', 'active_status': True,
                 'ctc': 63800.0, 'location': 'Pune', 'barcode': 'JUS666'},
                {'id': 1833, 'name': 'Indranil  Sarkar', 'pan_number': 'FCOPS2078K',
                 'job_title': 'Assistant General Manager', 'mobile_phone': '000000000', 'work_phone': '000000',
                 'birthday': datetime.date(1994, 11, 4), 'department_id': 2, 'parent_id': 1702, 'gender': 'male',
                 'joining_date': datetime.date(2024, 7, 8), 'departure_date': None, 'city': 'Pune', 'zip': '412308',
                 'private_email': 'sindranil0@gmail.com', 'corporate_email': 'indranil.sarkar@justo.co.in',
                 'work_email': 'indranil.sarkar@justo.co.in', 'mobile': '8697023045', 'marital': 'married',
                 'emergency_contact': '9804573107', 'active_status': True, 'ctc': 104167.0, 'location': 'Pune',
                 'barcode': 'JUS668'},
                {'id': 1837, 'name': 'Akshaysingh  Rajawat', 'pan_number': 'CDOPR5227D',
                 'job_title': 'Assistant Manager', 'mobile_phone': '000000000', 'work_phone': '000000',
                 'birthday': datetime.date(1997, 3, 19), 'department_id': 2, 'parent_id': 67, 'gender': 'male',
                 'joining_date': datetime.date(2024, 7, 8), 'departure_date': None, 'city': 'Navi Mumbai',
                 'zip': '400703', 'private_email': 'rajawatakshay86@gmail.com',
                 'corporate_email': 'akshaysingh.rajawat@justo.co.in', 'work_email': 'akshaysingh.rajawat@justo.co.in',
                 'mobile': '8767258679', 'marital': 'single', 'emergency_contact': '8652008468', 'active_status': True,
                 'ctc': 46000.0, 'location': 'Pune - ROM', 'barcode': 'JUS672'},
                {'id': 598, 'name': 'Aarti Bhandare', 'pan_number': 'BIGPB2603F', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1992, 9, 10),
                 'department_id': 2, 'parent_id': 890, 'gender': 'female', 'joining_date': datetime.date(2022, 6, 11),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'bhandareaarti09@gmail.com',
                 'corporate_email': 'aarti.bhandare@justo.co.in', 'work_email': 'aarti.bhandare@justo.co.in',
                 'mobile': '8692004973', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 59779.0, 'location': 'Mumbai Western', 'barcode': 'JUS0792'},
                {'id': 1935, 'name': 'Himanshu Dilip Mandal', 'pan_number': 'BEDPM7677B', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1994, 12, 22),
                 'department_id': 13, 'parent_id': 244, 'gender': 'male', 'joining_date': datetime.date(2024, 9, 9),
                 'departure_date': None, 'city': 'Mira road (E)', 'zip': '401107',
                 'private_email': 'hmandal0071@gmail.com', 'corporate_email': 'himanshu.mandal@justo.co.in',
                 'work_email': 'himanshu.mandal@justo.co.in', 'mobile': '8689968052', 'marital': 'single',
                 'emergency_contact': '7208309214', 'active_status': True, 'ctc': 54166.0, 'location': 'Navi Mumbai',
                 'barcode': 'JUS704'},
                {'id': 1932, 'name': 'Deepti  Subhash  Pillay', 'pan_number': '000000', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1980, 10, 3),
                 'department_id': 5, 'parent_id': 251, 'gender': 'female', 'joining_date': datetime.date(2024, 9, 10),
                 'departure_date': None, 'city': 'City', 'zip': '000000',
                 'private_email': 'pillay.deepti1980@gmail.com', 'corporate_email': 'pillay.deepti1980@gmail.com',
                 'work_email': 'pillay.deepti1980@gmail.com', 'mobile': '00000000', 'marital': 'single',
                 'emergency_contact': '00000000', 'active_status': True, 'ctc': 55000.0, 'location': 'Pune',
                 'barcode': 'JUS706'},
                {'id': 1827, 'name': 'Pooja  Shahaji  Devkar', 'pan_number': '000000', 'job_title': 'Assistant Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1998, 12, 7),
                 'department_id': 14, 'parent_id': 626, 'gender': 'female', 'joining_date': datetime.date(2024, 7, 1),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'poojade804@gmail.com',
                 'corporate_email': 'pooja.devkar@justo.co.in', 'work_email': 'pooja.devkar@justo.co.in',
                 'mobile': '00000000', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 28483.0, 'location': 'Pune', 'barcode': 'JUS661'},
                {'id': 1936, 'name': 'Manaswi Harish  Bhanushali', 'pan_number': 'FSNPB7538A',
                 'job_title': 'Senior Executive', 'mobile_phone': '000000000', 'work_phone': '000000',
                 'birthday': datetime.date(2003, 5, 11), 'department_id': 10, 'parent_id': 103, 'gender': 'female',
                 'joining_date': datetime.date(2024, 9, 9), 'departure_date': None, 'city': 'Mumbai', 'zip': '400080',
                 'private_email': 'bhadramanaswi@gmail.com', 'corporate_email': 'manaswi.bhanushali@justo.co.in',
                 'work_email': 'manaswi.bhanushali@justo.co.in', 'mobile': '8097416979', 'marital': 'single',
                 'emergency_contact': '8097147267', 'active_status': True, 'ctc': 35000.0, 'location': 'Mumbai Western',
                 'barcode': 'JUS707'},
                {'id': 103, 'name': 'Sanjeev Thadani', 'pan_number': 'ADCPT1892J',
                 'job_title': 'Deputy General Manager', 'mobile_phone': '000000000', 'work_phone': '000000',
                 'birthday': datetime.date(1979, 10, 31), 'department_id': 10, 'parent_id': 720, 'gender': 'male',
                 'joining_date': datetime.date(2022, 4, 21), 'departure_date': None, 'city': 'City', 'zip': '000000',
                 'private_email': 'sanjeevthadani@gmail.com', 'corporate_email': 'sanjeev.thadani@justo.co.in',
                 'work_email': 'sanjeev.thadani@justo.co.in', 'mobile': '8097444404', 'marital': 'single',
                 'emergency_contact': '00000000', 'active_status': True, 'ctc': 183000.0, 'location': 'Mumbai Western',
                 'barcode': 'JUS0689'},
                {'id': 1786, 'name': 'Aniket Ashokrao  Kalaskar', 'pan_number': 'JSOPK0097L', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1997, 11, 24),
                 'department_id': 2, 'parent_id': 319, 'gender': 'male', 'joining_date': datetime.date(2024, 6, 19),
                 'departure_date': None, 'city': 'Chatrapati sambhaji nagar ', 'zip': '431008',
                 'private_email': 'akalaskar9@gmail.com', 'corporate_email': 'Aniket.kalaskar@justo.co.in',
                 'work_email': 'Aniket.kalaskar@justo.co.in', 'mobile': '9175861752', 'marital': 'single',
                 'emergency_contact': '919975777517', 'active_status': True, 'ctc': 43800.0, 'location': 'Pune',
                 'barcode': 'JUS644'},
                {'id': 721, 'name': 'Subhransu Sahoo', 'pan_number': 'BCIPS7809E', 'job_title': 'General Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1984, 3, 25),
                 'department_id': 2, 'parent_id': 720, 'gender': 'male', 'joining_date': datetime.date(2022, 8, 18),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'subhransu.2011@gmail.com',
                 'corporate_email': 'subhransu.sahoo@justo.co.in', 'work_email': 'subhransu.sahoo@justo.co.in',
                 'mobile': '8007410100', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': False,
                 'ctc': 325000.0, 'location': 'BBSR Regional Office', 'barcode': 'JUS0866'},
                {'id': 1879, 'name': 'Dishant Mangesh Kelaskar', 'pan_number': 'JEZPK0324D',
                 'job_title': 'Senior Executive', 'mobile_phone': '000000000', 'work_phone': '000000',
                 'birthday': datetime.date(2001, 7, 22), 'department_id': 5, 'parent_id': 243, 'gender': 'male',
                 'joining_date': datetime.date(2024, 8, 1), 'departure_date': None, 'city': 'Virar', 'zip': '401305',
                 'private_email': 'kelaskardishant1@gmail.com', 'corporate_email': 'dishant.kelaskar@justo.co.in',
                 'work_email': 'dishant.kelaskar@justo.co.in', 'mobile': '7066419211', 'marital': 'single',
                 'emergency_contact': '9967505867', 'active_status': True, 'ctc': 30808.0, 'location': 'Mumbai Western',
                 'barcode': 'JUS682'},
                {'id': 1340, 'name': 'Majed Musa Shaikh', 'pan_number': 'AVDPS3106P', 'job_title': 'Manager',
                 'mobile_phone': '9284273636', 'work_phone': '000000', 'birthday': datetime.date(1980, 9, 6),
                 'department_id': 2, 'parent_id': 848, 'gender': 'male', 'joining_date': datetime.date(2024, 3, 3),
                 'departure_date': None, 'city': 'Ulhasnagar', 'zip': '421004',
                 'private_email': 'majedshaikh2009@gmail.com', 'corporate_email': 'majed.shaikh@justo.co.in',
                 'work_email': 'majed.shaikh@justo.co.in', 'mobile': '9284273636', 'marital': 'single',
                 'emergency_contact': '9834262011', 'active_status': True, 'ctc': 63800.0, 'location': 'Thane',
                 'barcode': 'JUS1428'},
                {'id': 335, 'name': 'Madhav Murhekar', 'pan_number': 'ABWPM4672M',
                 'job_title': 'Assistant General Manager', 'mobile_phone': '000000000', 'work_phone': '000000',
                 'birthday': datetime.date(1971, 5, 29), 'department_id': 2, 'parent_id': 1308, 'gender': 'male',
                 'joining_date': datetime.date(2022, 6, 15), 'departure_date': None, 'city': 'City', 'zip': '000000',
                 'private_email': 'madhav.murhekar@gmail.com', 'corporate_email': 'madhav.murhekar@justo.co.in',
                 'work_email': 'madhav.murhekar@justo.co.in', 'mobile': '7972229759', 'marital': 'single',
                 'emergency_contact': '00000000', 'active_status': True, 'ctc': 109484.0, 'location': 'Pune - ROM',
                 'barcode': 'JUS0804'},
                {'id': 1769, 'name': 'Lina Arun Deore', 'pan_number': 'DMLPD1362N', 'job_title': 'Assistant Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1998, 9, 2),
                 'department_id': 2, 'parent_id': 1950, 'gender': 'female', 'joining_date': datetime.date(2024, 6, 15),
                 'departure_date': None, 'city': 'Dhule ', 'zip': '424308', 'private_email': 'linadeore1998@gmail.com',
                 'corporate_email': 'lina.deore@justo.co.in', 'work_email': 'lina.deore@justo.co.in',
                 'mobile': '7219171681', 'marital': 'single', 'emergency_contact': '8378870574', 'active_status': True,
                 'ctc': 30000.0, 'location': 'Pune', 'barcode': 'JUS635'},
                {'id': 656, 'name': 'Laxmi Bhimte', 'pan_number': 'BTAPB5481J', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1983, 4, 25),
                 'department_id': 15, 'parent_id': 841, 'gender': 'female', 'joining_date': datetime.date(2022, 9, 14),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'laxmi.bhimte@gmail.com',
                 'corporate_email': 'laxmi.bhimte@justo.co.in', 'work_email': 'laxmi.bhimte@justo.co.in',
                 'mobile': '9860540520', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 101775.0, 'location': 'Regional Office _ Pune', 'barcode': 'JUS0899'},
                {'id': 1568, 'name': 'Mallikarjun Suryawanshi', 'pan_number': '000000',
                 'job_title': 'Assistant Manager', 'mobile_phone': '000000000', 'work_phone': '000000',
                 'birthday': datetime.date(1997, 3, 14), 'department_id': 2, 'parent_id': 993, 'gender': 'male',
                 'joining_date': datetime.date(2023, 7, 17), 'departure_date': None, 'city': 'City', 'zip': '000000',
                 'private_email': 'Suryawanshim854@gmail.com', 'corporate_email': 'mallikarjun.suryawanshi@justo.co.in',
                 'work_email': 'mallikarjun.suryawanshi@justo.co.in', 'mobile': '00000000', 'marital': 'single',
                 'emergency_contact': '00000000', 'active_status': True, 'ctc': 47500.0, 'location': 'Pune',
                 'barcode': 'JUS1225'},
                {'id': 1883, 'name': 'Chandni Sukhpal  Parche', 'pan_number': 'ENFPP5251J', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1997, 10, 14),
                 'department_id': 2, 'parent_id': 1163, 'gender': 'female', 'joining_date': datetime.date(2024, 8, 5),
                 'departure_date': None, 'city': 'Navi Mumbai ', 'zip': '410218',
                 'private_email': 'chandniparche97@gmail.com', 'corporate_email': 'chandni.parche@justo.co.in',
                 'work_email': 'chandni.parche@justo.co.in', 'mobile': '8657141307', 'marital': 'single',
                 'emergency_contact': '7208143599', 'active_status': True, 'ctc': 68000.0, 'location': 'Navi Mumbai',
                 'barcode': 'JUS691'},
                {'id': 1882, 'name': 'Arpit Singh', 'pan_number': 'OUIPS4274L', 'job_title': 'Assistant Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1997, 11, 26),
                 'department_id': 2, 'parent_id': 1163, 'gender': 'male', 'joining_date': datetime.date(2024, 8, 3),
                 'departure_date': None, 'city': 'Sagar', 'zip': '470004', 'private_email': 'arpitsingh26nov@gmail.com',
                 'corporate_email': 'arpit.singh@justo.co.in', 'work_email': 'arpit.singh@justo.co.in',
                 'mobile': '7509776944', 'marital': 'single', 'emergency_contact': '9826735400', 'active_status': True,
                 'ctc': 54000.0, 'location': 'Navi Mumbai', 'barcode': 'JUS690'},
                {'id': 1885, 'name': 'Amandeep  Singh  Bhatia ', 'pan_number': 'DHDPB9249D', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1998, 8, 22),
                 'department_id': 2, 'parent_id': 993, 'gender': 'male', 'joining_date': datetime.date(2024, 8, 1),
                 'departure_date': None, 'city': 'Dongargarh ', 'zip': '491445',
                 'private_email': 'amandeep.bhatia2297@gmail.com', 'corporate_email': 'amandeep.bhatia@justo.co.in',
                 'work_email': 'amandeep.bhatia@justo.co.in', 'mobile': '9691297297', 'marital': 'single',
                 'emergency_contact': '8770100297', 'active_status': True, 'ctc': 68750.0, 'location': 'Pune',
                 'barcode': 'JUS684'},
                {'id': 830, 'name': 'Ashutosh Lalit Gurkha', 'pan_number': 'BIIPK6593H', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1984, 12, 28),
                 'department_id': 2, 'parent_id': 100, 'gender': 'male', 'joining_date': datetime.date(2022, 8, 8),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'ashutoshk7@gmail.com',
                 'corporate_email': 'ashutosh.gurkha@justo.co.in', 'work_email': 'ashutosh.gurkha@justo.co.in',
                 'mobile': '9820969873', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 70222.0, 'location': 'Navi Mumbai', 'barcode': 'M0530'},
                {'id': 1005, 'name': 'Anil Sharma', 'pan_number': 'EEJPS7035Q', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1992, 7, 25),
                 'department_id': 2, 'parent_id': 848, 'gender': 'male', 'joining_date': datetime.date(2024, 1, 27),
                 'departure_date': datetime.date(2024, 5, 9), 'city': 'navi Mumbai', 'zip': '410210',
                 'private_email': 'sharmaalex417@gmail.com', 'corporate_email': 'anil.sharma@justo.co.in',
                 'work_email': 'anil.sharma@justo.co.in', 'mobile': '7021432344', 'marital': 'single',
                 'emergency_contact': '9518901238', 'active_status': True, 'ctc': 75000.0, 'location': 'Thane',
                 'barcode': 'M0772'},
                {'id': 1007, 'name': 'Anurag Hirapure', 'pan_number': 'AKRPH3402Q', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1995, 2, 22),
                 'department_id': 2, 'parent_id': 337, 'gender': 'male', 'joining_date': datetime.date(2024, 1, 16),
                 'departure_date': datetime.date(2024, 4, 8), 'city': 'Pune', 'zip': '411021',
                 'private_email': 'aburaghirapure.22@gmail.com', 'corporate_email': 'anurag.hirapure@justo.co.in',
                 'work_email': 'anurag.hirapure@justo.co.in', 'mobile': '7972501262', 'marital': 'single',
                 'emergency_contact': '73787458649', 'active_status': True, 'ctc': 53800.0, 'location': 'Pune',
                 'barcode': 'P0535'},
                {'id': 1132, 'name': 'Anand Kumar Narbdeshwar  Pandey', 'pan_number': '000000', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1994, 1, 23),
                 'department_id': 2, 'parent_id': 1043, 'gender': 'male', 'joining_date': datetime.date(2024, 4, 11),
                 'departure_date': datetime.date(2024, 5, 9), 'city': 'City', 'zip': '000000',
                 'private_email': 'anandp2317@gmail.com', 'corporate_email': 'anandkumar.pandey@justo.co.in',
                 'work_email': 'anandkumar.pandey@justo.co.in', 'mobile': '00000000', 'marital': 'single',
                 'emergency_contact': '00000000', 'active_status': True, 'ctc': 50000.0, 'location': 'Mumbai Western',
                 'barcode': 'M0842'},
                {'id': 1460, 'name': 'Ayush Pachori', 'pan_number': 'EHDPP0107D', 'job_title': 'Assistant Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1999, 4, 24),
                 'department_id': 2, 'parent_id': 563, 'gender': 'male', 'joining_date': datetime.date(2023, 6, 5),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'ayushpachori1@gmail.com',
                 'corporate_email': 'ayush.pachori@justo.co.in', 'work_email': 'ayush.pachori@justo.co.in',
                 'mobile': '00000000', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 44792.0, 'location': 'Navi Mumbai', 'barcode': 'JUS1173'},
                {'id': 1380, 'name': 'Arpan Sharma', 'pan_number': 'IEPPS3288B', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1996, 12, 17),
                 'department_id': 2, 'parent_id': 1163, 'gender': 'male', 'joining_date': datetime.date(2024, 6, 12),
                 'departure_date': None, 'city': 'kharghar', 'zip': '410210', 'private_email': 'arpansh2011@gmail.com',
                 'corporate_email': 'arpan.sharma@justo.co.in', 'work_email': 'arpan.sharma@justo.co.in',
                 'mobile': '8810204918', 'marital': 'married', 'emergency_contact': '9719322348', 'active_status': True,
                 'ctc': 70000.0, 'location': 'Navi Mumbai', 'barcode': 'JUS624'},
                {'id': 1474, 'name': 'Arjun Chalana', 'pan_number': 'AJNPC8470C', 'job_title': 'Deputy General Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1987, 4, 13),
                 'department_id': 2, 'parent_id': 243, 'gender': 'male', 'joining_date': datetime.date(2023, 7, 13),
                 'departure_date': datetime.date(2024, 9, 29), 'city': 'City', 'zip': '000000',
                 'private_email': 'arjunchalana@gmail.com', 'corporate_email': 'arjun.chalana@justo.co.in',
                 'work_email': 'arjun.chalana@justo.co.in', 'mobile': '00000000', 'marital': 'single',
                 'emergency_contact': '00000000', 'active_status': True, 'ctc': 250000.0, 'location': 'Mumbai Western',
                 'barcode': 'JUS1220'},
                {'id': 1341, 'name': 'Dipesh  Makwana', 'pan_number': 'HARPM8755C', 'job_title': 'Senior Executive',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1999, 10, 24),
                 'department_id': 5, 'parent_id': 244, 'gender': 'male', 'joining_date': datetime.date(2024, 4, 8),
                 'departure_date': None, 'city': 'MUMBAI', 'zip': '400081', 'private_email': 'm.dipesh.dm@gmail.com',
                 'corporate_email': 'dipesh.makwana@justo.co.in', 'work_email': 'dipesh.makwana@justo.co.in',
                 'mobile': '9619223563', 'marital': 'single', 'emergency_contact': '9967329132', 'active_status': True,
                 'ctc': 37500.0, 'location': 'Navi Mumbai', 'barcode': 'JUS1484'},
                {'id': 1787, 'name': 'Shubham Keservani', 'pan_number': 'EMMPK9013D', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1995, 8, 10),
                 'department_id': 2, 'parent_id': 56, 'gender': 'male', 'joining_date': datetime.date(2024, 6, 18),
                 'departure_date': None, 'city': 'Cantt Varanasi ', 'zip': '221002',
                 'private_email': 'shubhamkeservani@gmail.com', 'corporate_email': 'Shubham.keservani@justo.co.in',
                 'work_email': 'Shubham.keservani@justo.co.in', 'mobile': '8808124059', 'marital': 'single',
                 'emergency_contact': '9369747070', 'active_status': True, 'ctc': 50000.0, 'location': 'Pune',
                 'barcode': 'JUS643'},
                {'id': 1788, 'name': 'Onkar Surve', 'pan_number': 'DIYPS6332E', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1991, 3, 21),
                 'department_id': 2, 'parent_id': 887, 'gender': 'male', 'joining_date': datetime.date(2024, 6, 18),
                 'departure_date': None, 'city': 'Pune', 'zip': '411041', 'private_email': 'surveonkar21@gmail.com',
                 'corporate_email': 'onkar.surve@jusro.co.in', 'work_email': 'onkar.surve@jusro.co.in',
                 'mobile': '7276442103', 'marital': 'single', 'emergency_contact': '9850493871', 'active_status': True,
                 'ctc': 50000.0, 'location': 'Pune', 'barcode': 'JUS642'},
                {'id': 224, 'name': 'Amol Raskar', 'pan_number': 'AJJPR8231L', 'job_title': 'Assistant General Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1984, 5, 13),
                 'department_id': 10, 'parent_id': 841, 'gender': 'male', 'joining_date': datetime.date(2020, 11, 23),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'sample3@sample.com',
                 'corporate_email': 'amol.raskar@justo.co.in', 'work_email': 'amol.raskar@justo.co.in',
                 'mobile': '9423092701', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 122292.0, 'location': 'Pune', 'barcode': 'JUS0161'},
                {'id': 1810, 'name': 'Abhash Jha', 'pan_number': 'AHMPJ2172K', 'job_title': 'Deputy General Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1983, 6, 1),
                 'department_id': 2, 'parent_id': 1902, 'gender': 'male', 'joining_date': datetime.date(2024, 7, 1),
                 'departure_date': None, 'city': 'Panvel', 'zip': '410206', 'private_email': 'abhashr.jha@gmail.com',
                 'corporate_email': 'abhash.jha@justo.co.in', 'work_email': 'abhash.jha@justo.co.in',
                 'mobile': '9324857048', 'marital': 'married', 'emergency_contact': '9833885389', 'active_status': True,
                 'ctc': 166666.0, 'location': 'Navi Mumbai ', 'barcode': 'JUS656'},
                {'id': 215, 'name': 'Amol Zulzule', 'pan_number': 'AAGPZ9183M', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1982, 10, 16),
                 'department_id': 2, 'parent_id': 1835, 'gender': 'male', 'joining_date': datetime.date(2020, 10, 2),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'amol1016@gmail.com',
                 'corporate_email': 'amol.zulzule@justo.co.in', 'work_email': 'amol.zulzule@justo.co.in',
                 'mobile': '9021124245', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 59757.0, 'location': 'Pune', 'barcode': 'JUS0130'},
                {'id': 962, 'name': 'Altamash Akram Hawaldar', 'pan_number': 'AKQPH7537K', 'job_title': 'Manager',
                 'mobile_phone': '7977719588', 'work_phone': '000000', 'birthday': datetime.date(1995, 7, 22),
                 'department_id': 2, 'parent_id': 436, 'gender': 'male', 'joining_date': datetime.date(2023, 12, 1),
                 'departure_date': datetime.date(2024, 2, 29), 'city': 'City', 'zip': '000000',
                 'private_email': 'hawaldaraltamash1@gmail.com', 'corporate_email': 'altamash.hawaldar@justo.co.in',
                 'work_email': 'altamash.hawaldar@justo.co.in', 'mobile': '7977719588', 'marital': 'single',
                 'emergency_contact': '00000000', 'active_status': True, 'ctc': 58333.0, 'location': 'Navi Mumbai',
                 'barcode': 'M0740'},
                {'id': 1906, 'name': 'Akshay Madhukar Tale', 'pan_number': 'AQEPT6144N', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1994, 6, 5),
                 'department_id': 2, 'parent_id': None, 'gender': 'male', 'joining_date': datetime.date(2024, 8, 22),
                 'departure_date': None, 'city': 'Navi mumbai', 'zip': '400705',
                 'private_email': 'akshay.tale@justo.co.in', 'corporate_email': 'akshay.tale@justo.co.in',
                 'work_email': 'akshay.tale@justo.co.in', 'mobile': '09653383377', 'marital': 'married',
                 'emergency_contact': '8928712026', 'active_status': True, 'ctc': 81666.0, 'location': 'Navi Mumbai',
                 'barcode': 'JUS699'},
                {'id': 8, 'name': 'Abhinav Shekhar', 'pan_number': 'DFZPS3561B',
                 'job_title': 'Assistant General Manager', 'mobile_phone': '000000000', 'work_phone': '000000',
                 'birthday': datetime.date(1988, 10, 28), 'department_id': 2, 'parent_id': 576, 'gender': 'male',
                 'joining_date': datetime.date(2021, 10, 29), 'departure_date': datetime.date(2024, 5, 11),
                 'city': 'City', 'zip': '000000', 'private_email': 'shekhar.abhinav@yahoo.com',
                 'corporate_email': 'abhinav.shekhar@justo.co.in', 'work_email': 'abhinav.shekhar@justo.co.in',
                 'mobile': '7387912343', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 105000.0, 'location': 'Pune', 'barcode': 'JUS0468'},
                {'id': 316, 'name': 'Anil Sasane', 'pan_number': 'GNLPS2980H', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1988, 7, 1),
                 'department_id': 2, 'parent_id': 305, 'gender': 'male', 'joining_date': datetime.date(2021, 5, 21),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'sample3@sample.com',
                 'corporate_email': 'anil.sasane@justo.co.in', 'work_email': 'anil.sasane@justo.co.in',
                 'mobile': '9142732121', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 54757.0, 'location': 'Pune', 'barcode': 'JUS0257'},
                {'id': 1478, 'name': 'Apeksha Nagawade', 'pan_number': '000000', 'job_title': 'Assistant Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1998, 12, 1),
                 'department_id': 2, 'parent_id': 1835, 'gender': 'female', 'joining_date': datetime.date(2023, 6, 21),
                 'departure_date': None, 'city': 'City', 'zip': '000000',
                 'private_email': 'ApekshaNagawadedpugbsrc@gmail.com',
                 'corporate_email': 'apeksha.nagawade@justo.co.in', 'work_email': 'apeksha.nagawade@justo.co.in',
                 'mobile': '00000000', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 48611.0, 'location': 'Pune', 'barcode': 'JUS1202'},
                {'id': 225, 'name': 'Animesh Mathur', 'pan_number': 'BAOPM5474P',
                 'job_title': 'Assistant General Manager', 'mobile_phone': '000000000', 'work_phone': '000000',
                 'birthday': datetime.date(1991, 7, 8), 'department_id': 2, 'parent_id': 459, 'gender': 'male',
                 'joining_date': datetime.date(2021, 11, 8), 'departure_date': datetime.date(2024, 7, 24),
                 'city': 'City', 'zip': '000000', 'private_email': 'animeshmathur73@gmail.com',
                 'corporate_email': 'animesh.mathur@justo.co.in', 'work_email': 'animesh.mathur@justo.co.in',
                 'mobile': '7300097892', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 104184.0, 'location': 'Pune', 'barcode': 'JUS0475'},
                {'id': 303, 'name': 'Anurag Tiwari', 'pan_number': 'AYBPT4935E', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1996, 12, 26),
                 'department_id': 5, 'parent_id': 708, 'gender': 'male', 'joining_date': datetime.date(2021, 7, 31),
                 'departure_date': datetime.date(2024, 1, 18), 'city': 'City', 'zip': '000000',
                 'private_email': 'tiwarianurag261296@gmail.com', 'corporate_email': 'anurag.tiwari@justo.co.in',
                 'work_email': 'anurag.tiwari@justo.co.in', 'mobile': '8369382139', 'marital': 'single',
                 'emergency_contact': '00000000', 'active_status': True, 'ctc': 41667.0, 'location': 'KDMC',
                 'barcode': 'M0261'},
                {'id': 1240, 'name': 'Anil Rajmani Tiwari', 'pan_number': 'AYNPT7153N', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1996, 11, 11),
                 'department_id': 2, 'parent_id': 1309, 'gender': 'male', 'joining_date': datetime.date(2022, 9, 15),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'anilucky96@gmail.com',
                 'corporate_email': 'anil.tiwari@justo.co.in', 'work_email': 'anil.tiwari@justo.co.in',
                 'mobile': '8879473799', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 59779.0, 'location': 'Mumbai Western', 'barcode': 'JUS0900'},
                {'id': 1790, 'name': 'Ankita    Amrut Jadhav', 'pan_number': 'DANPJ0084H',
                 'job_title': 'Senior Executive', 'mobile_phone': '000000000', 'work_phone': '000000',
                 'birthday': datetime.date(2003, 11, 27), 'department_id': 15, 'parent_id': None, 'gender': 'female',
                 'joining_date': datetime.date(2024, 6, 24), 'departure_date': None, 'city': 'Pune', 'zip': '412115',
                 'private_email': 'ankitajadhav171@gmail.com', 'corporate_email': 'ankita.jadhav@justo.co.in',
                 'work_email': 'ankita.jadhav@justo.co.in', 'mobile': '7058984691', 'marital': 'married',
                 'emergency_contact': '7776023581', 'active_status': True, 'ctc': 27500.0,
                 'location': 'Regional Office _ Pune', 'barcode': 'JUS651'},
                {'id': 389, 'name': 'Arafatkhan Pathan', 'pan_number': 'CJJPP6799P',
                 'job_title': 'Assistant General Manager', 'mobile_phone': '000000000', 'work_phone': '000000',
                 'birthday': datetime.date(1989, 5, 16), 'department_id': 2, 'parent_id': 337, 'gender': 'male',
                 'joining_date': datetime.date(2022, 7, 9), 'departure_date': None, 'city': 'City', 'zip': '000000',
                 'private_email': 'arafatkhanpathan1989@gmail.com', 'corporate_email': 'arafatkhan.pathan@justo.co.in',
                 'work_email': 'arafatkhan.pathan@justo.co.in', 'mobile': '8788182915', 'marital': 'single',
                 'emergency_contact': '00000000', 'active_status': True, 'ctc': 109666.0, 'location': 'Pune',
                 'barcode': 'JUS0830'},
                {'id': 1712, 'name': 'Arati  Bhagvan  Gaikwad', 'pan_number': 'BJUPG2908R',
                 'job_title': 'Assistant Manager', 'mobile_phone': '000000000', 'work_phone': '000000',
                 'birthday': datetime.date(1994, 2, 19), 'department_id': 14, 'parent_id': 626, 'gender': 'female',
                 'joining_date': datetime.date(2024, 5, 18), 'departure_date': None, 'city': 'Satara', 'zip': '412803',
                 'private_email': 'aartibg19@gmail.com', 'corporate_email': 'aarti.gaikwad@justo.co.in',
                 'work_email': 'aarti.gaikwad@justo.co.in', 'mobile': '9518955844', 'marital': 'single',
                 'emergency_contact': '9923632783', 'active_status': True, 'ctc': 28800.0, 'location': 'Pune',
                 'barcode': 'JUS602'},
                {'id': 1782, 'name': 'Ashish Ramdas Kalokhe', 'pan_number': 'BXFPK6194N', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1989, 9, 29),
                 'department_id': 2, 'parent_id': 1824, 'gender': 'male', 'joining_date': datetime.date(2024, 6, 18),
                 'departure_date': None, 'city': 'Pune ', 'zip': '411037', 'private_email': '9764385004.ak@gmail.com',
                 'corporate_email': 'Ashish.kalokhe@justo.co.in', 'work_email': 'Ashish.kalokhe@justo.co.in',
                 'mobile': '7972739951', 'marital': 'married', 'emergency_contact': '7276442103', 'active_status': True,
                 'ctc': 50000.0, 'location': 'Pune', 'barcode': 'JUS641'},
                {'id': 451, 'name': 'Ashutosh Agarwal', 'pan_number': 'ATJPA1894N', 'job_title': 'Senior Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1990, 2, 4),
                 'department_id': 2, 'parent_id': 1800, 'gender': 'male', 'joining_date': datetime.date(2022, 5, 30),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'ashutosh0402@gmail.com',
                 'corporate_email': 'ashutosh.agarwal@justo.co.in', 'work_email': 'ashutosh.agarwal@justo.co.in',
                 'mobile': '7738427071', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 84779.0, 'location': 'Pune', 'barcode': 'JUS0760'},
                {'id': 825, 'name': 'Archana Patil', 'pan_number': 'BHIPP7394E', 'job_title': 'Executive',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1978, 9, 4),
                 'department_id': 17, 'parent_id': 1810, 'gender': 'female', 'joining_date': datetime.date(2020, 11, 3),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'patil.archana8@gmail.com',
                 'corporate_email': 'archana.patil@justo.co.in', 'work_email': 'archana.patil@justo.co.in',
                 'mobile': '9975240434', 'marital': 'married', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 31124.0, 'location': 'KDMC', 'barcode': 'JUS0142'},
                {'id': 1139, 'name': 'Arohit Anil Rai', 'pan_number': 'CKIPR4403E', 'job_title': 'Assistant Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1996, 9, 12),
                 'department_id': 14, 'parent_id': 946, 'gender': 'male', 'joining_date': datetime.date(2024, 5, 2),
                 'departure_date': None, 'city': 'Mumbai ', 'zip': '401208', 'private_email': 'arohitrai198@gmail.com',
                 'corporate_email': 'arohit.rai@justo.co.in', 'work_email': 'arohit.rai@justo.co.in',
                 'mobile': '8600731058', 'marital': 'single', 'emergency_contact': '8169547430', 'active_status': True,
                 'ctc': 22916.0, 'location': 'Mumbai Western', 'barcode': 'JUS593'},
                {'id': 243, 'name': 'Avishkar Jopulkar', 'pan_number': 'AGWPJ8800D',
                 'job_title': 'General Manager - Sales', 'mobile_phone': '000000000', 'work_phone': '000000',
                 'birthday': datetime.date(1983, 12, 24), 'department_id': 2, 'parent_id': 720, 'gender': 'male',
                 'joining_date': datetime.date(2020, 3, 14), 'departure_date': None, 'city': 'City', 'zip': '000000',
                 'private_email': 'avishkar.jopulkar@gmail.com', 'corporate_email': 'avishkar.jopulkar@justo.co.in',
                 'work_email': 'avishkar.jopulkar@justo.co.in', 'mobile': '9833372412', 'marital': 'single',
                 'emergency_contact': '00000000', 'active_status': True, 'ctc': 250000.0, 'location': 'Mumbai Western',
                 'barcode': 'JUS0103'},
                {'id': 987, 'name': 'Asvi Sanjay Kumari', 'pan_number': 'HZWPK3332M', 'job_title': 'Assistant Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(2000, 9, 18),
                 'department_id': 2, 'parent_id': 918, 'gender': 'female', 'joining_date': datetime.date(2024, 1, 11),
                 'departure_date': datetime.date(2024, 1, 11), 'city': 'mumbai', 'zip': '400012',
                 'private_email': 'sighasvi636@gmail.com', 'corporate_email': 'asvi.kumari@justo.co.in',
                 'work_email': 'asvi.kumari@justo.co.in', 'mobile': '9304385710', 'marital': 'single',
                 'emergency_contact': '8709806123', 'active_status': True, 'ctc': 63000.0, 'location': 'SoBo',
                 'barcode': 'M0764'},
                {'id': 1762, 'name': 'Balvir Singh Yadav', 'pan_number': 'AIRPY6996L', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1991, 4, 20),
                 'department_id': 2, 'parent_id': 896, 'gender': 'male', 'joining_date': datetime.date(2024, 6, 13),
                 'departure_date': None, 'city': 'Pune', 'zip': '411033',
                 'private_email': 'balvirsinghyadav491@gmail.com', 'corporate_email': 'balvir.yadav@justo.co.in',
                 'work_email': 'balvir.yadav@justo.co.in', 'mobile': '9850702963', 'marital': 'single',
                 'emergency_contact': '9506945090', 'active_status': True, 'ctc': 76800.0, 'location': 'Pune',
                 'barcode': 'JUS629'},
                {'id': 468, 'name': 'Bhairavi Tiwari', 'pan_number': 'BGCPT4290C', 'job_title': 'Assistant Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1999, 3, 25),
                 'department_id': 2, 'parent_id': 524, 'gender': 'female', 'joining_date': datetime.date(2022, 4, 1),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'tiwaribhairavi@gmail.com',
                 'corporate_email': 'bhairavi.tiwari@justo.co.in', 'work_email': 'bhairavi.tiwari@justo.co.in',
                 'mobile': '8454035870', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 45500.0, 'location': 'Thane', 'barcode': 'JUS0638'},
                {'id': 393, 'name': 'Bhagyashree Mangesh  Ghag', 'pan_number': 'ASKPG8434E',
                 'job_title': 'Senior Manager', 'mobile_phone': '000000000', 'work_phone': '000000',
                 'birthday': datetime.date(1990, 3, 19), 'department_id': 2, 'parent_id': 834, 'gender': 'female',
                 'joining_date': datetime.date(2021, 2, 2), 'departure_date': datetime.date(2024, 2, 19),
                 'city': 'City', 'zip': '000000', 'private_email': 'Bhagyashree.ghag@gmail.com',
                 'corporate_email': 'bhagyashree.ghag@justo.co.in', 'work_email': 'bhagyashree.ghag@justo.co.in',
                 'mobile': '8591008181', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 86167.0, 'location': 'KDMC', 'barcode': 'M0214'},
                {'id': 1858, 'name': 'Caitan Alphanso', 'pan_number': 'AIZPA9625Q',
                 'job_title': 'Deputy General Manager', 'mobile_phone': '000000000', 'work_phone': '000000',
                 'birthday': datetime.date(1986, 9, 28), 'department_id': 18, 'parent_id': None, 'gender': 'male',
                 'joining_date': datetime.date(2024, 7, 22), 'departure_date': None, 'city': 'Mumbai', 'zip': '400089',
                 'private_email': 'Caitan_alphanso@yahoo.com', 'corporate_email': 'caitan.alphanso@justo.co.in',
                 'work_email': 'caitan.alphanso@justo.co.in', 'mobile': '9594502173', 'marital': 'married',
                 'emergency_contact': '9045453477', 'active_status': True, 'ctc': 200000.0, 'location': 'Mumbai - HO',
                 'barcode': 'JUS677'},
                {'id': 1911, 'name': 'Chandrashekhar Mukesh  Goudmadhley', 'pan_number': 'AZIPG3967F',
                 'job_title': 'Manager', 'mobile_phone': '000000000', 'work_phone': '000000',
                 'birthday': datetime.date(1986, 9, 6), 'department_id': 13, 'parent_id': 244, 'gender': 'male',
                 'joining_date': datetime.date(2024, 8, 18), 'departure_date': None, 'city': 'Badlapur',
                 'zip': '421503', 'private_email': 'shekhar.cool.boy.143@gmail.com',
                 'corporate_email': 'chandrashekhar.goudmadhley@justo.co.in',
                 'work_email': 'chandrashekhar.goudmadhley@justo.co.in', 'mobile': '8169107500', 'marital': 'married',
                 'emergency_contact': '8369910873', 'active_status': True, 'ctc': 67083.0, 'location': 'Thane',
                 'barcode': 'JUS698'},
                {'id': 1890, 'name': 'Darshana Manish Band', 'pan_number': 'FPPPB4711C',
                 'job_title': 'Assistant Manager', 'mobile_phone': '000000000', 'work_phone': '000000',
                 'birthday': datetime.date(1999, 7, 5), 'department_id': 2, 'parent_id': 450, 'gender': 'female',
                 'joining_date': datetime.date(2024, 8, 2), 'departure_date': None, 'city': 'Amravati', 'zip': '444605',
                 'private_email': 'darshanaband01@gmail.com', 'corporate_email': 'darshana.band@justo.co.in',
                 'work_email': 'darshana.band@justo.co.in', 'mobile': '8208444590', 'marital': 'single',
                 'emergency_contact': '7020158483', 'active_status': True, 'ctc': 50000.0, 'location': 'Pune',
                 'barcode': 'JUS689'},
                {'id': 382, 'name': 'Deepak Pandey', 'pan_number': 'BEFPP6491G', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1986, 11, 14),
                 'department_id': 5, 'parent_id': 251, 'gender': 'male', 'joining_date': datetime.date(2021, 11, 22),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'dev.pandey00@gmail.com',
                 'corporate_email': 'deepak.pandey@justo.co.in', 'work_email': 'deepak.pandey@justo.co.in',
                 'mobile': '9993317022', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 49757.0, 'location': 'Pune', 'barcode': 'JUS0502'},
                {'id': 1750, 'name': 'Dasharath Patthe', 'pan_number': 'ECMPP3989K', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1994, 1, 31),
                 'department_id': 2, 'parent_id': 56, 'gender': 'male', 'joining_date': datetime.date(2024, 6, 13),
                 'departure_date': None, 'city': 'Buldhana ', 'zip': '443104',
                 'private_email': 'dasharathpatthe2015@gmail.com', 'corporate_email': 'dasharath.patthe@justo.co.in',
                 'work_email': 'dasharath.patthe@justo.co.in', 'mobile': '9623963609', 'marital': 'married',
                 'emergency_contact': '8421423457', 'active_status': True, 'ctc': 48800.0, 'location': 'Pune',
                 'barcode': 'JUS625'},
                {'id': 1815, 'name': 'Darshan Vilas Suryawanshi', 'pan_number': 'KWNPS5830M',
                 'job_title': 'Assistant Manager', 'mobile_phone': '000000000', 'work_phone': '000000',
                 'birthday': datetime.date(2000, 1, 1), 'department_id': 14, 'parent_id': None, 'gender': 'male',
                 'joining_date': datetime.date(2024, 7, 8), 'departure_date': None, 'city': 'Navi Mumbai ',
                 'zip': '400706', 'private_email': 'darshansuryawanshi2000@gmail.com',
                 'corporate_email': 'darshan.suryawanshi@justo.co.in', 'work_email': 'darshan.suryawanshi@justo.co.in',
                 'mobile': '7045263925', 'marital': 'single', 'emergency_contact': '8356994450', 'active_status': True,
                 'ctc': 40800.0, 'location': 'Navi Mumbai ', 'barcode': 'JUS665'},
                {'id': 427, 'name': 'Dharmendar  Tanwar', 'pan_number': 'BMDPT1367H', 'job_title': 'Assistant Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(2000, 4, 13),
                 'department_id': 2, 'parent_id': 563, 'gender': 'male', 'joining_date': datetime.date(2023, 2, 24),
                 'departure_date': None, 'city': 'City', 'zip': '000000',
                 'private_email': 'dharmendartanwar304@gmail.com', 'corporate_email': 'dharmendar.tanwar@justo.co.in',
                 'work_email': 'dharmendar.tanwar@justo.co.in', 'mobile': '8356080169', 'marital': 'single',
                 'emergency_contact': '00000000', 'active_status': True, 'ctc': 54079.0, 'location': 'Navi Mumbai',
                 'barcode': 'JUS1100'},
                {'id': 497, 'name': 'Dhananjay Nandedkar', 'pan_number': 'AHTPN0600R', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1990, 5, 2),
                 'department_id': 2, 'parent_id': 890, 'gender': 'male', 'joining_date': datetime.date(2022, 9, 19),
                 'departure_date': None, 'city': 'City', 'zip': '000000',
                 'private_email': 'daksnandedkar0207@gmail.com', 'corporate_email': 'dhananjay.nandedkar@justo.co.in',
                 'work_email': 'dhananjay.nandedkar@justo.co.in', 'mobile': '9987261889', 'marital': 'married',
                 'emergency_contact': '00000000', 'active_status': True, 'ctc': 67171.0, 'location': 'Mumbai Western',
                 'barcode': 'JUS0907'},
                {'id': 46, 'name': 'Devendra Shinde', 'pan_number': 'CDMPS7912L', 'job_title': 'Senior Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1986, 9, 18),
                 'department_id': 2, 'parent_id': 7, 'gender': 'male', 'joining_date': datetime.date(2022, 4, 9),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'sample3@sample.com',
                 'corporate_email': 'devendra.shinde@justo.co.in', 'work_email': 'devendra.shinde@justo.co.in',
                 'mobile': '9423016049', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 71754.0, 'location': 'Pune', 'barcode': 'JUS0658'},
                {'id': 39, 'name': 'Deven Javeri', 'pan_number': 'AHKPJ1074M', 'job_title': 'Assistant General Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1982, 8, 9),
                 'department_id': 10, 'parent_id': 841, 'gender': 'male', 'joining_date': datetime.date(2022, 5, 4),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'devenjaveri@gmail.com',
                 'corporate_email': 'deven.javeri@justo.co.in', 'work_email': 'deven.javeri@justo.co.in',
                 'mobile': '8766575442', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 146333.0, 'location': 'Pune', 'barcode': 'JUS0709'},
                {'id': 1772, 'name': 'Diksha Pimpliskar', 'pan_number': 'DMUPP3879R', 'job_title': 'Assistant Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1998, 6, 27),
                 'department_id': 2, 'parent_id': 1950, 'gender': 'female', 'joining_date': datetime.date(2024, 6, 17),
                 'departure_date': None, 'city': 'Nandurbar', 'zip': '425401',
                 'private_email': 'dpimpliskar93@gmail.com', 'corporate_email': 'diksha.pimpliskar@justo.co.in',
                 'work_email': 'diksha.pimpliskar@justo.co.in', 'mobile': '9265212896', 'marital': 'married',
                 'emergency_contact': '9404013312', 'active_status': True, 'ctc': 43833.0, 'location': 'Pune',
                 'barcode': 'JUS638'},
                {'id': 1742, 'name': 'Gaurav  More', 'pan_number': 'DKTPM9658E', 'job_title': 'Executive',
                 'mobile_phone': '9224775412', 'work_phone': '000000', 'birthday': datetime.date(1997, 8, 18),
                 'department_id': 9, 'parent_id': 689, 'gender': 'male', 'joining_date': datetime.date(2019, 10, 5),
                 'departure_date': None, 'city': 'Mumbai', 'zip': '400083', 'private_email': 'gauravmore188@gmail.com',
                 'corporate_email': 'gaurav.more@justo.co.in', 'work_email': 'gaurav.more@justo.co.in',
                 'mobile': '9224775412', 'marital': 'single', 'emergency_contact': '9372462019', 'active_status': True,
                 'ctc': 20000.0, 'location': 'Regional Office_Mumbai', 'barcode': 'JC0008'},
                {'id': 1795, 'name': 'Gaurav  Sahadeo  Joge', 'pan_number': '000000', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1991, 11, 15),
                 'department_id': 2, 'parent_id': 887, 'gender': 'male', 'joining_date': datetime.date(2024, 6, 25),
                 'departure_date': None, 'city': 'City', 'zip': '000000',
                 'private_email': 'gaurav.gauravjoge.joge@gmail.com', 'corporate_email': 'gaurav.joge@justo.co.in',
                 'work_email': 'gaurav.joge@justo.co.in', 'mobile': '00000000', 'marital': 'single',
                 'emergency_contact': '00000000', 'active_status': True, 'ctc': 47500.0, 'location': 'Pune',
                 'barcode': 'JUS652'},
                {'id': 1807, 'name': 'Fatima Makda', 'pan_number': 'GMMPM7283R', 'job_title': 'Assistant Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(2002, 4, 9),
                 'department_id': 2, 'parent_id': 1810, 'gender': 'female', 'joining_date': datetime.date(2024, 7, 1),
                 'departure_date': datetime.date(2024, 7, 13), 'city': 'Mumbai', 'zip': '400612',
                 'private_email': 'makdafatima3@gmail.com', 'corporate_email': 'Fatima.Makda@justo.co.in',
                 'work_email': 'Fatima.Makda@justo.co.in', 'mobile': '9920817241', 'marital': 'single',
                 'emergency_contact': '9699994846', 'active_status': False, 'ctc': 50900.0, 'location': 'Navi Mumbai',
                 'barcode': 'JUS655'},
                {'id': 1549, 'name': 'Harsh Pandey', 'pan_number': 'FEBPP6888B', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(2003, 9, 11),
                 'department_id': 2, 'parent_id': 422, 'gender': 'male', 'joining_date': datetime.date(2024, 4, 1),
                 'departure_date': None, 'city': 'Thane', 'zip': '421001', 'private_email': 'sample3@sample.com',
                 'corporate_email': 'harsh.pandey@justo.co.in', 'work_email': 'harsh.pandey@justo.co.in',
                 'mobile': '7267024311', 'marital': 'single', 'emergency_contact': '8604423392', 'active_status': True,
                 'ctc': 70833.0, 'location': 'Mumbai Western', 'barcode': 'JUS1467'},
                {'id': 531, 'name': 'Hanisha Manglani', 'pan_number': 'FMYPM3232B', 'job_title': 'Assistant Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1999, 12, 21),
                 'department_id': 5, 'parent_id': 933, 'gender': 'female', 'joining_date': datetime.date(2023, 8, 1),
                 'departure_date': None, 'city': 'City', 'zip': '000000',
                 'private_email': 'hunnymanglani2112@gmail.com', 'corporate_email': 'hanisha.manglani@justo.co.in',
                 'work_email': 'hanisha.manglani@justo.co.in', 'mobile': '7218219991', 'marital': 'single',
                 'emergency_contact': '00000000', 'active_status': True, 'ctc': 44167.0,
                 'location': 'Thane - Neelkanth Zen', 'barcode': 'M0698'},
                {'id': 636, 'name': 'Jayendra Ahvade', 'pan_number': 'CLVPA4458C', 'job_title': 'Assistant Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1995, 8, 10),
                 'department_id': 14, 'parent_id': 626, 'gender': 'male', 'joining_date': datetime.date(2022, 12, 13),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'ahvadejayendra@gmail.com',
                 'corporate_email': 'Jayendra.Ahvade@justo.co.in', 'work_email': 'Jayendra.Ahvade@justo.co.in',
                 'mobile': '886610554', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 23300.0, 'location': 'Regional Office _ Pune', 'barcode': 'P0355'},
                {'id': 299, 'name': 'Hunny Karamchandani', 'pan_number': 'AVXPK6711E', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1987, 3, 25),
                 'department_id': 2, 'parent_id': 126, 'gender': 'male', 'joining_date': datetime.date(2022, 5, 7),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'hunnyrk@rediffmail.com',
                 'corporate_email': 'hunny.karamchandani@justo.co.in', 'work_email': 'hunny.karamchandani@justo.co.in',
                 'mobile': '9326831016', 'marital': 'married', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 63923.0, 'location': 'Thane', 'barcode': 'JUS0721'},
                {'id': 1826, 'name': 'Jayesh  Jagannath  Ghadge', 'pan_number': '000000', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1982, 2, 5),
                 'department_id': 2, 'parent_id': 56, 'gender': 'male', 'joining_date': datetime.date(2024, 7, 1),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'jayesh.ghadge777@gmail.com',
                 'corporate_email': 'jayesh.ghadge@justo.co.in', 'work_email': 'jayesh.ghadge@justo.co.in',
                 'mobile': '00000000', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 68800.0, 'location': 'Pune', 'barcode': 'JUS660'},
                {'id': 1506, 'name': 'Jeetendra  Mandavkar', 'pan_number': 'ABcde000aaa', 'job_title': 'Executive',
                 'mobile_phone': '9920270990', 'work_phone': '000000', 'birthday': datetime.date(1980, 4, 20),
                 'department_id': 17, 'parent_id': None, 'gender': 'male', 'joining_date': datetime.date(2019, 7, 1),
                 'departure_date': None, 'city': 'Mumbai', 'zip': '0', 'private_email': 'sample3@sample.com',
                 'corporate_email': 'jeetendra.mandavkar@justo.co.in', 'work_email': 'jeetendra.mandavkar@justo.co.in',
                 'mobile': '9920270990', 'marital': 'single', 'emergency_contact': '0', 'active_status': True,
                 'ctc': 20000.0, 'location': 'Regional Office_Mumbai', 'barcode': 'JC004'},
                {'id': 65, 'name': 'Jayesh Raundal', 'pan_number': 'DZTPR3532P', 'job_title': 'Assistant Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1999, 6, 5),
                 'department_id': 2, 'parent_id': 1133, 'gender': 'male', 'joining_date': datetime.date(2022, 8, 29),
                 'departure_date': None, 'city': 'City', 'zip': '000000',
                 'private_email': 'jayeshraundal9975@gmail.com', 'corporate_email': 'jayesh.raundal@justo.co.in',
                 'work_email': 'jayesh.raundal@justo.co.in', 'mobile': '9156062753', 'marital': 'single',
                 'emergency_contact': '00000000', 'active_status': True, 'ctc': 39779.0, 'location': 'Pune',
                 'barcode': 'JUS0870'},
                {'id': 696, 'name': 'Jayshree Rao', 'pan_number': 'AJGPR6037H', 'job_title': 'General Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1979, 10, 29),
                 'department_id': 18, 'parent_id': 780, 'gender': 'female', 'joining_date': datetime.date(2022, 3, 14),
                 'departure_date': None, 'city': 'Pune', 'zip': '411014', 'private_email': 'jaidhev@yahoo.com',
                 'corporate_email': 'jayshree.rao@justo.co.in', 'work_email': 'jayshree.rao@justo.co.in',
                 'mobile': '9545550626', 'marital': 'single', 'emergency_contact': '9823006878', 'active_status': True,
                 'ctc': 213371.0, 'location': 'Regional Office _ Pune', 'barcode': 'JUS0622'},
                {'id': 910, 'name': 'Jyoti Rajaram Kanoje', 'pan_number': '000000', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1992, 9, 18),
                 'department_id': 2, 'parent_id': 741, 'gender': 'female', 'joining_date': datetime.date(2024, 3, 16),
                 'departure_date': datetime.date(2024, 4, 4), 'city': 'City', 'zip': '000000',
                 'private_email': 'jyoti.kanoje1892@gmail.com', 'corporate_email': 'jyoti1.kanoje@justo.co.in',
                 'work_email': 'jyoti1.kanoje@justo.co.in', 'mobile': '00000000', 'marital': 'single',
                 'emergency_contact': '00000000', 'active_status': True, 'ctc': 63000.0, 'location': 'KDMC',
                 'barcode': 'M0815'},
                {'id': 662, 'name': 'Kalpesh Ambre', 'pan_number': 'ASZPA0351K', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1992, 6, 3),
                 'department_id': 10, 'parent_id': 855, 'gender': 'male', 'joining_date': datetime.date(2022, 8, 2),
                 'departure_date': datetime.date(2024, 1, 13), 'city': 'City', 'zip': '000000',
                 'private_email': 'kalpeshambre255@gmail.com', 'corporate_email': 'kalpesh.ambre@justo.co.in',
                 'work_email': 'kalpesh.ambre@justo.co.in', 'mobile': '9004636326', 'marital': 'single',
                 'emergency_contact': '00000000', 'active_status': True, 'ctc': 77500.0, 'location': 'Mumbai Western',
                 'barcode': 'M0527'},
                {'id': 485, 'name': 'Kapil Narendra Pitroda', 'pan_number': 'ASJPP3605K', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1986, 10, 23),
                 'department_id': 10, 'parent_id': 103, 'gender': 'male', 'joining_date': datetime.date(2022, 6, 15),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'kapil.pitroda@gmail.com',
                 'corporate_email': 'kapil.pitroda@justo.co.in', 'work_email': 'kapil.pitroda@justo.co.in',
                 'mobile': '9833550560', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 64167.0, 'location': 'Navi Mumbai', 'barcode': 'M0505'},
                {'id': 925, 'name': 'Karan Singh', 'pan_number': 'JCKPS7684R', 'job_title': 'Manager',
                 'mobile_phone': '7983029397/9458778908', 'work_phone': '000000',
                 'birthday': datetime.date(1997, 7, 28), 'department_id': 2, 'parent_id': 436, 'gender': 'male',
                 'joining_date': datetime.date(2023, 11, 9), 'departure_date': None, 'city': 'City', 'zip': '000000',
                 'private_email': 'karan.thakur.1705@gmail.com', 'corporate_email': 'karan.singh@justo.co.in',
                 'work_email': 'karan.singh@justo.co.in', 'mobile': '00000000', 'marital': 'single',
                 'emergency_contact': '00000000', 'active_status': True, 'ctc': 50000.0, 'location': 'Navi Mumbai',
                 'barcode': 'M0730'},
                {'id': 480, 'name': 'Karan Ghanshyam  Bhatia', 'pan_number': 'EPPPB8208K',
                 'job_title': 'Assistant Manager', 'mobile_phone': '000000000', 'work_phone': '000000',
                 'birthday': datetime.date(2000, 4, 28), 'department_id': 2, 'parent_id': None, 'gender': 'male',
                 'joining_date': datetime.date(2023, 2, 11), 'departure_date': datetime.date(2024, 4, 9),
                 'city': 'City', 'zip': '000000', 'private_email': 'Karanbhatia0905@gmail.com',
                 'corporate_email': 'karan.bhatia@justo.co.in', 'work_email': 'karan.bhatia@justo.co.in',
                 'mobile': '7020973338', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 33050.0, 'location': 'KDMC', 'barcode': 'M0634'},
                {'id': 1791, 'name': 'Ketki Vikas Mandlekar', 'pan_number': 'AWHPP4206G', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1986, 7, 8),
                 'department_id': 2, 'parent_id': 524, 'gender': 'female', 'joining_date': datetime.date(2024, 6, 23),
                 'departure_date': None, 'city': 'Thane', 'zip': '400601',
                 'private_email': 'ketkimandlekar8786@gmail.com', 'corporate_email': 'Ketki.Mandlekar@justo.co.in',
                 'work_email': 'Ketki.Mandlekar@justo.co.in', 'mobile': '9143758786', 'marital': 'married',
                 'emergency_contact': '7208686410', 'active_status': True, 'ctc': 41666.0, 'location': 'Thane',
                 'barcode': 'JUS649'},
                {'id': 720, 'name': 'Puspamitra Das', 'pan_number': '000000', 'job_title': 'Director',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1968, 7, 2),
                 'department_id': 21, 'parent_id': None, 'gender': 'male', 'joining_date': datetime.date(2010, 3, 1),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'sample3@sample.com',
                 'corporate_email': 'pushp@justo.co.in', 'work_email': 'pushp@justo.co.in', 'mobile': '00000000',
                 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True, 'ctc': 0.0,
                 'location': 'Mumbai - HO', 'barcode': 'MGM001'},
                {'id': 505, 'name': 'Ketan Nagare', 'pan_number': 'AFFPN2079A', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1983, 11, 13),
                 'department_id': 2, 'parent_id': 12, 'gender': 'male', 'joining_date': datetime.date(2022, 9, 21),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'ketan1311@gmail.com',
                 'corporate_email': 'ketan.nagare@justo.co.in', 'work_email': 'ketan.nagare@justo.co.in',
                 'mobile': '9890144404', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 64757.0, 'location': 'Pune', 'barcode': 'JUS0910'},
                {'id': 652, 'name': 'Kavita Halijwale', 'pan_number': 'ABVPH3039E', 'job_title': 'Assistant Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1975, 5, 23),
                 'department_id': 14, 'parent_id': 626, 'gender': 'female', 'joining_date': datetime.date(2022, 12, 15),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'kavita.halijwale@gmail.com',
                 'corporate_email': 'Kavita.Halijwale@justo.co.in', 'work_email': 'Kavita.Halijwale@justo.co.in',
                 'mobile': '9665051534', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 26800.0, 'location': 'Pune', 'barcode': 'P0357'},
                {'id': 843, 'name': 'Kshetrabasi Mohapatra', 'pan_number': 'CXTPM1679R',
                 'job_title': 'Assistant Manager', 'mobile_phone': '000000000', 'work_phone': '000000',
                 'birthday': datetime.date(1987, 4, 5), 'department_id': 2, 'parent_id': 721, 'gender': 'male',
                 'joining_date': datetime.date(2023, 5, 16), 'departure_date': datetime.date(2023, 11, 21),
                 'city': 'City', 'zip': '000000', 'private_email': 'kshetrabasi.123456789@gmail.com',
                 'corporate_email': 'kshetrabasi.mohapatra@justo.co.in',
                 'work_email': 'kshetrabasi.mohapatra@justo.co.in', 'mobile': '00000000', 'marital': 'single',
                 'emergency_contact': '00000000', 'active_status': True, 'ctc': 33800.0,
                 'location': 'BBSR Regional Office', 'barcode': 'B0021'},
                {'id': 515, 'name': 'Kunal Sharma', 'pan_number': 'BHNPS1228R', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1984, 2, 12),
                 'department_id': 10, 'parent_id': 841, 'gender': 'male', 'joining_date': datetime.date(2021, 9, 28),
                 'departure_date': None, 'city': 'City', 'zip': '000000',
                 'private_email': 'kunalsharma_media@rediff.com', 'corporate_email': 'kunal.sharma@justo.co.in',
                 'work_email': 'kunal.sharma@justo.co.in', 'mobile': '96730 48833', 'marital': 'single',
                 'emergency_contact': '00000000', 'active_status': True, 'ctc': 64757.0, 'location': 'Pune',
                 'barcode': 'JUS0422'},
                {'id': 678, 'name': 'Kshitija Pagare', 'pan_number': 'GAUPP2509B', 'job_title': 'Executive',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(2002, 4, 1),
                 'department_id': 9, 'parent_id': 728, 'gender': 'female', 'joining_date': datetime.date(2022, 8, 29),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'sample3@sample.com',
                 'corporate_email': 'kshitija.pagare@justo.co.in', 'work_email': 'kshitija.pagare@justo.co.in',
                 'mobile': '9834808128', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 29779.0, 'location': 'Regional Office _ Pune', 'barcode': 'JUS0871'},
                {'id': 1829, 'name': 'Krishna  Abhayrao  Deshmukh', 'pan_number': '000000', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1997, 5, 6),
                 'department_id': 2, 'parent_id': 887, 'gender': 'male', 'joining_date': datetime.date(2024, 7, 1),
                 'departure_date': None, 'city': 'City', 'zip': '000000',
                 'private_email': 'krishnadeshmukh0605@gmail.com', 'corporate_email': 'krishna.deshmukh@justo.co.in',
                 'work_email': 'krishna.deshmukh@justo.co.in', 'mobile': '00000000', 'marital': 'single',
                 'emergency_contact': '00000000', 'active_status': True, 'ctc': 63800.0, 'location': 'Pune',
                 'barcode': 'JUS663'},
                {'id': 319, 'name': 'Kiran Shinde', 'pan_number': 'BBXPS5633J',
                 'job_title': 'Assistant General Manager', 'mobile_phone': '000000000', 'work_phone': '000000',
                 'birthday': datetime.date(1985, 3, 26), 'department_id': 2, 'parent_id': 459, 'gender': 'male',
                 'joining_date': datetime.date(2021, 1, 24), 'departure_date': None, 'city': 'City', 'zip': '000000',
                 'private_email': 'kirran.shinde@gmail.com', 'corporate_email': 'kiran.shinde@justo.co.in',
                 'work_email': 'kiran.shinde@justo.co.in', 'mobile': '9762585812', 'marital': 'single',
                 'emergency_contact': '00000000', 'active_status': True, 'ctc': 124666.0, 'location': 'Pune',
                 'barcode': 'JUS0217'},
                {'id': 1356, 'name': 'Manjiri Pritam Sawant', 'pan_number': 'OFHPS5461H', 'job_title': 'Executive',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(2003, 6, 2),
                 'department_id': 2, 'parent_id': 854, 'gender': 'female', 'joining_date': datetime.date(2024, 2, 5),
                 'departure_date': None, 'city': 'Mumbai', 'zip': '400055',
                 'private_email': 'sawantmanjiri46@gmail.com', 'corporate_email': 'manjiri.sawant@justo.co.in',
                 'work_email': 'manjiri.sawant@justo.co.in', 'mobile': '8104583088', 'marital': 'single',
                 'emergency_contact': '9702650575', 'active_status': True, 'ctc': 32400.0, 'location': 'Mumbai Western',
                 'barcode': 'JUS1390'},
                {'id': 1798, 'name': 'Manish Udutha', 'pan_number': 'AELPU3267N', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1995, 9, 20),
                 'department_id': 10, 'parent_id': None, 'gender': 'male', 'joining_date': datetime.date(2024, 6, 27),
                 'departure_date': None, 'city': 'Bhiwandi', 'zip': '421302', 'private_email': 'manishudutha@gmail.com',
                 'corporate_email': 'manish.udutha@JUSTO.CO.IN', 'work_email': 'manish.udutha@JUSTO.CO.IN',
                 'mobile': '9324657585', 'marital': 'single', 'emergency_contact': '9766888090', 'active_status': True,
                 'ctc': 91666.0, 'location': 'Navi Mumbai', 'barcode': 'JUS653'},
                {'id': 1484, 'name': 'Mashak Lalmahammad', 'pan_number': '000000', 'job_title': 'Assistant Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1997, 2, 16),
                 'department_id': 2, 'parent_id': 389, 'gender': 'male', 'joining_date': datetime.date(2023, 7, 13),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'mashakshah397@gmail.com',
                 'corporate_email': 'mashak.lalmahammad@justo.co.in', 'work_email': 'mashak.lalmahammad@justo.co.in',
                 'mobile': '00000000', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 47250.0, 'location': 'Pune', 'barcode': 'JUS1221'},
                {'id': 67, 'name': 'Mayur Gite', 'pan_number': 'ANBPG2200L', 'job_title': 'Senior Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1989, 10, 24),
                 'department_id': 2, 'parent_id': 1308, 'gender': 'male', 'joining_date': datetime.date(2022, 6, 6),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'mayurgt21@gmail.com',
                 'corporate_email': 'mayur.gite@justo.co.in', 'work_email': 'mayur.gite@justo.co.in',
                 'mobile': '9028024059', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 64779.0, 'location': 'Pune', 'barcode': 'JUS0782'},
                {'id': 1614, 'name': 'Manthan Dekate', 'pan_number': 'DPSPD7372N', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1998, 8, 18),
                 'department_id': 2, 'parent_id': 1133, 'gender': 'male', 'joining_date': datetime.date(2024, 1, 17),
                 'departure_date': None, 'city': 'Pune', 'zip': '411033', 'private_email': 'manthandekate@gmail.com',
                 'corporate_email': 'manthan.dekate@justo.co.in', 'work_email': 'manthan.dekate@justo.co.in',
                 'mobile': '9179603069', 'marital': 'single', 'emergency_contact': '9826755329', 'active_status': True,
                 'ctc': 53800.0, 'location': 'Pune', 'barcode': 'JUS1371'},
                {'id': 1707, 'name': 'Mansoor Ahmed Khan', 'pan_number': 'ESFPM3552L', 'job_title': 'Assistant Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1996, 2, 22),
                 'department_id': 2, 'parent_id': 1810, 'gender': 'male', 'joining_date': datetime.date(2024, 5, 27),
                 'departure_date': None, 'city': 'Akola', 'zip': '444002', 'private_email': 'mansoorakola96@gmail.com',
                 'corporate_email': 'mansoor.khan@justo.co.in', 'work_email': 'mansoor.khan@justo.co.in',
                 'mobile': '9987313430', 'marital': 'married', 'emergency_contact': '9913549646', 'active_status': True,
                 'ctc': 55000.0, 'location': 'Navi Mumbai', 'barcode': 'JUS606'},
                {'id': 369, 'name': 'Manojkumar Dhaygude', 'pan_number': 'ANJPD9901B', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1989, 12, 8),
                 'department_id': 2, 'parent_id': 388, 'gender': 'male', 'joining_date': datetime.date(2023, 4, 21),
                 'departure_date': None, 'city': 'City', 'zip': '000000',
                 'private_email': 'dhaigudemanojkumar08@gmail.com',
                 'corporate_email': 'manojkumar.dhaygude@justo.co.in', 'work_email': 'manojkumar.dhaygude@justo.co.in',
                 'mobile': '00000000', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 47800.0, 'location': 'Pune', 'barcode': 'JUS1125'},
                {'id': 1133, 'name': 'Mitosh Subhash Navale', 'pan_number': 'AHNPN1252D',
                 'job_title': 'Assistant General Manager', 'mobile_phone': '000000000', 'work_phone': '000000',
                 'birthday': datetime.date(1988, 9, 5), 'department_id': 2, 'parent_id': 75, 'gender': 'male',
                 'joining_date': datetime.date(2024, 4, 25), 'departure_date': None, 'city': 'Pune', 'zip': '411028',
                 'private_email': 'mitoshnavale33@gmail.com', 'corporate_email': 'mitosh.navale@justo.co.in',
                 'work_email': 'mitosh.navale@justo.co.in', 'mobile': '9142926464', 'marital': 'married',
                 'emergency_contact': '9823202198', 'active_status': True, 'ctc': 125000.0, 'location': 'Pune',
                 'barcode': 'JUS1515'},
                {'id': 648, 'name': 'Milind Patange', 'pan_number': 'ABEPP3813D', 'job_title': 'General Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1968, 12, 3),
                 'department_id': 7, 'parent_id': 6, 'gender': 'male', 'joining_date': datetime.date(2021, 9, 3),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'milind_patange@yahoo.com',
                 'corporate_email': 'milind.patange@justo.co.in', 'work_email': 'milind.patange@justo.co.in',
                 'mobile': '9823166443', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 298314.0, 'location': 'Regional Office _ Pune', 'barcode': 'JUS0394'},
                {'id': 943, 'name': 'Meghana  Gurav', 'pan_number': 'CXIPG0200R', 'job_title': 'Executive',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(2001, 3, 2),
                 'department_id': 15, 'parent_id': 882, 'gender': 'female', 'joining_date': datetime.date(2023, 8, 25),
                 'departure_date': datetime.date(2024, 4, 13), 'city': 'pune', 'zip': '411057',
                 'private_email': 'guravmeghana2001@gmail.com', 'corporate_email': 'meghana.gurav@justo.co.in',
                 'work_email': 'meghana.gurav@justo.co.in', 'mobile': '7028805615', 'marital': 'single',
                 'emergency_contact': '0', 'active_status': True, 'ctc': 28000.0, 'location': 'Regional Office _ Pune',
                 'barcode': 'P0492'},
                {'id': 728, 'name': 'Meghesh Kulkarni', 'pan_number': 'ALLPK9056A',
                 'job_title': 'Deputy General Manager', 'mobile_phone': '000000000', 'work_phone': '000000',
                 'birthday': datetime.date(1976, 3, 23), 'department_id': 9, 'parent_id': 6, 'gender': 'male',
                 'joining_date': datetime.date(2021, 10, 25), 'departure_date': None, 'city': 'City', 'zip': '000000',
                 'private_email': 'sample3@sample.com', 'corporate_email': 'meghesh.kulkarni@justo.co.in',
                 'work_email': 'meghesh.kulkarni@justo.co.in', 'mobile': '9082155993', 'marital': 'single',
                 'emergency_contact': '00000000', 'active_status': True, 'ctc': 0.0,
                 'location': 'Regional Office _ Pune', 'barcode': 'JUS0466'},
                {'id': 1780, 'name': 'Monali Chavan ', 'pan_number': 'CHDPR4279N', 'job_title': 'Senior Executive',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1990, 8, 29),
                 'department_id': 15, 'parent_id': 1824, 'gender': 'female', 'joining_date': datetime.date(2024, 6, 17),
                 'departure_date': None, 'city': 'pune ', 'zip': '411057', 'private_email': 'rmonali9@gmail.com',
                 'corporate_email': 'monali.chavan@justo.co.in', 'work_email': 'monali.chavan@justo.co.in',
                 'mobile': '7499776731', 'marital': 'married', 'emergency_contact': '9637471873', 'active_status': True,
                 'ctc': 30000.0, 'location': 'Pune', 'barcode': 'JUS639'},
                {'id': 1069, 'name': 'Mohammed Rizwan', 'pan_number': 'DSOPR6323A', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1994, 6, 28),
                 'department_id': 2, 'parent_id': 1810, 'gender': 'male', 'joining_date': datetime.date(2024, 3, 26),
                 'departure_date': None, 'city': 'Thane', 'zip': '421204', 'private_email': 'rizwanm879@gmail.com',
                 'corporate_email': 'mohammed.rizwan@justo.co.in', 'work_email': 'mohammed.rizwan@justo.co.in',
                 'mobile': '9156747641', 'marital': 'single', 'emergency_contact': '7276773334', 'active_status': True,
                 'ctc': 47833.0, 'location': 'Navi Mumbai', 'barcode': 'JUS1462'},
                {'id': 1928, 'name': 'Naman Lal saheb Singh', 'pan_number': 'NHNPS7529K', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(2000, 1, 1),
                 'department_id': 2, 'parent_id': 1043, 'gender': 'male', 'joining_date': datetime.date(2024, 9, 2),
                 'departure_date': None, 'city': 'Nashik', 'zip': '422009',
                 'private_email': 'namansinghbyk1742@gmail.com', 'corporate_email': 'naman.singh@justo.co.in',
                 'work_email': 'naman.singh@justo.co.in', 'mobile': '9325871742', 'marital': 'single',
                 'emergency_contact': '9370141920', 'active_status': True, 'ctc': 53800.0, 'location': 'Mumbai Western',
                 'barcode': 'JUS702'},
                {'id': 653, 'name': 'Mugdha Ambawale', 'pan_number': 'DNAPA1791Q', 'job_title': 'Management Trainee',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(2001, 2, 13),
                 'department_id': 18, 'parent_id': None, 'gender': 'female',
                 'joining_date': datetime.date(2022, 12, 22), 'departure_date': datetime.date(2024, 4, 26),
                 'city': 'Pune', 'zip': '412101', 'private_email': 'mugdha.ambawale0713@gmai.com',
                 'corporate_email': 'Mugdha.Ambawale@justo.co.in', 'work_email': 'Mugdha.Ambawale@justo.co.in',
                 'mobile': '9309538358', 'marital': 'single', 'emergency_contact': '9922888832', 'active_status': True,
                 'ctc': 43800.0, 'location': 'Regional Office _ Pune', 'barcode': 'P0363'},
                {'id': 1408, 'name': 'Monish  Ravindra Chaudhari', 'pan_number': 'ARXPC7843D',
                 'job_title': 'Senior Manager', 'mobile_phone': '000000000', 'work_phone': '000000',
                 'birthday': datetime.date(1988, 11, 4), 'department_id': 9, 'parent_id': 728, 'gender': 'male',
                 'joining_date': datetime.date(2024, 6, 3), 'departure_date': None, 'city': 'Domivli', 'zip': '421202',
                 'private_email': 'monishc80@gmail.com', 'corporate_email': 'monish.chaudhari@justo.co.in',
                 'work_email': 'monish.chaudhari@justo.co.in', 'mobile': '9619057244', 'marital': 'married',
                 'emergency_contact': '9967505649', 'active_status': True, 'ctc': 94167.0,
                 'location': 'Regional Office _ Pune', 'barcode': 'JUS616'},
                {'id': 1420, 'name': 'Mukesh Yadav', 'pan_number': 'ATCPY9723D', 'job_title': 'Assistant Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1998, 7, 30),
                 'department_id': 2, 'parent_id': None, 'gender': 'male', 'joining_date': datetime.date(2023, 7, 17),
                 'departure_date': datetime.date(2024, 7, 13), 'city': 'City', 'zip': '000000',
                 'private_email': 'sudo9930@gmail.com', 'corporate_email': 'mukesh.yadav@justo.co.in',
                 'work_email': 'mukesh.yadav@justo.co.in', 'mobile': '00000000', 'marital': 'single',
                 'emergency_contact': '00000000', 'active_status': True, 'ctc': 35000.0, 'location': 'Navi Mumbai',
                 'barcode': 'JUS1226'},
                {'id': 883, 'name': 'Nagesh Kamble', 'pan_number': 'CIHPK9700L', 'job_title': 'Senior Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1985, 11, 22),
                 'department_id': 2, 'parent_id': 993, 'gender': 'female', 'joining_date': datetime.date(2024, 2, 1),
                 'departure_date': datetime.date(2024, 2, 26), 'city': 'Pune', 'zip': '411032',
                 'private_email': 'nk.2211@gmail.com', 'corporate_email': 'nagesh.kamble@justo.co.in',
                 'work_email': 'nagesh.kamble@justo.co.in', 'mobile': '9356803290', 'marital': 'married',
                 'emergency_contact': '9821838280', 'active_status': True, 'ctc': 68800.0, 'location': 'Pune',
                 'barcode': 'P0546'},
                {'id': 1875, 'name': 'Mrugesh Trivedi', 'pan_number': 'AFRPT8473Q',
                 'job_title': 'Assistant General Manager', 'mobile_phone': '000000000', 'work_phone': '000000',
                 'birthday': datetime.date(1985, 12, 13), 'department_id': 2, 'parent_id': 1800, 'gender': 'male',
                 'joining_date': datetime.date(2024, 7, 22), 'departure_date': None, 'city': 'Pune', 'zip': '411033',
                 'private_email': 'mrugesh.trivedi01@gmail.com', 'corporate_email': 'mrugesh.trivedi@justo.co.in',
                 'work_email': 'mrugesh.trivedi@justo.co.in', 'mobile': '9822323507', 'marital': 'married',
                 'emergency_contact': '9881463275', 'active_status': True, 'ctc': 141667.0, 'location': 'Pune',
                 'barcode': 'JUS678'},
                {'id': 295, 'name': 'Navin Katariya', 'pan_number': 'DJSPK9790M', 'job_title': 'Assistant Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1994, 7, 26),
                 'department_id': 2, 'parent_id': 848, 'gender': 'male', 'joining_date': datetime.date(2022, 6, 15),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'navinkataria107@gmail.com',
                 'corporate_email': 'navin.kataria@justo.co.in', 'work_email': 'navin.kataria@justo.co.in',
                 'mobile': '8956587606', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 63946.0, 'location': 'Thane', 'barcode': 'JUS0805'},
                {'id': 888, 'name': 'Narendra B Mishara', 'pan_number': 'ACCPM7845B', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1973, 12, 31),
                 'department_id': 2, 'parent_id': 100, 'gender': 'male', 'joining_date': datetime.date(2024, 2, 1),
                 'departure_date': datetime.date(2024, 4, 7), 'city': 'Thane', 'zip': '400603',
                 'private_email': 'omkarenterprises.nmumbai@gmail.com',
                 'corporate_email': 'narendra.mishra@justo.co.in', 'work_email': 'narendra.mishra@justo.co.in',
                 'mobile': '9920295553', 'marital': 'married', 'emergency_contact': '7900078746', 'active_status': True,
                 'ctc': 43750.0, 'location': 'Navi Mumbai', 'barcode': 'M0776'},
                {'id': 921, 'name': 'Neha sharma', 'pan_number': '000000', 'job_title': 'Senior Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1985, 7, 2),
                 'department_id': 7, 'parent_id': 918, 'gender': 'female', 'joining_date': datetime.date(2024, 1, 4),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'mailton87@gmail.com',
                 'corporate_email': 'neha.sharma@justo.co.in', 'work_email': 'neha.sharma@justo.co.in',
                 'mobile': '00000000', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 20000.0, 'location': 'Regional Office_Mumbai', 'barcode': 'M0758'},
                {'id': 379, 'name': 'Nisha Bharti', 'pan_number': 'BYOPB4504R', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1993, 2, 11),
                 'department_id': 2, 'parent_id': 1593, 'gender': 'female', 'joining_date': datetime.date(2022, 7, 15),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'sample3@sample.com',
                 'corporate_email': 'nisha.bharti@justo.co.in', 'work_email': 'nisha.bharti@justo.co.in',
                 'mobile': '7030524817', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 64779.0, 'location': 'Pune', 'barcode': 'JUS0833'},
                {'id': 1760, 'name': 'Nikhil Vijay Kulkarni ', 'pan_number': 'ATHPK2944B', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1983, 9, 8),
                 'department_id': 7, 'parent_id': 648, 'gender': 'male', 'joining_date': datetime.date(2024, 6, 13),
                 'departure_date': None, 'city': 'Satara', 'zip': '415001',
                 'private_email': 'nikhilkulkarni303@gmail.com', 'corporate_email': 'nikhil.kulkarni@justo.co.in',
                 'work_email': 'nikhil.kulkarni@justo.co.in', 'mobile': '9890963303', 'marital': 'single',
                 'emergency_contact': '9764999966', 'active_status': True, 'ctc': 86250.0, 'location': 'Pune',
                 'barcode': 'JUS626'},
                {'id': 1891, 'name': 'Omkar Mahesh Janvekar', 'pan_number': 'CEVPJ0150B', 'job_title': 'Executive',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(2002, 1, 24),
                 'department_id': 10, 'parent_id': 841, 'gender': 'male', 'joining_date': datetime.date(2024, 8, 6),
                 'departure_date': None, 'city': 'Loni KD', 'zip': '413713', 'private_email': 'janvekaromkar@gmail.com',
                 'corporate_email': 'omkar.janekar@justo.co.in', 'work_email': 'omkar.janekar@justo.co.in',
                 'mobile': '09370602824', 'marital': 'single', 'emergency_contact': '9763867970', 'active_status': True,
                 'ctc': 40000.0, 'location': 'Pune', 'barcode': 'JUS692'},
                {'id': 516, 'name': 'Nitika Yadav', 'pan_number': 'AJAPY4555D', 'job_title': 'Assistant Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1994, 1, 6),
                 'department_id': 5, 'parent_id': 708, 'gender': 'female', 'joining_date': datetime.date(2023, 7, 7),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'nitikay2@gmail.com',
                 'corporate_email': 'nitika.yadav@justo.co.in', 'work_email': 'nitika.yadav@justo.co.in',
                 'mobile': '00000000', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 40417.0, 'location': 'KDMC', 'barcode': 'M0683'},
                {'id': 6, 'name': 'Nitin Pardeshi', 'pan_number': 'AHCPP9795J', 'job_title': 'DIrector',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1979, 2, 10),
                 'department_id': 24, 'parent_id': 720, 'gender': 'male', 'joining_date': datetime.date(2020, 2, 29),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'vpnitin1@gmail.com',
                 'corporate_email': 'nitin.pardeshi@justo.co.in', 'work_email': 'nitin.pardeshi@justo.co.in',
                 'mobile': '9930505330', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 1250000.0, 'location': 'Regional Office _ Pune', 'barcode': 'JUS0092'},
                {'id': 599, 'name': 'Nithin Jagdish Bhagath', 'pan_number': 'AEUPB1221Q',
                 'job_title': 'Senior Vice President', 'mobile_phone': '000000000', 'work_phone': '000000',
                 'birthday': datetime.date(1973, 7, 23), 'department_id': 2, 'parent_id': None, 'gender': 'male',
                 'joining_date': datetime.date(2022, 11, 24), 'departure_date': datetime.date(2024, 2, 29),
                 'city': 'City', 'zip': '000000', 'private_email': 'nithinbhagath1@gmail.com',
                 'corporate_email': 'nithin.bhagath@justo.co.in', 'work_email': 'nithin.bhagath@justo.co.in',
                 'mobile': '9167972289', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 585133.0, 'location': 'Mumbai - HO', 'barcode': 'M0586'},
                {'id': 1454, 'name': 'Nitin Sonawane', 'pan_number': '000000', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1987, 5, 17),
                 'department_id': 2, 'parent_id': 319, 'gender': 'male', 'joining_date': datetime.date(2023, 6, 1),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'Sonawane.Nitin12@gmail.com',
                 'corporate_email': 'nitin.sonawane@justo.co.in', 'work_email': 'nitin.sonawane@justo.co.in',
                 'mobile': '00000000', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 57500.0, 'location': 'Pune', 'barcode': 'JUS1165'},
                {'id': 1832, 'name': 'Nishant  Sharma', 'pan_number': '000000',
                 'job_title': 'Assistant General Manager', 'mobile_phone': '000000000', 'work_phone': '000000',
                 'birthday': datetime.date(1992, 1, 29), 'department_id': 2, 'parent_id': 1702, 'gender': 'male',
                 'joining_date': datetime.date(2024, 7, 8), 'departure_date': None, 'city': 'City', 'zip': '000000',
                 'private_email': 'nishant.sharma1992jan@gmail.com', 'corporate_email': 'nishant.sharma@justo.co.in',
                 'work_email': 'nishant.sharma@justo.co.in', 'mobile': '00000000', 'marital': 'single',
                 'emergency_contact': '00000000', 'active_status': True, 'ctc': 116667.0, 'location': 'Pune',
                 'barcode': 'JUS667'},
                {'id': 42, 'name': 'Ovez Shaikh', 'pan_number': 'BOOPS3182N', 'job_title': 'Senior Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1988, 8, 4),
                 'department_id': 2, 'parent_id': 1461, 'gender': 'male', 'joining_date': datetime.date(2022, 2, 14),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'sample3@sample.com',
                 'corporate_email': 'ovez.shaikh@justo.co.in', 'work_email': 'ovez.shaikh@justo.co.in',
                 'mobile': '7777070835', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 64757.0, 'location': 'Pune', 'barcode': 'JUS0599'},
                {'id': 17, 'name': 'Parag Chavaan', 'pan_number': 'AFCPC8097C', 'job_title': 'Senior Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1980, 12, 28),
                 'department_id': 2, 'parent_id': 56, 'gender': 'male', 'joining_date': datetime.date(2022, 5, 30),
                 'departure_date': None, 'city': 'Pune ', 'zip': '412101', 'private_email': 'paragchavaan@gmail.com',
                 'corporate_email': 'parag.chavaan@justo.co.in', 'work_email': 'parag.chavaan@justo.co.in',
                 'mobile': '8975003737', 'marital': 'married', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 84757.0, 'location': 'Pune', 'barcode': 'JUS0762'},
                {'id': 742, 'name': 'Pankaj Padol', 'pan_number': 'DWVPP0085A', 'job_title': 'Senior Executive',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1994, 3, 18),
                 'department_id': 2, 'parent_id': 8, 'gender': 'male', 'joining_date': datetime.date(2023, 5, 16),
                 'departure_date': datetime.date(2023, 9, 11), 'city': 'City', 'zip': '000000',
                 'private_email': 'PankajPadol@gmail.com', 'corporate_email': 'pankaj.padol@justo.co.in',
                 'work_email': 'pankaj.padol@justo.co.in', 'mobile': '00000000', 'marital': 'single',
                 'emergency_contact': '00000000', 'active_status': True, 'ctc': 33800.0, 'location': 'Pune',
                 'barcode': 'P0428'},
                {'id': 1247, 'name': 'Parag Bhoir', 'pan_number': 'CZWPB3446E', 'job_title': 'Executive',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1999, 5, 17),
                 'department_id': 10, 'parent_id': 855, 'gender': 'male', 'joining_date': datetime.date(2024, 5, 6),
                 'departure_date': None, 'city': 'Uran', 'zip': '400702', 'private_email': 'paragbhoir30@gmail.com',
                 'corporate_email': 'parag.bhoir@justo.co.in', 'work_email': 'parag.bhoir@justo.co.in',
                 'mobile': '9819366251', 'marital': 'single', 'emergency_contact': '9221396918', 'active_status': True,
                 'ctc': 41666.0, 'location': 'Navi Mumbai ', 'barcode': 'JUS596'},
                {'id': 626, 'name': 'Onkar Kulkarni', 'pan_number': 'AWXPK5710C',
                 'job_title': 'Assistant General Manager', 'mobile_phone': '000000000', 'work_phone': '000000',
                 'birthday': datetime.date(1986, 5, 26), 'department_id': 14, 'parent_id': 6, 'gender': 'male',
                 'joining_date': datetime.date(2022, 9, 6), 'departure_date': None, 'city': 'City', 'zip': '000000',
                 'private_email': 'omkar9700@gmail.com', 'corporate_email': 'onkar.kulkarni@justo.co.in',
                 'work_email': 'onkar.kulkarni@justo.co.in', 'mobile': '9011333009', 'marital': 'single',
                 'emergency_contact': '00000000', 'active_status': True, 'ctc': 149667.0,
                 'location': 'Regional Office _ Pune', 'barcode': 'JUS0887'},
                {'id': 32, 'name': 'Parikshit Paunikar', 'pan_number': 'CPZPP9557H', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1990, 5, 29),
                 'department_id': 5, 'parent_id': 251, 'gender': 'male', 'joining_date': datetime.date(2021, 8, 11),
                 'departure_date': None, 'city': 'City', 'zip': '000000',
                 'private_email': 'parikshitapaunikar@gmail.com', 'corporate_email': 'parikshit.paunikar@justo.co.in',
                 'work_email': 'parikshit.paunikar@justo.co.in', 'mobile': '7387645299', 'marital': 'single',
                 'emergency_contact': '00000000', 'active_status': True, 'ctc': 45360.0, 'location': 'Pune',
                 'barcode': 'JUS0369'},
                {'id': 70, 'name': 'Pinank Salunkhe', 'pan_number': 'DDYPS3497H', 'job_title': 'Senior Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1992, 7, 24),
                 'department_id': 5, 'parent_id': 251, 'gender': 'male', 'joining_date': datetime.date(2021, 7, 1),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'salunkepinank@gmail.com',
                 'corporate_email': 'pinank.salunke@justo.co.in', 'work_email': 'pinank.salunke@justo.co.in',
                 'mobile': '9767578776', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 74779.0, 'location': 'Pune', 'barcode': 'JUS0302'},
                {'id': 218, 'name': 'Piyush Bagarecha', 'pan_number': 'BKVPB3346J', 'job_title': 'Senior Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1991, 1, 15),
                 'department_id': 2, 'parent_id': 1308, 'gender': 'male', 'joining_date': datetime.date(2022, 12, 15),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'sample3@sample.com',
                 'corporate_email': 'Piyush.Bagarecha@justo.co.in', 'work_email': 'Piyush.Bagarecha@justo.co.in',
                 'mobile': '9765094146', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 99779.0, 'location': 'Pune - ROM', 'barcode': 'JUS1000'},
                {'id': 558, 'name': 'Pooja Kumari', 'pan_number': '000000', 'job_title': 'Assistant Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1992, 7, 6),
                 'department_id': 2, 'parent_id': 389, 'gender': 'female', 'joining_date': datetime.date(2023, 7, 7),
                 'departure_date': datetime.date(2024, 4, 7), 'city': 'City', 'zip': '000000',
                 'private_email': 'poojanagele7@gmail.com', 'corporate_email': 'pooja.kumari@justo.co.in',
                 'work_email': 'pooja.kumari@justo.co.in', 'mobile': '00000000', 'marital': 'single',
                 'emergency_contact': '00000000', 'active_status': True, 'ctc': 45000.0, 'location': 'Pune',
                 'barcode': 'P0469'},
                {'id': 1866, 'name': 'Pradipta Nayak', 'pan_number': 'AJAPN3135G', 'job_title': 'Senior Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(2000, 1, 1),
                 'department_id': 2, 'parent_id': 979, 'gender': 'male', 'joining_date': datetime.date(2024, 7, 24),
                 'departure_date': None, 'city': 'Nayagarh', 'zip': '750268',
                 'private_email': 'pradipta.knayak3@gmail.com', 'corporate_email': 'pradipta.nayak@justo.co.in',
                 'work_email': 'pradipta.nayak@justo.co.in', 'mobile': '7738428451', 'marital': 'married',
                 'emergency_contact': '8917506073', 'active_status': True, 'ctc': 100000.0,
                 'location': 'Mumbai Western', 'barcode': 'JUS679'},
                {'id': 207, 'name': 'Pradnyadip Wanjare', 'pan_number': 'AFNPW8834J', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1992, 9, 15),
                 'department_id': 2, 'parent_id': 225, 'gender': 'male', 'joining_date': datetime.date(2021, 9, 15),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'diprajpsw358@gmail.com',
                 'corporate_email': 'pradnyadip.wanjare@justo.co.in', 'work_email': 'pradnyadip.wanjare@justo.co.in',
                 'mobile': '7066353934', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 45779.0, 'location': 'Pune', 'barcode': 'JUS0409'},
                {'id': 385, 'name': 'Prajay Khale', 'pan_number': 'BEKPK7402P',
                 'job_title': 'Assistant General Manager', 'mobile_phone': '000000000', 'work_phone': '000000',
                 'birthday': datetime.date(1990, 8, 30), 'department_id': 2, 'parent_id': 12, 'gender': 'male',
                 'joining_date': datetime.date(2021, 11, 22), 'departure_date': None, 'city': 'City', 'zip': '000000',
                 'private_email': 'prajay.khale@justo.co.in', 'corporate_email': 'prajay.khale@justo.co.in',
                 'work_email': 'prajay.khale@justo.co.in', 'mobile': '8007734400', 'marital': 'single',
                 'emergency_contact': '00000000', 'active_status': True, 'ctc': 85948.0, 'location': 'Pune',
                 'barcode': 'JUS0505'},
                {'id': 1732, 'name': 'Prasad  Pramod  Palande', 'pan_number': '000000',
                 'job_title': 'Assistant General Manager', 'mobile_phone': '000000000', 'work_phone': '000000',
                 'birthday': datetime.date(1994, 1, 15), 'department_id': 2, 'parent_id': 75, 'gender': 'male',
                 'joining_date': datetime.date(2024, 5, 28), 'departure_date': None, 'city': 'City', 'zip': '000000',
                 'private_email': 'prasadpalande789@gmail.com', 'corporate_email': 'prasad.palande@justo.co.in',
                 'work_email': 'prasad.palande@justo.co.in', 'mobile': '00000000', 'marital': 'single',
                 'emergency_contact': '00000000', 'active_status': True, 'ctc': 120834.0, 'location': 'Pune',
                 'barcode': 'JUS608'},
                {'id': 1163, 'name': 'Pranav Umesh Samant', 'pan_number': 'CLAPS4912A',
                 'job_title': 'Assistant General Manager', 'mobile_phone': '000000000', 'work_phone': '000000',
                 'birthday': datetime.date(1985, 7, 17), 'department_id': 2, 'parent_id': 1902, 'gender': 'male',
                 'joining_date': datetime.date(2024, 5, 2), 'departure_date': None, 'city': 'Old Panvel',
                 'zip': '410206', 'private_email': 'pranav8008@yahoo.com',
                 'corporate_email': 'pranav.samant@justo.co.in', 'work_email': 'pranav.samant@justo.co.in',
                 'mobile': '7678091636', 'marital': 'married', 'emergency_contact': '9664242399', 'active_status': True,
                 'ctc': 133333.0, 'location': 'Navi Mumbai', 'barcode': 'JUS595'},
                {'id': 448, 'name': 'Pratikshya Das', 'pan_number': 'GORPD4118H', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1996, 6, 20),
                 'department_id': 2, 'parent_id': 721, 'gender': 'female', 'joining_date': datetime.date(2022, 11, 7),
                 'departure_date': None, 'city': 'Bhubaneswar', 'zip': '751010',
                 'private_email': 'daspratikshya1999@gmail.com', 'corporate_email': 'pratikshya.das@justo.co.in',
                 'work_email': 'pratikshya.das@justo.co.in', 'mobile': '7978415840', 'marital': 'single',
                 'emergency_contact': '00000000', 'active_status': True, 'ctc': 48800.0,
                 'location': 'BBSR Regional Office', 'barcode': 'JUS0971'},
                {'id': 285, 'name': 'Prashant Tiwari', 'pan_number': 'BAZPT3197H', 'job_title': 'Assistant Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1995, 4, 5),
                 'department_id': 2, 'parent_id': 1593, 'gender': 'male', 'joining_date': datetime.date(2022, 12, 21),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'sample3@sample.com',
                 'corporate_email': 'Prashant.Tiwari@justo.co.in', 'work_email': 'Prashant.Tiwari@justo.co.in',
                 'mobile': '7744896886', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 44779.0, 'location': 'Pune', 'barcode': 'JUS1006'},
                {'id': 334, 'name': 'Praveen Kumar', 'pan_number': 'CBCPK7715B', 'job_title': 'Assistant Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1990, 9, 13),
                 'department_id': 2, 'parent_id': 56, 'gender': 'male', 'joining_date': datetime.date(2022, 10, 6),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'praveen.pk3466@gmail.com',
                 'corporate_email': 'praveen.kumar@justo.co.in', 'work_email': 'praveen.kumar@justo.co.in',
                 'mobile': '9168168763', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 46800.0, 'location': 'Pune', 'barcode': 'JUS0940'},
                {'id': 1800, 'name': 'Praveen Padmakar Apte', 'pan_number': 'ADDPA4475F', 'job_title': 'DIrector',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1972, 1, 8),
                 'department_id': 2, 'parent_id': 720, 'gender': 'male', 'joining_date': datetime.date(2024, 6, 18),
                 'departure_date': None, 'city': 'Pune', 'zip': '411028', 'private_email': 'praveenapte@gmail.com',
                 'corporate_email': 'praveen.apte@justo.co.in', 'work_email': 'praveen.apte@justo.co.in',
                 'mobile': '9960030003', 'marital': 'married', 'emergency_contact': '9970184772', 'active_status': True,
                 'ctc': 576250.0, 'location': 'Pune', 'barcode': 'JUS637'},
                {'id': 839, 'name': 'Prateek Singh', 'pan_number': '000000', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1993, 12, 31),
                 'department_id': 2, 'parent_id': 887, 'gender': 'male', 'joining_date': datetime.date(2022, 9, 21),
                 'departure_date': datetime.date(2024, 5, 18), 'city': 'City', 'zip': '000000',
                 'private_email': 'sample3@sample.com', 'corporate_email': 'prateek.singh@justo.co.in',
                 'work_email': 'prateek.singh@justo.co.in', 'mobile': '9755181388', 'marital': 'single',
                 'emergency_contact': '00000000', 'active_status': True, 'ctc': 67275.0, 'location': 'Pune',
                 'barcode': 'JUS0912'},
                {'id': 212, 'name': 'Pratik Jejurikar', 'pan_number': '000000', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1999, 3, 26),
                 'department_id': 2, 'parent_id': 451, 'gender': 'male', 'joining_date': datetime.date(2022, 11, 10),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'sample3@sample.com',
                 'corporate_email': 'pratik.jejurikar@justo.co.in', 'work_email': 'pratik.jejurikar@justo.co.in',
                 'mobile': '9309771179', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 59779.0, 'location': 'Pune', 'barcode': 'JUS0973'},
                {'id': 1309, 'name': 'Pratik Shroff', 'pan_number': 'GFCPS3203G', 'job_title': 'Senior Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1997, 5, 16),
                 'department_id': 2, 'parent_id': 243, 'gender': 'male', 'joining_date': datetime.date(2024, 5, 11),
                 'departure_date': None, 'city': 'Mumbai', 'zip': '400074', 'private_email': 'shroffpratik16@gmail.com',
                 'corporate_email': 'pratik.shroff@justo.co.in', 'work_email': 'pratik.shroff@justo.co.in',
                 'mobile': '7021885945', 'marital': 'single', 'emergency_contact': '8976489680', 'active_status': True,
                 'ctc': 120467.0, 'location': 'Mumbai Western', 'barcode': 'JUS599'},
                {'id': 658, 'name': 'Priyanka Bhadkwad', 'pan_number': 'AXVPB6544L',
                 'job_title': 'Assistant General Manager', 'mobile_phone': '000000000', 'work_phone': '000000',
                 'birthday': datetime.date(1990, 2, 5), 'department_id': 7, 'parent_id': 648, 'gender': 'female',
                 'joining_date': datetime.date(2021, 7, 21), 'departure_date': datetime.date(2024, 6, 19),
                 'city': 'City', 'zip': '000000', 'private_email': 'piyu5290@gmail.com',
                 'corporate_email': 'priyanka.bhadkwad@justo.co.in', 'work_email': 'priyanka.bhadkwad@justo.co.in',
                 'mobile': '9069069699', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 86250.0, 'location': 'Regional Office _ Pune', 'barcode': 'JUS0329'},
                {'id': 632, 'name': 'Pritesh Poojary', 'pan_number': 'ASCPP7494H',
                 'job_title': 'Assistant General Manager', 'mobile_phone': '9167770663', 'work_phone': '000000',
                 'birthday': datetime.date(1984, 2, 28), 'department_id': 10, 'parent_id': 855, 'gender': 'male',
                 'joining_date': datetime.date(2023, 9, 5), 'departure_date': None, 'city': 'City', 'zip': '000000',
                 'private_email': 'poojary_pritesh@hotmail.com', 'corporate_email': 'sample3@sample.com',
                 'work_email': 'sample3@sample.com', 'mobile': '00000000', 'marital': 'married',
                 'emergency_contact': '00000000', 'active_status': True, 'ctc': 150000.0, 'location': 'Thane',
                 'barcode': 'M0713'},
                {'id': 899, 'name': 'Priyanka  Masram', 'pan_number': 'DLRPM8892P', 'job_title': 'Assistant Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1991, 4, 26),
                 'department_id': 2, 'parent_id': 896, 'gender': 'male', 'joining_date': datetime.date(2024, 1, 15),
                 'departure_date': datetime.date(2024, 4, 17), 'city': 'Pune', 'zip': '411027',
                 'private_email': 'priyankamasram0@gmail.com', 'corporate_email': 'priyanka.masram@justo.co.in',
                 'work_email': 'priyanka.masram@justo.co.in', 'mobile': '9595180379', 'marital': 'married',
                 'emergency_contact': '9860008449', 'active_status': True, 'ctc': 53800.0, 'location': 'Pune',
                 'barcode': 'P0529'},
                {'id': 957, 'name': 'Raees  Abdul Razzak Aga', 'pan_number': 'ALMPA7511R', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1989, 1, 27),
                 'department_id': 2, 'parent_id': 100, 'gender': 'male', 'joining_date': datetime.date(2023, 12, 4),
                 'departure_date': datetime.date(2024, 5, 8), 'city': 'City', 'zip': '000000',
                 'private_email': 'manageraees@gmail.com', 'corporate_email': 'Agaraees.razzak@justo.co.in',
                 'work_email': 'Agaraees.razzak@justo.co.in', 'mobile': '9082424377', 'marital': 'married',
                 'emergency_contact': '9984800748', 'active_status': True, 'ctc': 50000.0, 'location': 'Navi Mumbai',
                 'barcode': 'M0743'},
                {'id': 1828, 'name': 'Purva  Dilip Lipare', 'pan_number': 'AQXPL2711Q',
                 'job_title': 'Assistant Manager', 'mobile_phone': '000000000', 'work_phone': '000000',
                 'birthday': datetime.date(1998, 6, 24), 'department_id': 14, 'parent_id': 626, 'gender': 'female',
                 'joining_date': datetime.date(2024, 7, 1), 'departure_date': None, 'city': 'une', 'zip': '411051',
                 'private_email': 'purva.lipare98@gmail.com', 'corporate_email': 'purva.lipare@justo.co.in',
                 'work_email': 'purva.lipare@justo.co.in', 'mobile': '9403845087', 'marital': 'single',
                 'emergency_contact': '9511700262', 'active_status': True, 'ctc': 25000.0, 'location': 'Pune',
                 'barcode': 'JUS662'},
                {'id': 492, 'name': 'Priyanka Hole', 'pan_number': 'AMZPH2994R', 'job_title': 'Assistant Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1995, 2, 18),
                 'department_id': 2, 'parent_id': 388, 'gender': 'female', 'joining_date': datetime.date(2021, 5, 21),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'priyahole007@gmail.com',
                 'corporate_email': 'priyanka.hole@justo.co.in', 'work_email': 'priyanka.hole@justo.co.in',
                 'mobile': '9588692729', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 0.0, 'location': 'Pune', 'barcode': 'JUS0259'},
                {'id': 710, 'name': 'Rahul Pande', 'pan_number': '000000', 'job_title': 'Director',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1969, 3, 12),
                 'department_id': 21, 'parent_id': None, 'gender': 'male', 'joining_date': datetime.date(2012, 8, 1),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'sample3@sample.com',
                 'corporate_email': 'rahul@justo.co.in', 'work_email': 'rahul@justo.co.in', 'mobile': '00000000',
                 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True, 'ctc': 0.0,
                 'location': 'Mumbai - HO', 'barcode': 'MGM002'},
                {'id': 646, 'name': 'Rahul Patil', 'pan_number': 'AYAPP5791R', 'job_title': 'Senior Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1988, 11, 4),
                 'department_id': 17, 'parent_id': 696, 'gender': 'male', 'joining_date': datetime.date(2022, 9, 5),
                 'departure_date': None, 'city': 'Pune', 'zip': '411047', 'private_email': 'rrahul.patil5262@gmail.com',
                 'corporate_email': 'rahul.patil@justo.co.in', 'work_email': 'rahul.patil@justo.co.in',
                 'mobile': '7558680903', 'marital': 'married', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 84779.0, 'location': 'Regional Office _ Pune', 'barcode': 'JUS0884'},
                {'id': 1134, 'name': 'Ram Deva Sharma', 'pan_number': 'OWMPS0143E', 'job_title': 'Assistant Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(2002, 2, 24),
                 'department_id': 2, 'parent_id': 381, 'gender': 'male', 'joining_date': datetime.date(2024, 4, 23),
                 'departure_date': datetime.date(2024, 7, 17), 'city': 'akola', 'zip': '444001',
                 'private_email': 'Ramdsharma2024@gmail.com', 'corporate_email': 'Ram.Sharma@justo.co.in',
                 'work_email': 'Ram.Sharma@justo.co.in', 'mobile': '7385060159', 'marital': 'single',
                 'emergency_contact': '9823352387', 'active_status': True, 'ctc': 35800.0, 'location': 'Pune',
                 'barcode': 'JUS1514'},
                {'id': 1902, 'name': 'Rajesh Roy', 'pan_number': 'AMZPR4506K', 'job_title': 'Assistant Vice President',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1986, 8, 9),
                 'department_id': 2, 'parent_id': 720, 'gender': 'male', 'joining_date': datetime.date(2024, 8, 10),
                 'departure_date': None, 'city': 'Navi Mumbai', 'zip': '410210',
                 'private_email': 'rajeshrroy@gmail.com', 'corporate_email': 'rajesh.roy@justo.co.in',
                 'work_email': 'rajesh.roy@justo.co.in', 'mobile': '8879030434', 'marital': 'married',
                 'emergency_contact': '7410152997', 'active_status': True, 'ctc': 750000.0, 'location': 'Navi Mumbai ',
                 'barcode': 'JUS694'},
                {'id': 1907, 'name': 'Rajesh Sushil  Jha', 'pan_number': 'AHZPJ9481A', 'job_title': 'Senior Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1985, 8, 23),
                 'department_id': 2, 'parent_id': 436, 'gender': 'male', 'joining_date': datetime.date(2024, 8, 23),
                 'departure_date': None, 'city': 'Mumbai ', 'zip': '421605', 'private_email': 'rajeshjha1985@gmail.com',
                 'corporate_email': 'rajesh.jha@justo.co.in', 'work_email': 'rajesh.jha@justo.co.in',
                 'mobile': '7718912512', 'marital': 'married', 'emergency_contact': '7498291210', 'active_status': True,
                 'ctc': 95833.0, 'location': 'Navi Mumbai', 'barcode': 'JUS700'},
                {'id': 1874, 'name': 'Rajeshwar Abhijeet  Patil', 'pan_number': 'ENSPP9034C', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(2000, 4, 12),
                 'department_id': 2, 'parent_id': 1461, 'gender': 'male', 'joining_date': datetime.date(2024, 7, 25),
                 'departure_date': None, 'city': 'Pune', 'zip': '411028',
                 'private_email': 'rajeshwarpatil200@gmail.com', 'corporate_email': 'rajeshwar.patil@justo.co.in',
                 'work_email': 'rajeshwar.patil@justo.co.in', 'mobile': '9172626354', 'marital': 'single',
                 'emergency_contact': '9172145237', 'active_status': True, 'ctc': 63800.0, 'location': 'Pune',
                 'barcode': 'JUS680'},
                {'id': 322, 'name': 'Ranjan Sengupta', 'pan_number': 'AENPS3400H', 'job_title': 'General Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1966, 5, 7),
                 'department_id': 18, 'parent_id': 780, 'gender': 'male', 'joining_date': datetime.date(2021, 8, 2),
                 'departure_date': None, 'city': 'City', 'zip': '000000',
                 'private_email': 'ranjan.sengupta07@gmail.com', 'corporate_email': 'ranjan.sengupta@justo.co.in',
                 'work_email': 'ranjan.sengupta@justo.co.in', 'mobile': '7400079568', 'marital': 'single',
                 'emergency_contact': '00000000', 'active_status': True, 'ctc': 238425.0, 'location': 'Mumbai - HO',
                 'barcode': 'JUS0343'},
                {'id': 1048, 'name': 'Reshu Mansharam Kanojiya', 'pan_number': 'EEAPK9539A',
                 'job_title': 'Assistant Manager', 'mobile_phone': '000000000', 'work_phone': '000000',
                 'birthday': datetime.date(1997, 9, 21), 'department_id': 2, 'parent_id': 885, 'gender': 'male',
                 'joining_date': datetime.date(2024, 2, 26), 'departure_date': None, 'city': 'Mumbai', 'zip': '400052',
                 'private_email': 'reshukanojiya@gmail.com', 'corporate_email': 'reshu.kanojiya@justo.co.in',
                 'work_email': 'reshu.kanojiya@justo.co.in', 'mobile': '9819176268', 'marital': 'single',
                 'emergency_contact': '7208271737', 'active_status': True, 'ctc': 54166.0, 'location': 'SoBo',
                 'barcode': 'M0783'},
                {'id': 1844, 'name': 'Ravi Ranjan ', 'pan_number': 'BBAPR4151F', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1993, 11, 28),
                 'department_id': 2, 'parent_id': 56, 'gender': 'male', 'joining_date': datetime.date(2024, 7, 15),
                 'departure_date': None, 'city': 'Pune', 'zip': '411024', 'private_email': 'ravi28nov1993@gmail.com',
                 'corporate_email': 'ravi.ranjan@justo.co.in', 'work_email': 'ravi.ranjan@justo.co.in',
                 'mobile': '7798396765', 'marital': 'single', 'emergency_contact': '8669598456', 'active_status': True,
                 'ctc': 43800.0, 'location': 'Pune', 'barcode': 'JUS675'},
                {'id': 441, 'name': 'Rishi Sharma', 'pan_number': 'DFJPS8488M',
                 'job_title': 'Assistant General Manager', 'mobile_phone': '000000000', 'work_phone': '000000',
                 'birthday': datetime.date(1989, 7, 22), 'department_id': 2, 'parent_id': 1902, 'gender': 'male',
                 'joining_date': datetime.date(2021, 9, 6), 'departure_date': None, 'city': 'City', 'zip': '000000',
                 'private_email': 'rishisharma11165@yahoo.com', 'corporate_email': 'rishi.sharma@justo.co.in',
                 'work_email': 'rishi.sharma@justo.co.in', 'mobile': '9137003647', 'marital': 'single',
                 'emergency_contact': '00000000', 'active_status': True, 'ctc': 145173.0, 'location': 'Navi Mumbai',
                 'barcode': 'JUS0398'},
                {'id': 1436, 'name': 'Ravina Kumari', 'pan_number': 'EPKPK7772C', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1997, 11, 12),
                 'department_id': 2, 'parent_id': 450, 'gender': 'female', 'joining_date': datetime.date(2023, 1, 6),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'ravinarai1997@gmail.com',
                 'corporate_email': 'ravina.kumari@justo.co.in', 'work_email': 'ravina.kumari@justo.co.in',
                 'mobile': '7304010064', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 49779.0, 'location': 'Pune', 'barcode': 'JUS1336'},
                {'id': 447, 'name': 'Rizwan Shaikh', 'pan_number': 'EMXPS4509F',
                 'job_title': 'Assistant General Manager', 'mobile_phone': '000000000', 'work_phone': '000000',
                 'birthday': datetime.date(1993, 7, 21), 'department_id': 2, 'parent_id': 576, 'gender': 'male',
                 'joining_date': datetime.date(2020, 3, 11), 'departure_date': None, 'city': 'City', 'zip': '000000',
                 'private_email': 'rizwan.shaikh.211993@gmail.com', 'corporate_email': 'rizwan.shaikh@justo.co.in',
                 'work_email': 'rizwan.shaikh@justo.co.in', 'mobile': '9028812183', 'marital': 'single',
                 'emergency_contact': '00000000', 'active_status': True, 'ctc': 99698.0, 'location': 'Pune',
                 'barcode': 'JUS0101'},
                {'id': 1934, 'name': 'Robert Lobo', 'pan_number': '000000', 'job_title': 'Consultant',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(2000, 1, 1),
                 'department_id': 17, 'parent_id': 6, 'gender': 'male', 'joining_date': datetime.date(2024, 9, 11),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'a@gmai.com',
                 'corporate_email': 'robert.lobo@justo.co.in', 'work_email': 'robert.lobo@justo.co.in',
                 'mobile': '00000000', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 20000.0, 'location': 'Mumbai - HO', 'barcode': 'JC000'},
                {'id': 927, 'name': 'Ritu Bhanushali', 'pan_number': 'EBGPB0341J', 'job_title': 'GRE',
                 'mobile_phone': '8286861950', 'work_phone': '000000', 'birthday': datetime.date(2000, 7, 9),
                 'department_id': 11, 'parent_id': 741, 'gender': 'female', 'joining_date': datetime.date(2023, 11, 17),
                 'departure_date': None, 'city': 'City', 'zip': '000000',
                 'private_email': 'ritubhanushali8286861950@gmail.com',
                 'corporate_email': 'ritu.bhanushali@justo.co.in', 'work_email': 'ritu.bhanushali@justo.co.in',
                 'mobile': '00000000', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 28481.0, 'location': 'KDMC', 'barcode': 'M0734'},
                {'id': 621, 'name': 'Rohit Uttekar', 'pan_number': 'AIUPU4410G', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1997, 7, 20),
                 'department_id': 2, 'parent_id': 407, 'gender': 'male', 'joining_date': datetime.date(2022, 4, 29),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'sample3@sample.com',
                 'corporate_email': 'rohit.uttekar@justo.co.in', 'work_email': 'rohit.uttekar@justo.co.in',
                 'mobile': '8412992797', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 60041.0, 'location': 'Pune', 'barcode': 'P0257'},
                {'id': 900, 'name': 'Rohit Sharma', 'pan_number': 'DQGPS0753F', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1992, 6, 26),
                 'department_id': 2, 'parent_id': 896, 'gender': 'male', 'joining_date': datetime.date(2024, 1, 22),
                 'departure_date': None, 'city': 'Pune', 'zip': '411057',
                 'private_email': 'rohitsharma.info25@gmail.com', 'corporate_email': 'rohit.sharma@justo.co.in',
                 'work_email': 'rohit.sharma@justo.co.in', 'mobile': '9766253289', 'marital': 'single',
                 'emergency_contact': '9730537571', 'active_status': True, 'ctc': 58800.0, 'location': 'Pune',
                 'barcode': 'P0539'},
                {'id': 1849, 'name': 'Rohit Kanojia', 'pan_number': 'CBMPK8466M', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1997, 1, 28),
                 'department_id': 2, 'parent_id': 1043, 'gender': 'male', 'joining_date': datetime.date(2024, 7, 18),
                 'departure_date': datetime.date(2024, 10, 19), 'city': 'Mumbai', 'zip': '400101',
                 'private_email': 'ikanojiarohit@gmail.com', 'corporate_email': 'rohit.kanojia@justo.co.in',
                 'work_email': 'rohit.kanojia@justo.co.in', 'mobile': '9820680343', 'marital': 'single',
                 'emergency_contact': '9820031426', 'active_status': False, 'ctc': 66666.0,
                 'location': 'Mumbai Western', 'barcode': 'JUS676'},
                {'id': 101, 'name': 'Roshni Chawla', 'pan_number': 'BPDPC9248D', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1997, 9, 26),
                 'department_id': 5, 'parent_id': 244, 'gender': 'female', 'joining_date': datetime.date(2021, 10, 17),
                 'departure_date': datetime.date(2024, 10, 14), 'city': 'Mumbai', 'zip': '000000',
                 'private_email': 'chawlarosshni26@gmail.com', 'corporate_email': 'roshni.chawla@justo.co.in',
                 'work_email': 'roshni.chawla@justo.co.in', 'mobile': '8421429919', 'marital': 'single',
                 'emergency_contact': '00000000', 'active_status': False, 'ctc': 53196.0, 'location': 'KDMC',
                 'barcode': 'JUS0446'},
                {'id': 291, 'name': 'Rupesh Jadhav', 'pan_number': 'ALOPJ0680N', 'job_title': 'Assistant Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1981, 5, 29),
                 'department_id': 2, 'parent_id': 834, 'gender': 'male', 'joining_date': datetime.date(2022, 9, 26),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'jadhavrupesh226@gmail.com',
                 'corporate_email': 'rupesh.jadhav@justo.co.in', 'work_email': 'rupesh.jadhav@justo.co.in',
                 'mobile': '8369094835', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 35020.0, 'location': 'KDMC', 'barcode': 'M0565'},
                {'id': 992, 'name': 'Rupesh Katakdhond', 'pan_number': 'AUNPK0228K', 'job_title': 'Assistant Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1979, 9, 12),
                 'department_id': 2, 'parent_id': 896, 'gender': 'male', 'joining_date': datetime.date(2024, 1, 8),
                 'departure_date': datetime.date(2024, 2, 1), 'city': 'Pune', 'zip': '411027',
                 'private_email': 'katakdhondrupesh@gmail.com', 'corporate_email': 'rupesh.katakdhond@justo.co.in',
                 'work_email': 'rupesh.katakdhond@justo.co.in', 'mobile': '9607209340', 'marital': 'married',
                 'emergency_contact': '7262039230', 'active_status': True, 'ctc': 31250.0, 'location': 'Pune',
                 'barcode': 'P0515'},
                {'id': 1884, 'name': 'Sabiya Liyakat  Mulani', 'pan_number': 'BGOPM2547K', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1995, 12, 7),
                 'department_id': 5, 'parent_id': 218, 'gender': 'female', 'joining_date': datetime.date(2024, 8, 1),
                 'departure_date': None, 'city': 'Nashik', 'zip': '422101',
                 'private_email': 'sabiya1995mulani@gmail.com', 'corporate_email': 'sabiya.mulani@justo.co.in',
                 'work_email': 'sabiya.mulani@justo.co.in', 'mobile': '9552796519', 'marital': 'married',
                 'emergency_contact': '9579053160', 'active_status': True, 'ctc': 40000.0, 'location': 'Pune',
                 'barcode': 'JUS683'},
                {'id': 1231, 'name': 'Sagar  Molake', 'pan_number': 'BQXPM3783N', 'job_title': 'Executive',
                 'mobile_phone': '8082042196', 'work_phone': '000000', 'birthday': datetime.date(1993, 11, 26),
                 'department_id': 14, 'parent_id': 933, 'gender': 'male', 'joining_date': datetime.date(2022, 8, 12),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'sagarmolake@gmail.com',
                 'corporate_email': 'sagar.molake@justo.co.in', 'work_email': 'sagar.molake@justo.co.in',
                 'mobile': '00000000', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 20000.0, 'location': 'Regional Office_Mumbai', 'barcode': 'JC0005'},
                {'id': 863, 'name': 'Sachin Vilas Shinde', 'pan_number': 'BKMPS4106E', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1980, 2, 1),
                 'department_id': 2, 'parent_id': 100, 'gender': 'male', 'joining_date': datetime.date(2023, 12, 4),
                 'departure_date': datetime.date(2024, 4, 11), 'city': 'Navi Mumbai', 'zip': '410210',
                 'private_email': 'sachinformeet@gmail.com', 'corporate_email': 'sachin.shinde@justo.co.in',
                 'work_email': 'sachin.shinde@justo.co.in', 'mobile': '9920424479', 'marital': 'married',
                 'emergency_contact': '9920424479', 'active_status': True, 'ctc': 63750.0, 'location': 'Navi Mumbai',
                 'barcode': 'M0741'},
                {'id': 1816, 'name': 'Sachin Sohanlal  Vaishnav', 'pan_number': 'AJZPV8858P', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1991, 8, 26),
                 'department_id': 2, 'parent_id': 1810, 'gender': 'male', 'joining_date': datetime.date(2024, 7, 10),
                 'departure_date': None, 'city': 'Navi Mumbai ', 'zip': '400706',
                 'private_email': 'sachinvaishnav000@gmail.com', 'corporate_email': 'sachin.vaishnav@justo.co.in',
                 'work_email': 'sachin.vaishnav@justo.co.in', 'mobile': '7738405960', 'marital': 'single',
                 'emergency_contact': '9920826328', 'active_status': True, 'ctc': 68250.0, 'location': 'Navi Mumbai',
                 'barcode': 'JUS673'},
                {'id': 1783, 'name': 'SHUBHAM CHAUDHARY', 'pan_number': 'AZMPC8116A', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1995, 2, 4),
                 'department_id': 2, 'parent_id': 381, 'gender': 'male', 'joining_date': datetime.date(2024, 6, 20),
                 'departure_date': None, 'city': 'Bhind ', 'zip': '477441', 'private_email': 'shubh.23sep@gmail.com',
                 'corporate_email': 'shubham.chaudhary@justo.co.in', 'work_email': 'shubham.chaudhary@justo.co.in',
                 'mobile': '7441101640', 'marital': 'single', 'emergency_contact': '9098509738', 'active_status': True,
                 'ctc': 48800.0, 'location': 'Pune', 'barcode': 'JUS646'},
                {'id': 1520, 'name': 'Sadhana  Harshad  Jagdale', 'pan_number': 'ANLPD7655C',
                 'job_title': 'Assistant Manager', 'mobile_phone': '000000000', 'work_phone': '000000',
                 'birthday': datetime.date(1986, 12, 18), 'department_id': 2, 'parent_id': 426, 'gender': 'female',
                 'joining_date': datetime.date(2024, 6, 11), 'departure_date': datetime.date(2024, 10, 14),
                 'city': 'Navi Mumbai ', 'zip': '410218', 'private_email': 'jagdale.sadhana123456@gmail.com',
                 'corporate_email': 'sadhana.jagdale@justo.co.in', 'work_email': 'sadhana.jagdale@justo.co.in',
                 'mobile': '7021830509', 'marital': 'married', 'emergency_contact': '9594956059',
                 'active_status': False, 'ctc': 46800.0, 'location': 'Navi Mumbai', 'barcode': 'JUS621'},
                {'id': 950, 'name': 'Sahil Upadhyay', 'pan_number': '000000', 'job_title': 'Senior Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1997, 6, 29),
                 'department_id': 2, 'parent_id': 576, 'gender': 'male', 'joining_date': datetime.date(2024, 1, 3),
                 'departure_date': datetime.date(2024, 4, 2), 'city': 'City', 'zip': '000000',
                 'private_email': 'sahilupadhyay@live.com', 'corporate_email': 'sahil.upadhyay@justo.co.in',
                 'work_email': 'sahil.upadhyay@justo.co.in', 'mobile': '00000000', 'marital': 'single',
                 'emergency_contact': '00000000', 'active_status': True, 'ctc': 98750.0, 'location': 'Pune',
                 'barcode': 'P0512'},
                {'id': 57, 'name': 'Sagar Hundekari', 'pan_number': 'ACTPH8719E', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1989, 11, 18),
                 'department_id': 5, 'parent_id': 251, 'gender': 'male', 'joining_date': datetime.date(2021, 11, 8),
                 'departure_date': None, 'city': 'Pune', 'zip': '410507', 'private_email': 'sagarhundekari7@gmail.com',
                 'corporate_email': 'sagar.hundekari@justo.co.in', 'work_email': 'sagar.hundekari@justo.co.in',
                 'mobile': '9762908288', 'marital': 'married', 'emergency_contact': '9762139566', 'active_status': True,
                 'ctc': 49779.0, 'location': 'Pune', 'barcode': 'JUS0476'},
                {'id': 583, 'name': 'Sagarika Das', 'pan_number': 'BOLPD3829N', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1994, 12, 25),
                 'department_id': 2, 'parent_id': 385, 'gender': 'female', 'joining_date': datetime.date(2023, 1, 6),
                 'departure_date': None, 'city': 'TIinsukia', 'zip': '786125',
                 'private_email': 'sagarikadastsk25@gmail.com', 'corporate_email': 'sagarika.das@justo.co.in',
                 'work_email': 'sagarika.das@justo.co.in', 'mobile': '7002338196', 'marital': 'single',
                 'emergency_contact': '9309976342', 'active_status': True, 'ctc': 49779.0, 'location': 'Pune',
                 'barcode': 'JUS1028'},
                {'id': 1593, 'name': 'Sagar Waichole', 'pan_number': 'ABEPW9842K', 'job_title': 'Senior Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1990, 4, 7),
                 'department_id': 2, 'parent_id': 75, 'gender': 'male', 'joining_date': datetime.date(2023, 12, 26),
                 'departure_date': None, 'city': 'Pune', 'zip': '411061', 'private_email': 'sagarwaichole@gmail.com',
                 'corporate_email': 'sagar.waichole@justo.co.in', 'work_email': 'sagar.waichole@justo.co.in',
                 'mobile': '8329646859', 'marital': 'married', 'emergency_contact': '9146467764', 'active_status': True,
                 'ctc': 100000.0, 'location': 'Pune', 'barcode': 'JUS1330'},
                {'id': 841, 'name': 'Samrat Sarkar', 'pan_number': 'BUKPS7952N', 'job_title': 'General Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1984, 3, 14),
                 'department_id': 10, 'parent_id': 6, 'gender': 'male', 'joining_date': datetime.date(2021, 7, 24),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'sample3@sample.com',
                 'corporate_email': 'samrat.sarkar@justo.co.in', 'work_email': 'samrat.sarkar@justo.co.in',
                 'mobile': '9970802388', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 374370.0, 'location': 'Regional Office _ Pune', 'barcode': 'JUS0337'},
                {'id': 12, 'name': 'Sandeep Kulkarni', 'pan_number': 'AQTPK9462H', 'job_title': 'General Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1983, 8, 9),
                 'department_id': 2, 'parent_id': 1800, 'gender': 'male', 'joining_date': datetime.date(2020, 12, 21),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'sample3@sample.com',
                 'corporate_email': 'sandeep.kulkarni@justo.co.in', 'work_email': 'sandeep.kulkarni@justo.co.in',
                 'mobile': '7715035444', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 254371.0, 'location': 'Pune', 'barcode': 'JUS0186'},
                {'id': 1250, 'name': 'Sanjay  Raman  Chanda', 'pan_number': 'AMOPC2933J',
                 'job_title': 'Assistant General Manager', 'mobile_phone': '000000000', 'work_phone': '000000',
                 'birthday': datetime.date(1989, 10, 12), 'department_id': 7, 'parent_id': 918, 'gender': 'male',
                 'joining_date': datetime.date(2024, 5, 9), 'departure_date': None, 'city': 'Mumbai', 'zip': '400097',
                 'private_email': 'sanjay.chaanda@gmail.com', 'corporate_email': 'sanjay.chanda@justo.co.in',
                 'work_email': 'sanjay.chanda@justo.co.in', 'mobile': '8779339573', 'marital': 'married',
                 'emergency_contact': '8779396424', 'active_status': True, 'ctc': 133333.0,
                 'location': 'Regional Office_Mumbai', 'barcode': 'JUS597'},
                {'id': 1282, 'name': 'Santlal Hariprasad Kannojia', 'pan_number': 'BIJPK2159N', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1982, 6, 30),
                 'department_id': 2, 'parent_id': 1810, 'gender': 'male', 'joining_date': datetime.date(2023, 1, 5),
                 'departure_date': None, 'city': 'City', 'zip': '000000',
                 'private_email': 'sant_1kannojia@rediffmail.com', 'corporate_email': 'santlal.kannojia@justo.co.in',
                 'work_email': 'santlal.kannojia@justo.co.in', 'mobile': '9867586992', 'marital': 'single',
                 'emergency_contact': '00000000', 'active_status': True, 'ctc': 53575.0, 'location': 'Navi Mumbai',
                 'barcode': 'JUS1029'},
                {'id': 337, 'name': 'Sandesh Chavan', 'pan_number': 'AIQPC0204L', 'job_title': 'Deputy General Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1986, 2, 19),
                 'department_id': 2, 'parent_id': 6, 'gender': 'male', 'joining_date': datetime.date(2021, 6, 14),
                 'departure_date': None, 'city': 'Pune', 'zip': '411045', 'private_email': 'chavansandesh19@gmail.com',
                 'corporate_email': 'sandesh.chavan@justo.co.in', 'work_email': 'sandesh.chavan@justo.co.in',
                 'mobile': '9356870017', 'marital': 'married', 'emergency_contact': '9920670770', 'active_status': True,
                 'ctc': 207704.0, 'location': 'Pune', 'barcode': 'JUS0275'},
                {'id': 506, 'name': 'Santosh Ramchandra Kadam', 'pan_number': 'DBPPK9090F', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1985, 5, 14),
                 'department_id': 2, 'parent_id': 304, 'gender': 'male', 'joining_date': datetime.date(2023, 1, 6),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'sample3@sample.com',
                 'corporate_email': 'santosh.kadam@justo.co.in', 'work_email': 'santosh.kadam@justo.co.in',
                 'mobile': '9370428308', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 55757.0, 'location': 'Pune', 'barcode': 'JUS1030'},
                {'id': 691, 'name': 'Satej Lokhande', 'pan_number': 'AGPPL6791G', 'job_title': 'Assistant Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1983, 6, 30),
                 'department_id': 17, 'parent_id': 1902, 'gender': 'male', 'joining_date': datetime.date(2022, 5, 17),
                 'departure_date': None, 'city': 'City', 'zip': '000000',
                 'private_email': 'lokhande_satej@rediffmail.com', 'corporate_email': 'satej.lokhande@justo.co.in',
                 'work_email': 'satej.lokhande@justo.co.in', 'mobile': '9920398739', 'marital': 'single',
                 'emergency_contact': '00000000', 'active_status': True, 'ctc': 44340.0, 'location': 'Navi Mumbai',
                 'barcode': 'JUS0742'},
                {'id': 1586, 'name': 'Satyajeet  Tatysaheb  Nikam', 'pan_number': '000000',
                 'job_title': 'Senior Manager', 'mobile_phone': '000000000', 'work_phone': '000000',
                 'birthday': datetime.date(1987, 1, 29), 'department_id': 2, 'parent_id': 225, 'gender': 'male',
                 'joining_date': datetime.date(2024, 6, 11), 'departure_date': datetime.date(2024, 7, 10),
                 'city': 'City', 'zip': '000000', 'private_email': 'nikamsatyajeet9255@gmail.com',
                 'corporate_email': 'satyajeet.nikam@justo.co.in', 'work_email': 'satyajeet.nikam@justo.co.in',
                 'mobile': '00000000', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': False,
                 'ctc': 83334.0, 'location': 'Pune', 'barcode': 'JUS622'},
                {'id': 1053, 'name': 'Savio  Rego', 'pan_number': 'AJNPR6188E', 'job_title': 'General Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1973, 12, 19),
                 'department_id': 10, 'parent_id': 720, 'gender': 'male', 'joining_date': datetime.date(2024, 2, 29),
                 'departure_date': datetime.date(2024, 4, 8), 'city': 'Thane', 'zip': '400615',
                 'private_email': 'savio.rego@gmail.com', 'corporate_email': 'savio.rego@justo.co.in',
                 'work_email': 'savio.rego@justo.co.in', 'mobile': '9819399819', 'marital': 'married',
                 'emergency_contact': '9819321474', 'active_status': True, 'ctc': 166666.0, 'location': 'KDMC',
                 'barcode': 'M0786'},
                {'id': 1308, 'name': 'Sayan Chakraborty', 'pan_number': 'AHHPC1216E', 'job_title': 'General Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1983, 4, 6),
                 'department_id': 2, 'parent_id': 6, 'gender': 'male', 'joining_date': datetime.date(2024, 5, 10),
                 'departure_date': None, 'city': 'Pune', 'zip': '411057', 'private_email': 'sayanc3103@gmail.com',
                 'corporate_email': 'sayan.chakraborty@justo.co.in', 'work_email': 'sayan.chakraborty@justo.co.in',
                 'mobile': '7875406254', 'marital': 'married', 'emergency_contact': '9373977063', 'active_status': True,
                 'ctc': 250000.0, 'location': 'Pune', 'barcode': 'JUS598'},
                {'id': 133, 'name': 'Shahbaaz Khan', 'pan_number': 'DLKPK3657P', 'job_title': 'Senior Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1976, 4, 13),
                 'department_id': 2, 'parent_id': 1058, 'gender': 'male', 'joining_date': datetime.date(2022, 9, 15),
                 'departure_date': None, 'city': 'Thane', 'zip': '401107', 'private_email': 'nshahbaazkhan@gmail.com',
                 'corporate_email': 'shahbaaz.khan@justo.co.in', 'work_email': 'shahbaaz.khan@justo.co.in',
                 'mobile': '9892573283', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 74623.0, 'location': 'Mumbai Western', 'barcode': 'JUS0901'},
                {'id': 1605, 'name': 'Sharad  Pawar', 'pan_number': 'FEAPP5907J', 'job_title': 'Executive',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(2000, 6, 6),
                 'department_id': 2, 'parent_id': 319, 'gender': 'male', 'joining_date': datetime.date(2024, 1, 12),
                 'departure_date': datetime.date(2024, 5, 18), 'city': 'Pune', 'zip': '411045',
                 'private_email': 'sharadsp0007@gmail.com', 'corporate_email': 'sharad.pawar@justo.co.in',
                 'work_email': 'sharad.pawar@justo.co.in', 'mobile': '7448109313', 'marital': 'single',
                 'emergency_contact': '7219891020', 'active_status': True, 'ctc': 28800.0, 'location': 'Pune',
                 'barcode': 'JUS1355'},
                {'id': 595, 'name': 'Sharfuddin Rehmani', 'pan_number': 'BZZPR4967C', 'job_title': 'Assistant Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1997, 4, 2),
                 'department_id': 2, 'parent_id': 1474, 'gender': 'male', 'joining_date': datetime.date(2022, 9, 15),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'r.sharfuddin111@gmail.com',
                 'corporate_email': 'sharfuddin.rehmani@justo.co.in', 'work_email': 'sharfuddin.rehmani@justo.co.in',
                 'mobile': '9664866184', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 43680.0, 'location': 'Mumbai Western', 'barcode': 'M0551'},
                {'id': 1008, 'name': 'Shehzad Khan', 'pan_number': 'ALJPK0089K', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1988, 6, 23),
                 'department_id': 2, 'parent_id': 918, 'gender': 'male', 'joining_date': datetime.date(2024, 2, 1),
                 'departure_date': datetime.date(2024, 2, 1), 'city': 'Mumbai', 'zip': '400051',
                 'private_email': 'shehzad.sibermond@gmail.com', 'corporate_email': 'Shehzad.khan@justo.co.in',
                 'work_email': 'Shehzad.khan@justo.co.in', 'mobile': '9892942863', 'marital': 'single',
                 'emergency_contact': '72084821789', 'active_status': True, 'ctc': 0.0, 'location': 'SoBo',
                 'barcode': 'M0770'},
                {'id': 387, 'name': 'Shayad Sayyad', 'pan_number': 'LZYPS3232E', 'job_title': 'Assistant Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1998, 8, 13),
                 'department_id': 2, 'parent_id': 505, 'gender': 'male', 'joining_date': datetime.date(2022, 9, 21),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'shahidsayyad7620@gmail.com',
                 'corporate_email': 'shayad.sayyad@justo.co.in', 'work_email': 'shayad.sayyad@justo.co.in',
                 'mobile': '7057808637', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 39779.0, 'location': 'Pune', 'barcode': 'JUS0914'},
                {'id': 1748, 'name': 'Shivam Dinesh Gupta', 'pan_number': 'BXTPG7544L', 'job_title': 'Manager',
                 'mobile_phone': '8303140620', 'work_phone': '000000', 'birthday': datetime.date(1998, 10, 21),
                 'department_id': 2, 'parent_id': 1824, 'gender': 'male', 'joining_date': datetime.date(2024, 6, 13),
                 'departure_date': None, 'city': 'Deoria', 'zip': '274702', 'private_email': 'shivam.gupta@justo.co.in',
                 'corporate_email': 'shivam.gupta@justo.co.in', 'work_email': 'shivam.gupta@justo.co.in',
                 'mobile': '9960736346', 'marital': 'single', 'emergency_contact': '9665708565', 'active_status': True,
                 'ctc': 33800.0, 'location': 'Pune', 'barcode': 'JUS627'},
                {'id': 1834, 'name': 'Shreyash  Dilip Bangale', 'pan_number': 'CLMPB4239D', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1997, 12, 16),
                 'department_id': 2, 'parent_id': 993, 'gender': 'male', 'joining_date': datetime.date(2024, 7, 8),
                 'departure_date': None, 'city': 'Akola', 'zip': '444001', 'private_email': 'bangaleshreyash@gmail.com',
                 'corporate_email': 'shreyash.bangale@justo.co.in', 'work_email': 'shreyash.bangale@justo.co.in',
                 'mobile': '8308026714', 'marital': 'single', 'emergency_contact': '9096450811', 'active_status': True,
                 'ctc': 62000.0, 'location': 'Pune', 'barcode': 'JUS669'},
                {'id': 1400, 'name': 'Shweta Gavali', 'pan_number': '000000', 'job_title': 'Assistant Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1996, 5, 8),
                 'department_id': 2, 'parent_id': 304, 'gender': 'female', 'joining_date': datetime.date(2023, 7, 3),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'ShwetaGavali6@gmail.com',
                 'corporate_email': 'shweta.gawali@justo.co.in', 'work_email': 'shweta.gawali@justo.co.in',
                 'mobile': '00000000', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 40029.0, 'location': 'Pune', 'barcode': 'JUS1212'},
                {'id': 1740, 'name': 'Shreemant vasant Suryawanshi', 'pan_number': 'JEJPS5392B',
                 'job_title': 'Assistant Manager', 'mobile_phone': '000000000', 'work_phone': '000000',
                 'birthday': datetime.date(1997, 6, 24), 'department_id': 2, 'parent_id': 441, 'gender': 'male',
                 'joining_date': datetime.date(2024, 6, 3), 'departure_date': datetime.date(2024, 6, 6),
                 'city': 'Thane', 'zip': '400706', 'private_email': 'shreemant24@gmail.com',
                 'corporate_email': 'Shreemant.suryawanshi@justo.co.in',
                 'work_email': 'Shreemant.suryawanshi@justo.co.in', 'mobile': '9867745328', 'marital': 'single',
                 'emergency_contact': '9821851757', 'active_status': False, 'ctc': 35800.0, 'location': 'Navi Mumbai',
                 'barcode': 'JUS611'},
                {'id': 513, 'name': 'Shivali Shinde', 'pan_number': 'AFAPC0859E', 'job_title': 'Assistant Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1976, 6, 23),
                 'department_id': 5, 'parent_id': 251, 'gender': 'female', 'joining_date': datetime.date(2021, 1, 20),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'lalita.chaudhari@gmail.com',
                 'corporate_email': 'shivali.shinde@justo.co.in', 'work_email': 'shivali.shinde@justo.co.in',
                 'mobile': '8237438438', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 54623.0, 'location': 'Pune', 'barcode': 'JUS0213'},
                {'id': 7, 'name': 'Shrinivas Ugile', 'pan_number': 'AAMPU7434J',
                 'job_title': 'Assistant General Manager', 'mobile_phone': '000000000', 'work_phone': '000000',
                 'birthday': datetime.date(1976, 4, 11), 'department_id': 2, 'parent_id': 337, 'gender': 'male',
                 'joining_date': datetime.date(2020, 12, 11), 'departure_date': None, 'city': 'City', 'zip': '000000',
                 'private_email': 'sample3@sample.com', 'corporate_email': 'shrinivas.ugile@justo.co.in',
                 'work_email': 'shrinivas.ugile@justo.co.in', 'mobile': '9049898999', 'marital': 'single',
                 'emergency_contact': '00000000', 'active_status': True, 'ctc': 119484.0, 'location': 'Pune',
                 'barcode': 'JUS0178'},
                {'id': 304, 'name': 'Shriraj Patil', 'pan_number': 'DGYPP4973G', 'job_title': 'Senior Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1990, 5, 11),
                 'department_id': 2, 'parent_id': 75, 'gender': 'male', 'joining_date': datetime.date(2021, 5, 21),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'shriraj1105@gmail.com',
                 'corporate_email': 'shriraj.patil@justo.co.in', 'work_email': 'shriraj.patil@justo.co.in',
                 'mobile': '9665212921', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 91446.0, 'location': 'Pune', 'barcode': 'JUS0260'},
                {'id': 1781, 'name': 'Shubham Vijaysing  Patil', 'pan_number': 'FQCPP7993C',
                 'job_title': 'Assistant Manager', 'mobile_phone': '000000000', 'work_phone': '000000',
                 'birthday': datetime.date(1999, 1, 11), 'department_id': 2, 'parent_id': 887, 'gender': 'male',
                 'joining_date': datetime.date(2024, 6, 17), 'departure_date': None, 'city': 'Pune ', 'zip': '410509',
                 'private_email': 'sp509568@gmail.com', 'corporate_email': 'shubham.patil@justo.co.in',
                 'work_email': 'shubham.patil@justo.co.in', 'mobile': '9834751816', 'marital': 'single',
                 'emergency_contact': '8380043531', 'active_status': True, 'ctc': 45800.0, 'location': 'Pune',
                 'barcode': 'JUS640'},
                {'id': 92, 'name': 'Siddhant Ramesh  Gaikwad', 'pan_number': 'CDQPG2091G',
                 'job_title': 'Assistant Manager', 'mobile_phone': '000000000', 'work_phone': '000000',
                 'birthday': datetime.date(1999, 3, 28), 'department_id': 2, 'parent_id': 414, 'gender': 'male',
                 'joining_date': datetime.date(2022, 5, 28), 'departure_date': None, 'city': 'Thane', 'zip': '421503',
                 'private_email': 'Siddhantgaikwadsg820@gmail.com', 'corporate_email': 'siddhant.gaikwad@justo.co.in',
                 'work_email': 'siddhant.gaikwad@justo.co.in', 'mobile': '9834442506', 'marital': 'single',
                 'emergency_contact': '8788866495', 'active_status': True, 'ctc': 45833.0, 'location': 'KDMC',
                 'barcode': 'M0485'},
                {'id': 1824, 'name': 'Shubham Suresh Patil', 'pan_number': 'CTAPP3107Q',
                 'job_title': 'Assistant General Manager', 'mobile_phone': '000000000', 'work_phone': '000000',
                 'birthday': datetime.date(1996, 3, 29), 'department_id': 2, 'parent_id': 459, 'gender': 'male',
                 'joining_date': datetime.date(2024, 7, 1), 'departure_date': None, 'city': 'pune', 'zip': '412115',
                 'private_email': 'shubhamp857@gmail.com', 'corporate_email': 'shubhamsuresh.patil@justo.co.in',
                 'work_email': 'shubhamsuresh.patil@justo.co.in', 'mobile': '7350856937', 'marital': 'single',
                 'emergency_contact': '9890436789', 'active_status': True, 'ctc': 101083.0, 'location': 'Pune',
                 'barcode': 'JUS658'},
                {'id': 1801, 'name': 'Shubham Vijay  Rawalkar', 'pan_number': '000000', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1995, 4, 14),
                 'department_id': 2, 'parent_id': 1824, 'gender': 'male', 'joining_date': datetime.date(2024, 6, 13),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'rawalkarshubham@gmail.com',
                 'corporate_email': 'shubham.rawalkar@justo.co.in', 'work_email': 'shubham.rawalkar@justo.co.in',
                 'mobile': '00000000', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 35000.0, 'location': 'Pune', 'barcode': 'JUS633'},
                {'id': 1338, 'name': 'Shweta Kamble', 'pan_number': 'DPYPK8208C', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1995, 9, 13),
                 'department_id': 15, 'parent_id': 1798, 'gender': 'female', 'joining_date': datetime.date(2024, 1, 16),
                 'departure_date': None, 'city': 'mumbai', 'zip': '410210',
                 'private_email': 'shwetakamble226@gmail.com', 'corporate_email': 'shweta.kamble@justo.co.in',
                 'work_email': 'shweta.kamble@justo.co.in', 'mobile': '9324060148', 'marital': 'single',
                 'emergency_contact': '9819871332', 'active_status': True, 'ctc': 50000.0, 'location': 'Navi Mumbai ',
                 'barcode': 'JUS1370'},
                {'id': 1904, 'name': 'Shweta  Shinde', 'pan_number': 'GZZPS7259M', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1998, 7, 18),
                 'department_id': 2, 'parent_id': 741, 'gender': 'female', 'joining_date': datetime.date(2024, 8, 13),
                 'departure_date': None, 'city': 'Navi mumbai', 'zip': '410210',
                 'private_email': 'shwetashinde1807@gmail.com', 'corporate_email': 'Shweta.shinde@justo.co.in',
                 'work_email': 'Shweta.shinde@justo.co.in', 'mobile': '9321984386', 'marital': 'single',
                 'emergency_contact': '8433163708', 'active_status': True, 'ctc': 54166.0, 'location': 'Navi Mumbai ',
                 'barcode': 'JUS697'},
                {'id': 1686, 'name': 'Shweta  Bhardwaj', 'pan_number': 'CUQPB0547M', 'job_title': 'Senior Executive',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1995, 11, 25),
                 'department_id': 30, 'parent_id': None, 'gender': 'female', 'joining_date': datetime.date(2024, 4, 8),
                 'departure_date': None, 'city': 'Saharnpur', 'zip': '247341',
                 'private_email': 'csshwetabhardwaj@gmail.com', 'corporate_email': 'shweta.bhardwaj@justo.co.in',
                 'work_email': 'shweta.bhardwaj@justo.co.in', 'mobile': '9990100963', 'marital': 'single',
                 'emergency_contact': '9289715529', 'active_status': True, 'ctc': 45833.0, 'location': 'Mumbai - HO',
                 'barcode': 'JUS1488'},
                {'id': 1843, 'name': 'Smita Krishnakant  Kudale', 'pan_number': 'AIOPJ9331P', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1974, 9, 15),
                 'department_id': 2, 'parent_id': 896, 'gender': 'female', 'joining_date': datetime.date(2024, 7, 15),
                 'departure_date': None, 'city': 'Pune', 'zip': '411021', 'private_email': 'smita.jagtap15@gmail.com',
                 'corporate_email': 'smita.kudale@justo.co.in', 'work_email': 'smita.kudale@justo.co.in',
                 'mobile': '9545408008', 'marital': 'divorced', 'emergency_contact': '9545458528',
                 'active_status': True, 'ctc': 65000.0, 'location': 'Pune', 'barcode': 'JUS674'},
                {'id': 769, 'name': 'Sohan Sawariya', 'pan_number': 'PGLPS7854A', 'job_title': 'Assistant Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(2002, 7, 12),
                 'department_id': 2, 'parent_id': 848, 'gender': 'male', 'joining_date': datetime.date(2023, 7, 17),
                 'departure_date': datetime.date(2024, 5, 13), 'city': 'City', 'zip': '000000',
                 'private_email': 'sohansawariya1212@gmail.com', 'corporate_email': 'sohan.sawariya@justo.co.in',
                 'work_email': 'sohan.sawariya@justo.co.in', 'mobile': '00000000', 'marital': 'single',
                 'emergency_contact': '00000000', 'active_status': True, 'ctc': 32500.0, 'location': 'Thane',
                 'barcode': 'M0688'},
                {'id': 324, 'name': 'Sonam Thakur', 'pan_number': 'BNHPT2927E', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1995, 4, 25),
                 'department_id': 2, 'parent_id': 377, 'gender': 'female', 'joining_date': datetime.date(2021, 10, 11),
                 'departure_date': None, 'city': 'pune', 'zip': '411057', 'private_email': 'sona250495@gmail.com',
                 'corporate_email': 'sonam.thakur@justo.co.in', 'work_email': 'sonam.thakur@justo.co.in',
                 'mobile': '9022149234', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 59757.0, 'location': 'Pune', 'barcode': 'JUS0441'},
                {'id': 1700, 'name': 'Sonal  Vitthal Patil', 'pan_number': 'CSAPP3569F', 'job_title': 'Executive',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1995, 3, 13),
                 'department_id': 15, 'parent_id': None, 'gender': 'female', 'joining_date': datetime.date(2023, 8, 25),
                 'departure_date': None, 'city': 'pune', 'zip': '411021', 'private_email': 'patilsonal529@gmail.com',
                 'corporate_email': 'sonal.patil@justo.co.in', 'work_email': 'sonal.patil@justo.co.in',
                 'mobile': '7755964882', 'marital': 'single', 'emergency_contact': '9503848095', 'active_status': True,
                 'ctc': 31000.0, 'location': 'Regional Office _ Pune', 'barcode': 'JUS1264'},
                {'id': 460, 'name': 'Sourabh Ubale', 'pan_number': 'ABYPU3306J',
                 'job_title': 'Assistant General Manager', 'mobile_phone': '000000000', 'work_phone': '000000',
                 'birthday': datetime.date(1987, 8, 11), 'department_id': 5, 'parent_id': 251, 'gender': 'male',
                 'joining_date': datetime.date(2021, 4, 12), 'departure_date': None, 'city': 'City', 'zip': '000000',
                 'private_email': 'sample3@sample.com', 'corporate_email': 'sourabh.ubale@justo.co.in',
                 'work_email': 'sourabh.ubale@justo.co.in', 'mobile': '9168026161', 'marital': 'single',
                 'emergency_contact': '00000000', 'active_status': True, 'ctc': 94667.0, 'location': 'Pune',
                 'barcode': 'JUS0249'},
                {'id': 1143, 'name': 'Sunil Naik', 'pan_number': 'AMPPN2780F', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1983, 4, 14),
                 'department_id': 13, 'parent_id': 6, 'gender': 'male', 'joining_date': datetime.date(2020, 3, 16),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'suneelrnaik@gmail.com',
                 'corporate_email': 'sunil.naik@justo.co.in', 'work_email': 'sunil.naik@justo.co.in',
                 'mobile': '9011011599', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 74757.0, 'location': 'Regional Office _ Pune', 'barcode': 'JUS0104'},
                {'id': 251, 'name': 'Sunny John', 'pan_number': 'BFAPP0334J', 'job_title': 'Deputy General Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1984, 8, 29),
                 'department_id': 5, 'parent_id': 6, 'gender': 'male', 'joining_date': datetime.date(2021, 2, 17),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'sunny.john09@gmail.com',
                 'corporate_email': 'sunny.john@justo.co.in', 'work_email': 'sunny.john@justo.co.in',
                 'mobile': '9049103938', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 149667.0, 'location': 'Regional Office _ Pune', 'barcode': 'JUS0238'},
                {'id': 698, 'name': 'Sumit Dholey', 'pan_number': 'ANPPD6216P', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1988, 5, 2),
                 'department_id': 10, 'parent_id': 855, 'gender': 'male', 'joining_date': datetime.date(2022, 1, 3),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'd.sumit25@gmail.com',
                 'corporate_email': 'sumit.dholey@justo.co.in', 'work_email': 'sumit.dholey@justo.co.in',
                 'mobile': '9167513872', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 60000.0, 'location': 'KDMC', 'barcode': 'JUS0554'},
                {'id': 1741, 'name': 'Surajnath  Raju Upadhyay ', 'pan_number': 'AIBPU1464H', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1999, 11, 3),
                 'department_id': 2, 'parent_id': 1163, 'gender': 'male', 'joining_date': datetime.date(2024, 6, 5),
                 'departure_date': datetime.date(2024, 6, 6), 'city': 'Mumbai ', 'zip': '400074',
                 'private_email': 'surajupad16@gmail.com', 'corporate_email': 'surajnath.upadhyay@justo.co.in',
                 'work_email': 'surajnath.upadhyay@justo.co.in', 'mobile': '9769255674', 'marital': 'single',
                 'emergency_contact': '9167657370', 'active_status': True, 'ctc': 70833.0, 'location': 'Navi Mumbai',
                 'barcode': 'JUS618'},
                {'id': 1557, 'name': 'Susmita Janardan Chavan', 'pan_number': 'BAFPC5361L', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1995, 10, 23),
                 'department_id': 2, 'parent_id': None, 'gender': 'female', 'joining_date': datetime.date(2023, 7, 24),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'sushmitachavan70@gmail.com',
                 'corporate_email': 'susmita.chavan@justo.co.in', 'work_email': 'susmita.chavan@justo.co.in',
                 'mobile': '00000000', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 70050.0, 'location': 'Navi Mumbai', 'barcode': 'JUS1231'},
                {'id': 579, 'name': 'Suraj Bavkar', 'pan_number': 'FUDPB1395F', 'job_title': 'Assistant Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(2003, 6, 9),
                 'department_id': 2, 'parent_id': 993, 'gender': 'male', 'joining_date': datetime.date(2023, 1, 23),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'bavkarsuraj879@gmail.com',
                 'corporate_email': 'suraj.bavkar@justo.co.in', 'work_email': 'suraj.bavkar@justo.co.in',
                 'mobile': '8624988914', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 44779.0, 'location': 'Pune', 'barcode': 'JUS1060'},
                {'id': 1405, 'name': 'Surya Rastogi', 'pan_number': 'BULPR7534J',
                 'job_title': 'Assistant General Manager', 'mobile_phone': '000000000', 'work_phone': '000000',
                 'birthday': datetime.date(1994, 2, 16), 'department_id': 2, 'parent_id': 243, 'gender': 'male',
                 'joining_date': datetime.date(2024, 5, 21), 'departure_date': datetime.date(2024, 10, 15),
                 'city': 'Mumbai', 'zip': '400104', 'private_email': 'surya.rastogi.mum@gmail.com',
                 'corporate_email': 'surya.rastogi@justo.co.in', 'work_email': 'surya.rastogi@justo.co.in',
                 'mobile': '9769009943', 'marital': 'married', 'emergency_contact': '9029564882',
                 'active_status': False, 'ctc': 120833.0, 'location': 'Mumbai Western', 'barcode': 'JUS603'},
                {'id': 1461, 'name': 'Sushil  Babaji  Mandge', 'pan_number': '000000',
                 'job_title': 'Assistant General Manager', 'mobile_phone': '000000000', 'work_phone': '000000',
                 'birthday': datetime.date(1992, 3, 27), 'department_id': 2, 'parent_id': 75, 'gender': 'male',
                 'joining_date': datetime.date(2024, 6, 1), 'departure_date': None, 'city': 'City', 'zip': '000000',
                 'private_email': 'sushilmandge1427@gmail.com', 'corporate_email': 'sushil.mandge@justo.co.in',
                 'work_email': 'sushil.mandge@justo.co.in', 'mobile': '00000000', 'marital': 'single',
                 'emergency_contact': '00000000', 'active_status': True, 'ctc': 112000.0,
                 'location': 'Regional Office _ Pune', 'barcode': 'JUS614'},
                {'id': 10, 'name': 'Swapnil Adhav', 'pan_number': 'AMMPA4107A',
                 'job_title': 'Assistant General Manager', 'mobile_phone': '000000000', 'work_phone': '000000',
                 'birthday': datetime.date(1987, 3, 16), 'department_id': 2, 'parent_id': 459, 'gender': 'male',
                 'joining_date': datetime.date(2022, 3, 31), 'departure_date': datetime.date(2024, 4, 14),
                 'city': 'City', 'zip': '000000', 'private_email': 'adhavswapneel@gmail.com',
                 'corporate_email': 'swapnil.adhav@justo.co.in', 'work_email': 'swapnil.adhav@justo.co.in',
                 'mobile': '9529927331', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 109000.0, 'location': 'Pune', 'barcode': 'P0246'},
                {'id': 244, 'name': 'Swapnil Sahani', 'pan_number': 'BBLPS8939P',
                 'job_title': 'Assistant General Manager', 'mobile_phone': '000000000', 'work_phone': '000000',
                 'birthday': datetime.date(1979, 6, 12), 'department_id': 2, 'parent_id': 1117, 'gender': 'male',
                 'joining_date': datetime.date(2023, 2, 1), 'departure_date': None, 'city': 'City', 'zip': '000000',
                 'private_email': 'swapnilssahani@yahoo.com', 'corporate_email': 'swapnil.sahani@justo.co.in',
                 'work_email': 'swapnil.sahani@justo.co.in', 'mobile': '8657435106', 'marital': 'single',
                 'emergency_contact': '00000000', 'active_status': True, 'ctc': 221463.0,
                 'location': 'Regional Office_Mumbai', 'barcode': 'JUS1067'},
                {'id': 338, 'name': 'Swapnil Bhalekar', 'pan_number': 'CERPB5712F', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1995, 4, 12),
                 'department_id': 5, 'parent_id': 251, 'gender': 'male', 'joining_date': datetime.date(2021, 7, 12),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'sample3@sample.com',
                 'corporate_email': 'swapnil.bhalekar@justo.co.in', 'work_email': 'swapnil.bhalekar@justo.co.in',
                 'mobile': '7276722968', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 59779.0, 'location': 'Pune', 'barcode': 'JUS0311'},
                {'id': 331, 'name': 'Tanveer zameer pathan', 'pan_number': 'BQSPP4282N', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1992, 4, 28),
                 'department_id': 2, 'parent_id': 385, 'gender': 'male', 'joining_date': datetime.date(2021, 12, 27),
                 'departure_date': None, 'city': 'Pune', 'zip': '411005',
                 'private_email': 'tanveerzameerpathan@gmail.com', 'corporate_email': 'tanveer.pathan@justo.co.in',
                 'work_email': 'tanveer.pathan@justo.co.in', 'mobile': '9022774440', 'marital': 'married',
                 'emergency_contact': '00000000', 'active_status': True, 'ctc': 59779.0, 'location': 'Pune',
                 'barcode': 'JUS0548'},
                {'id': 622, 'name': 'System Admin', 'pan_number': 'AFP121212', 'job_title': 'Assistant General Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1980, 9, 3),
                 'department_id': 13, 'parent_id': 622, 'gender': 'male', 'joining_date': datetime.date(2018, 4, 1),
                 'departure_date': None, 'city': 'Pune', 'zip': '411048', 'private_email': 'sample3@sample.com',
                 'corporate_email': 'admin@workrig.com', 'work_email': 'admin@workrig.com', 'mobile': '7020174556',
                 'marital': 'single', 'emergency_contact': '121212121', 'active_status': True, 'ctc': 20000.0,
                 'location': 'Mumbai - HO', 'barcode': 'E001'},
                {'id': 1463, 'name': 'Sweta Kumari', 'pan_number': '000000', 'job_title': 'Management Trainee',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1998, 8, 8),
                 'department_id': 2, 'parent_id': None, 'gender': 'female', 'joining_date': datetime.date(2023, 6, 21),
                 'departure_date': datetime.date(2024, 7, 8), 'city': 'City', 'zip': '000000',
                 'private_email': 'SwetaKumaridpugbsrc@gmail.com', 'corporate_email': 'sweta.kumari@justo.co.in',
                 'work_email': 'sweta.kumari@justo.co.in', 'mobile': '00000000', 'marital': 'single',
                 'emergency_contact': '00000000', 'active_status': True, 'ctc': 41667.0, 'location': 'Pune',
                 'barcode': 'JUS1205'},
                {'id': 368, 'name': 'Tejashri Mhetre', 'pan_number': 'EHBPM1405D', 'job_title': 'Senior Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1997, 11, 20),
                 'department_id': 2, 'parent_id': 388, 'gender': 'female', 'joining_date': datetime.date(2020, 3, 18),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'tejamhetre20@gmail.com',
                 'corporate_email': 'tejashree.mhetre@justo.co.in', 'work_email': 'tejashree.mhetre@justo.co.in',
                 'mobile': '9527379504', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 74779.0, 'location': 'Pune', 'barcode': 'JUS0105'},
                {'id': 1903, 'name': 'Umang Umesh Joshi', 'pan_number': 'CFMPJ2575Q', 'job_title': 'Management Trainee',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1999, 12, 21),
                 'department_id': 10, 'parent_id': 841, 'gender': 'male', 'joining_date': datetime.date(2024, 8, 12),
                 'departure_date': None, 'city': 'Sendhwa', 'zip': '451666',
                 'private_email': 'Umangjoshi8109@gmail.com', 'corporate_email': 'umang.joshi@justo.co.in',
                 'work_email': 'umang.joshi@justo.co.in', 'mobile': '9131542359', 'marital': 'single',
                 'emergency_contact': '8120403072', 'active_status': True, 'ctc': 33333.0, 'location': 'Pune',
                 'barcode': 'JUS696'},
                {'id': 403, 'name': 'Tushar Kore', 'pan_number': 'GOIPK1921L', 'job_title': 'Assistant Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1999, 3, 30),
                 'department_id': 2, 'parent_id': 336, 'gender': 'male', 'joining_date': datetime.date(2021, 10, 21),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'tushar006kore@gmail.com',
                 'corporate_email': 'tushar.kore@justo.co.in', 'work_email': 'tushar.kore@justo.co.in',
                 'mobile': '8379034699', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 49779.0, 'location': 'Pune', 'barcode': 'JUS0461'},
                {'id': 967, 'name': 'Tejas Jadhav', 'pan_number': 'ASWPJ6548G', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1989, 3, 26),
                 'department_id': 2, 'parent_id': 563, 'gender': 'male', 'joining_date': datetime.date(2024, 3, 4),
                 'departure_date': datetime.date(2024, 10, 18), 'city': 'Navi Mumbai', 'zip': '400706',
                 'private_email': 'tezjadav@gmail.com', 'corporate_email': 'tejas.jadhav@justo.co.in',
                 'work_email': 'tejas.jadhav@justo.co.in', 'mobile': '9527779779', 'marital': 'single',
                 'emergency_contact': '9270464634', 'active_status': False, 'ctc': 56250.0, 'location': 'Navi Mumbai',
                 'barcode': 'JUS1430'},
                {'id': 52, 'name': 'Tushar Giridhar Bhosale', 'pan_number': 'CLFPB2973K',
                 'job_title': 'Assistant Manager', 'mobile_phone': '000000000', 'work_phone': '000000',
                 'birthday': datetime.date(1991, 6, 21), 'department_id': 2, 'parent_id': 1785, 'gender': 'male',
                 'joining_date': datetime.date(2023, 1, 6), 'departure_date': None, 'city': 'City', 'zip': '000000',
                 'private_email': 'Tushar.Bhosale9193@gmail.com',
                 'corporate_email': 'tushargiridhar.bhosale@justo.co.in',
                 'work_email': 'tushargiridhar.bhosale@justo.co.in', 'mobile': '8805345417', 'marital': 'single',
                 'emergency_contact': '00000000', 'active_status': True, 'ctc': 54779.0, 'location': 'Pune',
                 'barcode': 'JUS1034'},
                {'id': 478, 'name': 'Tushar Bhadane', 'pan_number': 'DRTPB0079M', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1997, 3, 28),
                 'department_id': 2, 'parent_id': 414, 'gender': 'male', 'joining_date': datetime.date(2022, 5, 4),
                 'departure_date': datetime.date(2024, 10, 14), 'city': 'Mumbai', 'zip': '000000',
                 'private_email': 'tushar@gmail.com', 'corporate_email': 'tushar.bhadane@justo.co.in',
                 'work_email': 'tushar.bhadane@justo.co.in', 'mobile': '9004938177', 'marital': 'single',
                 'emergency_contact': '00000000', 'active_status': False, 'ctc': 65100.0, 'location': 'KDMC',
                 'barcode': 'JUS0713'},
                {'id': 1880, 'name': 'VISHESH Rakesh SHARMA', 'pan_number': 'EAQPS6637R', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1993, 11, 11),
                 'department_id': 29, 'parent_id': 1799, 'gender': 'male', 'joining_date': datetime.date(2024, 8, 2),
                 'departure_date': None, 'city': 'Mumbai', 'zip': '400069', 'private_email': 'sharmavishesh5@gmail.com',
                 'corporate_email': 'vishesh.sharma@justo.co.in', 'work_email': 'vishesh.sharma@justo.co.in',
                 'mobile': '9892168109', 'marital': 'married', 'emergency_contact': '9167065356', 'active_status': True,
                 'ctc': 100000.0, 'location': 'Regional Office_Mumbai', 'barcode': 'JUS688'},
                {'id': 1124, 'name': 'Unnati Bharat  Bhanushali', 'pan_number': 'CCDPB0204Q', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1996, 2, 25),
                 'department_id': 2, 'parent_id': 243, 'gender': 'female', 'joining_date': datetime.date(2024, 4, 25),
                 'departure_date': datetime.date(2024, 7, 17), 'city': 'Mumbai ', 'zip': '400084',
                 'private_email': 'unnatikatariya@yahoo.in', 'corporate_email': 'unnati.bhanushali@justo.co.in',
                 'work_email': 'unnati.bhanushali@justo.co.in', 'mobile': '8850444792', 'marital': 'single',
                 'emergency_contact': '8169189810', 'active_status': False, 'ctc': 80000.0,
                 'location': 'Mumbai Western', 'barcode': 'JUS1516'},
                {'id': 1715, 'name': 'Umesh mohan  Bhat', 'pan_number': 'AZBPB4916A', 'job_title': 'Senior Executive',
                 'mobile_phone': '8454836053', 'work_phone': '000000', 'birthday': datetime.date(1987, 6, 15),
                 'department_id': 10, 'parent_id': 103, 'gender': 'male', 'joining_date': datetime.date(2024, 5, 24),
                 'departure_date': None, 'city': 'Mumbai', 'zip': '400042', 'private_email': 'umesh.bhat89@gmail.com',
                 'corporate_email': 'umesh.bhat@justo.co.in', 'work_email': 'umesh.bhat@justo.co.in',
                 'mobile': '8454836053', 'marital': 'married', 'emergency_contact': '9773008350', 'active_status': True,
                 'ctc': 42166.0, 'location': 'Regional Office_Mumbai', 'barcode': 'JUS604'},
                {'id': 1768, 'name': 'Vaishnavi Vijay Kapale', 'pan_number': 'HOZPK0519G',
                 'job_title': 'Assistant Manager', 'mobile_phone': '000000000', 'work_phone': '000000',
                 'birthday': datetime.date(1998, 1, 9), 'department_id': 2, 'parent_id': 1950, 'gender': 'female',
                 'joining_date': datetime.date(2024, 6, 15), 'departure_date': None, 'city': 'Nashik', 'zip': '422003',
                 'private_email': 'dollykapale@gmail.com', 'corporate_email': 'vaishnavi.kapale@justo.co.in',
                 'work_email': 'vaishnavi.kapale@justo.co.in', 'mobile': '9158854972', 'marital': 'single',
                 'emergency_contact': '9822825039', 'active_status': True, 'ctc': 30000.0, 'location': 'Pune',
                 'barcode': 'JUS634'},
                {'id': 1825, 'name': 'Vijay  Keshavrao  Vaidya', 'pan_number': '000000', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1991, 5, 17),
                 'department_id': 2, 'parent_id': 56, 'gender': 'male', 'joining_date': datetime.date(2024, 7, 1),
                 'departure_date': None, 'city': 'City', 'zip': '000000',
                 'private_email': 'vijayvaidya98228252161@gmail.com', 'corporate_email': 'vijay.vaidya@justo.co.in',
                 'work_email': 'vijay.vaidya@justo.co.in', 'mobile': '00000000', 'marital': 'single',
                 'emergency_contact': '00000000', 'active_status': True, 'ctc': 53800.0, 'location': 'Pune',
                 'barcode': 'JUS659'},
                {'id': 1563, 'name': 'Vijay Mallishe', 'pan_number': '000000', 'job_title': 'Assistant Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1989, 4, 28),
                 'department_id': 5, 'parent_id': 251, 'gender': 'male', 'joining_date': datetime.date(2023, 11, 16),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'vijay.mallishe@gmail.com',
                 'corporate_email': 'Vijay.mallishe@justo.co.in', 'work_email': 'Vijay.mallishe@justo.co.in',
                 'mobile': '00000000', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 48800.0, 'location': 'Regional Office _ Pune', 'barcode': 'JUS1304'},
                {'id': 501, 'name': 'Veena Mhatre', 'pan_number': 'GNPPM6010Q', 'job_title': 'Management Trainee',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(2000, 3, 12),
                 'department_id': 5, 'parent_id': 251, 'gender': 'female', 'joining_date': datetime.date(2023, 6, 5),
                 'departure_date': datetime.date(2023, 12, 4), 'city': 'City', 'zip': '000000',
                 'private_email': 'mhatrevena1@gmail.com', 'corporate_email': 'veena.mhatre@justo.co.in',
                 'work_email': 'veena.mhatre@justo.co.in', 'mobile': '00000000', 'marital': 'single',
                 'emergency_contact': '00000000', 'active_status': True, 'ctc': 33333.0, 'location': 'Pune',
                 'barcode': 'P0440'},
                {'id': 1194, 'name': 'Vinod  Agate', 'pan_number': '000000', 'job_title': 'Executive',
                 'mobile_phone': '8605832315', 'work_phone': '000000', 'birthday': datetime.date(2002, 2, 8),
                 'department_id': 17, 'parent_id': 800, 'gender': 'male', 'joining_date': datetime.date(2021, 11, 17),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'vinodagate53@gmail.com',
                 'corporate_email': 'vinod.agate@gmail.com', 'work_email': 'vinod.agate@gmail.com',
                 'mobile': '00000000', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 20000.0, 'location': 'Regional Office_Mumbai', 'barcode': 'JC0002'},
                {'id': 1799, 'name': 'Vipul Nalanda Ovhal', 'pan_number': 'AAWPO4034A', 'job_title': 'Consultant',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1988, 8, 19),
                 'department_id': 29, 'parent_id': 720, 'gender': 'male', 'joining_date': datetime.date(2024, 6, 3),
                 'departure_date': None, 'city': 'Mumbai', 'zip': '400080', 'private_email': 'vipul@maple-leaf.in',
                 'corporate_email': 'Vipul.ovhal@justo.co.in', 'work_email': 'Vipul.ovhal@justo.co.in',
                 'mobile': '9987480102', 'marital': 'single', 'emergency_contact': '0', 'active_status': True,
                 'ctc': 20000.0, 'location': 'Regional Office_Mumbai', 'barcode': 'JC008'},
                {'id': 320, 'name': 'Vinod Balaso Patole', 'pan_number': 'BCCPP6468G', 'job_title': 'Senior Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1990, 3, 23),
                 'department_id': 2, 'parent_id': 12, 'gender': 'male', 'joining_date': datetime.date(2022, 12, 5),
                 'departure_date': datetime.date(2024, 4, 16), 'city': 'City', 'zip': '000000',
                 'private_email': 'sample3@sample.com', 'corporate_email': 'vinod.patole@justo.co.in',
                 'work_email': 'vinod.patole@justo.co.in', 'mobile': '7498694657', 'marital': 'single',
                 'emergency_contact': '00000000', 'active_status': True, 'ctc': 101800.0, 'location': 'Pune',
                 'barcode': 'P0351'},
                {'id': 1701, 'name': 'Vikram  Mishra', 'pan_number': 'AXTPM5561G', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1989, 1, 17),
                 'department_id': 2, 'parent_id': 1163, 'gender': 'male', 'joining_date': datetime.date(2024, 5, 25),
                 'departure_date': None, 'city': 'Mumbai ', 'zip': '400074',
                 'private_email': 'mishravikram411@gmail.com', 'corporate_email': 'vikram.mishra@justo.co.in',
                 'work_email': 'vikram.mishra@justo.co.in', 'mobile': '8097299217', 'marital': 'married',
                 'emergency_contact': '9967773745', 'active_status': True, 'ctc': 60000.0, 'location': 'Navi Mumbai',
                 'barcode': 'JUS605'},
                {'id': 542, 'name': 'Vishal Pathak', 'pan_number': '000000', 'job_title': 'Assistant Manager',
                 'mobile_phone': '8010569601', 'work_phone': '000000', 'birthday': datetime.date(1993, 2, 12),
                 'department_id': 2, 'parent_id': 56, 'gender': 'male', 'joining_date': datetime.date(2023, 8, 5),
                 'departure_date': datetime.date(2023, 10, 31), 'city': 'City', 'zip': '000000',
                 'private_email': 'kashyapvishal1293@gmail.com', 'corporate_email': 'vishal.pathak@justo.co.in',
                 'work_email': 'vishal.pathak@justo.co.in', 'mobile': '00000000', 'marital': 'single',
                 'emergency_contact': '00000000', 'active_status': True, 'ctc': 45000.0, 'location': 'Pune',
                 'barcode': 'P0481'},
                {'id': 75, 'name': 'Vishal Vijay Thigale', 'pan_number': 'AEMPT1575A',
                 'job_title': 'Deputy General Manager', 'mobile_phone': '000000000', 'work_phone': '000000',
                 'birthday': datetime.date(1985, 7, 18), 'department_id': 2, 'parent_id': 6, 'gender': 'male',
                 'joining_date': datetime.date(2022, 4, 11), 'departure_date': None, 'city': 'Pune', 'zip': '411041',
                 'private_email': 'vishal.thigale@gmail.com', 'corporate_email': 'vishal.thigale@justo.co.in',
                 'work_email': 'vishal.thigale@justo.co.in', 'mobile': '9930992333', 'marital': 'married',
                 'emergency_contact': '8421795777', 'active_status': True, 'ctc': 299370.0, 'location': 'Pune',
                 'barcode': 'JUS0661'},
                {'id': 305, 'name': 'Vyaprosh Kale', 'pan_number': 'AGDPK7959B',
                 'job_title': 'Assistant General Manager', 'mobile_phone': '000000000', 'work_phone': '000000',
                 'birthday': datetime.date(1981, 11, 13), 'department_id': 2, 'parent_id': 576, 'gender': 'male',
                 'joining_date': datetime.date(2022, 5, 13), 'departure_date': None, 'city': 'City', 'zip': '000000',
                 'private_email': 'sample3@sample.com', 'corporate_email': 'vyaprosh.kale@justo.co.in',
                 'work_email': 'vyaprosh.kale@justo.co.in', 'mobile': '9960898346', 'marital': 'single',
                 'emergency_contact': '00000000', 'active_status': True, 'ctc': 129666.0, 'location': 'Pune',
                 'barcode': 'JUS0738'},
                {'id': 1611, 'name': 'Vrundavan  Purushottam  Wagh', 'pan_number': '000000',
                 'job_title': 'Senior Manager', 'mobile_phone': '000000000', 'work_phone': '000000',
                 'birthday': datetime.date(1985, 6, 15), 'department_id': 2, 'parent_id': 1461, 'gender': 'male',
                 'joining_date': datetime.date(2024, 6, 11), 'departure_date': None, 'city': 'City', 'zip': '000000',
                 'private_email': 'vrundavan.p.wagh@gmail.com', 'corporate_email': 'vrundavan.wagh@justo.co.in',
                 'work_email': 'vrundavan.wagh@justo.co.in', 'mobile': '00000000', 'marital': 'single',
                 'emergency_contact': '00000000', 'active_status': True, 'ctc': 75000.0, 'location': 'Pune',
                 'barcode': 'JUS623'},
                {'id': 450, 'name': 'Yakub  Rajjak Pathan', 'pan_number': 'CRPPP7636B', 'job_title': 'Senior Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1994, 8, 1),
                 'department_id': 2, 'parent_id': 337, 'gender': 'male', 'joining_date': datetime.date(2023, 2, 5),
                 'departure_date': None, 'city': 'Pune', 'zip': '411057', 'private_email': 'Yakub.pathan78@gmail.com',
                 'corporate_email': 'yakub.pathan@justo.co.in', 'work_email': 'yakub.pathan@justo.co.in',
                 'mobile': '7709128871', 'marital': 'single', 'emergency_contact': '7774987234', 'active_status': True,
                 'ctc': 99779.0, 'location': 'Pune', 'barcode': 'JUS1080'},
                {'id': 1806, 'name': 'Yasmin Aziz  Chowdhury', 'pan_number': 'AMJPC7902L', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1991, 6, 3),
                 'department_id': 2, 'parent_id': 563, 'gender': 'female', 'joining_date': datetime.date(2024, 7, 1),
                 'departure_date': None, 'city': 'Mumbai ', 'zip': '210410',
                 'private_email': 'yasminmaaz1981@gmail.com', 'corporate_email': 'Yasmin.Chowdhury@justo.co.in',
                 'work_email': 'Yasmin.Chowdhury@justo.co.in', 'mobile': '8369021388', 'marital': 'single',
                 'emergency_contact': '7977570747', 'active_status': True, 'ctc': 65000.0, 'location': 'Navi Mumbai',
                 'barcode': 'JUS654'},
                {'id': 426, 'name': 'Yashpal Singh Champavat', 'pan_number': 'BHPPC9251E',
                 'job_title': 'Assistant Manager', 'mobile_phone': '000000000', 'work_phone': '000000',
                 'birthday': datetime.date(1998, 3, 21), 'department_id': 2, 'parent_id': 1902, 'gender': 'male',
                 'joining_date': datetime.date(2023, 1, 21), 'departure_date': datetime.date(2024, 10, 12),
                 'city': 'Mumbai', 'zip': '000000', 'private_email': 'Yashpalsingh0217@gmail.com',
                 'corporate_email': 'yashpal.singh@justo.co.in', 'work_email': 'yashpal.singh@justo.co.in',
                 'mobile': '9867004665', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': False,
                 'ctc': 61929.0, 'location': 'Navi Mumbai', 'barcode': 'JUS1053'},
                {'id': 1539, 'name': 'Yasin Mehmood Shaikh', 'pan_number': 'EJMPS9923R', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1992, 8, 23),
                 'department_id': 2, 'parent_id': 1835, 'gender': 'male', 'joining_date': datetime.date(2024, 3, 20),
                 'departure_date': None, 'city': 'Mumbai', 'zip': '400083', 'private_email': 'yshaikh3033@gmail.com',
                 'corporate_email': 'yasin.shaikh@justo.co.in', 'work_email': 'yasin.shaikh@justo.co.in',
                 'mobile': '9833501631', 'marital': 'married', 'emergency_contact': '8169324709', 'active_status': True,
                 'ctc': 50000.0, 'location': 'Pune', 'barcode': 'JUS1458'},
                {'id': 1920, 'name': 'sonali Das', 'pan_number': 'ACTPD8779Q', 'job_title': 'Consultant',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1972, 9, 9),
                 'department_id': 10, 'parent_id': None, 'gender': 'female', 'joining_date': datetime.date(2024, 8, 26),
                 'departure_date': None, 'city': 'Mumbai', 'zip': '400098', 'private_email': 'sonali.das@gmail.com',
                 'corporate_email': 'sonali.das@justo.co.in', 'work_email': 'sonali.das@justo.co.in',
                 'mobile': '9769737340', 'marital': 'single', 'emergency_contact': '00', 'active_status': True,
                 'ctc': 0.0, 'location': 'Regional Office_Mumbai', 'barcode': 'JC9'},
                {'id': 210, 'name': 'Yogita Karekar', 'pan_number': 'DZCPK6794K', 'job_title': 'Assistant Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1993, 9, 22),
                 'department_id': 2, 'parent_id': 385, 'gender': 'female', 'joining_date': datetime.date(2021, 11, 8),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'yogitak004@gmail.com',
                 'corporate_email': 'yogita.karekar@justo.co.in', 'work_email': 'yogita.karekar@justo.co.in',
                 'mobile': '9764968944', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 37450.0, 'location': 'Pune', 'barcode': 'JUS0478'},
                {'id': 1112, 'name': 'pravin kedar', 'pan_number': 'GLYPK7158C', 'job_title': 'Senior Executive',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1997, 1, 4),
                 'department_id': 10, 'parent_id': 103, 'gender': 'male', 'joining_date': datetime.date(2024, 4, 11),
                 'departure_date': None, 'city': 'Mumbai', 'zip': '400083', 'private_email': 'pravinkedar97@gmail.com',
                 'corporate_email': 'pravin.kedar@justo.co.in', 'work_email': 'pravin.kedar@justo.co.in',
                 'mobile': '8369128652', 'marital': 'single', 'emergency_contact': '9869862539', 'active_status': True,
                 'ctc': 41666.0, 'location': 'Regional Office_Mumbai', 'barcode': 'M839'},
                {'id': 1734, 'name': 'manoj babu chavan', 'pan_number': 'CFTPC4273B', 'job_title': 'Executive',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(2002, 8, 11),
                 'department_id': 10, 'parent_id': 103, 'gender': 'male', 'joining_date': datetime.date(2024, 6, 4),
                 'departure_date': None, 'city': 'mumbai', 'zip': '400074',
                 'private_email': 'chavanmanoj8424@gmail.com', 'corporate_email': 'manoj.chavan@justo.co.in',
                 'work_email': 'manoj.chavan@justo.co.in', 'mobile': '8424952674', 'marital': 'single',
                 'emergency_contact': '8433536621', 'active_status': True, 'ctc': 22917.0,
                 'location': 'Regional Office_Mumbai', 'barcode': 'JUS617'},
                {'id': 1439, 'name': 'komal Ajay chandanshive', 'pan_number': 'BQWPC9486P',
                 'job_title': 'Assistant Manager', 'mobile_phone': '000000000', 'work_phone': '000000',
                 'birthday': datetime.date(1998, 7, 22), 'department_id': 2, 'parent_id': 563, 'gender': 'female',
                 'joining_date': datetime.date(2024, 6, 1), 'departure_date': None, 'city': 'Mumbai', 'zip': '400071',
                 'private_email': 'komalcah922@gmail.com', 'corporate_email': 'komal.chandanshive@justo.co.in',
                 'work_email': 'komal.chandanshive@justo.co.in', 'mobile': '7039577524', 'marital': 'single',
                 'emergency_contact': '9619572799', 'active_status': True, 'ctc': 45800.0, 'location': 'Navi Mumbai',
                 'barcode': 'JUS612'},
                {'id': 1835, 'name': 'Vivek  Yerande', 'pan_number': 'AFDPY3141C',
                 'job_title': 'Assistant General Manager', 'mobile_phone': '000000000', 'work_phone': '000000',
                 'birthday': datetime.date(1987, 6, 12), 'department_id': 2, 'parent_id': 459, 'gender': 'male',
                 'joining_date': datetime.date(2024, 7, 8), 'departure_date': None, 'city': 'pune', 'zip': '411058',
                 'private_email': 'vikipatil.vy@gmail.com', 'corporate_email': 'vivek.yerande@justo.co.in',
                 'work_email': 'vivek.yerande@justo.co.in', 'mobile': '8668931198', 'marital': 'married',
                 'emergency_contact': '7776089993', 'active_status': True, 'ctc': 125000.0, 'location': 'Pune',
                 'barcode': 'JUS670'},
                {'id': 381, 'name': 'Rahul Tirmare', 'pan_number': 'APVPT9668K',
                 'job_title': 'Assistant General Manager', 'mobile_phone': '000000000', 'work_phone': '000000',
                 'birthday': datetime.date(1989, 4, 27), 'department_id': 2, 'parent_id': 75, 'gender': 'male',
                 'joining_date': datetime.date(2022, 7, 15), 'departure_date': None, 'city': 'City', 'zip': '000000',
                 'private_email': 'rahul_tirmare@yahoo.com', 'corporate_email': 'rahul.tirmare@justo.co.in',
                 'work_email': 'rahul.tirmare@justo.co.in', 'mobile': '8055058650', 'marital': 'single',
                 'emergency_contact': '00000000', 'active_status': True, 'ctc': 99944.0, 'location': 'Pune',
                 'barcode': 'JUS0835'},
                {'id': 1785, 'name': 'Babita Rabbewar', 'pan_number': 'AZBPR3270R',
                 'job_title': 'Assistant General Manager', 'mobile_phone': '000000000', 'work_phone': '000000',
                 'birthday': datetime.date(1994, 2, 14), 'department_id': 2, 'parent_id': 1875, 'gender': 'female',
                 'joining_date': datetime.date(2024, 6, 20), 'departure_date': None, 'city': 'Pune', 'zip': '412101',
                 'private_email': 'babitaballal@gmail.com', 'corporate_email': 'babita.rabbewar@justo.co.in',
                 'work_email': 'babita.rabbewar@justo.co.in', 'mobile': '8766544089', 'marital': 'married',
                 'emergency_contact': '919373416911', 'active_status': True, 'ctc': 125000.0, 'location': 'Pune',
                 'barcode': 'JUS645'},
                {'id': 1702, 'name': 'Jitendra Singh', 'pan_number': 'DVFPS2752J',
                 'job_title': 'Deputy General Manager', 'mobile_phone': '000000000', 'work_phone': '000000',
                 'birthday': datetime.date(1990, 7, 25), 'department_id': 2, 'parent_id': 576, 'gender': 'male',
                 'joining_date': datetime.date(2024, 5, 15), 'departure_date': None, 'city': 'PUNE', 'zip': '411036',
                 'private_email': 'jitendra8febb@gmail.com', 'corporate_email': 'jitendra.singh@justo.co.in',
                 'work_email': 'jitendra.singh@justo.co.in', 'mobile': '7387108833', 'marital': 'married',
                 'emergency_contact': '9637535216', 'active_status': True, 'ctc': 220000.0, 'location': 'Pune',
                 'barcode': 'JUS601'},
                {'id': 560, 'name': 'Ashish Kalokhe', 'pan_number': '000000', 'job_title': 'Assistant Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1989, 9, 29),
                 'department_id': 2, 'parent_id': 1824, 'gender': 'male', 'joining_date': datetime.date(2023, 6, 1),
                 'departure_date': datetime.date(2024, 4, 7), 'city': 'City', 'zip': '000000', 'private_email': None,
                 'corporate_email': None, 'work_email': None, 'mobile': '00000000', 'marital': 'single',
                 'emergency_contact': '00000000', 'active_status': False, 'ctc': 40000.0, 'location': 'Pune',
                 'barcode': 'P0433'},
                {'id': 318, 'name': 'Nikhil Sisodiya', 'pan_number': 'FDKPS5370F', 'job_title': 'Senior Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1992, 10, 28),
                 'department_id': 2, 'parent_id': 337, 'gender': 'male', 'joining_date': datetime.date(2020, 10, 15),
                 'departure_date': None, 'city': 'pune', 'zip': '411041',
                 'private_email': 'nikhilsisodiya067@gmail.com', 'corporate_email': 'nikhil.sisodiya@justo.co.in',
                 'work_email': 'nikhil.sisodiya@justo.co.in', 'mobile': '+918668944001', 'marital': 'married',
                 'emergency_contact': '9284326405', 'active_status': True, 'ctc': 71779.0, 'location': 'Pune',
                 'barcode': 'JUS0134'},
                {'id': 1473, 'name': 'Shivam Balap', 'pan_number': 'BWDPB5144C', 'job_title': 'Assistant Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1990, 11, 23),
                 'department_id': 2, 'parent_id': 389, 'gender': 'male', 'joining_date': datetime.date(2023, 6, 19),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'ShivamBalap999@gmail.com',
                 'corporate_email': 'shivam.balap@justo.co.in', 'work_email': 'shivam.balap@justo.co.in',
                 'mobile': '00000000', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 64167.0, 'location': 'Pune', 'barcode': 'JUS1199'},
                {'id': 1764, 'name': 'Aniket Chakral', 'pan_number': 'BVKPC1248J', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1997, 12, 24),
                 'department_id': 2, 'parent_id': 389, 'gender': 'male', 'joining_date': datetime.date(2024, 6, 13),
                 'departure_date': None, 'city': 'Pune', 'zip': '411043',
                 'private_email': 'aniketchakral2412@gmail.com', 'corporate_email': 'aniket.chakral@justo.co.in',
                 'work_email': 'aniket.chakral@justo.co.in', 'mobile': '9561612412', 'marital': 'married',
                 'emergency_contact': '8983148696', 'active_status': True, 'ctc': 53800.0, 'location': 'Pune',
                 'barcode': 'JUS631'},
                {'id': 13, 'name': 'Sandeep Shivanand Kamat', 'pan_number': 'AMMPK3721E',
                 'job_title': 'General Manager', 'mobile_phone': '000000000', 'work_phone': '000000',
                 'birthday': datetime.date(1981, 11, 18), 'department_id': 5, 'parent_id': None, 'gender': 'male',
                 'joining_date': datetime.date(2022, 3, 15), 'departure_date': None, 'city': 'Mumbai', 'zip': '400012',
                 'private_email': 'sandeep.18kamat@gmail.com', 'corporate_email': 'sandeep.kamat@justo.co.in',
                 'work_email': 'sandeep.kamat@justo.co.in', 'mobile': '9920027688', 'marital': 'married',
                 'emergency_contact': '9920027585', 'active_status': True, 'ctc': 299370.0,
                 'location': 'Regional Office _ Pune', 'barcode': 'JUS0625'},
                {'id': 449, 'name': 'Kumari Snehlata', 'pan_number': 'GVHPS3763L', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1996, 1, 2),
                 'department_id': 2, 'parent_id': 336, 'gender': 'female', 'joining_date': datetime.date(2022, 6, 25),
                 'departure_date': None, 'city': 'pune', 'zip': '411045',
                 'private_email': 'kiumarisnehlata321@gmail.com', 'corporate_email': 'kumari.snehlata@justo.co.in',
                 'work_email': 'kumari.snehlata@justo.co.in', 'mobile': '7058498281', 'marital': 'single',
                 'emergency_contact': '0', 'active_status': True, 'ctc': 74779.0, 'location': 'Pune',
                 'barcode': 'JUS0818'},
                {'id': 388, 'name': 'Pratik Kolhapure', 'pan_number': 'BEXPK6096L',
                 'job_title': 'Assistant General Manager', 'mobile_phone': '000000000', 'work_phone': '000000',
                 'birthday': datetime.date(1987, 4, 18), 'department_id': 2, 'parent_id': 12, 'gender': 'male',
                 'joining_date': datetime.date(2021, 4, 1), 'departure_date': None, 'city': 'City', 'zip': '000000',
                 'private_email': 'sample3@sample.com', 'corporate_email': 'pratik.kolhapure@justo.co.in',
                 'work_email': 'pratik.kolhapure@justo.co.in', 'mobile': '9764221100', 'marital': 'single',
                 'emergency_contact': '00000000', 'active_status': True, 'ctc': 129666.0, 'location': 'Pune',
                 'barcode': 'JUS0248'},
                {'id': 499, 'name': 'Swapnil Neman', 'pan_number': 'AKNPN1361J', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1991, 6, 5),
                 'department_id': 2, 'parent_id': 854, 'gender': 'male', 'joining_date': datetime.date(2022, 6, 21),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'swapnil5neman6@gmail.com',
                 'corporate_email': 'swapnil.neman@justo.co.in', 'work_email': 'swapnil.neman@justo.co.in',
                 'mobile': '7303967788', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 59779.0, 'location': 'Mumbai Western', 'barcode': 'JUS0813'},
                {'id': 326, 'name': 'Jyoti Bhartiya', 'pan_number': 'BMVPB9333F', 'job_title': 'Senior Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1984, 12, 10),
                 'department_id': 2, 'parent_id': 896, 'gender': 'female', 'joining_date': datetime.date(2021, 8, 10),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'jyotibhartiya76@gmail.com',
                 'corporate_email': 'jyoti.bhartiya@justo.co.in', 'work_email': 'jyoti.bhartiya@justo.co.in',
                 'mobile': '9021860220', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 74757.0, 'location': 'Pune', 'barcode': 'JUS0364'},
                {'id': 367, 'name': 'Anita Jadhav ', 'pan_number': 'AOOPJ5482K', 'job_title': 'Manager',
                 'mobile_phone': '000000000', 'work_phone': '000000', 'birthday': datetime.date(1998, 4, 19),
                 'department_id': 2, 'parent_id': 304, 'gender': 'female', 'joining_date': datetime.date(2023, 3, 6),
                 'departure_date': None, 'city': 'City', 'zip': '000000', 'private_email': 'sample3@sample.com',
                 'corporate_email': 'anita.jadhav@justo.co.in', 'work_email': 'anita.jadhav@justo.co.in',
                 'mobile': '8668854760', 'marital': 'single', 'emergency_contact': '00000000', 'active_status': True,
                 'ctc': 59779.0, 'location': 'Pune', 'barcode': 'JUS1103'},
            ]

            for line in old_data:
                update_query = """
                        UPDATE hr_employee SET 
                            name = %s, 
                            pan_number = %s, 
                            job_title = %s, 
                            mobile_phone = %s, 
                            work_phone = %s, 
                            birthday = %s, 
                            department_id = %s, 
                            parent_id = %s, 
                            gender = %s, 
                            joining_date = %s, 
                            departure_date = %s, 
                            city = %s, 
                            zip = %s, 
                            private_email = %s, 
                            corporate_email = %s, 
                            work_email = %s, 
                            mobile = %s, 
                            marital = %s, 
                            emergency_contact = %s, 
                            active_status = %s, 
                            ctc = %s, 
                            location = %s, 
                            barcode = %s
                        WHERE id = %s
                    """

                # Prepare the values for the placeholders
                birthday = line['birthday']
                if birthday:
                    birthday = birthday.strftime('%Y-%m-%d')
                else:
                    birthday = None
                departure_date = line['departure_date']
                if departure_date:
                    departure_date = departure_date.strftime('%Y-%m-%d')
                else:
                    departure_date = None
                values = (
                    line['name'], line['pan_number'], line['job_title'], line['mobile_phone'], line['work_phone'],
                    birthday, line['department_id'], line['parent_id'], line['gender'], line['joining_date'],
                    departure_date, line['city'], line['zip'], line['private_email'], line['corporate_email'],
                    line['work_email'], line['mobile'], line['marital'], line['emergency_contact'], str(line['active_status']),
                    line['ctc'], line['location'], line['barcode'], line['id']
                )

                # Execute the update query
                request.env.cr.execute(update_query, values)
            return 'Success'
        else:
            return 'Access Denied'

    @http.route(['/correct_jv_cp_id'], type='http', auth="public")
    def correct_jv_cp_id(self):
        if request.env.user.has_group('base.group_system'):
            data = [
                ['Blisssful properties', 'A52100024923', '8600871297', 'siddhi.bansode@gmail.com',
                 '6735a5b15a2ed3e110bb2063'],
                ['360 Realtors Llp', 'A51900000246', '8830901727', 'shreya.ganbote@360realty.com',
                 '66f94255390dfbaa310f8a6e'],
                ['9 keys realty', 'A52100040492', '7083807270', 'nj31065@gmail.com', '66f7ddd6390dfbaa310e68d3'],
                ['Av capitals', 'A52100040042', '8698651643', 'vijay.masulkar@avcapitals.com',
                 '67232cabceda5e2444f1cdc0'],
                ['Ab Housing Realty Private Limited', 'A52100021653', '8888095947', 'abhousingrealty@gmail.com',
                 '66ff9e573cd31cb5d2cdd42e'],
                ['Abs realty capital pvt ltd', 'A52100044255', '9319150926', 'sumit.gore@gmail.com',
                 '67276d0ff1c39668e3032566'],
                ['Ace prime infra pvt ltd', 'A52100035520', '9910098941', 'aceprimeinfra@gmail.com',
                 '67028af73cd31cb5d2d06c45'],
                ['Ajay kakade ak homes', 'A52100035154', '7387363254', 'akankshadumal5@gmail.com',
                 '66f7a97e390dfbaa310e0f86'],
                ['Akshay chandrakant dev Ambika Properties', 'A52100034246', '7798253006',
                 'akshaydeo8340@gmail.com',
                 '670fa6ec191a101210fcdb96'],
                ['Growthwell', 'A52100045055', '9284423075', 'growthwell6@gmail.com', '6729e5946e0c89b7c41a2850'],
                ['Anarock Property Consultants Pvt. Ltd.', 'A51900000108', '9972880506', 'saksham1@trespect.com',
                 '66f7ce62390dfbaa310e4d19'],
                ['Apm reality pvt ltd', 'A52100046496', '8788676616', 'amol.dammewar@apmreality.in',
                 '67012f093cd31cb5d2cf0d2d'],
                ['Ashutosh singh', 'A52100033735', '8340291633', 'ashutosh.sbd@gmail.com',
                 '66f7ea13390dfbaa310e80d6'],
                ['Asset scout pvt ltd', 'A52100031596', '9552299404', 'pranav@assetscout.in',
                 '67023aab3cd31cb5d2cff691'],
                ['Assettrust services', 'A51600019792', '9588617213', 'vijay@assettrustservices.com',
                 '67162817191a10121000f5f8'],
                ['Aarohi properties', 'A52100046380', '9021431422', 'aarohiproperties05@gmail.com',
                 '672c76bbdc249b2bd717bfbd'],
                ['Abhidyu realcon', 'A52100047819', '7057611925', 'abhidyurealcon@gmail.com',
                 '66f92f74390dfbaa310f52ed'],
                ['Abhishek mishra', 'A52100028229', '7053432405', 'abhishek107380@gmail.com',
                 '67221008ceda5e2444ed9beb'],
                ['Aditya garg west bay properties', 'A52100032983', '7620639881', 'adityagargiitm@gmail.com',
                 '671f63d76cf8eb075795a29f'],
                ['Astra Realty', 'A51700015804', '8237027074', 'aditya123pai@gmail.com',
                 '67021f3d3cd31cb5d2cf7b1c'],
                ['We locate', 'A51800029242', '7378990404', 'welocate@gmail.com', '670ccb9e3cd31cb5d2da3558'],
                ['Akash ashok bhosale', 'A52100047999', '8262955103', 'akashbhosale9527@gmail.com',
                 '6736ee625a2ed3e110c4c1ee'],
                ['Home bhk', 'A52100023845', '7038866066', 'homebhk7@gmail.com', '670bcdad3cd31cb5d2d9f0e7'],
                ['Amit kumar', 'A52100026342', '9284702040', 'info.hirarealty@gmail.com',
                 '66f7ffc3390dfbaa310eaaab'],
                ['Banke emlak llp', 'A51800042388', '7666772374', 'bank.emlak@gmail.com',
                 '6723277cceda5e2444f19e8a'],
                ['Amol shalivan bhande', 'A52100032607', '9175320329', 'amolbhande888@gmail.com',
                 '67334994bbd062497bf56993'],
                ['Amoya consulting llp', 'A52100017509', '8928556422', 'info@amoya.in', '66fe24c10df68ea75968e652'],
                ['Angel realty', 'A52100027862', '8600285929', 'angelrealty@gmail.com', '6700fab63cd31cb5d2ceb436'],
                ['Aniruddh diwalkar', 'A52100044341', '9022826229', 'promoter.aniruddh@gmail.com',
                 '6736e64a5a2ed3e110c3f719'],
                ['Apna ghar lifespace', 'A52100008848', '8177856189', 'apg@gmail.com', '6735ed2c5a2ed3e110bfbf42'],
                ['Aristo real estate', 'A51700036861', '9769897464', 'aristorealestate@gmail.com',
                 '67348304bbd062497bfa1f92'],
                ['Sharukh shaikh optimum realty', 'A52100013692', '8999792539', 'shaikhsharukh506@gmail.com',
                 '672094f86cf8eb07579719fb'],
                ['Pragati properties', 'A52100038884', '7745054054', 'ashokdhole@gmail.com',
                 '6736e4105a2ed3e110c3ac6d'],
                ['Aspire Homes Sachin Deshmukh', 'A52100027726', '9028418778', 'sachin.deshmukh5559@gmail.com',
                 '66fe8c6ecb582bd7c920137d'],
                ['Asset ustaad', 'A52100046570', '7768849750', 'assetustaadpune@gmail.com',
                 '672df2b97f659ef37e2bb8ff'],
                ['Avinash kakade Axilencer International services', 'A52100030169', '8668679552',
                 'avinashkakade8596@gmail.com', '6714a729191a101210ff8911'],
                ['Blissful home properties', 'A52000044258', '8689871024', 'blissfulhomeproperties@gmail.com',
                 '673ed335997820df93f0b722'],
                ['Bhagyashri sushil kale', 'A52100047039', '9370091212', 'sskgrouppune@gmail.com',
                 '67320d3d64f82e5d641f1d46'],
                ['Ritesh bhate', 'A52100029945', '9730121618', 'ritesh.rb19@gmail.com', '6729ba6c6e0c89b7c418da19'],
                ['Bhawan realtors', 'A52100038360', '9142720883', 'amitkumarlife0809@gmail.com',
                 '66f7d3f6390dfbaa310e5ba0'],
                ['Sonali real estate services', 'A52100024018', '9561374561', 'sonali.kanade@gmail.com',
                 '67347c1abbd062497bf9bd79'],
                ['Bhivare and sons', 'A53100022631', '9881881838', 'bhivareandsons@gmail.com',
                 '672dfc087f659ef37e2c7dff'],
                ['Bhaumik doshi white collar property', 'A51900015530', '7875106106',
                 'whitecollarproperty@gmail.com',
                 '66ffc5eb3cd31cb5d2ce25a1'],
                ['Blackstone Realty', 'A51700026077', '9511818765', 'pune.blackstonerealty@gmail.com',
                 '66fcef580df68ea75968b763'],
                ['Bhagirath trivedi', 'A50500022229', '9403141134', 'shubhamukale@gmail.com',
                 '670bc9d03cd31cb5d2d9cc0e'],
                ['Bliss realty', 'A51900011464', '9665168764', 'info@blissred.com', '66f95a5a390dfbaa310fc81a'],
                ['Bohra associates', 'A52100047088', '7276507748', 'bohraassociates007@gmail.com',
                 '6712361d191a101210fd9990'],
                ['Bookmyvastu', 'A52100042145', '7558310187', 'skbookmyvastu@gmail.com',
                 '672a1352ca4700b10335fb27'],
                ['The bric spaces properties', 'A52100031660', '7875775880', 'info@bricspacesgmail.com',
                 '6720bf666cf8eb075798854e'],
                ['Brick stories', 'A52100026422', '8928895336', 'info@brickstories.com',
                 '670780b73cd31cb5d2d56eb1'],
                ['Bhivare and sons', 'A53100022631', '9881881838', 'bhivareandsons@gmail.com',
                 '672dfc087f659ef37e2c7dff'],
                ['Brickzone prop private limited', 'A52100045239', '8655443326',
                 'supriya.pandhare@brickzoneprop.com',
                 '66f7a39f390dfbaa310dfdac'],
                ["Bull's eye property solution", 'A52100036577', '9764880458', 'bullseyepropsol@gmail.com',
                 '6731bb0964f82e5d641c3c06'],
                ['Crii group', 'A52100030031', '9011881671', 'abhijit@criigroup.com', '672f3a3064f82e5d64101615'],
                ['Capital scouts', 'A52500047726', '8788133209', 'nisha.capitalscouts@gmail.com',
                 '672c72badc249b2bd7178241'],
                ['Clearspace proptech india pvt ltd', 'A52100037727', '9881290000', 'accounts@clearspacerealty.com',
                 '66f7f6e5390dfbaa310e9373'],
                ['Click ghar', 'A51700008159', '9137898698', 'info@clickghar.com', '6721dc0dceda5e2444ea6aca'],
                ['Somnath Raju Ghardale', 'A52100035022', '9834526374', 'somnathgardhale@gmail.com',
                 '672cb52c12e113376ccd5650'],
                ['Corazon Homes Private Limited', 'A52100028952', '7028320436', 'sales@corazonhomes.com',
                 '66f54ebbe23ec89ee8d67928'],
                ['Dattatray ashok thorat', 'A52100041568', '7030527363', 'er.swapnil88@gmail.com',
                 '672c8821514072df405db88a'],
                ['Destiny properties', 'A52000043046', '9819178547', 'destinyrealestates@gmail.com',
                 '672c6b03dc249b2bd7175776'],
                ['Dolphin homes', 'A52100039817', '8340703973', 'subhamjsr94@gmail.com',
                 '6722226aceda5e2444ee8335'],
                ['Dreamzone', 'A52100016538', '8806684534', 'waytodreamzone@gmail.com', '672b6eeadc249b2bd7163751'],
                ['Deepa amol kalamkar', 'A52100034349', '8669109390', 'amol.kalamkar@gmail.com',
                 '67348e08bbd062497bfa8e24'],
                ['Prop next', 'A52100029920', '9856235478', 'dikshantrqthode2@gmail.com',
                 '6729ea136e0c89b7c41a6b60'],
                ['Crystal realtors', 'A52100037274', '8087888005', 'crystalrealtors0005@gmail.com',
                 '6708fbdd3cd31cb5d2d7109a'],
                ['Nvt Property', 'A52100044265', '7038044015', 'vijay@nvthomes.com', '672afa6fdc249b2bd7141edb'],
                ['Susmit hingmire', 'A52600025868', '8928928972', 'susmit4s@gmail.com', '670289bd3cd31cb5d2d066cd'],
                ['Dream home/ nisha maskara', 'A52100021480', '9657424242', 'insurance.nisha@gmail.com',
                 '673335dbbbd062497bf4f660'],
                ['Dream nest', 'A52100013686', '7906831859', 'dreamnest07@gmail.com', '66f64647e23ec89ee8d68937'],
                ['Dream nest', 'A52100013686', '7906831859', 'dreamnest07@gmail.com', '66f64647e23ec89ee8d68937'],
                ['Dreams true realty', 'A51700024607', '8169842080', 'dreamstruerealty@gmail.com',
                 '673595f85a2ed3e110ba65c8'],
                ['Dream yards property consultants', 'A52100044181', '8390933555', 'rajendradhumal50@gmail.com',
                 '6736e7ee5a2ed3e110c43713'],
                ['Dweller pro', 'A52100042689', '9696467802', 'dwpro64@gmail.com', '672db19a96c7b44194b7ae7c'],
                ['Dwello', 'A51900000277', '7506177964', 'himanshu@dwello.com', '66d2cba5f20fc3269c7b0cfb'],
                ['Ecoview properties pvt ltd', 'A52100036807', '9921628292', 'babasahebsalgar@gmail.com',
                 '67011fd43cd31cb5d2cefb31'],
                ['Elite properties', 'A52100014212', '9985768190', 'eliteproperties57@gmail.com',
                 '670652fa3cd31cb5d2d4230f'],
                ['Esprit homes', 'A52100016153', '8551040205', 'subhamdeshmukh@esprithomes.in',
                 '671a027d191a10121002aecf'],
                ['Estate fort consulting', 'A52100027516', '9795980594', 'agmadsuhail.2010@gmail.com',
                 '671f5edd6cf8eb0757959dee'],
                ['Estatepedia llp', 'A52100019543', '8007776246', 'info@estatepedia.co.in',
                 '67139b55191a101210fea6c6'],
                ['First door realty', 'A52100038557', '9209214897', 'vivek@firstdoorrealty.com',
                 '66ffc1843cd31cb5d2ce1656'],
                ['Ravikant govardhan linge Flooricks Homes', 'A52100031282', '7420062981',
                 'floorickshomes@gmail.com',
                 '6704cebd3cd31cb5d2d197a0'],
                ['Fs homes', 'A52100047250', '9175593118', 'fshomes@gmail.com', '6721d9aeceda5e2444ea46ea'],
                ['Suraj suresh singh', 'A52100037191', '8208158225', 'fsrealty.sales1@gmail.com',
                 '67388a2f6d19f5adcaf8930f'],
                ['Propelite realty', 'A52100037278', '7028782431', 'sunnyrrajc@gmail.com',
                 '6739b309f92881c0b407c9d6'],
                ['Field fox realtors', 'A52100031569', '9022484870', 'shaikhaarif362@gmail.com',
                 '67231a66ceda5e2444f0b9f2'],
                ['Flatconn', 'A52100018378', '9356569522', 'pravin96.flatconrealtors@gmail.com',
                 '670241703cd31cb5d2cffffc'],
                ['Amit sharad sonawane first Flat property', 'A52100033893', '8656814151',
                 'sejalpatils23@gmail.com',
                 '672c5becdc249b2bd716fcea'],
                ['Future Bricks', 'A52100022479', '9673000053', 'futurebricks@gmail.com',
                 '6720bd026cf8eb075798718c'],
                ['Future Bricks', 'A52100022479', '9673000053', 'futurebricks@gmail.com',
                 '6720bd026cf8eb075798718c'],
                ['Ganesh Rajendra Chavan', 'A52100039988', '9146146165', 'ganeshchavanpatil07@gmail.com',
                 '66ffbf653cd31cb5d2ce1204'],
                ['Global homes', 'A52000013825', '9022777666', 'globalhome93@gmail.com',
                 '672da41496c7b44194b76f17'],
                ['Gr realty', 'A52100044171', '7208205055', 'grrealty4@gmail.com', '67231468ceda5e2444f05141'],
                ['Ganesh Rajendra Chavan', 'A52100039988', '9146146165', 'ganeshchavanpatil07@gmail.com',
                 '66ffbf653cd31cb5d2ce1204'],
                ['Gaura realtors', 'A52400033236', '8554924977', 'yelikar.ravi@gmail.com',
                 '673ee0bb997820df93f0e759'],
                ['Gourav gupta exceed venture', 'A52100026073', '9545779786', 'gauravgupta@yahoo.com',
                 '6730586964f82e5d6414e629'],
                ['Ga properties', 'A52100046049', '8766575658', 'ga.property01@gmail.con',
                 '673b2ea5f92881c0b417337f'],
                ['Vinit', 'A52100047757', '8605117615', 'vntktr@gmail.com', '6720ec8dceda5e2444e778b5'],
                ['Mode arch associate', 'A51800009501', '8832584345', 'mod.arch@gmail.com',
                 '673746206d19f5adcaf07cfc'],
                ['Global realtors', 'A52100000018', '8550990851', 'globalrealtorspune@gmail.com',
                 '672728f8f1c39668e3024af0'],
                ['Globein realty', 'A52100043919', '8329866768', 'shubhambagul21@gmail.com',
                 '6702999d3cd31cb5d2d0bcba'],
                ['Golden arrow realty', 'A52100033205', '9673671335', 'saurabhbhagwat32@gmail.com',
                 '6721eca4ceda5e2444ebddb4'],
                ['Rohan datta kawade golden key', 'A52300041381', '7499030399', 'rohan.kawade@gmail.com',
                 '6721c7afceda5e2444e8ab9d'],
                ['Goodlife properties', 'A52100022765', '9172856985', 'goodlifeproperties@gmail.com',
                 '67225eebceda5e2444efe1fb'],
                ['Grassroot', 'A51800045744', '8104970556', 'sunil.asrani@grassrootproperties.com',
                 '673301f5bbd062497bf2c958'],
                ['Bookmyvastu', 'A52100042145', '7558310187', 'skbookmyvastu@gmail.com',
                 '672a1352ca4700b10335fb27'],
                ['Heaven properties', 'A51700030077', '8800678921', 'heavenproperties@gmail.com',
                 '67275f16f1c39668e302fad9'],
                ['Homified consultant', 'A52100023900', '7588238863', 'homified.sales@gmail.com',
                 '6720d4ccd2fc37ef41bdbdb6'],
                ['Horizon financial', 'A51800001892', '9892851251', 'horizonfinancial@gmail.cpm',
                 '66cb35bb1182e1e14dc49830'],
                ['Happy homes', 'A52100023203', '8087622292', 'rajudavhale2084@gmail.com',
                 '66f4fb87e23ec89ee8d62d89'],
                ['Harshal patil unicorn properties', 'A52100039464', '7276748797',
                 'unicornproperties8797@gmail.com',
                 '672f5f1d64f82e5d641319fd'],
                ['Headways realty', 'A51700008078', '7378590959', 'pintu.debnath@headwaysrealty.com',
                 '66e7ef66fd1c56fbbea0f611'],
                ['Hello home real estate pankaj uttam aher', 'A52200040437', '7219184500',
                 'pankajaher222@gmail.com',
                 '6733248dbbd062497bf3de16'],
                ['Namrata jagdish kariya homehunt realty', 'A52100027203', '9890678805',
                 'namratajagdishkariya@gamil.com', '672cf78712e113376cce8760'],
                ['Home minister realty', 'A51700010876', '9224375453', 'nagesh.gosavi@gmail.com',
                 '670962c33cd31cb5d2d77799'],
                ['Home bazar', 'A52000000045', '8976931102', 'akshay.srinivasan@homebazar.com',
                 '66ff9f263cd31cb5d2cdd52d'],
                ['Namrata jagdish kariya homehunt realty', 'A52100027203', '9890678805',
                 'namratajagdishkariya@gamil.com', '672cf78712e113376cce8760'],
                ['Homemart realtor', 'A52100035311', '8459419936', 'homemartrealtors11@gmail.com',
                 '66f502e7e23ec89ee8d63c3a'],
                ['Homesca realtors pvt ltd', 'A52100041007', '8767888415', 'info@homescarealtors.com',
                 '671b8ca7191a101210039491'],
                ['Abhishek rajeev sawargaonkar (Hooterbux Realty)', 'A52100022515', '9011035350',
                 'abhishek@hooterbux.com', '6735c8cd5a2ed3e110bc17b3'],
                ['Suryaji duryodhan shrikhande House Mart Properties', 'A52100014943', '9325336230',
                 'housemartrealtor@gmail.com', '66f50570e23ec89ee8d64116'],
                ['House of bhk', 'A52100042410', '9284184089', 'houseofbhk1@gmail.com', '66f4ffffe23ec89ee8d637c3'],
                ['Housing Mantra', 'A52100044378', '7888041188', 'housingmantrapune@gmail.com',
                 '67028af73cd31cb5d2d06c52'],
                ['Nitesh shrivastav zuko homes', 'A52100028391', '9049345418', 'zukohomesindia@gmail.com',
                 '671ce6986cf8eb075793deff'],
                ['Imagine homeland pvt ltd', 'A52100043466', '9607371144', 'imaginehomeland@gmail.com',
                 '66f10645e23ec89ee8d5bc0d'],
                ['Anish vijay vichare Investors Hub', 'A52000043773', '7715976818', 'anish.vichare025@gmail.com',
                 '672da74496c7b44194b775b8'],
                ['Sagar mahadev varat Infinity Home', 'A52100030343', '9890524744', 'varatsagar15@gmail.com',
                 '66f4f918e23ec89ee8d62bdd'],
                ['Dhananjay thakare', 'A49800038493', '9373630007', 'dhananjaygthakare2244@gmail.com',
                 '66f7ccfb390dfbaa310e4b0d'],
                ['Skyo properties', 'A52100034450', '8329629288', 'skyoproperties@gmail.com',
                 '671cb43d191a10121004056a'],
                ['Infy dimensions', 'A52100028755', '8108431388', 'infydimension@gmail.com',
                 '672318c5ceda5e2444f08875'],
                ['Vikas Sahadev Gayakavad', 'A52100036223', '8308660668', 'vksgaikawad@gmail.com',
                 '66ffcc573cd31cb5d2ce4156'],
                ['Jp associate', 'A51700018038', '9867613486', 'jpassociate@gmail.com', '66d44fa9f20fc3269c7b51b8'],
                ['Jones lang lasalle property consultant', 'A51900000251', '8149569554', 'akshay.arvind@jll.com',
                 '66fe9b87cf515f2c0ab73a53'],
                ['Kumar Balasaheb Ranawade', 'A52100032221', '9657333433', 'sanjaylic@gmail.com',
                 '66f4f564e23ec89ee8d627d3'],
                ['Key mansion pvt ltd', 'A51900001761', '8976745049', 'ronak.keymansions@gmail.com',
                 '66f7ed22390dfbaa310e845e'],
                ['Roop Kumar', 'A52100030870', '9104441976', 'roopkumardm@gmail.com', '66ff85f73cd31cb5d2cd9ec7'],
                ['Remax v21', 'A52100012415', '9657176006', 'remaxv21@gmail.com', '670ce43d3cd31cb5d2da4448'],
                ['Swapnil chopade', 'A50000037255', '8806364765', 'chopde.swapnil@gmail.com',
                 '670a876f3cd31cb5d2d89cb2'],
                ['Mothers home', 'A52100035675', '9325971847', 'motherhome62@gmail.com',
                 '66f2a1e5e23ec89ee8d616c5'],
                ['Kunvarji Realty Advisors', 'A51800007837', '7574007054', 'properties@kunvarjirealty.com',
                 '66fe3eb90df68ea759692177'],
                ['Pankaj vijayakumar shirsath Key Housing', 'A51500043829', '7410767664', 'thevicky2688@gmail.com',
                 '66f4f322e23ec89ee8d6275a'],
                ['Anish ravat krom realtors', 'A52100030505', '7385694200', 'realtorskrom@gmail.com',
                 '672c92c4514072df405e3421'],
                ['Kunvarji Realty Advisors', 'A51800007837', '7574007054', 'properties@kunvarjirealty.com',
                 '66fe3eb90df68ea759692177'],
                ['Kutumbh realty ananda more', 'A52100026936', '8956490049', 'kutumbh.realty@gmail.com',
                 '671492f0191a101210ff6204'],
                ['Laxmi Realty', 'A52100003426', '9960319771', 'info.laxmirealty@gmail.com',
                 '672dfc937f659ef37e2c863e'],
                ['Lord Estate Roney Tilwani', 'A51700005828', '9820505154', 'lordestate@gmail.com',
                 '66d1b096f749684225d74356'],
                ['Luxury realty', 'A52100045628', '7722093913', 'luxury.realty07@gmail.com',
                 '66fe2bc60df68ea75968f6d8'],
                ['People 1st home', 'A52100042318', '7498521789', 'laxmikant.kadam@gmail.com',
                 '670a66ae3cd31cb5d2d81055'],
                ['Life space property solutions pvt ltd', 'A52100000993', '8446500016', 'lspscrm426@gmail.com',
                 '66f7eb5e390dfbaa310e8325'],
                ['Hrishikesh shridhar naikade', 'A52100024902', '7020098426', 'mavenspaces@gmail.com',
                 '670a4ebd3cd31cb5d2d7dbf1'],
                ['Mdn salesforce pvt ltd', 'A52100017448', '8380061188', 'mdnsalesforce@gmail.com',
                 '67125978191a101210fdb9ff'],
                ['Metro homes', 'A52100043797', '7879740777', 'metrohomespune@gmail.com',
                 '66f51da6e23ec89ee8d667d8'],
                ['MG Realtys', 'A52100036539', '8698315802', 'mgrealtys01@gmail.com', '66fe885b672c6c76d62f0068'],
                ['Mahesh koli mjk reality', 'A51700039752', '9870668712', 'mjkkoli@gmail.com',
                 '6730903164f82e5d64178299'],
                ['Ms prop', 'A52100026018', '7028283566', 'mahipawar0908@gmail.com', '670132b63cd31cb5d2cf1155'],
                ['Suresh Dattatray Pokale', 'A52300043706', '7620171210', 'pokalesuresh778899@gmail.com',
                 '66f921c6390dfbaa310f4145'],
                ['Vikas Sahadev Gayakavad', 'A52100036223', '8308660668', 'vksgaikawad@gmail.com',
                 '66ffcc573cd31cb5d2ce4156'],
                ['Magic homes', 'A52100046666', '9130029521', 'magichomes1208@gmail.com',
                 '66f10a38e23ec89ee8d5bef7'],
                ['Magic stone spaces llp', 'A52100024317', '9067769949', 'nilesh.deshmukh@magicstoneprop.com',
                 '66fe2d990df68ea75968fa8d'],
                ['Vijay uttam jadhav Maha Homes', 'A52100031504', '8055245580', 'office.vijay23@gmail.com',
                 '66efb0c1e23ec89ee8d58f2e'],
                ['Santosh datta kale', 'A52100018096', '8888493049', 'sumitdkale22@gmail.com',
                 '672cbbff12e113376ccd9853'],
                ['Dream housing mahesh babar', 'A52100019168', '7559456169', 'dreamhousing@gmail.com',
                 '672df2157f659ef37e2bb4a2'],
                ['Swastik group', 'A52100011463', '9766502949', 'mayurbrains@gmail.com',
                 '672c9e2c514072df405ebac1'],
                ['Umesh laxman baravkar Milestone Realty', 'A52100041773', '9403774225',
                 'milestonerealty55@gmail.com',
                 '66f4f759e23ec89ee8d629b1'],
                ['Sonu Dattu Shelke', 'A52100041730', '9356664656', 'modernreality23@gmail.com',
                 '66ff917e3cd31cb5d2cdba78'],
                ['Nestor properties', 'A52100036952', '8055256357', 'nestorpropertiespune@gmail.com',
                 '672b468bdc249b2bd715d5ac'],
                ['Nohra', 'A52100045810', '7040379765', 'nohararealtor@gmail.com', '6700e78c3cd31cb5d2ce9a68'],
                ['The proprightway group', 'A52100027405', '9373509567', 'asarammundhe01@gmail.com',
                 '6736ed775a2ed3e110c4be50'],
                ['Nidhi hrishikesh gokhle parth magic', 'A52100032366', '9359280265', 'nidhi.parthmagic@gmail.com',
                 '670290bb3cd31cb5d2d08b73'],
                ['Pune pride property', 'A52100027805', '7755942853', 'puneprideproperties@gmail.com',
                 '6708ebaf3cd31cb5d2d6ed44'],
                ['Nirvana homes', 'A52100032894', '7385591610', 'nirvanahomepune@gmail.com',
                 '66f7d550390dfbaa310e5cfc'],
                ['Nitesh shrivastav zuko homes', 'A52100028391', '9049345418', 'zukohomesindia@gmail.com',
                 '671ce6986cf8eb075793deff'],
                ['Nobroker Technologies Solutions Private Limited', 'A51800026821', '9769018719',
                 'kundansingh@nobroker.com', '66c9a8c62d1f5525cdd75989'],
                ['Nobroker Technologies Solutions Private Limited', 'A51800026821', '9769018719',
                 'kundansingh@nobroker.com', '66c9a8c62d1f5525cdd75989'],
                ['Octopus arms', 'A52100030484', '9284624395', 'shrikant.somvanshi@gmail.com',
                 '67064f193cd31cb5d2d40cdb'],
                ['Siddhant ravindra deshmukh Oikos Realty', 'A52100047988', '7620790857',
                 'kasarechaitanya777@gmail.com', '66f513f3e23ec89ee8d651c2'],
                ['Opera homes', 'A52100028045', '8482887686', 'operahomesranjeet@gmail.com',
                 '672329ebceda5e2444f1b73e'],
                ['Option one', 'A52100046539', '8080826913', 'option1dg@gmail.com', '6720acef6cf8eb075797cf9c'],
                ['Krystal realtors', 'A52100040750', '7972524726', 'adoankaj001@gmail.com',
                 '672339bbceda5e2444f222f2'],
                ['Rohit Radhu Temgire', 'A52100047725', '9503280891', 'partnerpulse2425@gmail.com',
                 '66ff84d33cd31cb5d2cd9cb9'],
                ['Pn properties', 'A52300012780', '8087799875', 'pankaj.n@gmail.com', '6720f046ceda5e2444e787e5'],
                ['Prop hunter property solutions', 'A52100043214', '7709276978', 'rahul.prophunter@gmail.com',
                 '66f90d48390dfbaa310f217c'],
                ['Prop earth', 'A52000035786', '8422035777', 'ref.tech.111@gmail.com', '673844336d19f5adcaf48f9a'],
                ['Property boyz', 'A52000033274', '7209415261', 'propertyboyz@gmail.com',
                 '67347efabbd062497bf9ec72'],
                ['Tejes Amrutsing Patil (property concepts)', 'A52100034439', '9552285000',
                 'info@propertyconcepts.in',
                 '6721b7eeceda5e2444e804ee'],
                ['Property guru', 'A51700043110', '8484840019', 'propertyguru1@gmail.com',
                 '6734a8a25a2ed3e110b8a882'],
                ['Saurabh kumar PropRock', 'A52100025007', '9049999011', 'saurabh.kumar@proprock.in',
                 '66f7dc95390dfbaa310e675c'],
                ['Proptiger Marketing Services Private Limited', 'A51700000030', '9850046595',
                 'ashish.singh@proptiger.com', '66e7dfb3fd1c56fbbea0f28f'],
                ['Prop vastu', 'A52100036143', '9322472131', 'propvasturealtorspvtltd@gmail.com',
                 '672f382f64f82e5d64100ab2'],
                ['Propweb', 'A52000019540', '7000982212', 'info@propweb.in', '6720befb6cf8eb0757987a52'],
                ['Pravin keshavrao pawar', 'A52100038873', '9322124256', 'pravinpawar@gmail.com',
                 '6738480a6d19f5adcaf4e870'],
                ['Padale properties', 'A52100030619', '9028124339', 'padaleproperties5@gmail.com',
                 '67222665ceda5e2444eec66e'],
                ['Pan india properties', 'A52100001922', '9021797338', 'sambanerjee@gmail.com',
                 '671a2a0b191a10121002e2d2'],
                ['Nidhi hrishikesh gokhle parth magic', 'A52100032366', '9359280265', 'nidhi.parthmagic@gmail.com',
                 '670290bb3cd31cb5d2d08b73'],
                ['Empire Property', 'A52100014727', '9850643336', 'pawanlalwani19@gmail.com',
                 '66ffc2d83cd31cb5d2ce1b5d'],
                ['Pearl quest', 'A52100001979', '8956339151', 'sales@pearlquest.in', '66f0fc24e23ec89ee8d5b457'],
                ['Pentagon Properties', 'A52100047697', '9527068313', 'vborkar313@gmail.com',
                 '6700e9f63cd31cb5d2cea08c'],
                ['Puneet pentagon', 'A09600029014', '7304600205', 'pentagon@gmail.com', '66e6e627fd1c56fbbea0e111'],
                ['Akshay anand gaikwad', 'A52100042582', '9699820978', 'akkigaikwad1043@gamil.com',
                 '66ff8e843cd31cb5d2cdb5b7'],
                ['Perfect homeland properties', 'A52100036578', '9371815043', 'perfecthomeland04@gmail.com',
                 '6700fca33cd31cb5d2ceb6b0'],
                ['Pratishtha homes', 'A99000019663', '8771778514', 'pratishthahomes@gmail.com',
                 '67347f4fbbd062497bf9f09f'],
                ['Primecitys properties com llp', 'A52100036070', '7666833366', 'info@primecityproperties.com',
                 '672067ce6cf8eb0757960c62'],
                ['Prime estate', 'A52100037496', '8888999303', 'akshay.348@gmail.com', '672dd2937f659ef37e2b2047'],
                ['Pro india realty', 'A52100033900', '9226091843', 'proindiarealty03@gmail.com',
                 '672f0f810f0a678b98d1427b'],
                ['Prop 24', 'A52100033587', '7875395559', 'prop24@gmail.com', '672f00550f0a678b98d092ab'],
                ['Propdeal realtors and consulting pvt ltd', 'A52100007278', '7875349694',
                 'sales.propdeal@gmail.com',
                 '67220e3dceda5e2444ed88b3'],
                ['Propgalaxy', 'A52100045567', '8007941644', 'sales@propgalaxy.in', '670120ca3cd31cb5d2cefc9b'],
                ['Propinn Ventures LLP', 'A52100038976', '8308555333', 'sales@propinn.in',
                 '6707631f3cd31cb5d2d4a91f'],
                ['Prop mystic pvt ltd', 'A57200037443', '8600610449', 'propmystic@gmail.com',
                 '67399754f92881c0b405b68d'],
                ['Abhishek rajkumar', 'A52100034414', '8381015294', 'pooja950pooja@gmail.com',
                 '6729ae2df48fecec2500a1dc'],
                ['Prop vastu', 'A52100036143', '9322472131', 'propvasturealtorspvtltd@gmail.com',
                 '672f382f64f82e5d64100ab2'],
                ['Propweb', 'A52000019540', '7000982212', 'info@propweb.in', '6720befb6cf8eb0757987a52'],
                ['Propbizz Real Estate', 'A52100039446', '8668890256', 'admin@propbizz.com',
                 '66f7b337390dfbaa310e27af'],
                ['Property discuss', 'A52100015342', '9540307979', 'punepropertydiscuss@gmail.com',
                 '66f4fd53e23ec89ee8d630b8'],
                ['Property pistol', 'A51700000043', '8484002302', 'propertypistol@gmail.com',
                 '67028c993cd31cb5d2d07417'],
                ['Propertydotpune', 'A52100047662', '9075163145', 'propertydotpune@gmail.com',
                 '672cfe3012e113376cce8df5'],
                ['Property plaaza', 'A51700009699', '9619871855', 'bikas.hbarnwal@gmail.com',
                 '66d2b33af20fc3269c7b01f7'],
                ['Property professionals', 'A52100047541', '7447311506', 'yogi.anu007@gmail.com',
                 '672ca51812e113376ccccc5f'],
                ['Propitious properties private limited', 'A52100040012', '8261887584',
                 'ovk.propitiousprop@gmail.com',
                 '6714d47a191a101210ffd699'],
                ['Propmart Technologies Limited', 'A51900028913', '9921112123', 'prakash.dwiwedi@propmart.com',
                 '66f1103ee23ec89ee8d5cac3'],
                ['Propnivesh private limited', 'A52100024528', '7219062982', 'aditya.jain@propnivesh.com',
                 '672cbdfc12e113376ccda8ea'],
                ['Proprise', 'A52100025032', '9112001494', 'director@proprise.co.in', '66f4ff06e23ec89ee8d63692'],
                ['Proprise', 'A52100025032', '9112001494', 'director@proprise.co.in', '66f4ff06e23ec89ee8d63692'],
                ['Prop solution realtech pvt ltd', 'A52100032616', '8103655558', 'aniketpropsolution@gmail.com',
                 '670a5b0b3cd31cb5d2d7f293'],
                ['Prop Tech Homes', 'A52100030203', '7249075924', 'proptechpune@gmail.com',
                 '66f80364390dfbaa310eb0f2'],
                ['Proptiger Marketing Services Private Limited', 'A51700000030', '9850046595',
                 'ashish.singh@proptiger.com', '66e7dfb3fd1c56fbbea0f28f'],
                ['Akash balaji madrewar Prop Trees', 'A52400043255', '7666499019', 'proptrees2023@gmail.com',
                 '66f4f868e23ec89ee8d62b97'],
                ['Dreams properties', 'A52100046299', '9881528944', 'sales.dreamsproperties@gmail.com',
                 '6729e5056e0c89b7c41a2669'],
                ['Pune property investor', 'A52100045158', '7070701494', 'na@na.com', '66f93369390dfbaa310f59da'],
                ['Reaholic mediators', 'A52100037865', '8530171188', 'aishwarya@reaholicmediators.com',
                 '67011cc33cd31cb5d2cef345'],
                ['Realty Assistant Private Limited', 'A09300024338', '9311660818',
                 'rakesh.petwal@realtyassistant.in',
                 '66fe9003cb582bd7c92020ff'],
                ['Meetu kiran Realty Essentia', 'A52100021426', '8149992492', 'sales.realtyessentia@gmail.com',
                 '66f65135390dfbaa310da4dd'],
                ['Propwise realtors', 'A52100047813', '8087078084', 'propwiserealtors@gmail.com',
                 '67220e39ceda5e2444ed8897'],
                ['Rajkumar bhosale', 'A52400046304', '9730001423', 'propsnap8@gmail.com',
                 '671cd4d16cf8eb075793b057'],
                ['Star properties', 'A52400039974', '9960203296', 'ramkedari12@gmail.com',
                 '6713a047191a101210feadcf'],
                ['Ramraj realty', 'A52100044779', '7057324580', 'ramrajrealty@gmail.com',
                 '6731f77064f82e5d641d0129'],
                ['Abhang estate ( ranjit magar)', 'A52100042681', '8550015003', 'abhangestates@gmail.com',
                 '67333e9bbbd062497bf52ff0'],
                ['Abhang estate ( ranjit magar)', 'A52100042681', '8550015003', 'abhangestates@gmail.com',
                 '67333e9bbbd062497bf52ff0'],
                ['Nvt Property', 'A52100044265', '7038044015', 'vijay@nvthomes.com', '672afa6fdc249b2bd7141edb'],
                ['Step pyramid properties', 'A52100014293', '7020502538', 'step.pyramidproperties@gmail.com',
                 '673829946d19f5adcaf2061b'],
                ['Real Asset co', 'A52100047046', '7058998484', 'realassetco@gmail.com',
                 '6714e702191a1012100001ea'],
                ['Realty Assistant Private Limited', 'A09300024338', '9311660818',
                 'rakesh.petwal@realtyassistant.in',
                 '66fe9003cb582bd7c92020ff'],
                ['Realty Assistant Private Limited', 'A09300024338', '9311660818',
                 'rakesh.petwal@realtyassistant.in',
                 '66fe9003cb582bd7c92020ff'],
                ['Red leaf realty and investment', 'A52100044540', '9011030800', 'anilagarwal399@gmail.com',
                 '6721fde8ceda5e2444ecde36'],
                ['Regal vastu', 'A52100047997', '7499624306', 'regalvastu21@gmail.com', '672a15e9ca4700b103361538'],
                ['Region realcon private limited', 'A52100020858', '9167877933', 'regionrealcon@co.in',
                 '6720b2dc6cf8eb07579801c4'],
                ['Revaa homes', 'A51800046254', '8898444460', 'mail@revaahomes.com', '67346cdabbd062497bf942a9'],
                ['Right at home', 'A52100042521', '8087520089', 'rightathome0707@gmail.com',
                 '67331851bbd062497bf37757'],
                ['Rising homes', 'A51700004600', '9892226670', 'info@rihosales.in', '672e18a57f659ef37e2f13e7'],
                ['] (Vastulaxmi Properties) Rohan shivaji shinde', 'A52100036407', '8830257676',
                 'vastulaxmi157@gmail.com', '6729adb6f48fecec25009f93'],
                ['Rohit kothare', 'A52100025164', '8329808605', 'irohitkothare@gmail.com',
                 '66f640bee23ec89ee8d683b4'],
                ['Risina nadir nilgiriwala', 'A52100031577', '9673667866', 'rozinanadir2323@gmail.com',
                 '672cbc9a12e113376ccd9ec6'],
                ['Sb realty', 'A52100046899', '7276099174', 'snehalbhalerao@gmail.com', '672cbb3812e113376ccd8ecb'],
                ['Sp investment', 'A52100024290', '9823168586', 'spinvestment113@gmail.com',
                 '67124a1e191a101210fda9b2'],
                ['San global', 'A52100033789', '9884866973', 'deepaksurana@sanglobal.co.in',
                 '672c5db1dc249b2bd7170fad'],
                ['Si property and consultant sanket ingulkar', 'A52100030079', '8668355993', 'siproperty@gmail.com',
                 '6721f726ceda5e2444ec912c'],
                ['Sd realty', 'A52100047517', '9764663666', 'sdrealty@gmail.com', '672cc44212e113376cce27c1'],
                ['Shivaji Nathuram Chavan', 'A52100042472', '8830495871', 'chavanshivaji546@gmail.com',
                 '67013cc33cd31cb5d2cf28ff'],
                ['Siddhant ravindra deshmukh Oikos Realty', 'A52100047988', '7620790857',
                 'kasarechaitanya777@gmail.com', '66f513f3e23ec89ee8d651c2'],
                ['Sk homes', 'A52100022613', '8552829334', 'skhomesproperties@gmail.com',
                 '66f7a582390dfbaa310e01b6'],
                ['Smc real estate advisors pvt ltd', 'A51900000042', '9156647777', 'vaibhavr@smcrealty.com',
                 '67024af53cd31cb5d2d013e8'],
                ['Santosh sopan magar', 'A52100039085', '9881391010', 'santoshmagar.32@gmail.com',
                 '672caf1312e113376ccd1af8'],
                ['Ss prime infra', 'A52100044653', '9833789560', 'ravi.ssprimeinfra@gmail.com',
                 '672b280adc249b2bd7156527'],
                ['Sunil mohan takawane ST Properties', 'A52100035303', '9767070162', 'stproperties7@gmail.com',
                 '66f94a83390dfbaa310f9ff9'],
                ['Suryaji duryodhan shrikhande House Mart Properties', 'A52100014943', '9325336230',
                 'housemartrealtor@gmail.com', '66f50570e23ec89ee8d64116'],
                ['Kailash more sai space realtors', 'A52100000417', '7030144001', 'saispacerealtors@gmail.com',
                 '672c9f32514072df405ec560'],
                ['Saijeet realtor', 'A52100000382', '9860040608', 'saijeetrealtor@gmail.com',
                 '67215097ceda5e2444e7f323'],
                ['Samrat spaces pvt. ltd. (sync)', 'A52100023118', '9527964347', 'gajananitax@gmail.com',
                 '672f1e480f0a678b98d1c128'],
                ['San global', 'A52100033789', '9884866973', 'deepaksurana@sanglobal.co.in',
                 '672c5db1dc249b2bd7170fad'],
                ['Vision sj realtors sandeep jadhav', 'A52100043556', '8855874189',
                 'visionsjrealtors8855@gmail.com',
                 '672cb2c712e113376ccd476c'],
                ['Sunshine sanjay salvi', 'A52100024208', '9823243444', 'sunshine_estate_pune@yahoo.in',
                 '6730559264f82e5d6414cc27'],
                ['Subak Home', 'A52100043960', '8149800777', 'subakhome@gmail.com', '672e0a467f659ef37e2e29e3'],
                ['Suprim pathare', 'A51700033515', '9820418409', 'suprim.sapphire@gmail.com',
                 '66d32185f20fc3269c7b36b0'],
                ['Sarvadnya realty', 'A52100030337', '9970591143', 'sarvadnyarealty@gmail.com',
                 '672b3175dc249b2bd715b737'],
                ['Satish uttareshwar tambare', 'A52100040906', '9960872957', 'nsutambare@gmail.com',
                 '66f7f311390dfbaa310e8e09'],
                ['Sartun asset wold llp', 'A52100045523', '9371660811', 'admin@sartunassetworld.com',
                 '6729adc6f48fecec25009fd4'],
                ['Scan Reality Private Limited', 'A52100033212', '7972517967', 'thescanreality@gmail.com',
                 '66ff8ff13cd31cb5d2cdb8d8'],
                ['Seventh key', 'A52100046492', '8468824887', 'seventhkey52@gmail.com', '672f619b64f82e5d64135861'],
                ['Shardul bade', 'A52100038187', '9890023467', 'shardul.bade@gmail.com',
                 '6706548b3cd31cb5d2d42619'],
                ['Shelter mentor', 'A52100024539', '9673039673', 'devan.kurwa@sheltormentorpvtltd.com',
                 '67028b283cd31cb5d2d06d28'],
                ['Shelter mentor', 'A52100024539', '9673039673', 'devan.kurwa@sheltormentorpvtltd.com',
                 '67028b283cd31cb5d2d06d28'],
                ['Shivansh Realty', 'A52100046843', '7020325436', 'rahul.singh2838@gmail.com',
                 '6721ccc3ceda5e2444e91906'],
                ['Shivnath sudhakar pache', 'A52100047801', '9730642824', 'shivnathpache1@gmail.com',
                 '66f517cae23ec89ee8d65b61'],
                ['Expertise realty', 'A52100036217', '9637103853', 'shohebrajput@gmail.com',
                 '672cab9d12e113376cccfe81'],
                ['Kiran nandkishor nagpure shree vkirqistaar properties', 'A52100019780', '8669821112',
                 'kirannagpure@gmail.com', '6739eac2f92881c0b40ae6ee'],
                ['Santosh datta kale', 'A52100018096', '8888493049', 'sumitdkale22@gmail.com',
                 '672cbbff12e113376ccd9853'],
                ['Sp investment', 'A52100024290', '9823168586', 'spinvestment113@gmail.com',
                 '67124a1e191a101210fda9b2'],
                ['Dolphin homes', 'A52100039817', '8340703973', 'subhamjsr94@gmail.com',
                 '6722226aceda5e2444ee8335'],
                ['Shubham Suresh Punekar', 'A53000047836', '9021663638', 'shubham.punekar6666@gmail.com',
                 '66f802ac390dfbaa310eaf5c'],
                ['Silver7solutions', 'A52100046790', '8299821051', 'silver7solutions@gmail.com',
                 '66fa4a78390dfbaa310fee61'],
                ['Skyo properties', 'A52100034450', '8329629288', 'skyoproperties@gmail.com',
                 '671cb43d191a10121004056a'],
                ['Satish Rohidas Kajaniya', 'A52100047623', '7219064686', 'satish.k4686@gmail.com',
                 '66f7ac19390dfbaa310e15d8'],
                ['Signature footprint', 'A52100026140', '8693098829', 'somnathjadhav@gmail.com',
                 '672ce6c712e113376cce64bc'],
                ['Sqft 2 Acres', 'A52100029685', '7666313131', 'sqftacres@gmail.com', '66f63e87e23ec89ee8d67fd8'],
                ['Square yards', 'A51800000454', '9970841943', 'avinash.zore@squareyards.co.in',
                 '66ffc5393cd31cb5d2ce2289'],
                ['Star estate', 'A51800037593', '9529351521', 'startestate@gmail.com', '672c83db514072df405da2a4'],
                ['Stepin Property Solution', 'A52100024943', '8767262788', 'stepinpropertysolution@gmail.com',
                 '672e08837f659ef37e2de461'],
                ['Ravikumar singh sunrise realtech', 'A52100032294', '9552445889', 'ravisingh78706@gmail.com',
                 '672096006cf8eb0757972005'],
                ['Surve homes', 'A52100043807', '7385787971', 'surveproperties20@gmail.com',
                 '66f4fe12e23ec89ee8d633d2'],
                ['pinki Swarajya realtors pvt ltd', 'A51700030059', '9004719070', 'dattatraychaudhry@gmail.com',
                 '66d1b79cf749684225d74b02'],
                ['Rachana rajendra katte Swastik Properties', 'A52100038239', '7071414100',
                 'rachanakatte3@gmail.com',
                 '670924b63cd31cb5d2d76a5f'],
                ['Anurag sutar', 'A52100043209', '9923727242', 'swayamrealty21@gmail.com',
                 '6729e21b6e0c89b7c41a20f3'],
                ['Times reality housine private limited', 'A52100044455', '7588623961', 'nitik1108@gmail.com',
                 '672c9378514072df405e3e32'],
                ['Mayuri basavaraj bhusare True Vision Homes', 'A52600037723', '8623029864',
                 'truevisionhomes599@gmail.com', '66f8df8c390dfbaa310eef40'],
                ['Twj infra prosperity realty llp', 'A52100046949', '7058632200', 'prospire@gmail.com',
                 '6720a49e6cf8eb075797a523'],
                ['Take a home', 'A52100047368', '9172798619', 'hello@takeahome.in', '6704ea4f3cd31cb5d2d1b583'],
                ['Tejashri tanaji patil( prop hunt)', 'A52100033447', '9527506362', 'prophuntreality@gmail.com',
                 '672d99e396c7b44194b74f87'],
                ['The lions crew', 'A52100012550', '7276828411', 'info.thelionscrew@gmail.com',
                 '66ff839b3cd31cb5d2cd9aef'],
                ['The Pune Properties', 'A52100047667', '9764656968', 'thepuneproperties95@gmail.com',
                 '6702180c3cd31cb5d2cf6be7'],
                ['The vintage homes', 'A52100040350', '8308396770', 'thevintagehomes@gmail.com',
                 '670b626f3cd31cb5d2d8c2ba'],
                ['Urban nest', 'A52100047645', '9284389060', 'urbanest446@gmail.com', '6729f3996e0c89b7c41aa16b'],
                ['Vasudha properties', 'A52100047234', '9830718818', 'vasudhaproperties5@gmail.com',
                 '671b9723191a10121003a358'],
                ['Vayu realty', 'A51700047118', '8696542094', 'sales@vayurealty.com', '66dc039af20fc3269c7b9bbe'],
                ['Vantage properties', 'A52100029821', '9423345383', 'vantagproperties8721@gmail.com',
                 '671c7e33191a10121003b4f7'],
                ['] (Vastulaxmi Properties) Rohan shivaji shinde', 'A52100036407', '8830257676',
                 'vastulaxmi157@gmail.com', '6729adb6f48fecec25009f93'],
                ['Abhijeet manathkar Vastu Nivesh', 'A51100030603', '9923548383', 'manathkar.abhi@gmail.com',
                 '6720c1056cf8eb075798a2e3'],
                ['Propkeeper', 'A52100020942', '7020708163', 'venkteshdhondale11@gmail.com',
                 '672de2cc7f659ef37e2b603c'],
                ['Verified builders cab service', 'A52100047862', '7972696963', 'balajiangjal@gmail.com',
                 '66ff7e6f3cd31cb5d2cd8d7c'],
                ['Vighnaharta Property', 'A52100044065', '7796200555', 'prajaktaaarote4@gmail.com',
                 '66f9233b390dfbaa310f41a9'],
                ['Vijay uttam jadhav Maha Homes', 'A52100031504', '8055245580', 'office.vijay23@gmail.com',
                 '66efb0c1e23ec89ee8d58f2e'],
                ['Vinod shinde', 'A52400043813', '8010349454', 'vinodshinde88@gmail.com',
                 '672caa6412e113376cccf29f'],
                ['Vikas nivrutti jorwar', 'A52100022272', '9673074193', 'vikasjorwar@gmail.com',
                 '672cecbb12e113376cce769e'],
                ['Vikramsinha sudhir patil vikram realty', 'A52100034885', '9359810081', 'support@vikramrealty.com',
                 '6734d2f35a2ed3e110b97b19'],
                ['Vm properties', 'A52100040861', '9284959303', 'bochkariraj@gmail.com',
                 '6708f9b33cd31cb5d2d70c55'],
                ['Vinay mishra 24estates next wave property solution', 'A52100009669', '8767617895',
                 'varun@24estates.co.in', '6720c5ba6cf8eb075798efaa'],
                ['Vinod vikram bhange VB realtors', 'A52100029465', '9175662222', 'vinodbhange04@gmail.com',
                 '66f91c29390dfbaa310f3841'],
                ['Vipin Bagul Property Advisory Group', 'A52100046791', '7768972164',
                 'vipinasbusinessdeveloper@gmail.com', '66f51070e23ec89ee8d64b6b'],
                ['Destiny homes', 'A52100030857', '7999290219', 'vipuljaiswaldestinyhomes@gmail.com',
                 '6720ed76ceda5e2444e77ad2'],
                ['Vishal tanaji dabhane', 'A52100029799', '9673642865', 'vishaldabhane12199@gmail.com',
                 '6720bbed6cf8eb0757986974'],
                ['Vishesh jalan right manak 4 u', 'A52100039292', '9957225486', 'visheshjalan32@gmail.com',
                 '673f291e02c4100b3868dc93'],
                ['Nexus reality group', 'A52100037089', '8767369097', 'sofiyan@123gmail.com',
                 '6736df9c5a2ed3e110c38125'],
                ['Yes homes', 'A52100017494', '9689090502', 'yeshomes2020@gmail.com', '6708ec1c3cd31cb5d2d6ee59'],
                ['Sankalp sanjay bhandare', 'A52100032764', '7709024049', 'info.yolohomes@gmail.com',
                 '672cb68912e113376ccd5f29'],
                ['Xprop realty', 'A52100041231', '8421292095', 'yogeshdoke95@gmail.com',
                 '672e00547f659ef37e2d2a38'],
                ['Vijay Sambhaji Mane', 'A52100038334', '8600495363', 'vijaymane607@gmail.com',
                 '66f7a824390dfbaa310e0c0d'],
                ['Nitesh shrivastav zuko homes', 'A52100028391', '9049345418', 'zukohomesindia@gmail.com',
                 '671ce6986cf8eb075793deff'],
                ['pinki Swarajya realtors pvt ltd', 'A51700030059', '9004719070', 'dattatraychaudhry@gmail.com',
                 '66d1b79cf749684225d74b02'],

            ]
            for record in data:
                name = record[0]
                rera_number = record[1]
                mobile = record[2]
                email = record[3]

                partner = request.env['res.partner'].sudo().search(
                    [('is_channel', '=', True),
                     # ('name', '=', name),
                     ('rera_number', '=', rera_number),]
                    # ('mobile', '=', mobile),
                    # ('email', '=', email)]
                    , limit=1)
                if partner:
                    cp_id = record[4]
                    partner.jv_cp_id = cp_id

            return "Partners updated successfully"

    @http.route(['/correct_flat_draft_booking'], type='http', auth="public")
    def correct_flat_draft_booking(self):
        if request.env.user.has_group('base.group_system'):
            flats = request.env['product.template'].search([('is_property', '=', True), ('state', '=', 'free')])
            for flat in flats:
                booking = request.env['unit.reservation'].search([('building_unit', '=', flat.id), ('state', '=', 'draft')])
                if booking:
                    flat.state = 'draft_booking'
            return 'Success'
        else:
            return 'Access Denied'

    @http.route(['/correct_user_access_control'], type='http', auth="public")
    def correct_user_access_control(self):
        if request.env.user.has_group('base.group_system'):
            data = {
                'allow_booking_confirm_backdate': 'itsys_real_estate.group_booking_confirm_backdate',
                'show_booking_cancel': 'itsys_real_estate.group_booking_cancel',
                'show_booking_reset_to_draft_in_confirm_state': 'itsys_real_estate.group_booking_reset_to_draft_confirmed',
                'booking_cancel_anytime': 'itsys_real_estate.group_booking_cancel_anytime',
                'show_booking_reset_to_draft': 'itsys_real_estate.group_booking_reset_to_draft',
                'show_evaluation_sheet_term_sheet_budgeting_confirm_button': 'real_estate_sheets.group_evaluation_budgeting_confirm',
                'all_projects_access': 'project_transactions.view_all_projects',
                'booking_confirm_anytime': 'itsys_real_estate.group_booking_confirm_anytime',
                'project_configurations': 'jupiter_accounts.group_project_configurations',
                'dashboard_3': 'jupiter_dashboard_tres.group_jupiter_dashboard_tres',
                'incentive_rate_slab_date': 'jupiter_accounts.edit_incentive_rate_slab_date',
            }
            users = request.env['res.users'].search([])
            for user in users:
                for item in data:
                    if user.has_group(data[item]):
                        request.env.cr.execute(f'update res_users set {item} = True where id = {user.id}')
                    else:
                        request.env.cr.execute(f'update res_users set {item} = False where id = {user.id}')
            return 'Success'
        else:
            return 'Access Denied'

    @http.route(['/merge_configurations'], type='http', auth="public")
    def merge_configurations(self):
        if request.env.user.has_group('base.group_system'):
            configurations = request.env['building.unit'].search([])
            duplicates = configurations.filtered(lambda x: '***' in x.name)
            originals = configurations.filtered(lambda x: '***' not in x.name)
            for dup in duplicates:
                name = dup.name.replace('***', '').replace(' ', '')
                original_conf = originals.filtered(lambda x: x.name.lower().replace(' ', '') == name.lower())
                print(dup.name, name, original_conf, original_conf.name)
                request.env.cr.execute(f'update product_template set flat_type = {original_conf.id} where flat_type = {dup.id}')
                request.env.cr.execute(f'update project_building_unit_rel set config_id = {original_conf.id} where config_id = {dup.id}')
                request.env.cr.execute(f'update unit_reservation set flat_type = {original_conf.id} where flat_type = {dup.id}')
                request.env.cr.execute(f'update project_registration set unit_type = {original_conf.id} where unit_type = {dup.id}')
                request.env.cr.execute(f'update competition_sheet set configuration = {original_conf.id} where configuration = {dup.id}')
                request.env.cr.execute(f'update budget_sheet_building_unit_rel set building_unit_id = {original_conf.id} where building_unit_id = {dup.id}')
                request.env.cr.execute(f'update building_unit_evaluation_sheet_rel set building_unit_id = {original_conf.id} where building_unit_id = {dup.id}')
            dup_str = ','.join([str(item.id) for item in duplicates])
            request.env.cr.execute(f'delete from building_unit where id in ({dup_str})')
            return 'Success'
        else:
            return 'Access Denied'

    @http.route(['/correct_employee_role'], type='http', auth="public")
    def correct_employee_role(self):
        if request.env.user.has_group('base.group_system'):
            projects = request.env['building'].search([])
            for project in projects:
                for line in project.crm_ids:
                    line.role = 'crm'
                for line in project.closing_manager_ids:
                    line.role = 'closing_manager'
                for line in project.sourcing_manager_ids:
                    line.role = 'sourcing_manager'
                for line in project.closing_tl_ids:
                    line.role = 'closing_tl'
                for line in project.sourcing_tl_ids:
                    line.role = 'sourcing_tl'
                for line in project.marketing_ids:
                    line.role = 'marketing'
                project.business_head_id.role = 'business_head'
                project.site_head_id.role = 'site_head'
                project.cluster_head_id.role = 'cluster_head'
            return 'Success'
        else:
            return 'Access Denied'


    @http.route('/correct_employee_code', type='http', auth='public')
    def correct_employee_code(self):
        if request.env.user.has_group('base.group_system'):
            doc = [
                ['P0011', 'JUS0092'],
                ['P0016', 'JUS0101'],
                ['P0017', 'JUS0103'],
                ['P0018', 'JUS0104'],
                ['P0019', 'JUS0105'],
                ['P0021', 'JUS0116'],
                ['P0023', 'JUS0130'],
                ['P0024', 'JUS0134'],
                ['M0170', 'JUS0142'],
                ['P0028', 'JUS0161'],
                ['P0029', 'JUS0163'],
                ['P0032', 'JUS0175'],
                ['P0034', 'JUS0178'],
                ['P0036', 'JUS0186'],
                ['P0041', 'JUS0188'],
                ['P0056', 'JUS0213'],
                ['P0058', 'JUS0214'],
                ['P0059', 'JUS0217'],
                ['P0060', 'JUS0224'],
                ['P0061', 'JUS0225'],
                ['P0064', 'JUS0238'],
                ['P0071', 'JUS0248'],
                ['P0072', 'JUS0249'],
                ['P0076', 'JUS0260'],
                ['P0080', 'JUS0257'],
                ['P0081', 'JUS0259'],
                ['P0082', 'JUS0255'],
                ['P0088', 'JUS0275'],
                ['P0089', 'JUS0279'],
                ['P0101', 'JUS0302'],
                ['P0106', 'JUS0311'],
                ['P0112', 'JUS0329'],
                ['P0121', 'JUS0337'],
                ['P0126', 'JUS0343'],
                ['P0134', 'JUS0364'],
                ['P0137', 'JUS0369'],
                ['P0149', 'JUS0394'],
                ['M0283', 'JUS0398'],
                ['P0152', 'JUS0406'],
                ['P0153', 'JUS0405'],
                ['P0154', 'JUS0409'],
                ['P0163', 'JUS0422'],
                ['P0169', 'JUS0435'],
                ['P0171', 'JUS0441'],
                ['M0306', 'JUS0446'],
                ['P0181', 'JUS0461'],
                ['CON005', 'JUS0466'],
                ['P0190', 'JUS0468'],
                ['P0193', 'JUS0475'],
                ['P0194', 'JUS0476'],
                ['P0195', 'JUS0478'],
                ['P0201', 'JUS0485'],
                ['P0209', 'JUS00498'],
                ['P0211', 'JUS0502'],
                ['P0212', 'JUS0505'],
                ['P0218', 'JUS0531'],
                ['P0229', 'JUS0548'],
                ['M0349', 'JUS0554'],
                ['P0232', 'JUS0572'],
                ['P0236', 'JUS0599'],
                ['P0240', 'JUS0622'],
                ['P0241', 'JUS0625'],
                ['P0244', 'JUS0627'],
                ['M0437', 'JUS0638'],
                ['P0248', 'JUS0648'],
                ['P0251', 'JUS0658'],
                ['P0252', 'JUS0661'],
                ['M0439', 'JUS0689'],
                ['M0449', 'JUS0713'],
                ['P0259', 'JUS0709'],
                ['M0462', 'JUS0721'],
                ['P0264', 'JUS0738'],
                ['M0476', 'JUS0742'],
                ['P0269', 'JUS0759'],
                ['P0270', 'JUS0762'],
                ['P0271', 'JUS0760'],
                ['P0281', 'JUS0782'],
                ['M0497', 'JUS0792'],
                ['M0504', 'JUS0805'],
                ['P0284', 'JUS0804'],
                ['P0286', 'JUS0807'],
                ['M0508', 'JUS0813'],
                ['P0287', 'JUS0818'],
                ['M0517', 'JUS0822'],
                ['P0293', 'JUS0830'],
                ['P0297', 'JUS0835'],
                ['P0298', 'JUS0833'],
                ['P0307', 'JUS0866'],
                ['P0309', 'JUS0870'],
                ['P0310', 'JUS0871'],
                ['P0312', 'JUS0884'],
                ['P0318', 'JUS0887'],
                ['M0543', 'JUS0891'],
                ['P0319', 'JUS0899'],
                ['M0552', 'JUS0900'],
                ['M0553', 'JUS0901'],
                ['M0560', 'JUS0907'],
                ['P0320', 'JUS0912'],
                ['P0321', 'JUS0910'],
                ['P0590', 'JUS1514'],
                ['M0858', 'JUS1516'],
                ['M0859', 'JUS2000'],
                ['P0591', 'JUS0591'],
                ['P0592', 'JUS0592'],
                ['M0862', 'JUS593'],
                ['M0860', 'JUS594'],
                ['M0861', 'JUS595'],
                ['JUS596', 'JUS596'],
            ]
            count = 0
            no_emp = []
            for i in doc:
                employee = request.env['hr.employee'].search([('barcode', '=', i[0])])
                employee_exist = request.env['hr.employee'].search([('barcode', '=', i[1])])
                if employee and not employee_exist:
                    count += 1
                    request.env.cr.execute("update hr_employee set barcode = '%s' where id = %s" % (str(i[1]), str(employee.id)))
                else:
                    no_emp.append(i[0])
            return 'success - ' + str(count) + str(no_emp)
        else:
            return 'Access Denied'

    @http.route(['/correct_developer_master_sequence'], type='http', auth="public")
    def correct_developer_master_sequence(self):
        if request.env.user.has_group('base.group_system'):
            seq = request.env['ir.sequence'].search([('code', '=', 'developer.master.sequence')])
            seq.use_date_range = False
            seq.number_next_actual = 1

            customers = request.env['res.partner'].search(
                [('is_owner', '=', True)], order='id')
            for customer in customers:
                dev_id = request.env['ir.sequence'].next_by_code(
                    'developer.master.sequence')
                request.env.cr.execute("update res_partner set developer_code = '%s' where id = %s" % (str(dev_id), str(customer.id)))
            return 'success'
        else:
            return 'Access Denied'

    @http.route(['/correct_customer_master_code'], type='http', auth="public")
    def correct_customer_master_code(self):
        if request.env.user.has_group('base.group_system'):
            seq = request.env['ir.sequence'].search([('code', '=', 'customer.master.sequence')])
            seq.use_date_range = False
            seq.number_next_actual = 1

            customers = request.env['res.partner'].search(
                [('is_tenant', '=', True)], order='id')
            for customer in customers:
                customer_code = request.env['ir.sequence'].next_by_code(
                    'customer.master.sequence')
                request.env.cr.execute("update res_partner set customer_code = '%s' where id = %s" % (str(customer_code), str(customer.id)))
            return 'success'
        else:
            return 'Access Denied'

    @http.route(['/correct_channel_partner_master_sequence'], type='http', auth="public")
    def correct_channel_partner_master_sequence(self):
        if request.env.user.has_group('base.group_system'):
            seq = request.env['ir.sequence'].search([('code', '=', 'channel.partner.sequence')])
            seq.use_date_range = False
            seq.number_next_actual = 1

            customers = request.env['res.partner'].search(
                [('is_channel', '=', True)], order='id')
            request.env.cr.execute("update res_partner set channel_id = null where is_channel = True")
            for customer in customers:
                channel_id = request.env['ir.sequence'].next_by_code(
                    'channel.partner.sequence')
                request.env.cr.execute("update res_partner set channel_id = '%s' where id = %s" % (str(channel_id), str(customer.id)))
                cp_emp = request.env['res.partner'].search([('is_channel_employee', '=', True), ('parent_id', '=', customer.id)])
                for cpe in cp_emp:
                    request.env.cr.execute(
                        "update res_partner set parent_channel_id = '%s' where id = %s" % (str(channel_id), str(cpe.id)))
            return 'success'
        else:
            return 'Access Denied'

    # @http.route(['/correct_customer_master_sequence/<string:action>/<int:add>'], type='http', auth="public")
    # def correct_customer_master_sequence(self, action, add):
    #     if request.env.user.has_group('base.group_system'):
    #         val = []
    #         customers = request.env['res.partner'].search([('create_date', '>=', '2024-01-01'), ('is_tenant', '=', True)], order='id')
    #         for customer in customers:
    #             customer_code = 'CU' + str(add)
    #             val.append((customer.customer_code, customer_code))
    #             if action == 'update':
    #                 customer.customer_code = customer_code
    #             add += 1
    #         return str(val) + '=====' + str(len(customers))
    #     else:
    #         return 'Access Denied'

    @http.route(['/correct_registration_sequence'], type='http', auth="public")
    def correct_registration_sequence(self):
        if request.env.user.has_group('base.group_system'):
            registrations = request.env['project.registration'].search([('state', 'not in', ('draft', 'canceled'))], order='id')
            for registration in registrations:
                registration.name = request.env['ir.sequence'].next_by_code('sequence.registration')
            drafts = request.env['project.registration'].search([('state', '=', 'draft')])
            for draft in drafts:
                draft.name = 'Draft'
            return 'Success'
        else:
            return 'Access Denied'

    @http.route(['/remove_unused_no_id_employees'], type='http', auth="public")
    def remove_unused_no_id_employees(self, **args):
        if request.env.user.has_group('base.group_system'):
            employees = request.env['hr.employee'].search([('barcode', 'in', (None, False)), ('id', '!=', 1)])
            needed_list = []
            delete_list = []
            for employee in employees:
                if request.env['building'].search([]).filtered(
                        lambda l: employee.id in l.closing_manager_ids.ids or employee.id in l.sourcing_manager_ids.ids or employee.id in l.closing_tl_ids.ids or employee.id in l.sourcing_tl_ids.ids or employee.id in l.crm_ids.ids or employee.id in l.marketing_ids.ids or l.id == l.cluster_head_id.id or l.id == l.business_head_id.id or l.id == l.site_head_id.id):
                    needed_list.append(employee.id)
                else:
                    delete_list.append(employee.id)
            needed_employees = request.env['hr.employee'].search([('id', 'in', needed_list)]).mapped('name')
            deleted_employees = request.env['hr.employee'].search([('id', 'in', delete_list)]).mapped('name')
            print('need', needed_list, request.env['hr.employee'].search([('id', 'in', needed_list)]).mapped('name'))
            print('delete', delete_list, request.env['hr.employee'].search([('id', 'in', delete_list)]).mapped('name'))
            request.env['hr.employee'].search([('id', 'in', delete_list)]).unlink()
            return 'Employees without id needed: ' + str(needed_employees) + '\n' + 'Deleted: ' + str(deleted_employees)
        else:
            return 'Access Denied'

    @http.route(['/correct_employee_user_relation'], type='http', auth="public")
    def correct_employee_user_relation(self, evaluation=None, **args):
        if request.env.user.has_group('base.group_system'):
            users = request.env['res.users'].search([])
            for user in users:
                employee = request.env['hr.employee'].search([('name', '=', user.name)])
                if len(employee) == 1:
                    request.env.cr.execute(
                        'update hr_employee set user_id=' + str(user.id) + ' where id=' + str(employee.id))
            return 'Success'
        else:
            return 'Access Denied'

    @http.route(['/correct_hide_menu_user22'], type='http', auth="public")
    def correct_hide_menu_user22(self):
        if request.env.user.has_group('base.group_system'):
            data = [{'uid': 44, 'menu_id': 84}

                ,{'uid': 44, 'menu_id': 210}

                ,{'uid': 44, 'menu_id': 182}

                ,{'uid': 44, 'menu_id': 114}

                ,{'uid': 44, 'menu_id': 332}

                ,{'uid': 44, 'menu_id': 404}

                ,{'uid': 44, 'menu_id': 246}

                ,{'uid': 44, 'menu_id': 77}

                ,{'uid': 44, 'menu_id': 5}

                ,{'uid': 44, 'menu_id': 4}

                ,{'uid': 13, 'menu_id': 249}

                ,{'uid': 13, 'menu_id': 248}

                ,{'uid': 13, 'menu_id': 84}

                ,{'uid': 13, 'menu_id': 211}

                ,{'uid': 13, 'menu_id': 221}

                ,{'uid': 13, 'menu_id': 258}

                ,{'uid': 13, 'menu_id': 377}

                ,{'uid': 13, 'menu_id': 451}

                ,{'uid': 13, 'menu_id': 324}

                ,{'uid': 13, 'menu_id': 182}

                ,{'uid': 13, 'menu_id': 215}

                ,{'uid': 13, 'menu_id': 216}

                ,{'uid': 13, 'menu_id': 217}

                ,{'uid': 13, 'menu_id': 379}

                ,{'uid': 13, 'menu_id': 384}

                ,{'uid': 13, 'menu_id': 212}

                ,{'uid': 13, 'menu_id': 218}

                ,{'uid': 13, 'menu_id': 381}

                ,{'uid': 13, 'menu_id': 226}

                ,{'uid': 13, 'menu_id': 382}

                ,{'uid': 13, 'menu_id': 114}

                ,{'uid': 13, 'menu_id': 386}

                ,{'uid': 13, 'menu_id': 220}

                ,{'uid': 13, 'menu_id': 389}

                ,{'uid': 13, 'menu_id': 253}

                ,{'uid': 13, 'menu_id': 332}

                ,{'uid': 13, 'menu_id': 404}

                ,{'uid': 13, 'menu_id': 246}

                ,{'uid': 13, 'menu_id': 238}

                ,{'uid': 13, 'menu_id': 229}

                ,{'uid': 13, 'menu_id': 5}

                ,{'uid': 13, 'menu_id': 4}

                ,{'uid': 13, 'menu_id': 232}

                ,{'uid': 13, 'menu_id': 213}

                ,{'uid': 26, 'menu_id': 290}

                ,{'uid': 26, 'menu_id': 249}

                ,{'uid': 26, 'menu_id': 248}

                ,{'uid': 26, 'menu_id': 221}

                ,{'uid': 26, 'menu_id': 258}

                ,{'uid': 26, 'menu_id': 182}

                ,{'uid': 26, 'menu_id': 215}

                ,{'uid': 26, 'menu_id': 216}

                ,{'uid': 26, 'menu_id': 217}

                ,{'uid': 26, 'menu_id': 218}

                ,{'uid': 26, 'menu_id': 226}

                ,{'uid': 26, 'menu_id': 114}

                ,{'uid': 26, 'menu_id': 220}

                ,{'uid': 26, 'menu_id': 253}

                ,{'uid': 26, 'menu_id': 332}

                ,{'uid': 26, 'menu_id': 404}

                ,{'uid': 26, 'menu_id': 246}

                ,{'uid': 26, 'menu_id': 238}

                ,{'uid': 26, 'menu_id': 5}

                ,{'uid': 26, 'menu_id': 4}

                ,{'uid': 26, 'menu_id': 232}

                ,{'uid': 39, 'menu_id': 249}

                ,{'uid': 39, 'menu_id': 248}

                ,{'uid': 39, 'menu_id': 221}

                ,{'uid': 39, 'menu_id': 258}

                ,{'uid': 39, 'menu_id': 377}

                ,{'uid': 39, 'menu_id': 182}

                ,{'uid': 39, 'menu_id': 215}

                ,{'uid': 39, 'menu_id': 216}

                ,{'uid': 39, 'menu_id': 217}

                ,{'uid': 39, 'menu_id': 218}

                ,{'uid': 39, 'menu_id': 226}

                ,{'uid': 39, 'menu_id': 114}

                ,{'uid': 39, 'menu_id': 220}

                ,{'uid': 39, 'menu_id': 389}

                ,{'uid': 39, 'menu_id': 253}

                ,{'uid': 39, 'menu_id': 332}

                ,{'uid': 39, 'menu_id': 404}

                ,{'uid': 39, 'menu_id': 246}

                ,{'uid': 39, 'menu_id': 238}

                ,{'uid': 39, 'menu_id': 229}

                ,{'uid': 39, 'menu_id': 5}

                ,{'uid': 39, 'menu_id': 4}

                ,{'uid': 39, 'menu_id': 232}

                ,{'uid': 39, 'menu_id': 213}

                ,{'uid': 47, 'menu_id': 249}

                ,{'uid': 47, 'menu_id': 248}

                ,{'uid': 47, 'menu_id': 211}

                ,{'uid': 47, 'menu_id': 221}

                ,{'uid': 47, 'menu_id': 258}

                ,{'uid': 47, 'menu_id': 377}

                ,{'uid': 47, 'menu_id': 324}

                ,{'uid': 47, 'menu_id': 378}

                ,{'uid': 47, 'menu_id': 182}

                ,{'uid': 47, 'menu_id': 215}

                ,{'uid': 47, 'menu_id': 216}

                ,{'uid': 47, 'menu_id': 217}

                ,{'uid': 47, 'menu_id': 379}

                ,{'uid': 47, 'menu_id': 218}

                ,{'uid': 47, 'menu_id': 226}

                ,{'uid': 47, 'menu_id': 380}

                ,{'uid': 47, 'menu_id': 114}

                ,{'uid': 47, 'menu_id': 386}

                ,{'uid': 47, 'menu_id': 387}

                ,{'uid': 47, 'menu_id': 220}

                ,{'uid': 47, 'menu_id': 389}

                ,{'uid': 47, 'menu_id': 253}

                ,{'uid': 47, 'menu_id': 332}

                ,{'uid': 47, 'menu_id': 404}

                ,{'uid': 47, 'menu_id': 246}

                ,{'uid': 47, 'menu_id': 238}

                ,{'uid': 47, 'menu_id': 229}

                ,{'uid': 47, 'menu_id': 5}

                ,{'uid': 47, 'menu_id': 4}

                ,{'uid': 47, 'menu_id': 232}

                ,{'uid': 47, 'menu_id': 213}

                ,{'uid': 62, 'menu_id': 84}

                ,{'uid': 62, 'menu_id': 487}

                ,{'uid': 62, 'menu_id': 523}

                ,{'uid': 62, 'menu_id': 471}

                ,{'uid': 62, 'menu_id': 182}

                ,{'uid': 62, 'menu_id': 114}

                ,{'uid': 62, 'menu_id': 332}

                ,{'uid': 62, 'menu_id': 404}

                ,{'uid': 62, 'menu_id': 5}

                ,{'uid': 62, 'menu_id': 4}

                ,{'uid': 48, 'menu_id': 249}

                ,{'uid': 48, 'menu_id': 248}

                ,{'uid': 48, 'menu_id': 211}

                ,{'uid': 48, 'menu_id': 221}

                ,{'uid': 48, 'menu_id': 258}

                ,{'uid': 48, 'menu_id': 377}

                ,{'uid': 48, 'menu_id': 378}

                ,{'uid': 48, 'menu_id': 182}

                ,{'uid': 48, 'menu_id': 215}

                ,{'uid': 48, 'menu_id': 216}

                ,{'uid': 48, 'menu_id': 217}

                ,{'uid': 48, 'menu_id': 379}

                ,{'uid': 48, 'menu_id': 218}

                ,{'uid': 48, 'menu_id': 226}

                ,{'uid': 48, 'menu_id': 380}

                ,{'uid': 48, 'menu_id': 114}

                ,{'uid': 48, 'menu_id': 386}

                ,{'uid': 48, 'menu_id': 387}

                ,{'uid': 48, 'menu_id': 220}

                ,{'uid': 48, 'menu_id': 389}

                ,{'uid': 48, 'menu_id': 253}

                ,{'uid': 48, 'menu_id': 332}

                ,{'uid': 48, 'menu_id': 404}

                ,{'uid': 48, 'menu_id': 246}

                ,{'uid': 48, 'menu_id': 238}

                ,{'uid': 48, 'menu_id': 229}

                ,{'uid': 48, 'menu_id': 5}

                ,{'uid': 48, 'menu_id': 4}

                ,{'uid': 48, 'menu_id': 232}

                ,{'uid': 48, 'menu_id': 213}

                ,{'uid': 43, 'menu_id': 249}

                ,{'uid': 43, 'menu_id': 248}

                ,{'uid': 43, 'menu_id': 221}

                ,{'uid': 43, 'menu_id': 258}

                ,{'uid': 43, 'menu_id': 377}

                ,{'uid': 43, 'menu_id': 182}

                ,{'uid': 43, 'menu_id': 215}

                ,{'uid': 43, 'menu_id': 216}

                ,{'uid': 43, 'menu_id': 217}

                ,{'uid': 43, 'menu_id': 218}

                ,{'uid': 43, 'menu_id': 226}

                ,{'uid': 43, 'menu_id': 114}

                ,{'uid': 43, 'menu_id': 220}

                ,{'uid': 43, 'menu_id': 389}

                ,{'uid': 43, 'menu_id': 253}

                ,{'uid': 43, 'menu_id': 332}

                ,{'uid': 43, 'menu_id': 404}

                ,{'uid': 43, 'menu_id': 246}

                ,{'uid': 43, 'menu_id': 238}

                ,{'uid': 43, 'menu_id': 229}

                ,{'uid': 43, 'menu_id': 5}

                ,{'uid': 43, 'menu_id': 4}

                ,{'uid': 43, 'menu_id': 232}

                ,{'uid': 43, 'menu_id': 213}

                ,{'uid': 59, 'menu_id': 249}

                ,{'uid': 59, 'menu_id': 248}

                ,{'uid': 59, 'menu_id': 211}

                ,{'uid': 59, 'menu_id': 221}

                ,{'uid': 59, 'menu_id': 258}

                ,{'uid': 59, 'menu_id': 377}

                ,{'uid': 59, 'menu_id': 324}

                ,{'uid': 59, 'menu_id': 378}

                ,{'uid': 59, 'menu_id': 182}

                ,{'uid': 59, 'menu_id': 215}

                ,{'uid': 59, 'menu_id': 216}

                ,{'uid': 59, 'menu_id': 217}

                ,{'uid': 59, 'menu_id': 379}

                ,{'uid': 59, 'menu_id': 218}

                ,{'uid': 59, 'menu_id': 226}

                ,{'uid': 59, 'menu_id': 380}

                ,{'uid': 59, 'menu_id': 114}

                ,{'uid': 59, 'menu_id': 386}

                ,{'uid': 59, 'menu_id': 387}

                ,{'uid': 59, 'menu_id': 220}

                ,{'uid': 59, 'menu_id': 389}

                ,{'uid': 59, 'menu_id': 253}

                ,{'uid': 59, 'menu_id': 332}

                ,{'uid': 59, 'menu_id': 404}

                ,{'uid': 59, 'menu_id': 246}

                ,{'uid': 59, 'menu_id': 238}

                ,{'uid': 59, 'menu_id': 229}

                ,{'uid': 59, 'menu_id': 5}

                ,{'uid': 59, 'menu_id': 4}

                ,{'uid': 59, 'menu_id': 232}

                ,{'uid': 59, 'menu_id': 213}

                ,{'uid': 17, 'menu_id': 249}

                ,{'uid': 17, 'menu_id': 248}

                ,{'uid': 17, 'menu_id': 221}

                ,{'uid': 17, 'menu_id': 258}

                ,{'uid': 17, 'menu_id': 182}

                ,{'uid': 17, 'menu_id': 215}

                ,{'uid': 17, 'menu_id': 216}

                ,{'uid': 17, 'menu_id': 217}

                ,{'uid': 17, 'menu_id': 218}

                ,{'uid': 17, 'menu_id': 226}

                ,{'uid': 17, 'menu_id': 114}

                ,{'uid': 17, 'menu_id': 220}

                ,{'uid': 17, 'menu_id': 253}

                ,{'uid': 17, 'menu_id': 332}

                ,{'uid': 17, 'menu_id': 404}

                ,{'uid': 17, 'menu_id': 246}

                ,{'uid': 17, 'menu_id': 238}

                ,{'uid': 17, 'menu_id': 5}

                ,{'uid': 17, 'menu_id': 4}

                ,{'uid': 17, 'menu_id': 232}

                ,{'uid': 51, 'menu_id': 249}

                ,{'uid': 51, 'menu_id': 248}

                ,{'uid': 51, 'menu_id': 211}

                ,{'uid': 51, 'menu_id': 221}

                ,{'uid': 51, 'menu_id': 258}

                ,{'uid': 51, 'menu_id': 377}

                ,{'uid': 51, 'menu_id': 378}

                ,{'uid': 51, 'menu_id': 182}

                ,{'uid': 51, 'menu_id': 215}

                ,{'uid': 51, 'menu_id': 216}

                ,{'uid': 51, 'menu_id': 217}

                ,{'uid': 51, 'menu_id': 379}

                ,{'uid': 51, 'menu_id': 218}

                ,{'uid': 51, 'menu_id': 226}

                ,{'uid': 51, 'menu_id': 380}

                ,{'uid': 51, 'menu_id': 114}

                ,{'uid': 51, 'menu_id': 386}

                ,{'uid': 51, 'menu_id': 387}

                ,{'uid': 51, 'menu_id': 220}

                ,{'uid': 51, 'menu_id': 389}

                ,{'uid': 51, 'menu_id': 253}

                ,{'uid': 51, 'menu_id': 332}

                ,{'uid': 51, 'menu_id': 404}

                ,{'uid': 51, 'menu_id': 246}

                ,{'uid': 51, 'menu_id': 238}

                ,{'uid': 51, 'menu_id': 229}

                ,{'uid': 51, 'menu_id': 5}

                ,{'uid': 51, 'menu_id': 4}

                ,{'uid': 51, 'menu_id': 232}

                ,{'uid': 51, 'menu_id': 213}

                ,{'uid': 37, 'menu_id': 249}

                ,{'uid': 37, 'menu_id': 248}

                ,{'uid': 37, 'menu_id': 221}

                ,{'uid': 37, 'menu_id': 258}

                ,{'uid': 37, 'menu_id': 377}

                ,{'uid': 37, 'menu_id': 182}

                ,{'uid': 37, 'menu_id': 215}

                ,{'uid': 37, 'menu_id': 216}

                ,{'uid': 37, 'menu_id': 217}

                ,{'uid': 37, 'menu_id': 218}

                ,{'uid': 37, 'menu_id': 226}

                ,{'uid': 37, 'menu_id': 114}

                ,{'uid': 37, 'menu_id': 220}

                ,{'uid': 37, 'menu_id': 389}

                ,{'uid': 37, 'menu_id': 253}

                ,{'uid': 37, 'menu_id': 332}

                ,{'uid': 37, 'menu_id': 404}

                ,{'uid': 37, 'menu_id': 246}

                ,{'uid': 37, 'menu_id': 238}

                ,{'uid': 37, 'menu_id': 229}

                ,{'uid': 37, 'menu_id': 5}

                ,{'uid': 37, 'menu_id': 4}

                ,{'uid': 37, 'menu_id': 232}

                ,{'uid': 37, 'menu_id': 213}

                ,{'uid': 7, 'menu_id': 221}

                ,{'uid': 7, 'menu_id': 258}

                ,{'uid': 7, 'menu_id': 182}

                ,{'uid': 7, 'menu_id': 215}

                ,{'uid': 7, 'menu_id': 216}

                ,{'uid': 7, 'menu_id': 217}

                ,{'uid': 7, 'menu_id': 218}

                ,{'uid': 7, 'menu_id': 226}

                ,{'uid': 7, 'menu_id': 114}

                ,{'uid': 7, 'menu_id': 220}

                ,{'uid': 7, 'menu_id': 253}

                ,{'uid': 7, 'menu_id': 332}

                ,{'uid': 7, 'menu_id': 404}

                ,{'uid': 7, 'menu_id': 238}

                ,{'uid': 7, 'menu_id': 5}

                ,{'uid': 7, 'menu_id': 232}

                ,{'uid': 12, 'menu_id': 249}

                ,{'uid': 12, 'menu_id': 248}

                ,{'uid': 12, 'menu_id': 130}

                ,{'uid': 12, 'menu_id': 84}

                ,{'uid': 12, 'menu_id': 221}

                ,{'uid': 12, 'menu_id': 258}

                ,{'uid': 12, 'menu_id': 182}

                ,{'uid': 12, 'menu_id': 215}

                ,{'uid': 12, 'menu_id': 216}

                ,{'uid': 12, 'menu_id': 217}

                ,{'uid': 12, 'menu_id': 218}

                ,{'uid': 12, 'menu_id': 226}

                ,{'uid': 12, 'menu_id': 114}

                ,{'uid': 12, 'menu_id': 220}

                ,{'uid': 12, 'menu_id': 253}

                ,{'uid': 12, 'menu_id': 332}

                ,{'uid': 12, 'menu_id': 246}

                ,{'uid': 12, 'menu_id': 238}

                ,{'uid': 12, 'menu_id': 229}

                ,{'uid': 12, 'menu_id': 5}

                ,{'uid': 12, 'menu_id': 4}

                ,{'uid': 12, 'menu_id': 232}

                ,{'uid': 63, 'menu_id': 84}

                ,{'uid': 63, 'menu_id': 487}

                ,{'uid': 63, 'menu_id': 523}

                ,{'uid': 63, 'menu_id': 211}

                ,{'uid': 63, 'menu_id': 471}

                ,{'uid': 63, 'menu_id': 324}

                ,{'uid': 63, 'menu_id': 182}

                ,{'uid': 63, 'menu_id': 225}

                ,{'uid': 63, 'menu_id': 226}

                ,{'uid': 63, 'menu_id': 380}

                ,{'uid': 63, 'menu_id': 114}

                ,{'uid': 63, 'menu_id': 386}

                ,{'uid': 63, 'menu_id': 387}

                ,{'uid': 63, 'menu_id': 388}

                ,{'uid': 63, 'menu_id': 389}

                ,{'uid': 63, 'menu_id': 332}

                ,{'uid': 63, 'menu_id': 404}

                ,{'uid': 63, 'menu_id': 246}

                ,{'uid': 63, 'menu_id': 238}

                ,{'uid': 63, 'menu_id': 77}

                ,{'uid': 63, 'menu_id': 229}

                ,{'uid': 63, 'menu_id': 5}

                ,{'uid': 63, 'menu_id': 4}

                ,{'uid': 63, 'menu_id': 213}

                ,{'uid': 27, 'menu_id': 249}

                ,{'uid': 27, 'menu_id': 248}

                ,{'uid': 27, 'menu_id': 221}

                ,{'uid': 27, 'menu_id': 258}

                ,{'uid': 27, 'menu_id': 182}

                ,{'uid': 27, 'menu_id': 215}

                ,{'uid': 27, 'menu_id': 216}

                ,{'uid': 27, 'menu_id': 217}

                ,{'uid': 27, 'menu_id': 218}

                ,{'uid': 27, 'menu_id': 226}

                ,{'uid': 27, 'menu_id': 114}

                ,{'uid': 27, 'menu_id': 220}

                ,{'uid': 27, 'menu_id': 253}

                ,{'uid': 27, 'menu_id': 332}

                ,{'uid': 27, 'menu_id': 404}

                ,{'uid': 27, 'menu_id': 246}

                ,{'uid': 27, 'menu_id': 238}

                ,{'uid': 27, 'menu_id': 5}

                ,{'uid': 27, 'menu_id': 4}

                ,{'uid': 27, 'menu_id': 232}

                ,{'uid': 53, 'menu_id': 249}

                ,{'uid': 53, 'menu_id': 248}

                ,{'uid': 53, 'menu_id': 211}

                ,{'uid': 53, 'menu_id': 221}

                ,{'uid': 53, 'menu_id': 258}

                ,{'uid': 53, 'menu_id': 377}

                ,{'uid': 53, 'menu_id': 324}

                ,{'uid': 53, 'menu_id': 378}

                ,{'uid': 53, 'menu_id': 182}

                ,{'uid': 53, 'menu_id': 215}

                ,{'uid': 53, 'menu_id': 216}

                ,{'uid': 53, 'menu_id': 217}

                ,{'uid': 53, 'menu_id': 379}

                ,{'uid': 53, 'menu_id': 218}

                ,{'uid': 53, 'menu_id': 226}

                ,{'uid': 53, 'menu_id': 380}

                ,{'uid': 53, 'menu_id': 114}

                ,{'uid': 53, 'menu_id': 386}

                ,{'uid': 53, 'menu_id': 387}

                ,{'uid': 53, 'menu_id': 220}

                ,{'uid': 53, 'menu_id': 389}

                ,{'uid': 53, 'menu_id': 253}

                ,{'uid': 53, 'menu_id': 332}

                ,{'uid': 53, 'menu_id': 404}

                ,{'uid': 53, 'menu_id': 246}

                ,{'uid': 53, 'menu_id': 238}

                ,{'uid': 53, 'menu_id': 229}

                ,{'uid': 53, 'menu_id': 5}

                ,{'uid': 53, 'menu_id': 4}

                ,{'uid': 53, 'menu_id': 232}

                ,{'uid': 53, 'menu_id': 213}

                ,{'uid': 50, 'menu_id': 249}

                ,{'uid': 50, 'menu_id': 248}

                ,{'uid': 50, 'menu_id': 211}

                ,{'uid': 50, 'menu_id': 221}

                ,{'uid': 50, 'menu_id': 258}

                ,{'uid': 50, 'menu_id': 377}

                ,{'uid': 50, 'menu_id': 378}

                ,{'uid': 50, 'menu_id': 182}

                ,{'uid': 50, 'menu_id': 215}

                ,{'uid': 50, 'menu_id': 216}

                ,{'uid': 50, 'menu_id': 217}

                ,{'uid': 50, 'menu_id': 379}

                ,{'uid': 50, 'menu_id': 218}

                ,{'uid': 50, 'menu_id': 226}

                ,{'uid': 50, 'menu_id': 380}

                ,{'uid': 50, 'menu_id': 114}

                ,{'uid': 50, 'menu_id': 386}

                ,{'uid': 50, 'menu_id': 387}

                ,{'uid': 50, 'menu_id': 220}

                ,{'uid': 50, 'menu_id': 389}

                ,{'uid': 50, 'menu_id': 253}

                ,{'uid': 50, 'menu_id': 332}

                ,{'uid': 50, 'menu_id': 404}

                ,{'uid': 50, 'menu_id': 246}

                ,{'uid': 50, 'menu_id': 238}

                ,{'uid': 50, 'menu_id': 229}

                ,{'uid': 50, 'menu_id': 5}

                ,{'uid': 50, 'menu_id': 4}

                ,{'uid': 50, 'menu_id': 232}

                ,{'uid': 50, 'menu_id': 213}

                ,{'uid': 14, 'menu_id': 249}

                ,{'uid': 14, 'menu_id': 84}

                ,{'uid': 14, 'menu_id': 211}

                ,{'uid': 14, 'menu_id': 221}

                ,{'uid': 14, 'menu_id': 258}

                ,{'uid': 14, 'menu_id': 324}

                ,{'uid': 14, 'menu_id': 182}

                ,{'uid': 14, 'menu_id': 215}

                ,{'uid': 14, 'menu_id': 216}

                ,{'uid': 14, 'menu_id': 217}

                ,{'uid': 14, 'menu_id': 218}

                ,{'uid': 14, 'menu_id': 226}

                ,{'uid': 14, 'menu_id': 114}

                ,{'uid': 14, 'menu_id': 220}

                ,{'uid': 14, 'menu_id': 253}

                ,{'uid': 14, 'menu_id': 332}

                ,{'uid': 14, 'menu_id': 404}

                ,{'uid': 14, 'menu_id': 246}

                ,{'uid': 14, 'menu_id': 238}

                ,{'uid': 14, 'menu_id': 229}

                ,{'uid': 14, 'menu_id': 5}

                ,{'uid': 14, 'menu_id': 4}

                ,{'uid': 14, 'menu_id': 232}

                ,{'uid': 14, 'menu_id': 213}

                ,{'uid': 36, 'menu_id': 249}

                ,{'uid': 36, 'menu_id': 248}

                ,{'uid': 36, 'menu_id': 221}

                ,{'uid': 36, 'menu_id': 258}

                ,{'uid': 36, 'menu_id': 377}

                ,{'uid': 36, 'menu_id': 182}

                ,{'uid': 36, 'menu_id': 215}

                ,{'uid': 36, 'menu_id': 216}

                ,{'uid': 36, 'menu_id': 217}

                ,{'uid': 36, 'menu_id': 218}

                ,{'uid': 36, 'menu_id': 226}

                ,{'uid': 36, 'menu_id': 114}

                ,{'uid': 36, 'menu_id': 220}

                ,{'uid': 36, 'menu_id': 389}

                ,{'uid': 36, 'menu_id': 253}

                ,{'uid': 36, 'menu_id': 332}

                ,{'uid': 36, 'menu_id': 404}

                ,{'uid': 36, 'menu_id': 246}

                ,{'uid': 36, 'menu_id': 238}

                ,{'uid': 36, 'menu_id': 229}

                ,{'uid': 36, 'menu_id': 5}

                ,{'uid': 36, 'menu_id': 4}

                ,{'uid': 36, 'menu_id': 232}

                ,{'uid': 36, 'menu_id': 213}

                ,{'uid': 56, 'menu_id': 249}

                ,{'uid': 56, 'menu_id': 248}

                ,{'uid': 56, 'menu_id': 221}

                ,{'uid': 56, 'menu_id': 258}

                ,{'uid': 56, 'menu_id': 182}

                ,{'uid': 56, 'menu_id': 215}

                ,{'uid': 56, 'menu_id': 216}

                ,{'uid': 56, 'menu_id': 217}

                ,{'uid': 56, 'menu_id': 218}

                ,{'uid': 56, 'menu_id': 454}

                ,{'uid': 56, 'menu_id': 226}

                ,{'uid': 56, 'menu_id': 114}

                ,{'uid': 56, 'menu_id': 220}

                ,{'uid': 56, 'menu_id': 253}

                ,{'uid': 56, 'menu_id': 332}

                ,{'uid': 56, 'menu_id': 404}

                ,{'uid': 56, 'menu_id': 246}

                ,{'uid': 56, 'menu_id': 238}

                ,{'uid': 56, 'menu_id': 229}

                ,{'uid': 56, 'menu_id': 5}

                ,{'uid': 56, 'menu_id': 4}

                ,{'uid': 56, 'menu_id': 232}

                ,{'uid': 56, 'menu_id': 213}

                ,{'uid': 60, 'menu_id': 249}

                ,{'uid': 60, 'menu_id': 248}

                ,{'uid': 60, 'menu_id': 211}

                ,{'uid': 60, 'menu_id': 221}

                ,{'uid': 60, 'menu_id': 258}

                ,{'uid': 60, 'menu_id': 377}

                ,{'uid': 60, 'menu_id': 324}

                ,{'uid': 60, 'menu_id': 378}

                ,{'uid': 60, 'menu_id': 182}

                ,{'uid': 60, 'menu_id': 215}

                ,{'uid': 60, 'menu_id': 216}

                ,{'uid': 60, 'menu_id': 217}

                ,{'uid': 60, 'menu_id': 379}

                ,{'uid': 60, 'menu_id': 218}

                ,{'uid': 60, 'menu_id': 226}

                ,{'uid': 60, 'menu_id': 380}

                ,{'uid': 60, 'menu_id': 114}

                ,{'uid': 60, 'menu_id': 386}

                ,{'uid': 60, 'menu_id': 387}

                ,{'uid': 60, 'menu_id': 220}

                ,{'uid': 60, 'menu_id': 389}

                ,{'uid': 60, 'menu_id': 253}

                ,{'uid': 60, 'menu_id': 332}

                ,{'uid': 60, 'menu_id': 404}

                ,{'uid': 60, 'menu_id': 246}

                ,{'uid': 60, 'menu_id': 238}

                ,{'uid': 60, 'menu_id': 229}

                ,{'uid': 60, 'menu_id': 5}

                ,{'uid': 60, 'menu_id': 4}

                ,{'uid': 60, 'menu_id': 232}

                ,{'uid': 60, 'menu_id': 213}

                ,{'uid': 52, 'menu_id': 249}

                ,{'uid': 52, 'menu_id': 248}

                ,{'uid': 52, 'menu_id': 211}

                ,{'uid': 52, 'menu_id': 221}

                ,{'uid': 52, 'menu_id': 258}

                ,{'uid': 52, 'menu_id': 377}

                ,{'uid': 52, 'menu_id': 324}

                ,{'uid': 52, 'menu_id': 378}

                ,{'uid': 52, 'menu_id': 182}

                ,{'uid': 52, 'menu_id': 215}

                ,{'uid': 52, 'menu_id': 216}

                ,{'uid': 52, 'menu_id': 217}

                ,{'uid': 52, 'menu_id': 379}

                ,{'uid': 52, 'menu_id': 218}

                ,{'uid': 52, 'menu_id': 226}

                ,{'uid': 52, 'menu_id': 380}

                ,{'uid': 52, 'menu_id': 114}

                ,{'uid': 52, 'menu_id': 386}

                ,{'uid': 52, 'menu_id': 387}

                ,{'uid': 52, 'menu_id': 220}

                ,{'uid': 52, 'menu_id': 389}

                ,{'uid': 52, 'menu_id': 253}

                ,{'uid': 52, 'menu_id': 332}

                ,{'uid': 52, 'menu_id': 404}

                ,{'uid': 52, 'menu_id': 246}

                ,{'uid': 52, 'menu_id': 238}

                ,{'uid': 52, 'menu_id': 229}

                ,{'uid': 52, 'menu_id': 5}

                ,{'uid': 52, 'menu_id': 4}

                ,{'uid': 52, 'menu_id': 232}

                ,{'uid': 52, 'menu_id': 213}

                ,{'uid': 64, 'menu_id': 84}

                ,{'uid': 64, 'menu_id': 487}

                ,{'uid': 64, 'menu_id': 523}

                ,{'uid': 64, 'menu_id': 241}

                ,{'uid': 64, 'menu_id': 258}

                ,{'uid': 64, 'menu_id': 471}

                ,{'uid': 64, 'menu_id': 214}

                ,{'uid': 64, 'menu_id': 324}

                ,{'uid': 64, 'menu_id': 182}

                ,{'uid': 64, 'menu_id': 372}

                ,{'uid': 64, 'menu_id': 384}

                ,{'uid': 64, 'menu_id': 225}

                ,{'uid': 64, 'menu_id': 226}

                ,{'uid': 64, 'menu_id': 373}

                ,{'uid': 64, 'menu_id': 114}

                ,{'uid': 64, 'menu_id': 374}

                ,{'uid': 64, 'menu_id': 383}

                ,{'uid': 64, 'menu_id': 253}

                ,{'uid': 64, 'menu_id': 332}

                ,{'uid': 64, 'menu_id': 404}

                ,{'uid': 64, 'menu_id': 238}

                ,{'uid': 64, 'menu_id': 213}

                ,{'uid': 29, 'menu_id': 72}

                ,{'uid': 29, 'menu_id': 207}

                ,{'uid': 29, 'menu_id': 249}

                ,{'uid': 29, 'menu_id': 248}

                ,{'uid': 29, 'menu_id': 221}

                ,{'uid': 29, 'menu_id': 258}

                ,{'uid': 29, 'menu_id': 182}

                ,{'uid': 29, 'menu_id': 215}

                ,{'uid': 29, 'menu_id': 216}

                ,{'uid': 29, 'menu_id': 217}

                ,{'uid': 29, 'menu_id': 218}

                ,{'uid': 29, 'menu_id': 226}

                ,{'uid': 29, 'menu_id': 114}

                ,{'uid': 29, 'menu_id': 220}

                ,{'uid': 29, 'menu_id': 253}

                ,{'uid': 29, 'menu_id': 332}

                ,{'uid': 29, 'menu_id': 404}

                ,{'uid': 29, 'menu_id': 246}

                ,{'uid': 29, 'menu_id': 238}

                ,{'uid': 29, 'menu_id': 5}

                ,{'uid': 29, 'menu_id': 4}

                ,{'uid': 29, 'menu_id': 232}

                ,{'uid': 38, 'menu_id': 249}

                ,{'uid': 38, 'menu_id': 248}

                ,{'uid': 38, 'menu_id': 221}

                ,{'uid': 38, 'menu_id': 258}

                ,{'uid': 38, 'menu_id': 377}

                ,{'uid': 38, 'menu_id': 182}

                ,{'uid': 38, 'menu_id': 215}

                ,{'uid': 38, 'menu_id': 216}

                ,{'uid': 38, 'menu_id': 217}

                ,{'uid': 38, 'menu_id': 218}

                ,{'uid': 38, 'menu_id': 226}

                ,{'uid': 38, 'menu_id': 114}

                ,{'uid': 38, 'menu_id': 220}

                ,{'uid': 38, 'menu_id': 389}

                ,{'uid': 38, 'menu_id': 253}

                ,{'uid': 38, 'menu_id': 332}

                ,{'uid': 38, 'menu_id': 404}

                ,{'uid': 38, 'menu_id': 246}

                ,{'uid': 38, 'menu_id': 238}

                ,{'uid': 38, 'menu_id': 229}

                ,{'uid': 38, 'menu_id': 5}

                ,{'uid': 38, 'menu_id': 4}

                ,{'uid': 38, 'menu_id': 232}

                ,{'uid': 38, 'menu_id': 213}

                ,{'uid': 42, 'menu_id': 249}

                ,{'uid': 42, 'menu_id': 248}

                ,{'uid': 42, 'menu_id': 221}

                ,{'uid': 42, 'menu_id': 258}

                ,{'uid': 42, 'menu_id': 377}

                ,{'uid': 42, 'menu_id': 182}

                ,{'uid': 42, 'menu_id': 215}

                ,{'uid': 42, 'menu_id': 216}

                ,{'uid': 42, 'menu_id': 217}

                ,{'uid': 42, 'menu_id': 218}

                ,{'uid': 42, 'menu_id': 226}

                ,{'uid': 42, 'menu_id': 114}

                ,{'uid': 42, 'menu_id': 220}

                ,{'uid': 42, 'menu_id': 389}

                ,{'uid': 42, 'menu_id': 253}

                ,{'uid': 42, 'menu_id': 332}

                ,{'uid': 42, 'menu_id': 404}

                ,{'uid': 42, 'menu_id': 246}

                ,{'uid': 42, 'menu_id': 238}

                ,{'uid': 42, 'menu_id': 229}

                ,{'uid': 42, 'menu_id': 5}

                ,{'uid': 42, 'menu_id': 4}

                ,{'uid': 42, 'menu_id': 232}

                ,{'uid': 42, 'menu_id': 213}

                ,{'uid': 15, 'menu_id': 249}

                ,{'uid': 15, 'menu_id': 248}

                ,{'uid': 15, 'menu_id': 84}

                ,{'uid': 15, 'menu_id': 211}

                ,{'uid': 15, 'menu_id': 221}

                ,{'uid': 15, 'menu_id': 258}

                ,{'uid': 15, 'menu_id': 324}

                ,{'uid': 15, 'menu_id': 182}

                ,{'uid': 15, 'menu_id': 215}

                ,{'uid': 15, 'menu_id': 216}

                ,{'uid': 15, 'menu_id': 217}

                ,{'uid': 15, 'menu_id': 218}

                ,{'uid': 15, 'menu_id': 226}

                ,{'uid': 15, 'menu_id': 114}

                ,{'uid': 15, 'menu_id': 220}

                ,{'uid': 15, 'menu_id': 253}

                ,{'uid': 15, 'menu_id': 332}

                ,{'uid': 15, 'menu_id': 404}

                ,{'uid': 15, 'menu_id': 246}

                ,{'uid': 15, 'menu_id': 238}

                ,{'uid': 15, 'menu_id': 229}

                ,{'uid': 15, 'menu_id': 5}

                ,{'uid': 15, 'menu_id': 4}

                ,{'uid': 15, 'menu_id': 232}

                ,{'uid': 15, 'menu_id': 213}

                ,{'uid': 41, 'menu_id': 249}

                ,{'uid': 41, 'menu_id': 248}

                ,{'uid': 41, 'menu_id': 221}

                ,{'uid': 41, 'menu_id': 258}

                ,{'uid': 41, 'menu_id': 377}

                ,{'uid': 41, 'menu_id': 182}

                ,{'uid': 41, 'menu_id': 215}

                ,{'uid': 41, 'menu_id': 216}

                ,{'uid': 41, 'menu_id': 217}

                ,{'uid': 41, 'menu_id': 218}

                ,{'uid': 41, 'menu_id': 226}

                ,{'uid': 41, 'menu_id': 114}

                ,{'uid': 41, 'menu_id': 220}

                ,{'uid': 41, 'menu_id': 389}

                ,{'uid': 41, 'menu_id': 253}

                ,{'uid': 41, 'menu_id': 332}

                ,{'uid': 41, 'menu_id': 404}

                ,{'uid': 41, 'menu_id': 246}

                ,{'uid': 41, 'menu_id': 238}

                ,{'uid': 41, 'menu_id': 229}

                ,{'uid': 41, 'menu_id': 5}

                ,{'uid': 41, 'menu_id': 4}

                ,{'uid': 41, 'menu_id': 232}

                ,{'uid': 41, 'menu_id': 213}

                ,{'uid': 61, 'menu_id': 249}

                ,{'uid': 61, 'menu_id': 248}

                ,{'uid': 61, 'menu_id': 211}

                ,{'uid': 61, 'menu_id': 221}

                ,{'uid': 61, 'menu_id': 258}

                ,{'uid': 61, 'menu_id': 377}

                ,{'uid': 61, 'menu_id': 324}

                ,{'uid': 61, 'menu_id': 378}

                ,{'uid': 61, 'menu_id': 182}

                ,{'uid': 61, 'menu_id': 215}

                ,{'uid': 61, 'menu_id': 216}

                ,{'uid': 61, 'menu_id': 217}

                ,{'uid': 61, 'menu_id': 379}

                ,{'uid': 61, 'menu_id': 218}

                ,{'uid': 61, 'menu_id': 226}

                ,{'uid': 61, 'menu_id': 380}

                ,{'uid': 61, 'menu_id': 114}

                ,{'uid': 61, 'menu_id': 386}

                ,{'uid': 61, 'menu_id': 387}

                ,{'uid': 61, 'menu_id': 220}

                ,{'uid': 61, 'menu_id': 389}

                ,{'uid': 61, 'menu_id': 253}

                ,{'uid': 61, 'menu_id': 332}

                ,{'uid': 61, 'menu_id': 404}

                ,{'uid': 61, 'menu_id': 246}

                ,{'uid': 61, 'menu_id': 238}

                ,{'uid': 61, 'menu_id': 229}

                ,{'uid': 61, 'menu_id': 5}

                ,{'uid': 61, 'menu_id': 4}

                ,{'uid': 61, 'menu_id': 232}

                ,{'uid': 61, 'menu_id': 213}

                ,{'uid': 28, 'menu_id': 249}

                ,{'uid': 28, 'menu_id': 248}

                ,{'uid': 28, 'menu_id': 221}

                ,{'uid': 28, 'menu_id': 258}

                ,{'uid': 28, 'menu_id': 182}

                ,{'uid': 28, 'menu_id': 215}

                ,{'uid': 28, 'menu_id': 216}

                ,{'uid': 28, 'menu_id': 217}

                ,{'uid': 28, 'menu_id': 218}

                ,{'uid': 28, 'menu_id': 226}

                ,{'uid': 28, 'menu_id': 114}

                ,{'uid': 28, 'menu_id': 220}

                ,{'uid': 28, 'menu_id': 253}

                ,{'uid': 28, 'menu_id': 332}

                ,{'uid': 28, 'menu_id': 404}

                ,{'uid': 28, 'menu_id': 246}

                ,{'uid': 28, 'menu_id': 238}

                ,{'uid': 28, 'menu_id': 5}

                ,{'uid': 28, 'menu_id': 4}

                ,{'uid': 28, 'menu_id': 232}

                ,{'uid': 54, 'menu_id': 249}

                ,{'uid': 54, 'menu_id': 248}

                ,{'uid': 54, 'menu_id': 211}

                ,{'uid': 54, 'menu_id': 221}

                ,{'uid': 54, 'menu_id': 258}

                ,{'uid': 54, 'menu_id': 377}

                ,{'uid': 54, 'menu_id': 324}

                ,{'uid': 54, 'menu_id': 378}

                ,{'uid': 54, 'menu_id': 182}

                ,{'uid': 54, 'menu_id': 215}

                ,{'uid': 54, 'menu_id': 216}

                ,{'uid': 54, 'menu_id': 217}

                ,{'uid': 54, 'menu_id': 379}

                ,{'uid': 54, 'menu_id': 218}

                ,{'uid': 54, 'menu_id': 226}

                ,{'uid': 54, 'menu_id': 380}

                ,{'uid': 54, 'menu_id': 114}

                ,{'uid': 54, 'menu_id': 386}

                ,{'uid': 54, 'menu_id': 387}

                ,{'uid': 54, 'menu_id': 220}

                ,{'uid': 54, 'menu_id': 389}

                ,{'uid': 54, 'menu_id': 253}

                ,{'uid': 54, 'menu_id': 332}

                ,{'uid': 54, 'menu_id': 404}

                ,{'uid': 54, 'menu_id': 246}

                ,{'uid': 54, 'menu_id': 238}

                ,{'uid': 54, 'menu_id': 229}

                ,{'uid': 54, 'menu_id': 5}

                ,{'uid': 54, 'menu_id': 4}

                ,{'uid': 54, 'menu_id': 232}

                ,{'uid': 54, 'menu_id': 213}

                ,{'uid': 58, 'menu_id': 290}

                ,{'uid': 58, 'menu_id': 249}

                ,{'uid': 58, 'menu_id': 248}

                ,{'uid': 58, 'menu_id': 221}

                ,{'uid': 58, 'menu_id': 258}

                ,{'uid': 58, 'menu_id': 182}

                ,{'uid': 58, 'menu_id': 215}

                ,{'uid': 58, 'menu_id': 216}

                ,{'uid': 58, 'menu_id': 217}

                ,{'uid': 58, 'menu_id': 218}

                ,{'uid': 58, 'menu_id': 226}

                ,{'uid': 58, 'menu_id': 114}

                ,{'uid': 58, 'menu_id': 220}

                ,{'uid': 58, 'menu_id': 253}

                ,{'uid': 58, 'menu_id': 332}

                ,{'uid': 58, 'menu_id': 404}

                ,{'uid': 58, 'menu_id': 246}

                ,{'uid': 58, 'menu_id': 238}

                ,{'uid': 58, 'menu_id': 5}

                ,{'uid': 58, 'menu_id': 4}

                ,{'uid': 58, 'menu_id': 232}

                ,{'uid': 49, 'menu_id': 249}

                ,{'uid': 49, 'menu_id': 248}

                ,{'uid': 49, 'menu_id': 211}

                ,{'uid': 49, 'menu_id': 221}

                ,{'uid': 49, 'menu_id': 258}

                ,{'uid': 49, 'menu_id': 377}

                ,{'uid': 49, 'menu_id': 378}

                ,{'uid': 49, 'menu_id': 182}

                ,{'uid': 49, 'menu_id': 215}

                ,{'uid': 49, 'menu_id': 216}

                ,{'uid': 49, 'menu_id': 217}

                ,{'uid': 49, 'menu_id': 379}

                ,{'uid': 49, 'menu_id': 218}

                ,{'uid': 49, 'menu_id': 226}

                ,{'uid': 49, 'menu_id': 380}

                ,{'uid': 49, 'menu_id': 114}

                ,{'uid': 49, 'menu_id': 386}

                ,{'uid': 49, 'menu_id': 387}

                ,{'uid': 49, 'menu_id': 220}

                ,{'uid': 49, 'menu_id': 389}

                ,{'uid': 49, 'menu_id': 253}

                ,{'uid': 49, 'menu_id': 332}

                ,{'uid': 49, 'menu_id': 404}

                ,{'uid': 49, 'menu_id': 246}

                ,{'uid': 49, 'menu_id': 238}

                ,{'uid': 49, 'menu_id': 229}

                ,{'uid': 49, 'menu_id': 5}

                ,{'uid': 49, 'menu_id': 4}

                ,{'uid': 49, 'menu_id': 232}

                ,{'uid': 49, 'menu_id': 213}

                ,{'uid': 40, 'menu_id': 249}

                ,{'uid': 40, 'menu_id': 248}

                ,{'uid': 40, 'menu_id': 221}

                ,{'uid': 40, 'menu_id': 258}

                ,{'uid': 40, 'menu_id': 377}

                ,{'uid': 40, 'menu_id': 182}

                ,{'uid': 40, 'menu_id': 215}

                ,{'uid': 40, 'menu_id': 216}

                ,{'uid': 40, 'menu_id': 217}

                ,{'uid': 40, 'menu_id': 218}

                ,{'uid': 40, 'menu_id': 226}

                ,{'uid': 40, 'menu_id': 114}

                ,{'uid': 40, 'menu_id': 220}

                ,{'uid': 40, 'menu_id': 389}

                ,{'uid': 40, 'menu_id': 253}

                ,{'uid': 40, 'menu_id': 332}

                ,{'uid': 40, 'menu_id': 404}

                ,{'uid': 40, 'menu_id': 246}

                ,{'uid': 40, 'menu_id': 238}

                ,{'uid': 40, 'menu_id': 229}

                ,{'uid': 40, 'menu_id': 5}

                ,{'uid': 40, 'menu_id': 4}

                ,{'uid': 40, 'menu_id': 232}

                ,{'uid': 40, 'menu_id': 213}

                ,{'uid': 30, 'menu_id': 249}

                ,{'uid': 30, 'menu_id': 248}

                ,{'uid': 30, 'menu_id': 221}

                ,{'uid': 30, 'menu_id': 258}

                ,{'uid': 30, 'menu_id': 182}

                ,{'uid': 30, 'menu_id': 215}

                ,{'uid': 30, 'menu_id': 216}

                ,{'uid': 30, 'menu_id': 217}

                ,{'uid': 30, 'menu_id': 218}

                ,{'uid': 30, 'menu_id': 226}

                ,{'uid': 30, 'menu_id': 114}

                ,{'uid': 30, 'menu_id': 220}

                ,{'uid': 30, 'menu_id': 253}

                ,{'uid': 30, 'menu_id': 332}

                ,{'uid': 30, 'menu_id': 404}

                ,{'uid': 30, 'menu_id': 246}

                ,{'uid': 30, 'menu_id': 238}

                ,{'uid': 30, 'menu_id': 5}

                ,{'uid': 30, 'menu_id': 4}

                ,{'uid': 30, 'menu_id': 232}

                ,{'uid': 25, 'menu_id': 249}

                ,{'uid': 25, 'menu_id': 248}

                ,{'uid': 25, 'menu_id': 221}

                ,{'uid': 25, 'menu_id': 258}

                ,{'uid': 25, 'menu_id': 182}

                ,{'uid': 25, 'menu_id': 215}

                ,{'uid': 25, 'menu_id': 216}

                ,{'uid': 25, 'menu_id': 217}

                ,{'uid': 25, 'menu_id': 218}

                ,{'uid': 25, 'menu_id': 226}

                ,{'uid': 25, 'menu_id': 114}

                ,{'uid': 25, 'menu_id': 220}

                ,{'uid': 25, 'menu_id': 253}

                ,{'uid': 25, 'menu_id': 332}

                ,{'uid': 25, 'menu_id': 404}

                ,{'uid': 25, 'menu_id': 246}

                ,{'uid': 25, 'menu_id': 238}

                ,{'uid': 25, 'menu_id': 5}

                ,{'uid': 25, 'menu_id': 4}

                ,{'uid': 25, 'menu_id': 232}

                ,{'uid': 45, 'menu_id': 249}

                ,{'uid': 45, 'menu_id': 248}

                ,{'uid': 45, 'menu_id': 211}

                ,{'uid': 45, 'menu_id': 221}

                ,{'uid': 45, 'menu_id': 258}

                ,{'uid': 45, 'menu_id': 377}

                ,{'uid': 45, 'menu_id': 378}

                ,{'uid': 45, 'menu_id': 182}

                ,{'uid': 45, 'menu_id': 215}

                ,{'uid': 45, 'menu_id': 216}

                ,{'uid': 45, 'menu_id': 217}

                ,{'uid': 45, 'menu_id': 379}

                ,{'uid': 45, 'menu_id': 218}

                ,{'uid': 45, 'menu_id': 226}

                ,{'uid': 45, 'menu_id': 380}

                ,{'uid': 45, 'menu_id': 114}

                ,{'uid': 45, 'menu_id': 386}

                ,{'uid': 45, 'menu_id': 387}

                ,{'uid': 45, 'menu_id': 220}

                ,{'uid': 45, 'menu_id': 389}

                ,{'uid': 45, 'menu_id': 253}

                ,{'uid': 45, 'menu_id': 332}

                ,{'uid': 45, 'menu_id': 404}

                ,{'uid': 45, 'menu_id': 246}

                ,{'uid': 45, 'menu_id': 238}

                ,{'uid': 45, 'menu_id': 229}

                ,{'uid': 45, 'menu_id': 5}

                ,{'uid': 45, 'menu_id': 4}

                ,{'uid': 45, 'menu_id': 232}

                ,{'uid': 45, 'menu_id': 213}

                ,{'uid': 35, 'menu_id': 249}

                ,{'uid': 35, 'menu_id': 248}

                ,{'uid': 35, 'menu_id': 221}

                ,{'uid': 35, 'menu_id': 258}

                ,{'uid': 35, 'menu_id': 377}

                ,{'uid': 35, 'menu_id': 182}

                ,{'uid': 35, 'menu_id': 215}

                ,{'uid': 35, 'menu_id': 216}

                ,{'uid': 35, 'menu_id': 217}

                ,{'uid': 35, 'menu_id': 218}

                ,{'uid': 35, 'menu_id': 226}

                ,{'uid': 35, 'menu_id': 114}

                ,{'uid': 35, 'menu_id': 220}

                ,{'uid': 35, 'menu_id': 389}

                ,{'uid': 35, 'menu_id': 253}

                ,{'uid': 35, 'menu_id': 332}

                ,{'uid': 35, 'menu_id': 404}

                ,{'uid': 35, 'menu_id': 246}

                ,{'uid': 35, 'menu_id': 238}

                ,{'uid': 35, 'menu_id': 229}

                ,{'uid': 35, 'menu_id': 5}

                ,{'uid': 35, 'menu_id': 4}

                ,{'uid': 35, 'menu_id': 232}

                ,{'uid': 35, 'menu_id': 213}

                ,{'uid': 57, 'menu_id': 249}

                ,{'uid': 57, 'menu_id': 248}

                ,{'uid': 57, 'menu_id': 221}

                ,{'uid': 57, 'menu_id': 258}

                ,{'uid': 57, 'menu_id': 377}

                ,{'uid': 57, 'menu_id': 378}

                ,{'uid': 57, 'menu_id': 182}

                ,{'uid': 57, 'menu_id': 215}

                ,{'uid': 57, 'menu_id': 216}

                ,{'uid': 57, 'menu_id': 217}

                ,{'uid': 57, 'menu_id': 319}

                ,{'uid': 57, 'menu_id': 379}

                ,{'uid': 57, 'menu_id': 218}

                ,{'uid': 57, 'menu_id': 320}

                ,{'uid': 57, 'menu_id': 454}

                ,{'uid': 57, 'menu_id': 226}

                ,{'uid': 57, 'menu_id': 380}

                ,{'uid': 57, 'menu_id': 114}

                ,{'uid': 57, 'menu_id': 386}

                ,{'uid': 57, 'menu_id': 387}

                ,{'uid': 57, 'menu_id': 220}

                ,{'uid': 57, 'menu_id': 389}

                ,{'uid': 57, 'menu_id': 223}

                ,{'uid': 57, 'menu_id': 253}

                ,{'uid': 57, 'menu_id': 318}

                ,{'uid': 57, 'menu_id': 332}

                ,{'uid': 57, 'menu_id': 404}

                ,{'uid': 57, 'menu_id': 246}

                ,{'uid': 57, 'menu_id': 238}

                ,{'uid': 57, 'menu_id': 229}

                ,{'uid': 57, 'menu_id': 5}

                ,{'uid': 57, 'menu_id': 4}

                ,{'uid': 57, 'menu_id': 232}

                ,{'uid': 57, 'menu_id': 213}

                ,{'uid': 46, 'menu_id': 249}

                ,{'uid': 46, 'menu_id': 248}

                ,{'uid': 46, 'menu_id': 211}

                ,{'uid': 46, 'menu_id': 221}

                ,{'uid': 46, 'menu_id': 258}

                ,{'uid': 46, 'menu_id': 377}

                ,{'uid': 46, 'menu_id': 324}

                ,{'uid': 46, 'menu_id': 378}

                ,{'uid': 46, 'menu_id': 182}

                ,{'uid': 46, 'menu_id': 215}

                ,{'uid': 46, 'menu_id': 216}

                ,{'uid': 46, 'menu_id': 217}

                ,{'uid': 46, 'menu_id': 379}

                ,{'uid': 46, 'menu_id': 218}

                ,{'uid': 46, 'menu_id': 226}

                ,{'uid': 46, 'menu_id': 380}

                ,{'uid': 46, 'menu_id': 114}

                ,{'uid': 46, 'menu_id': 386}

                ,{'uid': 46, 'menu_id': 387}

                ,{'uid': 46, 'menu_id': 220}

                ,{'uid': 46, 'menu_id': 389}

                ,{'uid': 46, 'menu_id': 253}

                ,{'uid': 46, 'menu_id': 332}

                ,{'uid': 46, 'menu_id': 404}

                ,{'uid': 46, 'menu_id': 246}

                ,{'uid': 46, 'menu_id': 238}

                ,{'uid': 46, 'menu_id': 229}

                ,{'uid': 46, 'menu_id': 5}

                ,{'uid': 46, 'menu_id': 4}

                ,{'uid': 46, 'menu_id': 232}

                ,{'uid': 46, 'menu_id': 213}

                ,{'uid': 31, 'menu_id': 249}

                ,{'uid': 31, 'menu_id': 248}

                ,{'uid': 31, 'menu_id': 221}

                ,{'uid': 31, 'menu_id': 258}

                ,{'uid': 31, 'menu_id': 182}

                ,{'uid': 31, 'menu_id': 215}

                ,{'uid': 31, 'menu_id': 216}

                ,{'uid': 31, 'menu_id': 217}

                ,{'uid': 31, 'menu_id': 218}

                ,{'uid': 31, 'menu_id': 226}

                ,{'uid': 31, 'menu_id': 114}

                ,{'uid': 31, 'menu_id': 220}

                ,{'uid': 31, 'menu_id': 253}

                ,{'uid': 31, 'menu_id': 332}

                ,{'uid': 31, 'menu_id': 404}

                ,{'uid': 31, 'menu_id': 246}

                ,{'uid': 31, 'menu_id': 238}

                ,{'uid': 31, 'menu_id': 5}

                ,{'uid': 31, 'menu_id': 4}

                ,{'uid': 31, 'menu_id': 232}

                ,{'uid': 16, 'menu_id': 249}

                ,{'uid': 16, 'menu_id': 248}

                ,{'uid': 16, 'menu_id': 221}

                ,{'uid': 16, 'menu_id': 258}

                ,{'uid': 16, 'menu_id': 182}

                ,{'uid': 16, 'menu_id': 215}

                ,{'uid': 16, 'menu_id': 216}

                ,{'uid': 16, 'menu_id': 217}

                ,{'uid': 16, 'menu_id': 218}

                ,{'uid': 16, 'menu_id': 226}

                ,{'uid': 16, 'menu_id': 114}

                ,{'uid': 16, 'menu_id': 220}

                ,{'uid': 16, 'menu_id': 253}

                ,{'uid': 16, 'menu_id': 332}

                ,{'uid': 16, 'menu_id': 404}

                ,{'uid': 16, 'menu_id': 246}

                ,{'uid': 16, 'menu_id': 238}

                ,{'uid': 16, 'menu_id': 5}

                ,{'uid': 16, 'menu_id': 4}

                ,{'uid': 16, 'menu_id': 232}

                ,{'uid': 18, 'menu_id': 249}

                ,{'uid': 18, 'menu_id': 248}

                ,{'uid': 18, 'menu_id': 221}

                ,{'uid': 18, 'menu_id': 258}

                ,{'uid': 18, 'menu_id': 182}

                ,{'uid': 18, 'menu_id': 215}

                ,{'uid': 18, 'menu_id': 216}

                ,{'uid': 18, 'menu_id': 217}

                ,{'uid': 18, 'menu_id': 218}

                ,{'uid': 18, 'menu_id': 226}

                ,{'uid': 18, 'menu_id': 114}

                ,{'uid': 18, 'menu_id': 220}

                ,{'uid': 18, 'menu_id': 253}

                ,{'uid': 18, 'menu_id': 332}

                ,{'uid': 18, 'menu_id': 404}

                ,{'uid': 18, 'menu_id': 246}

                ,{'uid': 18, 'menu_id': 238}

                ,{'uid': 18, 'menu_id': 5}

                ,{'uid': 18, 'menu_id': 4}

                ,{'uid': 18, 'menu_id': 232}

                ,{'uid': 19, 'menu_id': 249}

                ,{'uid': 19, 'menu_id': 248}

                ,{'uid': 19, 'menu_id': 221}

                ,{'uid': 19, 'menu_id': 258}

                ,{'uid': 19, 'menu_id': 182}

                ,{'uid': 19, 'menu_id': 215}

                ,{'uid': 19, 'menu_id': 216}

                ,{'uid': 19, 'menu_id': 217}

                ,{'uid': 19, 'menu_id': 218}

                ,{'uid': 19, 'menu_id': 226}

                ,{'uid': 19, 'menu_id': 114}

                ,{'uid': 19, 'menu_id': 220}

                ,{'uid': 19, 'menu_id': 253}

                ,{'uid': 19, 'menu_id': 332}

                ,{'uid': 19, 'menu_id': 404}

                ,{'uid': 19, 'menu_id': 246}

                ,{'uid': 19, 'menu_id': 238}

                ,{'uid': 19, 'menu_id': 5}

                ,{'uid': 19, 'menu_id': 4}

                ,{'uid': 19, 'menu_id': 232}

                ,{'uid': 44, 'menu_id': 487}

                ,{'uid': 44, 'menu_id': 523}

                ,{'uid': 44, 'menu_id': 471}

                ,{'uid': 62, 'menu_id': 211}

                ,{'uid': 62, 'menu_id': 324}

                ,{'uid': 62, 'menu_id': 225}

                ,{'uid': 62, 'menu_id': 226}

                ,{'uid': 62, 'menu_id': 238}

                ,{'uid': 62, 'menu_id': 229}

                ,{'uid': 62, 'menu_id': 213}

                ,{'uid': 62, 'menu_id': 377}

                ,{'uid': 62, 'menu_id': 378}

                ,{'uid': 62, 'menu_id': 379}

                ,{'uid': 62, 'menu_id': 380}

                ,{'uid': 62, 'menu_id': 386}

                ,{'uid': 62, 'menu_id': 387}

                ,{'uid': 62, 'menu_id': 388}

                ,{'uid': 62, 'menu_id': 389}

                ,{'uid': 13, 'menu_id': 531}

                ,{'uid': 26, 'menu_id': 531}

                ,{'uid': 39, 'menu_id': 531}

                ,{'uid': 47, 'menu_id': 531}

                ,{'uid': 48, 'menu_id': 531}

                ,{'uid': 43, 'menu_id': 531}

                ,{'uid': 59, 'menu_id': 531}

                ,{'uid': 17, 'menu_id': 531}

                ,{'uid': 51, 'menu_id': 531}

                ,{'uid': 37, 'menu_id': 531}

                ,{'uid': 12, 'menu_id': 531}

                ,{'uid': 63, 'menu_id': 531}

                ,{'uid': 27, 'menu_id': 531}

                ,{'uid': 53, 'menu_id': 531}

                ,{'uid': 50, 'menu_id': 531}

                ,{'uid': 14, 'menu_id': 531}

                ,{'uid': 36, 'menu_id': 531}

                ,{'uid': 56, 'menu_id': 531}

                ,{'uid': 60, 'menu_id': 531}

                ,{'uid': 52, 'menu_id': 531}

                ,{'uid': 64, 'menu_id': 531}

                ,{'uid': 29, 'menu_id': 531}

                ,{'uid': 38, 'menu_id': 531}

                ,{'uid': 42, 'menu_id': 531}

                ,{'uid': 15, 'menu_id': 531}

                ,{'uid': 41, 'menu_id': 531}

                ,{'uid': 61, 'menu_id': 531}

                ,{'uid': 28, 'menu_id': 531}

                ,{'uid': 54, 'menu_id': 531}

                ,{'uid': 58, 'menu_id': 531}

                ,{'uid': 49, 'menu_id': 531}

                ,{'uid': 40, 'menu_id': 531}

                ,{'uid': 30, 'menu_id': 531}

                ,{'uid': 25, 'menu_id': 531}

                ,{'uid': 45, 'menu_id': 531}

                ,{'uid': 35, 'menu_id': 531}

                ,{'uid': 57, 'menu_id': 531}

                ,{'uid': 46, 'menu_id': 531}

                ,{'uid': 31, 'menu_id': 531}

                ,{'uid': 16, 'menu_id': 531}

                ,{'uid': 18, 'menu_id': 531}

                ,{'uid': 19, 'menu_id': 531}

                ,{'uid': 65, 'menu_id': 84}

                ,{'uid': 65, 'menu_id': 487}

                ,{'uid': 65, 'menu_id': 523}

                ,{'uid': 65, 'menu_id': 211}

                ,{'uid': 65, 'menu_id': 377}

                ,{'uid': 65, 'menu_id': 471}

                ,{'uid': 65, 'menu_id': 324}

                ,{'uid': 65, 'menu_id': 378}

                ,{'uid': 65, 'menu_id': 182}

                ,{'uid': 65, 'menu_id': 379}

                ,{'uid': 65, 'menu_id': 225}

                ,{'uid': 65, 'menu_id': 226}

                ,{'uid': 65, 'menu_id': 380}

                ,{'uid': 65, 'menu_id': 114}

                ,{'uid': 65, 'menu_id': 386}

                ,{'uid': 65, 'menu_id': 387}

                ,{'uid': 65, 'menu_id': 388}

                ,{'uid': 65, 'menu_id': 389}

                ,{'uid': 65, 'menu_id': 332}

                ,{'uid': 65, 'menu_id': 404}

                ,{'uid': 65, 'menu_id': 238}

                ,{'uid': 65, 'menu_id': 229}

                ,{'uid': 65, 'menu_id': 5}

                ,{'uid': 65, 'menu_id': 4}

                ,{'uid': 65, 'menu_id': 213}

                ,{'uid': 66, 'menu_id': 249}

                ,{'uid': 66, 'menu_id': 248}

                ,{'uid': 66, 'menu_id': 211}

                ,{'uid': 66, 'menu_id': 221}

                ,{'uid': 66, 'menu_id': 258}

                ,{'uid': 66, 'menu_id': 377}

                ,{'uid': 66, 'menu_id': 324}

                ,{'uid': 66, 'menu_id': 378}

                ,{'uid': 66, 'menu_id': 182}

                ,{'uid': 66, 'menu_id': 215}

                ,{'uid': 66, 'menu_id': 216}

                ,{'uid': 66, 'menu_id': 217}

                ,{'uid': 66, 'menu_id': 379}

                ,{'uid': 66, 'menu_id': 218}

                ,{'uid': 66, 'menu_id': 226}

                ,{'uid': 66, 'menu_id': 380}

                ,{'uid': 66, 'menu_id': 114}

                ,{'uid': 66, 'menu_id': 386}

                ,{'uid': 66, 'menu_id': 387}

                ,{'uid': 66, 'menu_id': 220}

                ,{'uid': 66, 'menu_id': 389}

                ,{'uid': 66, 'menu_id': 531}

                ,{'uid': 66, 'menu_id': 253}

                ,{'uid': 66, 'menu_id': 332}

                ,{'uid': 66, 'menu_id': 404}

                ,{'uid': 66, 'menu_id': 246}

                ,{'uid': 66, 'menu_id': 238}

                ,{'uid': 66, 'menu_id': 229}

                ,{'uid': 66, 'menu_id': 5}

                ,{'uid': 66, 'menu_id': 4}

                ,{'uid': 66, 'menu_id': 232}

                ,{'uid': 66, 'menu_id': 213}

                ,{'uid': 67, 'menu_id': 84}

                ,{'uid': 67, 'menu_id': 210}

                ,{'uid': 67, 'menu_id': 523}

                ,{'uid': 67, 'menu_id': 182}

                ,{'uid': 67, 'menu_id': 332}

                ,{'uid': 67, 'menu_id': 404}

                ,{'uid': 67, 'menu_id': 246}

                ,{'uid': 67, 'menu_id': 5}

                ,{'uid': 67, 'menu_id': 471}

                ,{'uid': 67, 'menu_id': 114}

                ,{'uid': 68, 'menu_id': 84}

                ,{'uid': 68, 'menu_id': 210}

                ,{'uid': 68, 'menu_id': 523}

                ,{'uid': 68, 'menu_id': 471}

                ,{'uid': 68, 'menu_id': 182}

                ,{'uid': 68, 'menu_id': 114}

                ,{'uid': 68, 'menu_id': 332}

                ,{'uid': 68, 'menu_id': 404}

                ,{'uid': 68, 'menu_id': 246}

                ,{'uid': 68, 'menu_id': 5}

                ,{'uid': 69, 'menu_id': 84}

                ,{'uid': 69, 'menu_id': 210}

                ,{'uid': 69, 'menu_id': 523}

                ,{'uid': 69, 'menu_id': 471}

                ,{'uid': 69, 'menu_id': 182}

                ,{'uid': 69, 'menu_id': 114}

                ,{'uid': 69, 'menu_id': 332}

                ,{'uid': 69, 'menu_id': 404}

                ,{'uid': 69, 'menu_id': 246}

                ,{'uid': 69, 'menu_id': 5}

                ,{'uid': 48, 'menu_id': 487}

                ,{'uid': 48, 'menu_id': 523}

                ,{'uid': 48, 'menu_id': 471}

                ,{'uid': 56, 'menu_id': 487}

                ,{'uid': 56, 'menu_id': 523}

                ,{'uid': 56, 'menu_id': 471}

                ,{'uid': 56, 'menu_id': 241}

                ,{'uid': 56, 'menu_id': 214}

                ,{'uid': 56, 'menu_id': 372}

                ,{'uid': 56, 'menu_id': 373}

                ,{'uid': 56, 'menu_id': 374}

                ,{'uid': 56, 'menu_id': 324}

                ,{'uid': 56, 'menu_id': 377}

                ,{'uid': 56, 'menu_id': 378}

                ,{'uid': 56, 'menu_id': 379}

                ,{'uid': 56, 'menu_id': 380}

                ,{'uid': 56, 'menu_id': 386}

                ,{'uid': 56, 'menu_id': 387}

                ,{'uid': 56, 'menu_id': 389}

                ,{'uid': 70, 'menu_id': 249}

                ,{'uid': 70, 'menu_id': 248}

                ,{'uid': 70, 'menu_id': 221}

                ,{'uid': 70, 'menu_id': 258}

                ,{'uid': 70, 'menu_id': 377}

                ,{'uid': 70, 'menu_id': 182}

                ,{'uid': 70, 'menu_id': 215}

                ,{'uid': 70, 'menu_id': 216}

                ,{'uid': 70, 'menu_id': 217}

                ,{'uid': 70, 'menu_id': 218}

                ,{'uid': 70, 'menu_id': 226}

                ,{'uid': 70, 'menu_id': 114}

                ,{'uid': 70, 'menu_id': 220}

                ,{'uid': 70, 'menu_id': 389}

                ,{'uid': 70, 'menu_id': 531}

                ,{'uid': 70, 'menu_id': 253}

                ,{'uid': 70, 'menu_id': 332}

                ,{'uid': 70, 'menu_id': 404}

                ,{'uid': 70, 'menu_id': 246}

                ,{'uid': 70, 'menu_id': 238}

                ,{'uid': 70, 'menu_id': 229}

                ,{'uid': 70, 'menu_id': 5}

                ,{'uid': 70, 'menu_id': 4}

                ,{'uid': 70, 'menu_id': 232}

                ,{'uid': 70, 'menu_id': 213}

                ,{'uid': 48, 'menu_id': 66}

                ,{'uid': 48, 'menu_id': 535}

                ,{'uid': 45, 'menu_id': 535}

                ,{'uid': 45, 'menu_id': 487}

                ,{'uid': 45, 'menu_id': 523}

                ,{'uid': 45, 'menu_id': 471}

                ,{'uid': 71, 'menu_id': 72}

                ,{'uid': 71, 'menu_id': 207}

                ,{'uid': 71, 'menu_id': 221}

                ,{'uid': 71, 'menu_id': 258}

                ,{'uid': 71, 'menu_id': 182}

                ,{'uid': 71, 'menu_id': 215}

                ,{'uid': 71, 'menu_id': 216}

                ,{'uid': 71, 'menu_id': 217}

                ,{'uid': 71, 'menu_id': 218}

                ,{'uid': 71, 'menu_id': 226}

                ,{'uid': 71, 'menu_id': 114}

                ,{'uid': 71, 'menu_id': 220}

                ,{'uid': 71, 'menu_id': 253}

                ,{'uid': 71, 'menu_id': 332}

                ,{'uid': 71, 'menu_id': 404}

                ,{'uid': 71, 'menu_id': 238}

                ,{'uid': 71, 'menu_id': 5}

                ,{'uid': 71, 'menu_id': 4}

                ,{'uid': 71, 'menu_id': 232}

                ,{'uid': 72, 'menu_id': 249}

                ,{'uid': 72, 'menu_id': 248}

                ,{'uid': 72, 'menu_id': 84}

                ,{'uid': 72, 'menu_id': 211}

                ,{'uid': 72, 'menu_id': 221}

                ,{'uid': 72, 'menu_id': 258}

                ,{'uid': 72, 'menu_id': 324}

                ,{'uid': 72, 'menu_id': 182}

                ,{'uid': 72, 'menu_id': 215}

                ,{'uid': 72, 'menu_id': 216}

                ,{'uid': 72, 'menu_id': 217}

                ,{'uid': 72, 'menu_id': 384}

                ,{'uid': 72, 'menu_id': 218}

                ,{'uid': 72, 'menu_id': 226}

                ,{'uid': 72, 'menu_id': 114}

                ,{'uid': 72, 'menu_id': 220}

                ,{'uid': 72, 'menu_id': 531}

                ,{'uid': 72, 'menu_id': 253}

                ,{'uid': 72, 'menu_id': 332}

                ,{'uid': 72, 'menu_id': 404}

                ,{'uid': 72, 'menu_id': 246}

                ,{'uid': 72, 'menu_id': 238}

                ,{'uid': 72, 'menu_id': 229}

                ,{'uid': 72, 'menu_id': 5}

                ,{'uid': 72, 'menu_id': 4}

                ,{'uid': 72, 'menu_id': 232}

                ,{'uid': 72, 'menu_id': 213}

                ,{'uid': 73, 'menu_id': 249}

                ,{'uid': 73, 'menu_id': 248}

                ,{'uid': 73, 'menu_id': 84}

                ,{'uid': 73, 'menu_id': 211}

                ,{'uid': 73, 'menu_id': 221}

                ,{'uid': 73, 'menu_id': 258}

                ,{'uid': 73, 'menu_id': 324}

                ,{'uid': 73, 'menu_id': 182}

                ,{'uid': 73, 'menu_id': 215}

                ,{'uid': 73, 'menu_id': 216}

                ,{'uid': 73, 'menu_id': 217}

                ,{'uid': 73, 'menu_id': 384}

                ,{'uid': 73, 'menu_id': 218}

                ,{'uid': 73, 'menu_id': 226}

                ,{'uid': 73, 'menu_id': 114}

                ,{'uid': 73, 'menu_id': 220}

                ,{'uid': 73, 'menu_id': 531}

                ,{'uid': 73, 'menu_id': 253}

                ,{'uid': 73, 'menu_id': 332}

                ,{'uid': 73, 'menu_id': 404}

                ,{'uid': 73, 'menu_id': 246}

                ,{'uid': 73, 'menu_id': 238}

                ,{'uid': 73, 'menu_id': 229}

                ,{'uid': 73, 'menu_id': 5}

                ,{'uid': 73, 'menu_id': 4}

                ,{'uid': 73, 'menu_id': 232}

                ,{'uid': 73, 'menu_id': 213}

                ,{'uid': 50, 'menu_id': 224}

                ,{'uid': 50, 'menu_id': 318}

                ,{'uid': 50, 'menu_id': 223}

                ,{'uid': 75, 'menu_id': 66}

                ,{'uid': 75, 'menu_id': 249}

                ,{'uid': 75, 'menu_id': 248}

                ,{'uid': 75, 'menu_id': 487}

                ,{'uid': 75, 'menu_id': 523}

                ,{'uid': 75, 'menu_id': 211}

                ,{'uid': 75, 'menu_id': 221}

                ,{'uid': 75, 'menu_id': 258}

                ,{'uid': 75, 'menu_id': 377}

                ,{'uid': 75, 'menu_id': 471}

                ,{'uid': 75, 'menu_id': 378}

                ,{'uid': 75, 'menu_id': 182}

                ,{'uid': 75, 'menu_id': 215}

                ,{'uid': 75, 'menu_id': 216}

                ,{'uid': 75, 'menu_id': 217}

                ,{'uid': 75, 'menu_id': 379}

                ,{'uid': 75, 'menu_id': 218}

                ,{'uid': 75, 'menu_id': 226}

                ,{'uid': 75, 'menu_id': 380}

                ,{'uid': 75, 'menu_id': 114}

                ,{'uid': 75, 'menu_id': 386}

                ,{'uid': 75, 'menu_id': 387}

                ,{'uid': 75, 'menu_id': 220}

                ,{'uid': 75, 'menu_id': 389}

                ,{'uid': 75, 'menu_id': 531}

                ,{'uid': 75, 'menu_id': 253}

                ,{'uid': 75, 'menu_id': 535}

                ,{'uid': 75, 'menu_id': 332}

                ,{'uid': 75, 'menu_id': 404}

                ,{'uid': 75, 'menu_id': 246}

                ,{'uid': 75, 'menu_id': 238}

                ,{'uid': 75, 'menu_id': 229}

                ,{'uid': 75, 'menu_id': 5}

                ,{'uid': 75, 'menu_id': 4}

                ,{'uid': 75, 'menu_id': 232}

                ,{'uid': 75, 'menu_id': 213}

                ,{'uid': 76, 'menu_id': 66}

                ,{'uid': 76, 'menu_id': 249}

                ,{'uid': 76, 'menu_id': 248}

                ,{'uid': 76, 'menu_id': 487}

                ,{'uid': 76, 'menu_id': 523}

                ,{'uid': 76, 'menu_id': 211}

                ,{'uid': 76, 'menu_id': 221}

                ,{'uid': 76, 'menu_id': 258}

                ,{'uid': 76, 'menu_id': 377}

                ,{'uid': 76, 'menu_id': 471}

                ,{'uid': 76, 'menu_id': 378}

                ,{'uid': 76, 'menu_id': 182}

                ,{'uid': 76, 'menu_id': 215}

                ,{'uid': 76, 'menu_id': 216}

                ,{'uid': 76, 'menu_id': 217}

                ,{'uid': 76, 'menu_id': 379}

                ,{'uid': 76, 'menu_id': 218}

                ,{'uid': 76, 'menu_id': 226}

                ,{'uid': 76, 'menu_id': 380}

                ,{'uid': 76, 'menu_id': 114}

                ,{'uid': 76, 'menu_id': 386}

                ,{'uid': 76, 'menu_id': 387}

                ,{'uid': 76, 'menu_id': 220}

                ,{'uid': 76, 'menu_id': 389}

                ,{'uid': 76, 'menu_id': 531}

                ,{'uid': 76, 'menu_id': 253}

                ,{'uid': 76, 'menu_id': 535}

                ,{'uid': 76, 'menu_id': 332}

                ,{'uid': 76, 'menu_id': 404}

                ,{'uid': 76, 'menu_id': 246}

                ,{'uid': 76, 'menu_id': 238}

                ,{'uid': 76, 'menu_id': 229}

                ,{'uid': 76, 'menu_id': 5}

                ,{'uid': 76, 'menu_id': 4}

                ,{'uid': 76, 'menu_id': 232}

                ,{'uid': 76, 'menu_id': 213}

                ,{'uid': 77, 'menu_id': 66}

                ,{'uid': 77, 'menu_id': 249}

                ,{'uid': 77, 'menu_id': 248}

                ,{'uid': 77, 'menu_id': 487}

                ,{'uid': 77, 'menu_id': 523}

                ,{'uid': 77, 'menu_id': 211}

                ,{'uid': 77, 'menu_id': 221}

                ,{'uid': 77, 'menu_id': 258}

                ,{'uid': 77, 'menu_id': 377}

                ,{'uid': 77, 'menu_id': 471}

                ,{'uid': 77, 'menu_id': 378}

                ,{'uid': 77, 'menu_id': 182}

                ,{'uid': 77, 'menu_id': 215}

                ,{'uid': 77, 'menu_id': 216}

                ,{'uid': 77, 'menu_id': 217}

                ,{'uid': 77, 'menu_id': 379}

                ,{'uid': 77, 'menu_id': 218}

                ,{'uid': 77, 'menu_id': 226}

                ,{'uid': 77, 'menu_id': 380}

                ,{'uid': 77, 'menu_id': 114}

                ,{'uid': 77, 'menu_id': 386}

                ,{'uid': 77, 'menu_id': 387}

                ,{'uid': 77, 'menu_id': 220}

                ,{'uid': 77, 'menu_id': 389}

                ,{'uid': 77, 'menu_id': 531}

                ,{'uid': 77, 'menu_id': 253}

                ,{'uid': 77, 'menu_id': 535}

                ,{'uid': 77, 'menu_id': 332}

                ,{'uid': 77, 'menu_id': 404}

                ,{'uid': 77, 'menu_id': 246}

                ,{'uid': 77, 'menu_id': 238}

                ,{'uid': 77, 'menu_id': 229}

                ,{'uid': 77, 'menu_id': 5}

                ,{'uid': 77, 'menu_id': 4}

                ,{'uid': 77, 'menu_id': 232}

                ,{'uid': 77, 'menu_id': 213}

                ,{'uid': 78, 'menu_id': 66}

                ,{'uid': 78, 'menu_id': 249}

                ,{'uid': 78, 'menu_id': 248}

                ,{'uid': 78, 'menu_id': 487}

                ,{'uid': 78, 'menu_id': 523}

                ,{'uid': 78, 'menu_id': 211}

                ,{'uid': 78, 'menu_id': 221}

                ,{'uid': 78, 'menu_id': 258}

                ,{'uid': 78, 'menu_id': 377}

                ,{'uid': 78, 'menu_id': 471}

                ,{'uid': 78, 'menu_id': 378}

                ,{'uid': 78, 'menu_id': 182}

                ,{'uid': 78, 'menu_id': 215}

                ,{'uid': 78, 'menu_id': 216}

                ,{'uid': 78, 'menu_id': 217}

                ,{'uid': 78, 'menu_id': 379}

                ,{'uid': 78, 'menu_id': 218}

                ,{'uid': 78, 'menu_id': 226}

                ,{'uid': 78, 'menu_id': 380}

                ,{'uid': 78, 'menu_id': 114}

                ,{'uid': 78, 'menu_id': 386}

                ,{'uid': 78, 'menu_id': 387}

                ,{'uid': 78, 'menu_id': 220}

                ,{'uid': 78, 'menu_id': 389}

                ,{'uid': 78, 'menu_id': 531}

                ,{'uid': 78, 'menu_id': 253}

                ,{'uid': 78, 'menu_id': 535}

                ,{'uid': 78, 'menu_id': 332}

                ,{'uid': 78, 'menu_id': 404}

                ,{'uid': 78, 'menu_id': 246}

                ,{'uid': 78, 'menu_id': 238}

                ,{'uid': 78, 'menu_id': 229}

                ,{'uid': 78, 'menu_id': 5}

                ,{'uid': 78, 'menu_id': 4}

                ,{'uid': 78, 'menu_id': 232}

                ,{'uid': 78, 'menu_id': 213}

                ,{'uid': 79, 'menu_id': 66}

                ,{'uid': 79, 'menu_id': 249}

                ,{'uid': 79, 'menu_id': 248}

                ,{'uid': 79, 'menu_id': 487}

                ,{'uid': 79, 'menu_id': 523}

                ,{'uid': 79, 'menu_id': 211}

                ,{'uid': 79, 'menu_id': 221}

                ,{'uid': 79, 'menu_id': 258}

                ,{'uid': 79, 'menu_id': 377}

                ,{'uid': 79, 'menu_id': 471}

                ,{'uid': 79, 'menu_id': 378}

                ,{'uid': 79, 'menu_id': 182}

                ,{'uid': 79, 'menu_id': 215}

                ,{'uid': 79, 'menu_id': 216}

                ,{'uid': 79, 'menu_id': 217}

                ,{'uid': 79, 'menu_id': 379}

                ,{'uid': 79, 'menu_id': 218}

                ,{'uid': 79, 'menu_id': 226}

                ,{'uid': 79, 'menu_id': 380}

                ,{'uid': 79, 'menu_id': 114}

                ,{'uid': 79, 'menu_id': 386}

                ,{'uid': 79, 'menu_id': 387}

                ,{'uid': 79, 'menu_id': 220}

                ,{'uid': 79, 'menu_id': 389}

                ,{'uid': 79, 'menu_id': 531}

                ,{'uid': 79, 'menu_id': 253}

                ,{'uid': 79, 'menu_id': 535}

                ,{'uid': 79, 'menu_id': 332}

                ,{'uid': 79, 'menu_id': 404}

                ,{'uid': 79, 'menu_id': 246}

                ,{'uid': 79, 'menu_id': 238}

                ,{'uid': 79, 'menu_id': 229}

                ,{'uid': 79, 'menu_id': 5}

                ,{'uid': 79, 'menu_id': 4}

                ,{'uid': 79, 'menu_id': 232}

                ,{'uid': 79, 'menu_id': 213}

                ,{'uid': 80, 'menu_id': 66}

                ,{'uid': 80, 'menu_id': 249}

                ,{'uid': 80, 'menu_id': 248}

                ,{'uid': 80, 'menu_id': 487}

                ,{'uid': 80, 'menu_id': 523}

                ,{'uid': 80, 'menu_id': 211}

                ,{'uid': 80, 'menu_id': 221}

                ,{'uid': 80, 'menu_id': 258}

                ,{'uid': 80, 'menu_id': 377}

                ,{'uid': 80, 'menu_id': 471}

                ,{'uid': 80, 'menu_id': 378}

                ,{'uid': 80, 'menu_id': 182}

                ,{'uid': 80, 'menu_id': 215}

                ,{'uid': 80, 'menu_id': 216}

                ,{'uid': 80, 'menu_id': 217}

                ,{'uid': 80, 'menu_id': 379}

                ,{'uid': 80, 'menu_id': 218}

                ,{'uid': 80, 'menu_id': 226}

                ,{'uid': 80, 'menu_id': 380}

                ,{'uid': 80, 'menu_id': 114}

                ,{'uid': 80, 'menu_id': 386}

                ,{'uid': 80, 'menu_id': 387}

                ,{'uid': 80, 'menu_id': 220}

                ,{'uid': 80, 'menu_id': 389}

                ,{'uid': 80, 'menu_id': 531}

                ,{'uid': 80, 'menu_id': 253}

                ,{'uid': 80, 'menu_id': 535}

                ,{'uid': 80, 'menu_id': 332}

                ,{'uid': 80, 'menu_id': 404}

                ,{'uid': 80, 'menu_id': 246}

                ,{'uid': 80, 'menu_id': 238}

                ,{'uid': 80, 'menu_id': 229}

                ,{'uid': 80, 'menu_id': 5}

                ,{'uid': 80, 'menu_id': 4}

                ,{'uid': 80, 'menu_id': 232}

                ,{'uid': 80, 'menu_id': 213}

                ,{'uid': 80, 'menu_id': 539}

                ,{'uid': 80, 'menu_id': 540}

                ,{'uid': 80, 'menu_id': 541}

                ,{'uid': 80, 'menu_id': 542}

                ,{'uid': 80, 'menu_id': 538}

                ,{'uid': 7, 'menu_id': 386}

                ,{'uid': 71, 'menu_id': 386}

                ,{'uid': 51, 'menu_id': 224}

                ,{'uid': 51, 'menu_id': 318}

                ,{'uid': 51, 'menu_id': 212}

                ,{'uid': 51, 'menu_id': 202}

                ,{'uid': 51, 'menu_id': 571}

                ,{'uid': 51, 'menu_id': 539}

                ,{'uid': 51, 'menu_id': 551}

                ,{'uid': 51, 'menu_id': 560}

                ,{'uid': 51, 'menu_id': 540}

                ,{'uid': 51, 'menu_id': 566}

                ,{'uid': 51, 'menu_id': 533}

                ,{'uid': 51, 'menu_id': 559}

                ,{'uid': 51, 'menu_id': 542}

                ,{'uid': 51, 'menu_id': 538}

                ,{'uid': 81, 'menu_id': 66}

                ,{'uid': 81, 'menu_id': 249}

                ,{'uid': 81, 'menu_id': 248}

                ,{'uid': 81, 'menu_id': 487}

                ,{'uid': 81, 'menu_id': 523}

                ,{'uid': 81, 'menu_id': 211}

                ,{'uid': 81, 'menu_id': 221}

                ,{'uid': 81, 'menu_id': 258}

                ,{'uid': 81, 'menu_id': 471}

                ,{'uid': 81, 'menu_id': 182}

                ,{'uid': 81, 'menu_id': 215}

                ,{'uid': 81, 'menu_id': 216}

                ,{'uid': 81, 'menu_id': 217}

                ,{'uid': 81, 'menu_id': 218}

                ,{'uid': 81, 'menu_id': 226}

                ,{'uid': 81, 'menu_id': 380}

                ,{'uid': 81, 'menu_id': 114}

                ,{'uid': 81, 'menu_id': 386}

                ,{'uid': 81, 'menu_id': 387}

                ,{'uid': 81, 'menu_id': 220}

                ,{'uid': 81, 'menu_id': 389}

                ,{'uid': 81, 'menu_id': 531}

                ,{'uid': 81, 'menu_id': 253}

                ,{'uid': 81, 'menu_id': 535}

                ,{'uid': 81, 'menu_id': 332}

                ,{'uid': 81, 'menu_id': 404}

                ,{'uid': 81, 'menu_id': 246}

                ,{'uid': 81, 'menu_id': 238}

                ,{'uid': 81, 'menu_id': 229}

                ,{'uid': 81, 'menu_id': 5}

                ,{'uid': 81, 'menu_id': 4}

                ,{'uid': 81, 'menu_id': 232}

                ,{'uid': 81, 'menu_id': 213}

                ,{'uid': 81, 'menu_id': 473}

                ,{'uid': 81, 'menu_id': 136}

                ,{'uid': 81, 'menu_id': 476}

                ,{'uid': 81, 'menu_id': 477}

                ,{'uid': 81, 'menu_id': 475}

                ,{'uid': 81, 'menu_id': 478}

                ,{'uid': 81, 'menu_id': 347}

                ,{'uid': 81, 'menu_id': 474}

                ,{'uid': 81, 'menu_id': 472}

                ,{'uid': 81, 'menu_id': 519}

                ,{'uid': 81, 'menu_id': 540}

                ,{'uid': 81, 'menu_id': 552}

                ,{'uid': 81, 'menu_id': 525}

                ,{'uid': 81, 'menu_id': 557}

                ,{'uid': 81, 'menu_id': 559}

                ,{'uid': 81, 'menu_id': 520}

                ,{'uid': 81, 'menu_id': 532}

                ,{'uid': 81, 'menu_id': 587}

                ,{'uid': 81, 'menu_id': 524}

                ,{'uid': 81, 'menu_id': 581}

                ,{'uid': 81, 'menu_id': 526}

                ,{'uid': 81, 'menu_id': 350}

                ,{'uid': 81, 'menu_id': 563}

                ,{'uid': 81, 'menu_id': 569}

                ,{'uid': 81, 'menu_id': 117}

                ,{'uid': 81, 'menu_id': 148}

                ,{'uid': 81, 'menu_id': 572}

                ,{'uid': 81, 'menu_id': 568}

                ,{'uid': 81, 'menu_id': 570}

                ,{'uid': 81, 'menu_id': 203}

                ,{'uid': 81, 'menu_id': 573}

                ,{'uid': 81, 'menu_id': 202}

                ,{'uid': 81, 'menu_id': 571}

                ,{'uid': 81, 'menu_id': 577}

                ,{'uid': 81, 'menu_id': 566}

                ,{'uid': 81, 'menu_id': 539}

                ,{'uid': 81, 'menu_id': 551}

                ,{'uid': 81, 'menu_id': 560}

                ,{'uid': 81, 'menu_id': 26}

                ,{'uid': 81, 'menu_id': 324}

                ,{'uid': 81, 'menu_id': 498}

                ,{'uid': 81, 'menu_id': 556}

                ,{'uid': 81, 'menu_id': 562}

                ,{'uid': 81, 'menu_id': 453}

                ,{'uid': 81, 'menu_id': 541}

                ,{'uid': 81, 'menu_id': 549}

                ,{'uid': 81, 'menu_id': 553}

                ,{'uid': 81, 'menu_id': 150}

                ,{'uid': 81, 'menu_id': 188}

                ,{'uid': 81, 'menu_id': 225}

                ,{'uid': 81, 'menu_id': 542}

                ,{'uid': 81, 'menu_id': 554}

                ,{'uid': 81, 'menu_id': 561}

                ,{'uid': 81, 'menu_id': 550}

                ,{'uid': 81, 'menu_id': 382}

                ,{'uid': 81, 'menu_id': 538}

                ,{'uid': 81, 'menu_id': 584}

                ,{'uid': 81, 'menu_id': 533}

                ,{'uid': 81, 'menu_id': 335}

                ,{'uid': 81, 'menu_id': 565}

                ,{'uid': 81, 'menu_id': 388}

                ,{'uid': 82, 'menu_id': 66}

                ,{'uid': 82, 'menu_id': 117}

                ,{'uid': 82, 'menu_id': 148}

                ,{'uid': 82, 'menu_id': 249}

                ,{'uid': 82, 'menu_id': 473}

                ,{'uid': 82, 'menu_id': 569}

                ,{'uid': 82, 'menu_id': 572}

                ,{'uid': 82, 'menu_id': 136}

                ,{'uid': 82, 'menu_id': 203}

                ,{'uid': 82, 'menu_id': 476}

                ,{'uid': 82, 'menu_id': 568}

                ,{'uid': 82, 'menu_id': 570}

                ,{'uid': 82, 'menu_id': 573}

                ,{'uid': 82, 'menu_id': 202}

                ,{'uid': 82, 'menu_id': 248}

                ,{'uid': 82, 'menu_id': 477}

                ,{'uid': 82, 'menu_id': 571}

                ,{'uid': 82, 'menu_id': 475}

                ,{'uid': 82, 'menu_id': 577}

                ,{'uid': 82, 'menu_id': 478}

                ,{'uid': 82, 'menu_id': 347}

                ,{'uid': 82, 'menu_id': 474}

                ,{'uid': 82, 'menu_id': 487}

                ,{'uid': 82, 'menu_id': 523}

                ,{'uid': 82, 'menu_id': 26}

                ,{'uid': 82, 'menu_id': 211}

                ,{'uid': 82, 'menu_id': 221}

                ,{'uid': 82, 'menu_id': 258}

                ,{'uid': 82, 'menu_id': 472}

                ,{'uid': 82, 'menu_id': 519}

                ,{'uid': 82, 'menu_id': 539}

                ,{'uid': 82, 'menu_id': 551}

                ,{'uid': 82, 'menu_id': 560}

                ,{'uid': 82, 'menu_id': 566}

                ,{'uid': 82, 'menu_id': 471}

                ,{'uid': 82, 'menu_id': 324}

                ,{'uid': 82, 'menu_id': 498}

                ,{'uid': 82, 'menu_id': 525}

                ,{'uid': 82, 'menu_id': 540}

                ,{'uid': 82, 'menu_id': 552}

                ,{'uid': 82, 'menu_id': 556}

                ,{'uid': 82, 'menu_id': 562}

                ,{'uid': 82, 'menu_id': 182}

                ,{'uid': 82, 'menu_id': 215}

                ,{'uid': 82, 'menu_id': 216}

                ,{'uid': 82, 'menu_id': 217}

                ,{'uid': 82, 'menu_id': 453}

                ,{'uid': 82, 'menu_id': 520}

                ,{'uid': 82, 'menu_id': 541}

                ,{'uid': 82, 'menu_id': 549}

                ,{'uid': 82, 'menu_id': 553}
                ,{'uid': 82, 'menu_id': 557}
                ,{'uid': 82, 'menu_id': 559}
                ,{'uid': 82, 'menu_id': 150}
                ,{'uid': 82, 'menu_id': 188}
                ,{'uid': 82, 'menu_id': 218}
                ,{'uid': 82, 'menu_id': 225}
                ,{'uid': 82, 'menu_id': 542}
                ,{'uid': 82, 'menu_id': 554}
                ,{'uid': 82, 'menu_id': 561}
                ,{'uid': 82, 'menu_id': 226}
                ,{'uid': 82, 'menu_id': 380}
                ,{'uid': 82, 'menu_id': 382}
                ,{'uid': 82, 'menu_id': 550}
                ,{'uid': 82, 'menu_id': 565}
                ,{'uid': 82, 'menu_id': 114}
                ,{'uid': 82, 'menu_id': 386}
                ,{'uid': 82, 'menu_id': 524}
                ,{'uid': 82, 'menu_id': 532}
                ,{'uid': 82, 'menu_id': 538}
                ,{'uid': 82, 'menu_id': 587}
                ,{'uid': 82, 'menu_id': 387}
                ,{'uid': 82, 'menu_id': 526}
                ,{'uid': 82, 'menu_id': 581}
                ,{'uid': 82, 'menu_id': 584}
                ,{'uid': 82, 'menu_id': 388}
                ,{'uid': 82, 'menu_id': 220}
                ,{'uid': 82, 'menu_id': 389}
                ,{'uid': 82, 'menu_id': 531}
                ,{'uid': 82, 'menu_id': 533}
                ,{'uid': 82, 'menu_id': 350}
                ,{'uid': 82, 'menu_id': 253}
                ,{'uid': 82, 'menu_id': 335}
                ,{'uid': 82, 'menu_id': 563}
                ,{'uid': 82, 'menu_id': 535}
                ,{'uid': 82, 'menu_id': 332}
                ,{'uid': 82, 'menu_id': 404}
                ,{'uid': 82, 'menu_id': 246}
                ,{'uid': 82, 'menu_id': 238}
                ,{'uid': 82, 'menu_id': 229}
                ,{'uid': 82, 'menu_id': 5}
                ,{'uid': 82, 'menu_id': 4}
                ,{'uid': 82, 'menu_id': 232}
                ,{'uid': 82, 'menu_id': 213}
                ,{'uid': 38, 'menu_id': 156}
                ,{'uid': 38, 'menu_id': 159}
                ,{'uid': 38, 'menu_id': 486}
                ,{'uid': 38, 'menu_id': 569}
                ,{'uid': 38, 'menu_id': 568}
                ,{'uid': 38, 'menu_id': 570}
                ,{'uid': 38, 'menu_id': 158}
                ,{'uid': 38, 'menu_id': 130}
                ,{'uid': 38, 'menu_id': 487}
                ,{'uid': 38, 'menu_id': 83}
                ,{'uid': 38, 'menu_id': 291}
                ,{'uid': 38, 'menu_id': 296}
                ,{'uid': 38, 'menu_id': 488}
                ,{'uid': 38, 'menu_id': 489}
                ,{'uid': 38, 'menu_id': 566}
                ,{'uid': 38, 'menu_id': 502}
                ,{'uid': 38, 'menu_id': 212}
                ,{'uid': 38, 'menu_id': 386}
                ,{'uid': 38, 'menu_id': 532}
                ,{'uid': 38, 'menu_id': 563}
                ,{'uid': 83, 'menu_id': 84}
                ,{'uid': 83, 'menu_id': 487}
                ,{'uid': 83, 'menu_id': 523}
                ,{'uid': 83, 'menu_id': 211}
                ,{'uid': 83, 'menu_id': 471}
                ,{'uid': 83, 'menu_id': 324}
                ,{'uid': 83, 'menu_id': 182}
                ,{'uid': 83, 'menu_id': 225}
                ,{'uid': 83, 'menu_id': 226}
                ,{'uid': 83, 'menu_id': 380}
                ,{'uid': 83, 'menu_id': 114}
                ,{'uid': 83, 'menu_id': 386}
                ,{'uid': 83, 'menu_id': 387}
                ,{'uid': 83, 'menu_id': 388}
                ,{'uid': 83, 'menu_id': 389}
                ,{'uid': 83, 'menu_id': 531}
                ,{'uid': 83, 'menu_id': 332}
                ,{'uid': 83, 'menu_id': 404}
                ,{'uid': 83, 'menu_id': 246}
                ,{'uid': 83, 'menu_id': 238}
                ,{'uid': 83, 'menu_id': 77}
                ,{'uid': 83, 'menu_id': 229}
                ,{'uid': 83, 'menu_id': 5}
                ,{'uid': 83, 'menu_id': 4}
                ,{'uid': 83, 'menu_id': 213}
                ,{'uid': 85, 'menu_id': 84}
                ,{'uid': 85, 'menu_id': 487}
                ,{'uid': 85, 'menu_id': 523}
                ,{'uid': 85, 'menu_id': 211}
                ,{'uid': 85, 'menu_id': 471}
                ,{'uid': 85, 'menu_id': 324}
                ,{'uid': 85, 'menu_id': 182}
                ,{'uid': 85, 'menu_id': 225}
                ,{'uid': 85, 'menu_id': 226}
                ,{'uid': 85, 'menu_id': 380}
                ,{'uid': 85, 'menu_id': 114}
                ,{'uid': 85, 'menu_id': 386}
                ,{'uid': 85, 'menu_id': 387}
                ,{'uid': 85, 'menu_id': 388}
                ,{'uid': 85, 'menu_id': 389}
                ,{'uid': 85, 'menu_id': 531}
                ,{'uid': 85, 'menu_id': 332}
                ,{'uid': 85, 'menu_id': 404}
                ,{'uid': 85, 'menu_id': 246}
                ,{'uid': 85, 'menu_id': 238}
                ,{'uid': 85, 'menu_id': 77}
                ,{'uid': 85, 'menu_id': 229}
                ,{'uid': 85, 'menu_id': 5}
                ,{'uid': 85, 'menu_id': 4}
                ,{'uid': 85, 'menu_id': 213}
                ,{'uid': 86, 'menu_id': 84}
                ,{'uid': 86, 'menu_id': 487}
                ,{'uid': 86, 'menu_id': 523}
                ,{'uid': 86, 'menu_id': 211}
                ,{'uid': 86, 'menu_id': 471}
                ,{'uid': 86, 'menu_id': 324}
                ,{'uid': 86, 'menu_id': 182}
                ,{'uid': 86, 'menu_id': 225}
                ,{'uid': 86, 'menu_id': 226}
                ,{'uid': 86, 'menu_id': 380}
                ,{'uid': 86, 'menu_id': 114}
                ,{'uid': 86, 'menu_id': 386}
                ,{'uid': 86, 'menu_id': 387}
                ,{'uid': 86, 'menu_id': 388}
                ,{'uid': 86, 'menu_id': 389}
                ,{'uid': 86, 'menu_id': 531}
                ,{'uid': 86, 'menu_id': 332}
                ,{'uid': 86, 'menu_id': 404}
                ,{'uid': 86, 'menu_id': 246}
                ,{'uid': 86, 'menu_id': 238}
                ,{'uid': 86, 'menu_id': 77}
                ,{'uid': 86, 'menu_id': 229}
                ,{'uid': 86, 'menu_id': 5}
                ,{'uid': 86, 'menu_id': 4}
                ,{'uid': 86, 'menu_id': 213}
                ,{'uid': 86, 'menu_id': 563}
                ,{'uid': 86, 'menu_id': 117}
                ,{'uid': 86, 'menu_id': 148}
                ,{'uid': 86, 'menu_id': 569}
                ,{'uid': 86, 'menu_id': 572}
                ,{'uid': 86, 'menu_id': 203}
                ,{'uid': 86, 'menu_id': 568}
                ,{'uid': 86, 'menu_id': 570}
                ,{'uid': 86, 'menu_id': 573}
                ,{'uid': 86, 'menu_id': 202}
                ,{'uid': 86, 'menu_id': 571}
                ,{'uid': 86, 'menu_id': 539}
                ,{'uid': 86, 'menu_id': 551}
                ,{'uid': 86, 'menu_id': 560}
                ,{'uid': 86, 'menu_id': 566}
                ,{'uid': 86, 'menu_id': 540}
                ,{'uid': 86, 'menu_id': 552}
                ,{'uid': 86, 'menu_id': 562}
                ,{'uid': 86, 'menu_id': 541}
                ,{'uid': 86, 'menu_id': 549}
                ,{'uid': 86, 'menu_id': 553}
                ,{'uid': 86, 'menu_id': 559}
                ,{'uid': 86, 'menu_id': 542}
                ,{'uid': 86, 'menu_id': 554}
                ,{'uid': 86, 'menu_id': 558}
                ,{'uid': 86, 'menu_id': 561}
                ,{'uid': 86, 'menu_id': 550}
                ,{'uid': 86, 'menu_id': 538}
                ,{'uid': 86, 'menu_id': 585}
                ,{'uid': 86, 'menu_id': 533}
                ,{'uid': 86, 'menu_id': 534}
                ,{'uid': 86, 'menu_id': 535}
                ,{'uid': 85, 'menu_id': 569}
                ,{'uid': 85, 'menu_id': 117}
                ,{'uid': 85, 'menu_id': 148}
                ,{'uid': 85, 'menu_id': 152}
                ,{'uid': 85, 'menu_id': 572}
                ,{'uid': 85, 'menu_id': 568}
                ,{'uid': 85, 'menu_id': 570}
                ,{'uid': 85, 'menu_id': 203}
                ,{'uid': 85, 'menu_id': 573}
                ,{'uid': 85, 'menu_id': 202}
                ,{'uid': 85, 'menu_id': 571}
                ,{'uid': 85, 'menu_id': 566}
                ,{'uid': 85, 'menu_id': 539}
                ,{'uid': 85, 'menu_id': 551}
                ,{'uid': 85, 'menu_id': 560}
                ,{'uid': 85, 'menu_id': 540}
                ,{'uid': 85, 'menu_id': 552}
                ,{'uid': 85, 'menu_id': 562}
                ,{'uid': 85, 'menu_id': 541}
                ,{'uid': 85, 'menu_id': 549}
                ,{'uid': 85, 'menu_id': 553}
                ,{'uid': 85, 'menu_id': 559}
                ,{'uid': 85, 'menu_id': 542}
                ,{'uid': 85, 'menu_id': 554}
                ,{'uid': 85, 'menu_id': 561}
                ,{'uid': 85, 'menu_id': 550}
                ,{'uid': 85, 'menu_id': 538}
                ,{'uid': 85, 'menu_id': 585}
                ,{'uid': 85, 'menu_id': 533}
                ,{'uid': 85, 'menu_id': 563}
                ,{'uid': 83, 'menu_id': 569}
                ,{'uid': 83, 'menu_id': 117}
                ,{'uid': 83, 'menu_id': 148}
                ,{'uid': 83, 'menu_id': 152}
                ,{'uid': 83, 'menu_id': 572}
                ,{'uid': 83, 'menu_id': 568}
                ,{'uid': 83, 'menu_id': 570}
                ,{'uid': 83, 'menu_id': 203}
                ,{'uid': 83, 'menu_id': 573}
                ,{'uid': 83, 'menu_id': 202}
                ,{'uid': 83, 'menu_id': 571}
                ,{'uid': 83, 'menu_id': 566}
                ,{'uid': 83, 'menu_id': 539}
                ,{'uid': 83, 'menu_id': 551}
                ,{'uid': 83, 'menu_id': 560}
                ,{'uid': 83, 'menu_id': 540}
                ,{'uid': 83, 'menu_id': 552}
                ,{'uid': 83, 'menu_id': 562}
                ,{'uid': 83, 'menu_id': 541}
                ,{'uid': 83, 'menu_id': 549}
                ,{'uid': 83, 'menu_id': 553}
                ,{'uid': 83, 'menu_id': 559}
                ,{'uid': 83, 'menu_id': 542}
                ,{'uid': 83, 'menu_id': 554}
                ,{'uid': 83, 'menu_id': 561}
                ,{'uid': 83, 'menu_id': 558}
                ,{'uid': 83, 'menu_id': 550}
                ,{'uid': 83, 'menu_id': 538}
                ,{'uid': 83, 'menu_id': 585}
                ,{'uid': 83, 'menu_id': 533}
                ,{'uid': 83, 'menu_id': 563}
                ,{'uid': 83, 'menu_id': 534}
                ,{'uid': 83, 'menu_id': 535}
                ,{'uid': 15, 'menu_id': 377}
                ,{'uid': 15, 'menu_id': 451}
                ,{'uid': 15, 'menu_id': 378}
                ,{'uid': 15, 'menu_id': 379}
                ,{'uid': 15, 'menu_id': 541}
                ,{'uid': 15, 'menu_id': 381}
                ,{'uid': 15, 'menu_id': 454}
                ,{'uid': 15, 'menu_id': 382}
                ,{'uid': 15, 'menu_id': 386}
                ,{'uid': 15, 'menu_id': 389}
                ,{'uid': 15, 'menu_id': 563}
                ,{'uid': 15, 'menu_id': 534}
                ,{'uid': 15, 'menu_id': 535}
                ,{'uid': 15, 'menu_id': 156}
                ,{'uid': 15, 'menu_id': 159}
                ,{'uid': 15, 'menu_id': 486}
                ,{'uid': 15, 'menu_id': 569}
                ,{'uid': 15, 'menu_id': 568}
                ,{'uid': 15, 'menu_id': 570}
                ,{'uid': 15, 'menu_id': 158}
                ,{'uid': 15, 'menu_id': 130}
                ,{'uid': 15, 'menu_id': 487}
                ,{'uid': 15, 'menu_id': 83}
                ,{'uid': 15, 'menu_id': 291}
                ,{'uid': 15, 'menu_id': 296}
                ,{'uid': 15, 'menu_id': 488}
                ,{'uid': 15, 'menu_id': 489}
                ,{'uid': 15, 'menu_id': 566}
                ,{'uid': 15, 'menu_id': 502}
                ,{'uid': 15, 'menu_id': 380}
                ,{'uid': 15, 'menu_id': 387}
                ,{'uid': 78, 'menu_id': 569}
                ,{'uid': 78, 'menu_id': 568}
                ,{'uid': 78, 'menu_id': 570}
                ,{'uid': 78, 'menu_id': 566}
                ,{'uid': 78, 'menu_id': 224}
                ,{'uid': 78, 'menu_id': 538}
                ,{'uid': 78, 'menu_id': 533}
                ,{'uid': 78, 'menu_id': 318}
                ,{'uid': 78, 'menu_id': 563}
                ,{'uid': 87, 'menu_id': 249}
                ,{'uid': 87, 'menu_id': 248}
                ,{'uid': 87, 'menu_id': 130}
                ,{'uid': 87, 'menu_id': 84}
                ,{'uid': 87, 'menu_id': 221}
                ,{'uid': 87, 'menu_id': 258}
                ,{'uid': 87, 'menu_id': 182}
                ,{'uid': 87, 'menu_id': 215}
                ,{'uid': 87, 'menu_id': 216}
                ,{'uid': 87, 'menu_id': 217}
                ,{'uid': 87, 'menu_id': 218}
                ,{'uid': 87, 'menu_id': 226}
                ,{'uid': 87, 'menu_id': 220}
                ,{'uid': 87, 'menu_id': 531}
                ,{'uid': 87, 'menu_id': 253}
                ,{'uid': 87, 'menu_id': 332}
                ,{'uid': 87, 'menu_id': 246}
                ,{'uid': 87, 'menu_id': 238}
                ,{'uid': 87, 'menu_id': 5}
                ,{'uid': 87, 'menu_id': 4}
                ,{'uid': 87, 'menu_id': 232}
                ,{'uid': 87, 'menu_id': 114}
                ,{'uid': 87, 'menu_id': 377}
                ,{'uid': 87, 'menu_id': 386}
                ,{'uid': 87, 'menu_id': 532}
                ,{'uid': 87, 'menu_id': 563}
                ,{'uid': 87, 'menu_id': 324}
                ,{'uid': 87, 'menu_id': 384}
                ,{'uid': 87, 'menu_id': 225}
                ,{'uid': 87, 'menu_id': 538}
                ,{'uid': 87, 'menu_id': 533}
                ,{'uid': 87, 'menu_id': 213}
                ,{'uid': 70, 'menu_id': 571}
                ,{'uid': 70, 'menu_id': 451}
                ,{'uid': 70, 'menu_id': 379}
                ,{'uid': 70, 'menu_id': 549}
                ,{'uid': 70, 'menu_id': 212}
                ,{'uid': 70, 'menu_id': 454}
                ,{'uid': 70, 'menu_id': 382}
                ,{'uid': 70, 'menu_id': 386}
                ,{'uid': 70, 'menu_id': 532}
                ,{'uid': 70, 'menu_id': 538}
                ,{'uid': 70, 'menu_id': 563}
                ,{'uid': 70, 'menu_id': 569}
                ,{'uid': 70, 'menu_id': 568}
                ,{'uid': 70, 'menu_id': 570}
                ,{'uid': 70, 'menu_id': 158}
                ,{'uid': 70, 'menu_id': 130}
                ,{'uid': 70, 'menu_id': 487}
                ,{'uid': 70, 'menu_id': 211}
                ,{'uid': 70, 'menu_id': 224}
                ,{'uid': 70, 'menu_id': 488}
                ,{'uid': 70, 'menu_id': 566}
                ,{'uid': 70, 'menu_id': 378}
                ,{'uid': 70, 'menu_id': 380}
                ,{'uid': 70, 'menu_id': 533}
                ,{'uid': 70, 'menu_id': 318}
                ,{'uid': 70, 'menu_id': 535}
                ,{'uid': 88, 'menu_id': 117}
                ,{'uid': 88, 'menu_id': 148}
                ,{'uid': 88, 'menu_id': 152}
                ,{'uid': 88, 'menu_id': 569}
                ,{'uid': 88, 'menu_id': 572}
                ,{'uid': 88, 'menu_id': 203}
                ,{'uid': 88, 'menu_id': 568}
                ,{'uid': 88, 'menu_id': 570}
                ,{'uid': 88, 'menu_id': 573}
                ,{'uid': 88, 'menu_id': 202}
                ,{'uid': 88, 'menu_id': 571}
                ,{'uid': 88, 'menu_id': 84}
                ,{'uid': 88, 'menu_id': 487}
                ,{'uid': 88, 'menu_id': 523}
                ,{'uid': 88, 'menu_id': 211}
                ,{'uid': 88, 'menu_id': 539}
                ,{'uid': 88, 'menu_id': 551}
                ,{'uid': 88, 'menu_id': 560}
                ,{'uid': 88, 'menu_id': 566}
                ,{'uid': 88, 'menu_id': 471}
                ,{'uid': 88, 'menu_id': 324}
                ,{'uid': 88, 'menu_id': 540}
                ,{'uid': 88, 'menu_id': 552}
                ,{'uid': 88, 'menu_id': 562}
                ,{'uid': 88, 'menu_id': 182}
                ,{'uid': 88, 'menu_id': 541}
                ,{'uid': 88, 'menu_id': 549}
                ,{'uid': 88, 'menu_id': 553}
                ,{'uid': 88, 'menu_id': 559}
                ,{'uid': 88, 'menu_id': 225}
                ,{'uid': 88, 'menu_id': 542}
                ,{'uid': 88, 'menu_id': 554}
                ,{'uid': 88, 'menu_id': 561}
                ,{'uid': 88, 'menu_id': 226}
                ,{'uid': 88, 'menu_id': 380}
                ,{'uid': 88, 'menu_id': 550}
                ,{'uid': 88, 'menu_id': 114}
                ,{'uid': 88, 'menu_id': 386}
                ,{'uid': 88, 'menu_id': 538}
                ,{'uid': 88, 'menu_id': 387}
                ,{'uid': 88, 'menu_id': 585}
                ,{'uid': 88, 'menu_id': 388}
                ,{'uid': 88, 'menu_id': 389}
                ,{'uid': 88, 'menu_id': 531}
                ,{'uid': 88, 'menu_id': 533}
                ,{'uid': 88, 'menu_id': 563}
                ,{'uid': 88, 'menu_id': 332}
                ,{'uid': 88, 'menu_id': 404}
                ,{'uid': 88, 'menu_id': 246}
                ,{'uid': 88, 'menu_id': 238}
                ,{'uid': 88, 'menu_id': 77}
                ,{'uid': 88, 'menu_id': 229}
                ,{'uid': 88, 'menu_id': 5}
                ,{'uid': 88, 'menu_id': 4}
                ,{'uid': 88, 'menu_id': 213}
                ,{'uid': 14, 'menu_id': 248}
                ,{'uid': 14, 'menu_id': 377}
                ,{'uid': 14, 'menu_id': 378}
                ,{'uid': 14, 'menu_id': 379}
                ,{'uid': 14, 'menu_id': 380}
                ,{'uid': 14, 'menu_id': 389}
                ,{'uid': 14, 'menu_id': 563}
                ,{'uid': 14, 'menu_id': 535}
                ,{'uid': 89, 'menu_id': 221}
                ,{'uid': 89, 'menu_id': 258}
                ,{'uid': 89, 'menu_id': 182}
                ,{'uid': 89, 'menu_id': 215}
                ,{'uid': 89, 'menu_id': 216}
                ,{'uid': 89, 'menu_id': 217}
                ,{'uid': 89, 'menu_id': 218}
                ,{'uid': 89, 'menu_id': 226}
                ,{'uid': 89, 'menu_id': 114}
                ,{'uid': 89, 'menu_id': 386}
                ,{'uid': 89, 'menu_id': 220}
                ,{'uid': 89, 'menu_id': 253}
                ,{'uid': 89, 'menu_id': 332}
                ,{'uid': 89, 'menu_id': 404}
                ,{'uid': 89, 'menu_id': 238}
                ,{'uid': 89, 'menu_id': 5}
                ,{'uid': 89, 'menu_id': 232}
                ,{'uid': 90, 'menu_id': 249}
                ,{'uid': 90, 'menu_id': 248}
                ,{'uid': 90, 'menu_id': 221}
                ,{'uid': 90, 'menu_id': 258}
                ,{'uid': 90, 'menu_id': 182}
                ,{'uid': 90, 'menu_id': 215}
                ,{'uid': 90, 'menu_id': 216}
                ,{'uid': 90, 'menu_id': 217}
                ,{'uid': 90, 'menu_id': 218}
                ,{'uid': 90, 'menu_id': 226}
                ,{'uid': 90, 'menu_id': 114}
                ,{'uid': 90, 'menu_id': 220}
                ,{'uid': 90, 'menu_id': 531}
                ,{'uid': 90, 'menu_id': 253}
                ,{'uid': 90, 'menu_id': 332}
                ,{'uid': 90, 'menu_id': 404}
                ,{'uid': 90, 'menu_id': 246}
                ,{'uid': 90, 'menu_id': 238}
                ,{'uid': 90, 'menu_id': 5}
                ,{'uid': 90, 'menu_id': 4}
                ,{'uid': 90, 'menu_id': 232}
                ,{'uid': 90, 'menu_id': 377}
                ,{'uid': 90, 'menu_id': 212}
                ,{'uid': 90, 'menu_id': 386}
                ,{'uid': 90, 'menu_id': 532}
                ,{'uid': 90, 'menu_id': 487}
                ,{'uid': 90, 'menu_id': 566}
                ,{'uid': 90, 'menu_id': 211}
                ,{'uid': 90, 'menu_id': 378}
                ,{'uid': 90, 'menu_id': 379}
                ,{'uid': 90, 'menu_id': 541}
                ,{'uid': 90, 'menu_id': 380}
                ,{'uid': 90, 'menu_id': 389}
                ,{'uid': 90, 'menu_id': 533}
                ,{'uid': 90, 'menu_id': 318}
                ,{'uid': 90, 'menu_id': 563}
                ,{'uid': 90, 'menu_id': 534}
                ,{'uid': 90, 'menu_id': 535}
                ,{'uid': 90, 'menu_id': 213}
                ,{'uid': 90, 'menu_id': 224}
                ,{'uid': 90, 'menu_id': 538}
                ,{'uid': 90, 'menu_id': 210}
                ,{'uid': 90, 'menu_id': 319}
                ,{'uid': 90, 'menu_id': 320}
                ,{'uid': 90, 'menu_id': 223}
                ,{'uid': 95, 'menu_id': 249}
                ,{'uid': 95, 'menu_id': 248}
                ,{'uid': 95, 'menu_id': 210}
                ,{'uid': 95, 'menu_id': 487}
                ,{'uid': 95, 'menu_id': 211}
                ,{'uid': 95, 'menu_id': 221}
                ,{'uid': 95, 'menu_id': 224}
                ,{'uid': 95, 'menu_id': 258}
                ,{'uid': 95, 'menu_id': 377}
                ,{'uid': 95, 'menu_id': 566}
                ,{'uid': 95, 'menu_id': 378}
                ,{'uid': 95, 'menu_id': 182}
                ,{'uid': 95, 'menu_id': 215}
                ,{'uid': 95, 'menu_id': 216}
                ,{'uid': 95, 'menu_id': 217}
                ,{'uid': 95, 'menu_id': 319}
                ,{'uid': 95, 'menu_id': 379}
                ,{'uid': 95, 'menu_id': 541}
                ,{'uid': 95, 'menu_id': 212}
                ,{'uid': 95, 'menu_id': 218}
                ,{'uid': 95, 'menu_id': 320}
                ,{'uid': 95, 'menu_id': 226}
                ,{'uid': 95, 'menu_id': 380}
                ,{'uid': 95, 'menu_id': 114}
                ,{'uid': 95, 'menu_id': 386}
                ,{'uid': 95, 'menu_id': 532}
                ,{'uid': 95, 'menu_id': 538}
                ,{'uid': 95, 'menu_id': 220}
                ,{'uid': 95, 'menu_id': 389}
                ,{'uid': 95, 'menu_id': 531}
                ,{'uid': 95, 'menu_id': 533}
                ,{'uid': 95, 'menu_id': 223}
                ,{'uid': 95, 'menu_id': 253}
                ,{'uid': 95, 'menu_id': 318}
                ,{'uid': 95, 'menu_id': 534}
                ,{'uid': 95, 'menu_id': 563}
                ,{'uid': 95, 'menu_id': 535}
                ,{'uid': 95, 'menu_id': 332}
                ,{'uid': 95, 'menu_id': 404}
                ,{'uid': 95, 'menu_id': 246}
                ,{'uid': 95, 'menu_id': 238}
                ,{'uid': 95, 'menu_id': 5}
                ,{'uid': 95, 'menu_id': 4}
                ,{'uid': 95, 'menu_id': 232},{'uid': 95, 'menu_id': 213}]
            for item in data:
                request.env.cr.execute(f'select uid, menu_id from ir_ui_hide_menu_rel where uid = {str(item["uid"])} and menu_id = {str(item["menu_id"])}')
                row = request.env.cr.dictfetchall()
                if not row:
                    if request.env['res.users'].search([('id', '=', item['uid'])]) and request.env['ir.ui.menu'].search([('id', '=', item['menu_id'])]):
                        request.env.cr.execute(f'insert into ir_ui_hide_menu_rel (uid, menu_id) values ({str(item["uid"])}, {str(item["menu_id"])})')
            return 'Success'
        else:
            return 'Access Denied'


    @http.route(['/correct_employee_role_with_xl'], type='http', auth="public")
    def correct_employee_role_with_xl(self):
        if request.env.user.has_group('base.group_system'):
            data = {
                'JUS0092': "Business Head",
                'JUS0101': "Closing TL",
                'JUS0103': "Cluster Head",
                'JUS0105': "Closing",
                'JUS0116': "Cluster Head",
                'P0022': "Closing",
                'JUS0130': "Closing",
                'M0160': "CRM",
                'JUS0134': "Closing",
                'JUS0163': "Closing",
                'JUS0175': "Closing",
                'JUS0178': "Closing TL",
                'JUS0186': "Cluster Head",
                'JUS0213': "CRM",
                'JUS0214': "Closing",
                'JUS0217': "Sourcing TL",
                'JUS0224': "Closing TL",
                'M0214': "Closing TL",
                'P0063': "Closing",
                'JUS0238': "CRM",
                'JUS0248': "Closing TL",
                'JUS0249': "CRM",
                'JUS0260': "Closing TL",
                'JUS0257': "Closing",
                'JUS0259': "Closing",
                'JUS0255': "Closing",
                'JUS0275': "Cluster Head",
                'JUS0279': "Closing TL",
                'JUS0302': "CRM",
                'JUS0311': "CRM",
                'P0127': "Closing",
                'JUS0364': "Closing",
                'JUS0369': "CRM",
                'JUS0398': "Closing TL",
                'JUS0406': "Closing",
                'JUS0405': "Sourcing",
                'JUS0409': "Closing",
                'M0296': "Closing",
                'JUS0435': "Closing",
                'JUS0441': "Closing",
                'JUS0446': "CRM",
                'JUS0461': "Closing",
                'JUS0468': "Sourcing TL",
                'JUS0475': "Closing TL",
                'JUS0476': "CRM",
                'JUS0478': "Closing",
                'JUS0485': "Sourcing TL",
                'JUS00498': "Closing",
                'JUS0502': "CRM",
                'JUS0505': "Closing TL",
                'JUS0531': "Closing",
                'P0225': "Sourcing",
                'JUS0548': "Closing",
                'JUS0572': "Sourcing",
                'JUS0599': "Sourcing",
                'JUS0625': "Cluster Head",
                'JUS0627': "Closing TL",
                'P0246': "Closing TL",
                'JUS0638': "Closing",
                'JUS0658': "Closing TL",
                'JUS0661': "Cluster Head",
                'P0257': "Closing",
                'JUS0713': "Closing",
                'JUS0721': "Sourcing",
                'JUS0738': "Closing TL",
                'M0485': "Closing",
                'JUS0759': "Closing",
                'JUS0762': "Sourcing",
                'JUS0760': "Closing",
                'JUS0782': "Sourcing",
                'JUS0792': "Sourcing",
                'JUS0805': "Closing",
                'JUS0804': "Sourcing TL",
                'JUS0807': "Sourcing",
                'JUS0813': "Sourcing",
                'JUS0818': "Closing",
                'P0288': "Closing",
                'JUS0830': "Sourcing TL",
                'JUS0835': "Closing TL",
                'JUS0833': "Closing",
                'JUS0866': "Business Head",
                'JUS0870': "Closing",
                'JUS0891': "Sourcing",
                'JUS0900': "Sourcing",
                'JUS0901': "Closing",
                'JUS0907': "Sourcing",
                'M0562': "Sourcing",
                'JUS0912': "Sourcing",
                'JUS0910': "Sourcing",
                'JUS0914': "Sourcing",
                'JUS0923': "Closing",
                'M0566': "Closing",
                'JUS0935': "Sourcing",
                'JUS0940': "Sourcing",
                'JUS0942': "Sourcing",
                'JUS0951': "CRM",
                'JUS0952': "CRM",
                'P0340': "Sourcing",
                'JUS0971': "Closing",
                'JUS0973': "Closing",
                'JUS0974': "Sourcing",
                'JUS0980': "Sourcing",
                'JUS0984': "Cluster Head",
                'B0015': "Closing",
                'P0351': "Sourcing TL",
                'JUS1000': "Closing TL",
                'JUS1005': "Closing",
                'JUS1004': "Closing",
                'JUS1006': "Closing",
                'JUS1011': "Closing",
                'JUS1021': "Sourcing",
                'M0593': "Sourcing",
                'M0594': "Sourcing",
                'JUS1029': "Sourcing",
                'JUS1032': "Sourcing",
                'JUS1014': "Sourcing",
                'JUS1036': "Sourcing",
                'P0371': "Closing",
                'P0372': "Closing",
                'JUS1336': "Closing",
                'JUS1019': "Closing",
                'JUS1028': "Closing",
                'JUS1022': "Closing",
                'JUS1034': "Closing",
                'JUS1030': "Closing",
                'JUS1039': "Sourcing",
                'JUS1041': "Sourcing",
                'JUS1051': "Closing TL",
                'JUS1053': "Closing TL",
                'JUS1050': "Closing",
                'JUS1061': "Closing TL",
                'JUS1057': "Closing",
                'JUS1060': "Sourcing",
                'JUS1062': "Closing TL",
                'JUS1067': "CRM",
                'JUS1069': "Closing",
                'JUS1080': "Closing",
                'JUS1072': "Sourcing",
                'P0393': "Sourcing",
                'P0395': "Sourcing",
                'JUS1081': "Closing TL",
                'JUS1073': "Sourcing",
                'JUS1083': "Closing",
                'JUS1085': "Closing TL",
                'M0634': "Sourcing",
                'JUS1090': "Closing",
                'M0629': "Sourcing",
                'M0640': "Closing",
                'JUS1100': "Closing",
                'JUS1103': "Closing",
                'P0406': "Sourcing",
                'JUS1108': "Sourcing",
                'JUS1110': "Sourcing",
                'JUS1114': "Closing",
                'JUS1116': "Sourcing",
                'JUS1117': "Sourcing",
                'JUS1119': "Closing",
                'JUS1124': "Sourcing",
                'JUS1125': "Closing",
                'JUS1128': "Closing TL",
                'JUS1126': "Sourcing",
                'JUS1127': "Closing",
                'P0417': "Closing",
                'JUS1135': "Sourcing",
                'JUS1136': "Closing",
                'JUS1138': "Sourcing",
                'B0020': "Closing",
                'JUS1140': "Sourcing",
                'JUS1147': "Closing",
                'JUS1150': "Sourcing",
                'JUS1145': "Sourcing",
                'JUS1144': "Sourcing",
                'JUS1148': "Closing",
                'JUS1151': "Sourcing",
                'JUS1152': "Closing TL",
                'JUS1156': "Sourcing",
                'M0669': "Closing",
                'M0671': "CRM",
                'P0433': "Sourcing",
                'JUS1165': "Sourcing",
                'JUS1163': "Closing",
                'JUS1168': "CRM",
                'JUS1178': "Closing",
                'JUS1173': "Closing",
                'JUS1175': "CRM",
                'JUS1171': "Closing",
                'JUS1170': "Closing",
                'JUS1179': "Closing",
                'JUS1180': "Closing",
                'JUS1186': "Closing",
                'JUS1191': "Closing TL",
                'P0455': "Sourcing",
                'JUS1194': "Closing TL",
                'JUS1195': "Cluster Head",
                'P0457': "Sourcing",
                'JUS1200': "Sourcing",
                'JUS1199': "Sourcing",
                'JUS1196': "Cluster Head",
                'JUS1201': "Closing",
                'JUS1203': "Closing",
                'JUS1205': "Closing",
                'JUS1202': "Closing",
                'JUS1204': "Closing",
                'JUS1212': "Closing",
                'P0469': "Sourcing",
                'M0684': "CRM",
                'P0470': "Closing",
                'JUS1220': "Sourcing TL",
                'JUS1221': "Sourcing",
                'M0688': "Sourcing",
                'JUS1226': "Sourcing",
                'JUS1225': "Sourcing",
                'JUS1227': "Sourcing",
                'JUS1229': "Sourcing",
                'JUS1231': "Closing",
                'JUS1237': "Sourcing",
                'P0477': "Sourcing",
                'P0479': "Sourcing",
                'JUS1244': "Sourcing",
                'P0482': "Closing",
                'JUS1248': "Sourcing",
                'JUS1254': "Sourcing",
                'P0484': "Closing",
                'JUS1253': "Closing",
                'JUS1265': "Sourcing",
                'M0711': "CRM",
                'JUS1269': "Closing",
                'JUS1270': "Closing",
                'JUS1271': "Closing",
                'JUS1275': "Closing TL",
                'JUS1279': "Cluster Head",
                'JUS1280': "Sourcing TL",
                'JUS1281': "Closing TL",
                'M0722': "Cluster Head",
                'JUS1288': "Closing",
                'M0724': "CRM",
                'JUS1287': "Sourcing",
                'JUS1286': "Sourcing",
                'M0728': "Sourcing",
                'JUS1296': "Sourcing",
                'JUS1295': "Closing",
                'JUS1292': "Sourcing",
                'JUS1300': "Closing",
                'JUS1301': "Sourcing",
                'JUS1302': "Closing",
                'P0501': "Sourcing TL",
                'JUS1304': "CRM",
                'JUS1305': "Closing",
                'JUS1308': "Sourcing",
                'M0740': "Closing",
                'P0504': "Sourcing",
                'P0505': "Sourcing",
                'M0741': "Sourcing",
                'M0743': "Sourcing",
                'JUS1314': "Sourcing",
                'JUS1317': "Sourcing",
                'JUS1316': "Sourcing TL",
                'JUS1319': "Sourcing",
                'P0506': "Closing TL",
                'P0507': "Sourcing",
                'JUS1322': "Closing TL",
                'M0750': "Closing TL",
                'JUS1324': "Closing",
                'JUS1325': "Closing",
                'JUS1330': "Closing TL",
                'JUS1329': "Sourcing",
                'JUS1326': "Closing",
                'JUS1328': "Closing",
                'M0753': "Sourcing",
                'M0755': "Sourcing",
                'M0757': "Sourcing TL",
                'P0512': "Closing TL",
                'JUS1338': "Closing",
                'JUS1343': "Closing",
                'JUS1342': "Sourcing",
                'JUS1340': "Sourcing",
                'JUS1341': "Closing",
                'P0515': "Closing",
                'JUS1345': "Sourcing",
                'JUS1346': "Sourcing",
                'JUS1339': "Sourcing",
                'JUS1347': "Sourcing",
                'JUS1349': "Closing",
                'JUS1352': "Sourcing",
                'JUS1354': "Closing",
                'JUS1353': "Closing",
                'JUS1355': "Sourcing",
                'JUS1357': "Closing",
                'JUS1358': "Closing TL",
                'JUS1359': "Sourcing",
                'JUS1361': "Closing",
                'JUS1362': "Sourcing TL",
                'JUS1363': "Sourcing TL",
                'P0529': "Closing",
                'JUS1365': "Closing",
                'JUS1366': "Closing",
                'JUS1367': "Closing",
                'JUS1356': "Closing",
                'P0535': "Closing",
                'JUS1371': "Closing",
                'JUS1372': "Closing",
                'JUS1373': "Closing",
                'P0539': "Closing",
                'JUS1374': "Sourcing",
                'JC006': "Business Head",
                'JUS1378': "Sourcing",
                'M0772': "Sourcing",
                'JUS1380': "CRM",
                'M0770': "Sourcing",
                'JUS1382': "Closing",
                'JUS1384': "Closing",
                'JUS1387': "Closing",
                'P0546': "Closing",
                'M0776': "Sourcing",
                'JUS1391': "Sourcing TL",
                'JUS1390': "Sourcing",
                'JUS1392': "Sourcing",
                'JUS1389': "Sourcing",
                'JUS1393': "Closing",
                'JUS1395': "Sourcing",
                'JUS1394': "Closing",
                'JUS1396': "Closing",
                'JUS1399': "Closing",
                'JUS1398': "Sourcing",
                'JUS1397': "Closing",
                'JUS1400': "Closing",
                'JUS1401': "Closing",
                'JUS1404': "Closing",
                'JUS1402': "Closing",
                'JUS1403': "Sourcing",
                'JUS1406': "Sourcing",
                'JUS1405': "Closing",
                'JUS1407': "Closing",
                'JUS1408': "CRM",
                'JUS1409': "Closing",
                'JUS1411': "Closing",
                'JUS1412': "Sourcing TL",
                'JUS1413': "Closing TL",
                'JUS1414': "Closing",
                'JUS1418': "Sourcing",
                'M0783': "Sourcing",
                'JUS1417': "Closing",
                'JUS1421': "Closing",
                'JUS1415': "Closing",
                'JUS1420': "Sourcing",
                'JUS1422': "Closing",
                'JUS1424': "Sourcing",
                'JUS1425': "Sourcing",
                'JUS1426': "Sourcing",
                'JUS1428': "Closing",
                'JUS1429': "Closing TL",
                'JUS1430': "Closing",
                'JUS1431': "Sourcing",
                'JUS1432': "Sourcing",
                'JUS1433': "Closing",
                'JUS1434': "Sourcing",
                'JUS1435': "Sourcing",
                'JUS1436': "Sourcing",
                'JUS1437': "Sourcing",
                'JUS1438': "Closing",
                'JUS1441': "Sourcing",
                'JUS1442': "Sourcing",
                'JUS1440': "Sourcing",
                'JUS1443': "Sourcing",
                'JUS1446': "Closing",
                'JUS1445': "Sourcing TL",
                'JUS1449': "Closing",
                'JUS1451': "Closing",
                'JUS1453': "Closing",
                'JUS1452': "Closing",
                'M0815': "Closing",
                'JUS1454': "Closing",
                'JUS1456': "Closing",
                'JUS1455': "Sourcing",
                'JUS1458': "Closing",
                'JUS1460': "Closing",
                'JUS1459': "Closing",
                'JUS1463': "Sourcing TL",
                'JUS1461': "Sourcing",
                'JUS1462': "Sourcing",
                'JUS1465': "Sourcing",
                'JUS1470': "Closing",
                'JUS1467': "Sourcing",
                'JUS1468': "Sourcing",
                'JUS1469': "Sourcing",
                'M0827': "Closing",
                'JUS1473': "Sourcing",
                'JUS1474': "Sourcing",
                'JUS1477': "Closing",
                'JUS1478': "Sourcing",
                'JUS1480': "Sourcing",
                'JUS1479': "Closing",
                'JUS1481': "Sourcing",
                'JUS1482': "CRM",
                'JUS1486': "Sourcing",
                'JUS1484': "CRM",
                'JUS1485': "Closing",
                'JUS1490': "Sourcing",
                'JUS1493': "Sourcing",
                'JUS1491': "Sourcing",
                'M0842': "Sourcing",
                'JUS1494': "CRM",
                'JUS1495': "Sourcing",
                'JUS1497': "Closing",
                'JUS1499': "Sourcing",
                'JUS1500': "CRM",
                'JUS1498': "Closing",
                'JUS1501': "Closing",
                'JUS1502': "Sourcing",
                'M0843': "Sourcing",
                'JUS1504': "Sourcing",
                'JUS1505': "Sourcing",
                'JUS1506': "Sourcing",
                'JUS1508': "CRM",
                'JUS1507': "Closing",
                'JUS1510': "Sourcing",
                'JUS1512': "Sourcing",
                'JUS1514': "Closing",
                'JUS1515': "Closing",
                'JUS1516': "Closing",
                'JUS2000': "Sourcing",
                'JUS591': "Sourcing",
                'JUS592': "Closing TL",
                'JUS594': "Closing TL",
                'JUS595': "Sourcing TL",
                'JUS598': "Cluster Head",
                'JUS599': "Sourcing TL",
                'JUS601': "Sourcing TL",
                'JUS603': "Sourcing TL",
                'JUS605': "Sourcing",
                'JUS607': "Sourcing",
                'JUS606': "Sourcing",
                'JUS608': "Closing TL",
                'JUS609': "Sourcing",
                'JUS613': "Sourcing TL",
                'JUS614': "Sourcing TL",
                'JUS612': "Closing",
                'JUS615': "Closing",
                'JUS611': "Sourcing",
                'JUS618': "Sourcing",
                'JUS619': "Closing",
                'JUS620': "Sourcing",
                'JUS622': "Closing",
                'JUS623': "Sourcing",
                'JUS621': "Sourcing",
                'JUS624': "Sourcing",
                'JUS625': "Sourcing",
                'JUS627': "Sourcing",
                'JUS628': "Sourcing",
                'JUS629': "Sourcing",
                'JUS630': "Sourcing",
                'JUS631': "Sourcing",
                'JUS632': "Closing",
                'JUS633': "Sourcing",
                'JUS638': "Closing",
                'JUS635': "Closing",
                'JUS640': "Sourcing",
                'JUS636': "Closing",
                'JUS634': "Closing",
                'JUS643': "Sourcing",
                'JUS641': "Sourcing",
                'JUS642': "Sourcing",
                'JUS637': "Business Head",
                'JUS644': "Sourcing",
                'JUS645': "Closing TL",
                'JUS646': "Closing",
                'JUS647': "Sourcing",
                'JUS649': "Closing",
                'JUS650': "Sourcing",
                'JUS652': "Sourcing",
                'JUS657': "Sourcing",
                'JUS658': "Sourcing",
                'JUS659': "Sourcing",
                'JUS660': "Sourcing",
                'JUS663': "Sourcing",
                'JUS654': "Closing",
                'JUS655': "Closing",
                'JUS656': "Cluster Head",
                'JUS664': "Closing TL",
                'JUS666': "CRM",
                'JUS667': "Sourcing TL",
                'JUS668': "Sourcing TL",
                'JUS669': "Sourcing",
                'JUS670': "Closing TL",
                'JUS671': "Closing",
                'JUS672': "Sourcing",
                'JUS673': "Closing",
                'JUS674': "Closing",
                'JUS675': "Sourcing",
                'JUS676': "Closing",
                'JUS678': "Closing TL",
                'JUS679': "Closing",
                'JUS680': "Sourcing",
                'JUS683': "CRM",
                'JUS684': "Sourcing",
                'JUS685': "Closing",
                'JUS686': "Closing",
                'JUS687': "Closing",
                'JUS689': "Closing",
                'JUS682': "CRM",
                'JUS690': "Sourcing",
                'JUS691': "Sourcing",
                'B0021': "Closing",
                'M0092': "Closing TL",
                'M0202': "CRM",
                'M0206': "CRM",
                'M0220': "CRM",
                'M0236': "CRM",
                'M0247': "Closing",
                'M0259': "CRM",
                'M0261': "CRM",
                'M0263': "CRM",
                'M0358': "Closing",
                'M0435': "CRM",
                'M0440': "CRM",
                'M0498': "Closing",
                'M0501': "Sourcing TL",
                'M0503': "Closing",
                'M0509': "CRM",
                'M0510': "Sourcing",
                'M0530': "Sourcing",
                'M0551': "Sourcing",
                'M0554': "CRM",
                'M0558': "CRM",
                'M0565': "Closing TL",
                'M0587': "CRM",
                'M0589': "CRM",
                'M0596': "CRM",
                'M0598': "Closing",
                'M0610': "Closing",
                'M0612': "Sourcing TL",
                'M0632': "Sourcing",
                'M0633': "Sourcing",
                'M0661': "Sourcing",
                'M0663': "Sourcing",
                'M0672': "Closing",
                'M0677': "Closing",
                'M0678': "CRM",
                'M0683': "CRM",
                'M0698': "CRM",
                'M0702': "Closing",
                'M0703': "Sourcing",
                'M0704': "Sourcing",
                'M0712': "Sourcing",
                'M0717': "Closing",
                'M0730': "Closing",
                'M0739': "Sourcing",
                'M0742': "Closing",
                'M0764': "Sourcing",
                'P0025': "CRM",
                'P0030': "CRM",
                'P0069': "CRM",
                'P0084': "CRM",
                'P0095': "Closing",
                'P0098': "Closing",
                'P0160': "Closing",
                'P0164': "Closing",
                'P0173': "CRM",
                'P0184': "Closing",
                'P0210': "CRM",
                'P0223': "Sourcing",
                'P0233': "Closing",
                'P0250': "Closing",
                'P0255': "CRM",
                'P0274': "Closing",
                'P0305': "Sourcing",
                'P0327': "Closing",
                'P0339': "Closing TL",
                'P0366': "Sourcing",
                'P0370': "Sourcing",
                'P0383': "Sourcing",
                'P0384': "Closing",
                'P0385': "Sourcing",
                'P0386': "CRM",
                'P0388': "Closing",
                'P0412': "Closing",
                'P0427': "Closing",
                'P0428': "Sourcing",
                'P0436': "Closing",
                'P0440': "CRM",
                'P0481': "Sourcing",
                'P0494': "Sourcing",

            }
            for item in data:
                employee = request.env['hr.employee'].search([('barcode', '=', item)], limit=1)
                if employee:
                    if data[item] == 'Business Head':
                        employee.role = 'business_head'
                    elif data[item] == 'Closing TL':
                        employee.role = 'closing_tl'
                    elif data[item] == 'Cluster Head':
                        employee.role = 'cluster_head'
                    elif data[item] == 'Closing':
                        employee.role = 'closing_manager'
                    elif data[item] == 'CRM':
                        employee.role = 'crm'
                    elif data[item] == 'Sourcing':
                        employee.role = 'sourcing_manager'
                    elif data[item] == 'Sourcing TL':
                        employee.role = 'sourcing_tl'

            return 'Success'
        else:
            return 'Access Denied'


    @http.route(['/correct_employee_role_xl_10'], type='http', auth="public")
    def correct_employee_role_xl_10(self):
        if request.env.user.has_group('base.group_system'):
            data = [{'employee': 'rizwan.shaikh@justo.co.in', 'role': 'Closing TL', 'parent': 'ajaykumar.singh@justo.co.in'},
                    {'employee': 'tejashree.mhetre@justo.co.in', 'role': 'Closing', 'parent': 'pratik.kolhapure@justo.co.in'},
                    {'employee': 'karan.sarwade@justo.co.in', 'role': 'Cluster Head', 'parent': 'nitin.pardeshi@justo.co.in'},
                    {'employee': 'amol.zulzule@justo.co.in', 'role': 'Closing', 'parent': 'prajay.khale@justo.co.in'},
                    {'employee': 'ajinkya.jadhav@justo.co.in', 'role': 'Closing', 'parent': 'vivek.yerande@justo.co.in'},
                    {'employee': 'mayur.shinde@justo.co.in', 'role': 'Closing', 'parent': 'pratik.kolhapure@justo.co.in'},
                    {'employee': 'shrinivas.ugile@justo.co.in', 'role': 'Closing TL', 'parent': 'sandesh.chavan@justo.co.in'},
                    {'employee': 'sandeep.kulkarni@justo.co.in', 'role': 'Cluster Head', 'parent': 'praveen.apte@justo.co.in'},
                    {'employee': 'shivali.shinde@justo.co.in', 'role': 'CRM', 'parent': 'sunny.john@justo.co.in'},
                    {'employee': 'akash.ozarkar@justo.co.in', 'role': 'Closing', 'parent': 'mrugesh.trivedi@justo.co.in'},
                    {'employee': 'kiran.shinde@justo.co.in', 'role': 'Sourcing TL', 'parent': 'karan.sarwade@justo.co.in'},
                    {'employee': 'ashwini.kumar@justo.co.in', 'role': 'Closing TL', 'parent': 'sandesh.chavan@justo.co.in'},
                    {'employee': 'sunny.john@justo.co.in', 'role': 'CRM', 'parent': 'nitin.pardeshi@justo.co.in'},
                    {'employee': 'pratik.kolhapure@justo.co.in', 'role': 'Closing TL', 'parent': 'ajaykumar.singh@justo.co.in'},
                    {'employee': 'sourabh.ubale@justo.co.in', 'role': 'CRM', 'parent': 'sunny.john@justo.co.in'},
                    {'employee': 'anil.sasane@justo.co.in', 'role': 'Closing', 'parent': 'vyaprosh.kale@justo.co.in'},
                    {'employee': 'shriraj.patil@justo.co.in', 'role': 'Closing TL', 'parent': 'vishal.thigale@justo.co.in'},
                    {'employee': 'akash.kotwal@justo.co.in', 'role': 'Closing', 'parent': 'prajay.khale@justo.co.in'},
                    {'employee': 'sandesh.chavan@justo.co.in', 'role': 'Cluster Head', 'parent': 'nitin.pardeshi@justo.co.in'},
                    {'employee': 'amarnath.dhone@justo.co.in', 'role': 'Closing TL', 'parent': 'karan.sarwade@justo.co.in'},
                    {'employee': 'pinank.salunke@justo.co.in', 'role': 'CRM', 'parent': 'sunny.john@justo.co.in'},
                    {'employee': 'swapnil.Bhalekar@justo.co.in', 'role': 'CRM', 'parent': 'sunny.john@justo.co.in'},
                    {'employee': 'jyoti.bhartiya@justo.co.in', 'role': 'Closing', 'parent': 'ashwini.kumar@justo.co.in'},
                    {'employee': 'aniket.pathade@justo.co.in', 'role': 'Sourcing', 'parent': 'madhav.murhekar@justo.co.in'},
                    {'employee': 'sonam.thakur@justo.co.in', 'role': 'Closing', 'parent': 'ashwini.kumar@justo.co.in'},
                    {'employee': 'tushar.kore@justo.co.in', 'role': 'Closing', 'parent': 'amarnath.dhone@justo.co.in'},
                    {'employee': 'sagar.hundekari@justo.co.in', 'role': 'CRM', 'parent': 'sunny.john@justo.co.in'},
                    {'employee': 'sakar.diwase@justo.co.in', 'role': 'Sourcing TL', 'parent': 'sandeep.kulkarni@justo.co.in'},
                    {'employee': 'prashant.bhide@justo.co.in', 'role': 'Closing', 'parent': 'babita.rabbewar@justo.co.in'},
                    {'employee': 'deepak.pandey@justo.co.in', 'role': 'CRM', 'parent': 'sunny.john@justo.co.in'},
                    {'employee': 'prajay.khale@justo.co.in', 'role': 'Closing TL', 'parent': 'sandeep.kulkarni@justo.co.in'},
                    {'employee': 'dhondiba.aptekar@justo.co.in', 'role': 'Closing', 'parent': 'mrugesh.trivedi@justo.co.in'},
                    {'employee': 'tanveer.pathan@justo.co.in', 'role': 'Closing', 'parent': 'prajay.khale@justo.co.in'},
                    {'employee': 'ovez.shaikh@justo.co.in', 'role': 'Sourcing ', 'parent': 'sakar.diwase@justo.co.in'},
                    {'employee': 'sandeep.kamat@justo.co.in', 'role': 'Cluster Head', 'parent': 'nitin.pardeshi@justo.co.in'},
                    {'employee': 'devendra.shinde@justo.co.in', 'role': 'Closing TL', 'parent': 'sandeep.kamat@justo.co.in'},
                    {'employee': 'vishal.thigale@justo.co.in', 'role': 'Cluster Head', 'parent': 'nitin.pardeshi@justo.co.in'},
                    {'employee': 'vyaprosh.kale@justo.co.in', 'role': 'Closing TL', 'parent': 'ajaykumar.singh@justo.co.in'},
                    {'employee': 'tushar.bhosale@justo.co.in', 'role': 'Closing', 'parent': 'shriraj.patil@justo.co.in'},
                    {'employee': 'parag.chavaan@justo.co.in', 'role': 'Sourcing', 'parent': 'sakar.diwase@justo.co.in'},
                    {'employee': 'ashutosh.agarwal@justo.co.in', 'role': 'Closing', 'parent': 'prajay.khale@justo.co.in'},
                    {'employee': 'mayur.gite@justo.co.in', 'role': 'Sourcing TL', 'parent': 'sayan.chakraborty@justo.co.in'},
                    {'employee': 'madhav.murhekar@justo.co.in', 'role': 'Sourcing TL', 'parent': 'sayan.chakraborty@justo.co.in'},
                    {'employee': 'arafatkhan.pathan@justo.co.in', 'role': 'Sourcing TL', 'parent': 'sandesh.chavan@justo.co.in'},
                    {'employee': 'rahul.tirmare@justo.co.in', 'role': 'Closing TL', 'parent': 'sandeep.kamat@justo.co.in'},
                    {'employee': 'nisha.bharti@justo.co.in', 'role': 'Closing', 'parent': 'sagar.waichole@justo.co.in'},
                    {'employee': 'subhransu.sahoo@justo.co.in', 'role': 'Business Head', 'parent': 'pushp@justo.co.in'},
                    {'employee': 'jayesh.raundal@justo.co.in', 'role': 'Closing', 'parent': 'pushp@justo.co.in'},
                    {'employee': 'ketan.nagare@justo.co.in', 'role': 'Sourcing ', 'parent': 'sakar.diwase@justo.co.in'},
                    {'employee': 'shayad.sayyad@justo.co.in', 'role': 'Sourcing ', 'parent': 'shubhamsuresh.patil@justo.co.in'},
                    {'employee': 'manali.mahamuni@justo.co.in', 'role': 'Closing', 'parent': 'shrinivas.ugile@justo.co.in'},
                    {'employee': 'sunil.nikam@justo.co.in', 'role': 'Sourcing ', 'parent': 'jitendra.singh@justo.co.in'},
                    {'employee': 'shantanu.jain@justo.co.in', 'role': 'Sourcing ', 'parent': 'kiran.shinde@justo.co.in'},
                    {'employee': 'varsha.punde@justo.co.in', 'role': 'CRM', 'parent': 'sunny.john@justo.co.in'},
                    {'employee': 'shubham.jadhav@justo.co.in', 'role': 'Sourcing', 'parent': 'arafatkhan.pathan@justo.co.in'},
                    {'employee': 'pratik.jejurikar@justo.co.in', 'role': 'Closing', 'parent': 'mrugesh.trivedi@justo.co.in'},
                    {'employee': 'rohit.more@justo.co.in', 'role': 'Sourcing ', 'parent': 'kiran.shinde@justo.co.in'},
                    {'employee': 'Piyush.Bagarecha@justo.co.in', 'role': 'Closing TL', 'parent': 'sayan.chakraborty@justo.co.in'},
                    {'employee': 'Pawan.Sharma@justo.co.in', 'role': 'Closing', 'parent': 'shrinivas.ugile@justo.co.in'},
                    {'employee': 'Laxman.Nitnaware@justo.co.in', 'role': 'Closing', 'parent': 'vyaprosh.kale@justo.co.in'},
                    {'employee': 'Prashant.Tiwari@justo.co.in', 'role': 'Sourcing ', 'parent': 'sagar.waichole@justo.co.in'},
                    {'employee': 'santosh.kadam@justo.co.in', 'role': 'Closing', 'parent': 'prasad.palande@justo.co.in'},
                    {'employee': 'monika.walunj@justo.co.in', 'role': 'Closing', 'parent': 'prasad.palande@justo.co.in'},
                    {'employee': 'tushargiridhar.bhosale@justo.co.in', 'role': 'Closing', 'parent': 'babita.rabbewar@justo.co.in'},
                    {'employee': 'sagarika.das@justo.co.in', 'role': 'Closing', 'parent': 'prajay.khale@justo.co.in'},
                    {'employee': 'subhendu.das@justo.co.in', 'role': 'Sourcing ', 'parent': 'kiran.shinde@justo.co.in'},
                    {'employee': 'vishal.kawane@justo.co.in', 'role': 'Sourcing ', 'parent': 'pankaj.singh@justo.co.in'},
                    {'employee': 'ravina.kumari@justo.co.in', 'role': 'Closing TL', 'parent': 'sandesh.chavan@justo.co.in'},
                    {'employee': 'mayuresh.asabe@justo.co.in', 'role': 'Sourcing ', 'parent': 'kiran.shinde@justo.co.in'},
                    {'employee': 'divya.waghela@justo.co.in', 'role': 'Closing', 'parent': 'prasad.palande@justo.co.in'},
                    {'employee': 'sainath.pise@justo.co.in', 'role': 'Closing', 'parent': 'shrinivas.ugile@justo.co.in'},
                    {'employee': 'rajesh.surve@justo.co.in', 'role': 'Closing', 'parent': 'avinash.tribhuvan@justo.co.in'},
                    {'employee': 'suraj.bavkar@justo.co.in', 'role': 'Sourcing ', 'parent': 'indranil.sarkar@justo.co.in'},
                    {'employee': 'yakub.pathan@justo.co.in', 'role': 'Closing', 'parent': 'amarnath.dhone@justo.co.in'},
                    {'employee': 'ajay.dixit@justo.co.in', 'role': 'Sourcing ', 'parent': 'kiran.shinde@justo.co.in'},
                    {'employee': 'shubhanshu.gupta@justo.co.in', 'role': 'Sourcing', 'parent': 'sakar.diwase@justo.co.in'},
                    {'employee': 'devendra.hydrabadkar@justo.co.in', 'role': 'Closing', 'parent': 'amarnath.dhone@justo.co.in'},
                    {'employee': 'gaurav.wagh@justo.co.in', 'role': 'Closing', 'parent': 'sagar.waichole@justo.co.in'},
                    {'employee': 'anita.jadhav@justo.co.in', 'role': 'Closing', 'parent': 'vyaprosh.kale@justo.co.in'},
                    {'employee': 'avinash.rathod@justo.co.in', 'role': 'Sourcing ', 'parent': 'sakar.diwase@justo.co.in'},
                    {'employee': 'kumari.priya@justo.co.in', 'role': 'Sourcing ', 'parent': 'sakar.diwase@justo.co.in'},
                    {'employee': 'jasvinder.kaur@justo.co.in', 'role': 'Closing', 'parent': 'rizwan.shaikh@justo.co.in'},
                    {'employee': 'sujit.phatak@justo.co.in', 'role': 'Closing TL', 'parent': 'ajaykumar.singh@justo.co.in'},
                    {'employee': 'nisha.samudre@justo.co.in', 'role': 'Closing', 'parent': 'nikhil.sisodiya@justo.co.in'},
                    {'employee': 'namrata.phatak@justo.co.in', 'role': 'Sourcing ', 'parent': 'pratik.kolhapure@justo.co.in'},
                    {'employee': 'aditya.thakare@justo.co.in', 'role': 'Sourcing ', 'parent': 'pankaj.singh@justo.co.in'},
                    {'employee': 'ashwin.shrikhande@justo.co.in', 'role': 'Closing', 'parent': 'pratik.kolhapure@justo.co.in'},
                    {'employee': 'sadanand.dhumal@justo.co.in', 'role': 'Sourcing ', 'parent': 'arafatkhan.pathan@justo.co.in'},
                    {'employee': 'yash.kajve@justo.co.in', 'role': 'Sourcing', 'parent': 'pankaj.singh@justo.co.in'},
                    {'employee': 'ajay.rajput@justo.co.in', 'role': 'Sourcing ', 'parent': 'kiran.shinde@justo.co.in'},
                    {'employee': 'balaji.shinde@justo.co.in', 'role': 'Sourcing ', 'parent': 'arafatkhan.pathan@justo.co.in'},
                    {'employee': 'somesh.naikwade@justo.co.in', 'role': 'Sourcing ', 'parent': 'kiran.shinde@justo.co.in'},
                    {'employee': 'sanket.sanas@justo.co.in', 'role': 'Closing', 'parent': 'mrugesh.trivedi@justo.co.in'},
                    {'employee': 'Nitin.Sonawane@justo.co.in', 'role': 'Sourcing ', 'parent': 'kiran.shinde@justo.co.in'},
                    {'employee': 'vivek.kulkarni@justo.co.in', 'role': 'CRM', 'parent': 'sunny.john@justo.co.in'},
                    {'employee': 'Jayesh.Badgujar@justo.co.in', 'role': 'Closing', 'parent': 'shrinivas.ugile@justo.co.in'},
                    {'employee': 'sourabh.nevase@justo.co.in', 'role': 'Closing', 'parent': 'prasad.palande@justo.co.in'},
                    {'employee': 'akash.thorat@justo.co.in', 'role': 'Closing', 'parent': 'rahul.tirmare@justo.co.in'},
                    {'employee': 'adityasingh.virat@justo.co.in', 'role': 'Closing', 'parent': 'rizwan.shaikh@justo.co.in'},
                    {'employee': 'ayush.jadhav@justo.co.in', 'role': 'Closing', 'parent': 'mitosh.navale@justo.co.in'},
                    {'employee': 'avinash.tribhuvan@justo.co.in', 'role': 'Cluster Head', 'parent': 'zubaid.shaikh@justo.co.in'},
                    {'employee': 'ajaykumar.singh@justo.co.in', 'role': 'Cluster Head', 'parent': 'nitin.pardeshi@justo.co.in'},
                    {'employee': 'vishal.khutwad@justo.co.in', 'role': 'Sourcing ', 'parent': 'jitendra.singh@justo.co.in'},
                    {'employee': 'shivam.balap@justo.co.in', 'role': 'Sourcing ', 'parent': 'vyaprosh.kale@justo.co.in'},
                    {'employee': 'minakshi.sonone@justo.co.in', 'role': 'Closing', 'parent': 'mitosh.navale@justo.co.in'},
                    {'employee': 'apeksha.nagawade@justo.co.in', 'role': 'Closing', 'parent': 'mrugesh.trivedi@justo.co.in'},
                    {'employee': 'shruti.kodelwar@justo.co.in', 'role': 'Closing', 'parent': 'mitosh.navale@justo.co.in'},
                    {'employee': 'shweta.gawali@justo.co.in', 'role': 'Closing', 'parent': 'prasad.palande@justo.co.in'},
                    {'employee': 'mashak.lalmahammad@justo.co.in', 'role': 'Sourcing ', 'parent': 'arafatkhan.pathan@justo.co.in'},
                    {'employee': 'mallikarjun.suryawanshi@justo.co.in', 'role': 'Sourcing ', 'parent': 'prasad.wakhare@justo.co.in'},
                    {'employee': 'rushikesh.sawant@justo.co.in', 'role': 'Sourcing', 'parent': 'sayan.chakraborty@justo.co.in'},
                    {'employee': 'manoj.gutthe@justo.co.in', 'role': 'Sourcing', 'parent': 'avinash.tribhuvan@justo.co.in'},
                    {'employee': 'gaurav.pardeshi@justo.co.in', 'role': 'Sourcing ', 'parent': 'arafatkhan.pathan@justo.co.in'},
                    {'employee': 'rupesh.kapadnis@justo.co.in', 'role': 'Sourcing', 'parent': 'Piyush.Bagarecha@justo.co.in'},
                    {'employee': 'kiran.chavan@justo.co.in', 'role': 'Closing', 'parent': 'mitosh.navale@justo.co.in'},
                    {'employee': 'rajesh.andhale@justo.co.in', 'role': 'Sourcing ', 'parent': 'arafatkhan.pathan@justo.co.in'},
                    {'employee': 'mino.ketan@justo.co.in', 'role': 'Sourcing', 'parent': 'subhransu.sahoo@justo.co.in'},
                    {'employee': 'anirudha.somvanshi@justo.co.in', 'role': 'Sourcing ', 'parent': 'sakar.diwase@justo.co.in'},
                    {'employee': 'azmatullah.menon@justo.co.in', 'role': 'Sourcing', 'parent': 'sakar.diwase@justo.co.in'},
                    {'employee': 'Vijay.mallishe@justo.co.in', 'role': 'CRM', 'parent': 'sunny.john@justo.co.in'},
                    {'employee': 'rohit.patil@justo.co.in', 'role': 'Sourcing', 'parent': 'Piyush.Bagarecha@justo.co.in'},
                    {'employee': 'sagar.waichole@justo.co.in', 'role': 'Closing TL', 'parent': 'vishal.thigale@justo.co.in'},
                    {'employee': 'harshal.nikas@justo.co.in', 'role': 'Sourcing ', 'parent': 'sakar.diwase@justo.co.in'},
                    {'employee': 'anuja.rungta@justo.co.in', 'role': 'Closing', 'parent': 'amarnath.dhone@justo.co.in'},
                    {'employee': 'aditya.nagare1@justo.co.in', 'role': 'Closing', 'parent': 'shriraj.patil@justo.co.in'},
                    {'employee': 'divyanshu.singh@justo.co.in', 'role': 'Closing', 'parent': 'avinash.tribhuvan@justo.co.in'},
                    {'employee': 'anoop.dwevidi@justo.co.in', 'role': 'Sourcing ', 'parent': 'niket.mule@justo.co.in'},
                    {'employee': 'shrishailya.deshpande@justo.co.in', 'role': 'Sourcing ', 'parent': 'sushil.mandge@justo.co.in'},
                    {'employee': 'sachin.amrute@justo.co.in', 'role': 'Sourcing ', 'parent': 'niket.mule@justo.co.in'},
                    {'employee': 'abhishek.chauhan@justo.co.in', 'role': 'Closing', 'parent': 'pratik.kolhapure@justo.co.in'},
                    {'employee': 'ajay.yelase@justo.co.in', 'role': 'Sourcing ', 'parent': 'sakar.diwase@justo.co.in'},
                    {'employee': 'laxmi.bamne@justo.co.in', 'role': 'Closing', 'parent': 'mrugesh.trivedi@justo.co.in'},
                    {'employee': 'nasir.sayyed@justo.co.in', 'role': 'Closing', 'parent': 'amyn.khoja@justo.co.in'},
                    {'employee': 'niket.mule@justo.co.in', 'role': 'Sourcing TL', 'parent': 'sandesh.chavan@justo.co.in'},
                    {'employee': 'chandan.choudhary@justo.co.in', 'role': 'Closing TL', 'parent': 'sandesh.chavan@justo.co.in'},
                    {'employee': 'athhar.shaikh@justo.co.in', 'role': 'Closing', 'parent': 'sujit.phatak@justo.co.in'},
                    {'employee': 'prasad.wakhare@justo.co.in', 'role': 'Sourcing TL', 'parent': 'ajaykumar.singh@justo.co.in'},
                    {'employee': 'shruti.dekate@justo.co.in', 'role': 'Closing', 'parent': 'prajay.khale@justo.co.in'},
                    {'employee': 'shweta.garade@justo.co.in', 'role': 'Closing', 'parent': 'shriraj.patil@justo.co.in'},
                    {'employee': 'hariom.ambore@justo.co.in', 'role': 'Sourcing ', 'parent': 'niket.mule@justo.co.in'},
                    {'employee': 'manthan.dekate@justo.co.in', 'role': 'Closing', 'parent': 'mitosh.navale@justo.co.in'},
                    {'employee': 'pravin.tiwari@justo.co.in', 'role': 'Closing', 'parent': 'amyn.khoja@justo.co.in'},
                    {'employee': 'ashutosh.singh@justo.co.in', 'role': 'Closing ', 'parent': 'sujit.phatak@justo.co.in'},
                    {'employee': 'ashish.bhosale@justo.co.in', 'role': 'CRM', 'parent': 'sunny.john@justo.co.in'},
                    {'employee': 'ganesh.chaudhari@justo.co.in', 'role': 'Closing', 'parent': 'chandan.choudhary@justo.co.in'},
                    {'employee': 'abhinav.mathur@justo.co.in', 'role': 'Sourcing', 'parent': 'sakar.diwase@justo.co.in'},
                    {'employee': 'pankaj.singh@justo.co.in', 'role': 'Sourcing TL', 'parent': 'sandeep.kamat@justo.co.in'},
                    {'employee': 'ashish.more@justo.co.in', 'role': 'Closing', 'parent': 'ashwini.kumar@justo.co.in'},
                    {'employee': 'kiran.uttapure@justo.co.in', 'role': 'Sourcing', 'parent': 'niket.mule@justo.co.in'},
                    {'employee': 'gaurav.mahajan@justo.co.in', 'role': 'Closing', 'parent': 'shriraj.patil@justo.co.in'},
                    {'employee': 'avinash.ghorpade@justo.co.in', 'role': 'Closing', 'parent': 'prajay.khale@justo.co.in'},
                    {'employee': 'mayur.bartakke@justo.co.in', 'role': 'Closing', 'parent': 'ashwini.kumar@justo.co.in'},
                    {'employee': 'raj.thakur@justo.co.in', 'role': 'Closing', 'parent': 'chandan.choudhary@justo.co.in'},
                    {'employee': 'hrushikesh.jadkar@justo.co.in', 'role': 'Sourcing ', 'parent': 'prasad.wakhare@justo.co.in'},
                    {'employee': 'sakshi.gogawale@justo.co.in', 'role': 'Closing', 'parent': 'chandan.choudhary@justo.co.in'},
                    {'employee': 'pralhad.kapre@justo.co.in', 'role': 'Sourcing ', 'parent': 'prasad.wakhare@justo.co.in'},
                    {'employee': 'arshad.sayyed@justo.co.in', 'role': 'Closing', 'parent': 'sujit.phatak@justo.co.in'},
                    {'employee': 'tejas.giri@justo.co.in', 'role': 'CRM', 'parent': 'sunny.john@justo.co.in'},
                    {'employee': 'vandana.singh@justo.co.in', 'role': 'Closing', 'parent': 'amarnath.dhone@justo.co.in'},
                    {'employee': 'asawari.parit@justo.co.in', 'role': 'Closing', 'parent': 'prasad.palande@justo.co.in'},
                    {'employee': 'saket.atkare@justo.co.in', 'role': 'Sourcing', 'parent': 'avinash.tribhuvan@justo.co.in'},
                    {'employee': 'jinesh.sontakke@justo.co.in', 'role': 'Closing', 'parent': 'rahul.tirmare@justo.co.in'},
                    {'employee': 'samruddhi.patankar@justo.co.in', 'role': 'Closing', 'parent': 'sagar.waichole@justo.co.in'},
                    {'employee': 'aadesh.deshmukh@justo.co.in', 'role': 'Closing', 'parent': 'ajaykumar.singh@justo.co.in'},
                    {'employee': 'ankita.vyas@justo.co.in', 'role': 'Closing', 'parent': 'amarnath.dhone@justo.co.in'},
                    {'employee': 'siddhesh.sakpal@justo.co.in', 'role': 'Sourcing', 'parent': 'avinash.tribhuvan@justo.co.in'},
                    {'employee': 'harsh.takone@justo.co.in', 'role': 'Sourcing', 'parent': 'prasad.wakhare@justo.co.in'},
                    {'employee': 'mohan.dethe@justo.co.in', 'role': 'Sourcing', 'parent': 'kiran.shinde@justo.co.in'},
                    {'employee': 'rishabh.sinha@justo.co.in', 'role': 'Sourcing', 'parent': 'prasad.wakhare@justo.co.in'},
                    {'employee': 'aditya.giri@justo.co.in', 'role': 'Closing', 'parent': 'vivek.yerande@justo.co.in'},
                    {'employee': 'ashok.lokare@justo.co.in', 'role': 'Sourcing', 'parent': 'sayan.chakraborty@justo.co.in'},
                    {'employee': 'yasin.shaikh@justo.co.in', 'role': 'Closing', 'parent': 'vivek.yerande@justo.co.in'},
                    {'employee': 'suraj.jirage@justo.co.in', 'role': 'Sourcing', 'parent': 'pankaj.singh@justo.co.in'},
                    {'employee': 'prashant.gaikwad@justo.co.in', 'role': 'Sourcing', 'parent': 'sayan.chakraborty@justo.co.in'},
                    {'employee': 'shubham.mali@justo.co.in', 'role': 'Sourcing', 'parent': 'shubhamsuresh.patil@justo.co.in'},
                    {'employee': 'gaurav.patil@justo.co.in', 'role': 'Sourcing ', 'parent': 'kiran.shinde@justo.co.in'},
                    {'employee': 'zubaid.shaikh@justo.co.in', 'role': 'Cluster Head', 'parent': 'praveen.apte@justo.co.in'},
                    {'employee': 'Siddheshwar.koli@justo.co.in', 'role': 'Sourcing', 'parent': 'vyaprosh.kale@justo.co.in'},
                    {'employee': 'akshay.bagul@justo.co.in', 'role': 'Closing TL', 'parent': 'sandesh.chavan@justo.co.in'},
                    {'employee': 'harshavardhan.dongre@justo.co.in', 'role': 'Closing', 'parent': 'sandeep.kamat@justo.co.in'},
                    {'employee': 'ashwin.jeswani@justo.co.in', 'role': 'Sourcing', 'parent': 'shubhamsuresh.patil@justo.co.in'},
                    {'employee': 'sayan.chakraborty@justo.co.in', 'role': 'Cluster Head', 'parent': 'nitin.pardeshi@justo.co.in'},
                    {'employee': 'jitendra.singh@justo.co.in', 'role': 'Sourcing Lead', 'parent': 'ajaykumar.singh@justo.co.in'},
                    {'employee': 'nikhil.kumbhar@justo.co.in', 'role': 'Sourcing', 'parent': 'sakar.diwase@justo.co.in'},
                    {'employee': 'akash.bachhav@justo.co.in', 'role': 'Sourcing', 'parent': 'indranil.sarkar@justo.co.in'},
                    {'employee': 'prasad.palande@justo.co.in', 'role': 'Closing TL', 'parent': 'vishal.thigale@justo.co.in'},
                    {'employee': 'sushil.mandge@justo.co.in', 'role': 'Sourcing TL', 'parent': 'vishal.thigale@justo.co.in'},
                    {'employee': 'piyush.ashtekar@justo.co.in', 'role': 'Sourcing Lead', 'parent': 'nitin.pardeshi@justo.co.in'},
                    {'employee': 'samina.mulla@justo.co.in', 'role': 'Closing', 'parent': 'avinash.tribhuvan@justo.co.in'},
                    {'employee': 'manish.auji@justo.co.in', 'role': 'Sourcing', 'parent': 'sushil.mandge@justo.co.in'},
                    {'employee': 'vishal.jadhav@justo.co.in', 'role': 'Closing', 'parent': 'Piyush.Bagarecha@justo.co.in'},
                    {'employee': 'vrundavan.wagh@justo.co.in', 'role': 'Sourcing', 'parent': 'sushil.mandge@justo.co.in'},
                    {'employee': 'prashant.fakatkar@justo.co.in', 'role': 'Sourcing', 'parent': 'sakar.diwase@justo.co.in'},
                    {'employee': 'balvir.yadav@justo.co.in', 'role': 'Sourcing', 'parent': 'sakar.diwase@justo.co.in'},
                    {'employee': 'dasharath.patthe@justo.co.in', 'role': 'Sourcing', 'parent': 'sakar.diwase@justo.co.in'},
                    {'employee': 'shubham.rawalkar@justo.co.in', 'role': 'Sourcing', 'parent': 'shubhamsuresh.patil@justo.co.in'},
                    {'employee': 'aniket.chakral@justo.co.in', 'role': 'Sourcing', 'parent': 'vyaprosh.kale@justo.co.in'},
                    {'employee': 'shivam.gupta@justo.co.in', 'role': 'Sourcing', 'parent': 'shubhamsuresh.patil@justo.co.in'},
                    {'employee': 'ajinkya.gulumkar@justo.co.in', 'role': 'Sourcing', 'parent': 'kiran.shinde@justo.co.in'},
                    {'employee': 'vaishnavi.kapale@justo.co.in', 'role': 'Closing', 'parent': 'Piyush.Bagarecha@justo.co.in'},
                    {'employee': 'lina.deore@justo.co.in', 'role': 'Closing', 'parent': 'Piyush.Bagarecha@justo.co.in'},
                    {'employee': 'diksha.pimpliskar@justo.co.in', 'role': 'Closing', 'parent': 'Piyush.Bagarecha@justo.co.in'},
                    {'employee': 'monali.chavan@justo.co.in', 'role': 'Sourcing', 'parent': 'shubhamsuresh.patil@justo.co.in'},
                    {'employee': 'praveen.apte@justo.co.in', 'role': 'Business Head', 'parent': 'pushp@justo.co.in'},
                    {'employee': 'Ashish.kalokhe@justo.co.in', 'role': 'Sourcing', 'parent': 'pankaj.singh@justo.co.in'},
                    {'employee': 'onkarp.surve@jusro.co.in', 'role': 'Sourcing', 'parent': 'pankaj.singh@justo.co.in'},
                    {'employee': 'shubham.patil@justo.co.in', 'role': 'Sourcing', 'parent': 'pankaj.singh@justo.co.in'},
                    {'employee': 'Aniket.kalaskar@justo.co.in', 'role': 'Sourcing', 'parent': 'kiran.shinde@justo.co.in'},
                    {'employee': 'babita.rabbewar@justo.co.in', 'role': 'Closing TL', 'parent': 'sandeep.kamat@justo.co.in'},
                    {'employee': 'shubham.chaudhary@justo.co.in', 'role': 'Closing', 'parent': 'rahul.tirmare@justo.co.in'},
                    {'employee': 'ranjeet.kale@justo.co.on', 'role': 'Sourcing', 'parent': 'kiran.shinde@justo.co.in'},
                    {'employee': 'devesh.pithawe@justo.co.in', 'role': 'Sourcing', 'parent': 'pankaj.singh@justo.co.in'},
                    {'employee': 'gaurav.joge@justo.co.in', 'role': 'Sourcing', 'parent': 'pankaj.singh@justo.co.in'},
                    {'employee': 'jayesh.ghadge@justo.co.in', 'role': 'Sourcing', 'parent': 'pankaj.singh@justo.co.in'},
                    {'employee': 'vijay.vaidya@justo.co.in', 'role': 'Sourcing', 'parent': 'sakar.diwase@justo.co.in'},
                    {'employee': 'ashish.katgaye@justo.co.in', 'role': 'Sourcing', 'parent': 'pankaj.singh@justo.co.in'},
                    {'employee': 'shubhamsuresh.patil@justo.co.in', 'role': 'Sourcing TL', 'parent': 'karan.sarwade@justo.co.in'},
                    {'employee': 'krishna.deshmukh@justo.co.in', 'role': 'Sourcing', 'parent': 'pankaj.singh@justo.co.in'},
                    {'employee': 'amyn.khoja@justo.co.in', 'role': 'Closing TL', 'parent': 'ajaykumar.singh@justo.co.in'},
                    {'employee': 'abhijeet.gaikwad@justo.co.in', 'role': 'CRM', 'parent': 'sunny.john@justo.co.in'},
                    {'employee': 'vivek.yerande@justo.co.in', 'role': 'Closing TL', 'parent': 'sandeep.kamat@justo.co.in'},
                    {'employee': 'nishant.sharma@justo.co.in', 'role': 'Sourcing TL', 'parent': 'ajaykumar.singh@justo.co.in'},
                    {'employee': 'indranil.sarkar@justo.co.in', 'role': 'Sourcing TL', 'parent': 'ajaykumar.singh@justo.co.in'},
                    {'employee': 'akshaysingh.rajawat@justo.co.in', 'role': 'Sourcing', 'parent': 'mayur.gite@justo.co.in'},
                    {'employee': 'shreyash.bangale@justo.co.in', 'role': 'Sourcing', 'parent': 'indranil.sarkar@justo.co.in'},
                    {'employee': 'smita.kudale@justo.co.in', 'role': 'Closing', 'parent': 'vivek.yerande@justo.co.in'},
                    {'employee': 'ravi.ranjan@justo.co.in', 'role': 'Sourcing', 'parent': 'sakar.diwase@justo.co.in'},
                    {'employee': 'mrugesh.trivedi@justo.co.in', 'role': 'Closing TL', 'parent': 'vishal.thigale@justo.co.in'},
                    {'employee': 'rajeshwar.patil@justo.co.in', 'role': 'Sourcing', 'parent': 'sushil.mandge@justo.co.in'},
                    {'employee': 'sabiya.mulani@justo.co.in', 'role': 'CRM', 'parent': 'Piyush.Bagarecha@justo.co.in'},
                    {'employee': 'amandeep.bhatia@justo.co.in', 'role': 'Sourcing', 'parent': 'nishant.sharma@justo.co.in'},
                    {'employee': 'farheen.shaik@justo.co.in', 'role': 'Closing', 'parent': 'mrugesh.trivedi@justo.co.in'},
                    {'employee': 'kalyani.bhimewar@justo.co.in', 'role': 'Closing', 'parent': 'prasad.palande@justo.co.in'},
                    {'employee': 'kamini.kate@justo.co.in', 'role': 'Closing', 'parent': 'prasad.palande@justo.co.in'},
                    {'employee': 'darshana.band@justo.co.in', 'role': 'Closing', 'parent': 'nikhil.sisodiya@justo.co.in'}]
            for item in data:
                employee = request.env['hr.employee'].sudo().search([('work_email', '=', item['employee'])], limit=1)
                if not employee:
                    employee = request.env['hr.employee'].sudo().search([('private_email', '=', item['employee'])], limit=1)
                    if not employee:
                        employee = request.env['hr.employee'].sudo().search([('corporate_email', '=', item['employee'])],
                                                                            limit=1)
                if employee:
                    role = False
                    if item['role'] == 'Business Head':
                        role = 'business_head'
                    elif item['role'] == 'Closing TL':
                        role = 'closing_tl'
                    elif item['role'] == 'Cluster Head':
                        role = 'cluster_head'
                    elif item['role'] == 'Closing':
                        role = 'closing_manager'
                    elif item['role'] == 'CRM':
                        role = 'crm'
                    elif item['role'] == 'Sourcing':
                        role = 'sourcing_manager'
                    elif item['role'] == 'Sourcing TL':
                        role = 'sourcing_tl'
                    if role:
                        parent = request.env['hr.employee'].sudo().search([('work_email', '=', item['parent'])], limit=1)
                        if not parent:
                            parent = request.env['hr.employee'].sudo().search([('private_email', '=', item['parent'])], limit=1)
                            if not parent:
                                parent = request.env['hr.employee'].sudo().search([('corporate_email', '=', item['parent'])],
                                                                                  limit=1)
                        if parent:
                            request.env.cr.execute(f"update hr_employee set role = '{role}' where id = {employee.id}")
                            request.env.cr.execute(f"update hr_employee set parent_id = {parent.id} where id = {employee.id}")
            return 'Success'
        else:
            return 'Access Denied'

    @http.route(['/correct_employee_city_email'], type='http', auth="public")
    def correct_employee_city_email(self):
        if request.env.user.has_group('base.group_system'):
            data = [{"badge": "P0567", "email" : "aadesh.deshmukh@justo.co.in", "city": "Pune"},
                    {"badge": "JUS0188", "email" : "aaira.ansari@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS1356", "email" : "aarti.bachwani@justo.co.in", "city": "Thane"},
                    {"badge": "JUS0792", "email" : "aarti.bhandare@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0597", "email" : "aarushi.shinde@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0306", "email" : "aashiya.dhepe@justo.co.in", "city": "Pune"},
                    {"badge": "M0605", "email" : "aashrish.kolekar@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0403", "email" : "aayushi.sonawane@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS656", "email" : "abhash.jha@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS666", "email" : "abhijeet.gaikwad@justo.co.in", "city": "Pune"},
                    {"badge": "M0614", "email" : "abhijit.kumar@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0548", "email" : "abhinav.mathur@justo.co.in", "city": "Pune"},
                    {"badge": "JUS0468", "email" : "abhinav.shekhar@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0580", "email" : "abhishar.yadav@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0519", "email" : "abhishek.chauhan@justo.co.in", "city": "Pune"},
                    {"badge": "P0444", "email" : "abhishek.chavan@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0305", "email" : "abhishek.newale@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0830", "email" : "abhishek.pandey@justo.co.in", "city": "Thane"},
                    {"badge": "JUS1140", "email" : "abhishek.upadhyay@justo.co.in", "city": "Thane"},
                    {"badge": "M0808", "email" : "aditya.giri@justo.co.in", "city": "Faridabad"},
                    {"badge": "P0345", "email" : "aditya.nagare@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS1135", "email" : "aditya.thakare@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0441", "email" : "adityasingh.virat@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0531", "email" : "adnan.shaikh@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0497", "email" : "adwait.baiju@justo.co.in", "city": "Pune"},
                    {"badge": "M0801", "email" : "aishwarya.parmar@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0391", "email" : "ajay.dixit@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0499", "email" : "ajay.jogra@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0849", "email" : "ajay.pal@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0424", "email" : "ajay.rajput@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0522", "email" : "ajay.yelase@justo.co.in", "city": "Pune"},
                    {"badge": "P0460", "email" : "ajaykumar.singh@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS600", "email" : "ajinkya.bhawar@justo.co.in", "city": "Thane"},
                    {"badge": "JUS0163", "email" : "ajinkya.jadhav@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS630", "email" : "ajinkya.gulumkar@justo.co.in", "city": "Pune"},
                    {"badge": "P0490", "email" : "ajit.jadhav@justo.co.in", "city": "Pune"},
                    {"badge": "JUS607", "email" : "akash.bachhav@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0542", "email" : "akash.astalkar@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0411", "email" : "akash.kamble@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS0255", "email" : "akash.kotwal@justo.co.in", "city": "Pune"},
                    {"badge": "JUS0214", "email" : "akash.ozarkar@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS1171", "email" : "akash.thorat@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0636", "email" : "", "city": "Mumbai"},
                    {"badge": "M0681", "email" : "akshat.tiwari@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0552", "email" : "akshay.daga@justo.co.in", "city": "Pune"},
                    {"badge": "JUS594", "email" : "akshay.bagul@justo.co.in", "city": "Pune"},
                    {"badge": "JUS610", "email" : "akshay.more@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0503", "email" : "akshay.dupate@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS699", "email" : "akshay.tale@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0796", "email" : "akshay.mhatre@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0583", "email" : "akshay.rajani@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0632", "email" : "akshay.gupta@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0063", "email" : "akshay.somani@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS1014", "email" : "akshay.timbole@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS672", "email" : "akshaysingh.rajawat@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0059", "email" : "", "city": "Mumbai"},
                    {"badge": "M0740", "email" : "altamash.hawaldar@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0379", "email" : "amancio.rodrigues@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS684", "email" : "amandeep.bhatia@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0069", "email" : "amar.dhepe@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS0279", "email" : "amarnath.dhone@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0576", "email" : "ambika.chalwadi@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS0627", "email" : "amey.pathak@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0500", "email" : "amit.pampattiwar@justo.co.in", "city": "Pune"},
                    {"badge": "P0325", "email" : "amit.baghel@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0373", "email" : "amit.chavan@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0394", "email" : "amit.debnath@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS1512", "email" : "Amit.dhibar@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS1496", "email" : "amit.jagdale@justo.co.in", "city": "Thane"},
                    {"badge": "M0567", "email" : "amit.pal@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0585", "email" : "amit.samgiskar@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0528", "email" : "amitesh.mukherjee@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0780", "email" : "amitkumar.pandey@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0274", "email" : "amjad.khan@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS0161", "email" : "amol.raskar@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS0130", "email" : "amol.zulzule@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0650", "email" : "amruta.ghodke@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0440", "email" : "amruta.sawant@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS664", "email" : "amyn.khoja@justo.co.in", "city": "Pune"},
                    {"badge": "P0435", "email" : "anamika.pardhi@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0842", "email" : "anandkumar.pandey@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0370", "email" : "anant.sawant@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0670", "email" : "anas.dabir@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS644", "email" : "Aniket.kalaskar@justo.co.in", "city": "Pune"},
                    {"badge": "M0584", "email" : "", "city": "Mumbai"},
                    {"badge": "JUS631", "email" : "aniket.chakral@justo.co.in", "city": "Pune"},
                    {"badge": "M0644", "email" : "aniket.navale@justo.co.in", "city": "Thane"},
                    {"badge": "JUS0405", "email" : "aniket.pathade@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS0900", "email" : "anil.tiwari@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS0257", "email" : "anil.sasane@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0772", "email" : "anil.sharma@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS0822", "email" : "animesh.dutta@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS0475", "email" : "animesh.mathur@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0499", "email" : "anirudha.somvanshi@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS1103", "email" : "anita.jadhav@justo.co.in", "city": "Pune"},
                    {"badge": "B0017", "email" : "Anjali.Biswal@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0749", "email" : "ankesh.mishra@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS651", "email" : "ankita.jadhav@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0569", "email" : "ankita.vyas@justo.co.in", "city": "Pune"},
                    {"badge": "M0412", "email" : "ankur.tandon@justo.co.in", "city": "Pune"},
                    {"badge": "P0516", "email" : "anoop.dwevidi@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0511", "email" : "anuja.rungta@justo.co.in", "city": "Pune"},
                    {"badge": "M0722", "email" : "anup.singh@justo.co.in", "city": "Pune"},
                    {"badge": "P0225", "email" : "", "city": "Thane"},
                    {"badge": "P0572", "email" : "anurag.hiwale@justo.co.in", "city": "Pune"},
                    {"badge": "P0451", "email" : "anurag.badhe@justo.co.in", "city": "Pune"},
                    {"badge": "P0535", "email" : "anurag.hirapure@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0261", "email" : "anurag.tiwari@justo.co.in", "city": "Pune"},
                    {"badge": "M0721", "email" : "anusha.shetye@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0855", "email" : "anushka.chavan@justo.co.in", "city": "Thane"},
                    {"badge": "M0607", "email" : "", "city": "Mumbai"},
                    {"badge": "JUS1202", "email" : "apeksha.nagawade@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0395", "email" : "", "city": "Mumbai"},
                    {"badge": "JUS0830", "email" : "arafatkhan.pathan@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS602", "email" : "aarti.gaikwad@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS0142", "email" : "archana.patil@justo.co.in", "city": "Pune"},
                    {"badge": "M0785", "email" : "arindom.chakraborty@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS1220", "email" : "arjun.chalana@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0811", "email" : "arlen.pengal@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0453", "email" : "arnab.barman@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS593", "email" : "arohit.rai@justo.co.in", "city": "Mumbai"},
                    {"badge": "B0015", "email" : "arpan.mohanty@justo.co.in", "city": "Mumbai "},
                    {"badge": "JUS624", "email" : "arpan.sharma@justo.co.in", "city": "Bhubaneswar"},
                    {"badge": "JUS690", "email" : "arpit.singh@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0560", "email" : "arshad.sayyed@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0348", "email" : "aruna.kivlekar@justo.co.in", "city": "Pune"},
                    {"badge": "CON009", "email" : "arvind.kale@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0564", "email" : "asawari.parit@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS657", "email" : "ashish.katgaye@justo.co.in", "city": "Pune"},
                    {"badge": "P0541", "email" : "ashish.bhosale@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0433", "email" : "", "city": "Pune"},
                    {"badge": "M0857", "email" : "ashish.singh@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0549", "email" : "ashish.more@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS641", "email" : "Ashish.kalokhe@justo.co.in", "city": "Pune"},
                    {"badge": "P0575", "email" : "ashok.lokare@justo.co.in", "city": "Pune"},
                    {"badge": "M0800", "email" : "ashok.yadav@justo.co.in", "city": "Kolhapur"},
                    {"badge": "JUS0760", "email" : "ashutosh.agarwal@justo.co.in", "city": "Thane"},
                    {"badge": "M0530", "email" : "ashutosh.gurkha@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0458", "email" : "ashutosh.mahawar@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0538", "email" : "ashutosh.singh@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS0591", "email" : "ashwin.jeswani@justo.co.in", "city": "Pune"},
                    {"badge": "P0421", "email" : "ashwin.shrikhande@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS0224", "email" : "ashwini.kumar@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0764", "email" : "asvi.kumari@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0755", "email" : "atesh.kamble@justo.co.in", "city": "mumbai"},
                    {"badge": "P0584", "email" : "atharva.awachat@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0526", "email" : "athhar.shaikh@justo.co.in", "city": "Nagpur"},
                    {"badge": "M0660", "email" : "atul.rai@justo.co.in", "city": "Pune"},
                    {"badge": "M0535", "email" : "aura.saikar@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0555", "email" : "avinash.ghorpade@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0408", "email" : "avinash.rathod@justo.co.in", "city": "Pune"},
                    {"badge": "P0456", "email" : "avinash.tribhuvan@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS0103", "email" : "avishkar.jopulkar@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0579", "email" : "powai.reception@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0450", "email" : "ayush.jadhav@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS1173", "email" : "ayush.pachori@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS1287", "email" : "azmatullah.menon@justo.com", "city": "Mumbai"},
                    {"badge": "P0436", "email" : "", "city": "Pune"},
                    {"badge": "M0807", "email" : "baban.negi@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0510", "email" : "babita.negi@justo.co.in", "city": "Panvel"},
                    {"badge": "JUS645", "email" : "babita.rabbewar@justo.co.in", "city": "Pune"},
                    {"badge": "M0719", "email" : "balaji.reddy@justo.co.in", "city": "Pune"},
                    {"badge": "P0423", "email" : "balaji.shinde@justo.co.in", "city": "Thane"},
                    {"badge": "M0495", "email" : "balamurugan.pandaram@justo.co.in", "city": ""},
                    {"badge": "M0728", "email" : "baljeet.kaur@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS629", "email" : "balvir.yadav@justo.co.in", "city": ""},
                    {"badge": "B0022", "email" : "basundhara.panda@justo.co.in", "city": "Pune"},
                    {"badge": "M0214", "email" : "bhagyashree.ghag@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS0638", "email" : "bhairavi.tiwari@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0817", "email" : "bhavika.shinde@justo.co.in", "city": "Thane"},
                    {"badge": "M0390", "email" : "bhavna.jediya@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS687", "email" : "kalyani.bhimewar@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0294", "email" : "bindu.yadav@justo.co.in", "city": "Pune"},
                    {"badge": "P0501", "email" : "brajendra.singh@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0627", "email" : "brijesh.tiwari@justo.co.in", "city": "Pune"},
                    {"badge": "P0030", "email" : "brishti.samanta@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS677", "email" : "caitan.alphanso@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0805", "email" : "carlton.fernandes@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0234", "email" : "catherine.louis@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0233", "email" : "chaitanya.koli@justo.co.in", "city": ""},
                    {"badge": "P0366", "email" : "", "city": "Bhopal"},
                    {"badge": "M0408", "email" : "", "city": "Mumbai"},
                    {"badge": "P0525", "email" : "chandan.choudhary@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0793", "email" : "chandan.jaiswal@justo.co.in", "city": "Pune"},
                    {"badge": "JUS703", "email" : "Chandni.khatri@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS691", "email" : "chandni.parche@justo.co.in", "city": "Thane"},
                    {"badge": "M0787", "email" : "chandrashekar.goli@justo.co.in", "city": "Mumbai "},
                    {"badge": "JUS698", "email" : "chandrashekhar.goudmadhley@justo.co.in", "city": "Mumbai"},
                    {"badge": "M08060806", "email" : "Chetan.kamble@justo.co.in", "city": "Badlapur"},
                    {"badge": "JUS0648", "email" : "chetan.buddhadev@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0850", "email" : "chetan.soni@justo.co.in", "city": "Pune"},
                    {"badge": "P0365", "email" : "chinmay.babhale@justo.co.in", "city": "Thane"},
                    {"badge": "M0843", "email" : "chitransh.nigam@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0819", "email" : "darshan.patil@justo.co.in", "city": "Mumbai "},
                    {"badge": "JUS665", "email" : "darshan.suryawanshi@justo.co.in", "city": "Thane"},
                    {"badge": "JUS689", "email" : "darshana.band@justo.co.in", "city": "Mumbai "},
                    {"badge": "JUS625", "email" : "dasharath.patthe@justo.co.in", "city": "Pune"},
                    {"badge": "M0695", "email" : "dattaprasad.shetye@justo.co.in", "city": "Mumbai "},
                    {"badge": "M0699", "email" : "", "city": "Mumbai"},
                    {"badge": "M0284", "email" : "", "city": "Mumbai"},
                    {"badge": "M0185", "email" : "deepak.bhatt@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0617", "email" : "", "city": "Mumbai"},
                    {"badge": "JUS0502", "email" : "deepak.pandey@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS0225", "email" : "deepak.nikam@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0833", "email" : "deepak.vishwakarma@justo.co.in", "city": "Pune"},
                    {"badge": "JUS706", "email" : "pillay.deepti1980@gmail.com", "city": "Mumbai"},
                    {"badge": "JUS0709", "email" : "deven.javeri@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS1083", "email" : "devendra.hydrabadkar@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS0658", "email" : "devendra.shinde@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0160", "email" : "", "city": "Mumbai"},
                    {"badge": "JUS650", "email" : "devesh.pithawe@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0616", "email" : "devprakash.mishra@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0485", "email" : "devyani.rajput@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS0907", "email" : "dhananjay.nandedkar@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0482", "email" : "dhanyata.jadhav@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS1100", "email" : "dharmendar.tanwar@justo.co.in", "city": "Pune"},
                    {"badge": "M0794", "email" : "dhiraj.karia@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0665", "email" : "", "city": "Thane"},
                    {"badge": "M0703", "email" : "dhiraj.yadav@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0563", "email" : "", "city": "Mumbai"},
                    {"badge": "M0429", "email" : "", "city": "Mumbai"},
                    {"badge": "JUS0531", "email" : "dhondiba.aptekar@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS638", "email" : "diksha.pimpliskar@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0170", "email" : "", "city": ""},
                    {"badge": "P0371", "email" : "", "city": "Mumbai"},
                    {"badge": "M0831", "email" : "dinesh.dolar@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS1484", "email" : "dipesh.makwana@justo.co.in", "city": "Palghar"},
                    {"badge": "P0339", "email" : "dipesh.gunjite@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0352", "email" : "disha.hule@justo.co.inn", "city": ""},
                    {"badge": "M0769", "email" : "disha.oza@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS682", "email" : "dishant.kelaskar@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS1019", "email" : "divya.waghela@justo.co.in", "city": "Pune"},
                    {"badge": "P0514", "email" : "divyanshu.singh@justo.co.in", "city": "Pune"},
                    {"badge": "P0098", "email" : "divyanshu.soni@justo.co.in", "city": "Pune"},
                    {"badge": "M0330", "email" : "durgesh.sarwal@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS681", "email" : "ekta.lunagariya@yahoo.com", "city": "Mumbai"},
                    {"badge": "M0851", "email" : "ekta.upadhyay@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0844", "email" : "fatema.manasawala@justo.co.in", "city": "Thane"},
                    {"badge": "JUS655", "email" : "Fatima.Makda@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS685", "email" : "farheen.shaik@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0845", "email" : "gufran.khan@justo.co.in", "city": "Pune"},
                    {"badge": "P0542", "email" : "ganesh.chaudhari@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0612", "email" : "ganesh.yadav@justo.co.in", "city": "Pune"},
                    {"badge": "P0022", "email" : "garima.verma@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0479", "email" : "gaurav.chincholkar@justo.co.in", "city": "Mumbai"},
                    {"badge": "JC0008", "email" : "gaurav.more@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS652", "email" : "gaurav.joge@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0583", "email" : "gaurav.fegade@justo.co.in", "city": ""},
                    {"badge": "P0551", "email" : "gaurav.mahajan@justo.co.in", "city": "Pune"},
                    {"badge": "P0582", "email" : "gaurav.patil@justo.co.in", "city": "Pune"},
                    {"badge": "P0476", "email" : "gaurav.pardeshi@justo.co.in", "city": "Pune"},
                    {"badge": "M0672", "email" : "gaurav.pandey@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0402", "email" : "gaurav.wagh@justo.co.in", "city": "Mumbai "},
                    {"badge": "P0473", "email" : "gauri.shrikant@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0253", "email" : "gautami.verma@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0475", "email" : "gokul.krishnan@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0578", "email" : "gopal.pawar@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0592", "email" : "gourang.mestry@justo.co.in", "city": "Pune"},
                    {"badge": "P0400", "email" : "gouri.anand@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0773", "email" : "gyanesh.gupta@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0698", "email" : "hanisha.manglani@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0757", "email" : "haresh.kapoor@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0530", "email" : "hariom.ambore@justo.co.in", "city": "mumbai"},
                    {"badge": "M0674", "email" : "hariom.pandey@justo.co.in", "city": "Pune"},
                    {"badge": "JUS1467", "email" : "harsh.pandey@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0571", "email" : "harsh.takone@justo.co.in", "city": "Thane"},
                    {"badge": "P0508", "email" : "harshal.nikas@justo.co.in", "city": "Pune"},
                    {"badge": "M0060", "email" : "admin@justo.co.in", "city": "Pune"},
                    {"badge": "JUS0592", "email" : "harshavardhan.dongre@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0799", "email" : "heema.shah@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0452", "email" : "himali.kore@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0738", "email" : "himanshu.gupta@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0750", "email" : "himanshu.nagda@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0841", "email" : "hitesh.bhaktiyapuri@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0380", "email" : "hitesh.punjabi@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0554", "email" : "hrushikesh.jadkar@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0405", "email" : "humera.sayyad@justo.co.in", "city": "Pune"},
                    {"badge": "JUS0721", "email" : "hunny.karamchandani@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS668", "email" : "indranil.sarkar@justo.co.in", "city": "Thane"},
                    {"badge": "P0315", "email" : "isha.sharma@justo.co.in", "city": "Pune"},
                    {"badge": "M0514", "email" : "jamal.ahsan@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0410", "email" : "jasvinder.kaur@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0407", "email" : "jay.pardeshi@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0594", "email" : "", "city": "Mumbai"},
                    {"badge": "P0301", "email" : "jayanta.mukherjee@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0355", "email" : "Jayendra.Ahvade@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS660", "email" : "jayesh.ghadge@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0430", "email" : "jayesh.badgujar@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS0870", "email" : "jayesh.raundal@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS0622", "email" : "jayshree.rao@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0591", "email" : "jaysingh.yadav@justo.co.in", "city": "Pune"},
                    {"badge": "JC004", "email" : "jeetendra.mandavkar@justo.co.in", "city": ""},
                    {"badge": "JUS0891", "email" : "jia.gupta@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0723", "email" : "jignisha.singhadia@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0751", "email" : "jinal.trivedi@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0565", "email" : "jines.sontakke@justo.co.in", "city": "mumbai"},
                    {"badge": "P0341", "email" : "jitendra.choudhary@justo.co.in", "city": "Pune"},
                    {"badge": "JUS601", "email" : "jitendra.singh@justo.co.in", "city": "Pune"},
                    {"badge": "P0523", "email" : "jiya.satakshi@justo.co.in", "city": ""},
                    {"badge": "M0288", "email" : "john.vincent@justo.co.in", "city": "Pune"},
                    {"badge": "P0486", "email" : "Jyoti.sutar@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS0364", "email" : "jyoti.bhartiya@justo.co.in", "city": "Jalgaon"},
                    {"badge": "M0815", "email" : "jyoti1.kanoje@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0545", "email" : "jyoti.ramgir@justo.co.in", "city": "Mumbai"},
                    {"badge": "CONT3", "email" : "kailash.padwal@justo.co.in", "city": "Pune"},
                    {"badge": "M0666", "email" : "kailash.reddy@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0527", "email" : "kalpesh.ambre@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0677", "email" : "kalpesh.nakar@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0478", "email" : "kalyani.wagh@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0685", "email" : "kamal.garewal@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS686", "email" : "kamini.kate@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0609", "email" : "kamleshsingh.rawat@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0663", "email" : "kanchan.naryani@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0588", "email" : "kanil.shah@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0724", "email" : "kannan.sundaram@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0505", "email" : "", "city": "mumbai"},
                    {"badge": "M0718", "email" : "kapil.vyas@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0634", "email" : "karan.bhatia@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0802", "email" : "karan.ingle@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS0116", "email" : "karan.sarwade@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0196", "email" : "karan.sharma@justo.co.in", "city": "Pune"},
                    {"badge": "M0730", "email" : "karan.singh@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0589", "email" : "kathrina.ashworth@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0710", "email" : "kaushil.dani@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0564", "email" : "kavita.chugh@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0357", "email" : "Kavita.Halijwale@justo.co.in", "city": "Mumbai"},
                    {"badge": "CON013", "email" : "keshav.pandey@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS0910", "email" : "ketan.nagare@justo.co.in", "city": ""},
                    {"badge": "P0302", "email" : "Ketan.rode@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS649", "email" : "Ketki.Mandlekar@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0853", "email" : "khushboo.shaikh@justo.co.in", "city": "Thane"},
                    {"badge": "P0438", "email" : "khushbu.jain@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0160", "email" : "khushi.pardeshi@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0550", "email" : "kiran.uttapure@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0488", "email" : "kiran.chavan@justo.co.in", "city": "Pune"},
                    {"badge": "M0645", "email" : "kiran.jaitpal@justo.co.in", "city": "Pune"},
                    {"badge": "M0733", "email" : "kiranrohidas.shinde@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS0217", "email" : "kiran.shinde@justo.co.in", "city": "Thane"},
                    {"badge": "M0562", "email" : "kishan.mishra@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0846", "email" : "komal.prajapati@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS663", "email" : "krishna.deshmukh@justo.co.in", "city": "mumbai"},
                    {"badge": "P0445", "email" : "krishna.jadhav@justo.co.in", "city": "Mumbai"},
                    {"badge": "B0021", "email" : "kshetrabasi.mohapatra@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS0871", "email" : "kshitija.pagare@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0409", "email" : "kumari.priya@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS0818", "email" : "kumari.snehlata@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS0422", "email" : "kunal.sharma@justo.co.in", "city": "Pune"},
                    {"badge": "JUS0435", "email" : "lalit.balu@justo.co.in", "city": ""},
                    {"badge": "P0543", "email" : "lavu.raut@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0360", "email" : "Laxman.Nitnaware@justo.co.in", "city": "Pune"},
                    {"badge": "P0521", "email" : "laxmi.bamne@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS0899", "email" : "laxmi.bhimte@justo.co.in", "city": "Pune"},
                    {"badge": "P0277", "email" : "laxmi.singh@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS635", "email" : "lina.deore@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS1508", "email" : "maaz.momin@justo.co.in", "city": "Dhule "},
                    {"badge": "JUS0804", "email" : "madhav.murhekar@justo.co.in", "city": "Thane"},
                    {"badge": "P0362", "email" : "madhuri.kalita@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0540", "email" : "madhuri.singh@justo.co.in", "city": "Pune"},
                    {"badge": "M0573", "email" : "maheboob.pasha@justo.co.in", "city": "Pune"},
                    {"badge": "M0569", "email" : "mahesh.gupta@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS695", "email" : "mahima.jena@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS1428", "email" : "majed.shaikh@justo.co.in", "city": "Thane"},
                    {"badge": "JUS1225", "email" : "mallikarjun.suryawanshi@justo.co.in", "city": "Thane"},
                    {"badge": "P0324", "email" : "manali.mahamuni@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0708", "email" : "manan.goradia@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0706", "email" : "maninder.singh@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS620", "email" : "manish.auji@justo.co.in", "city": "Thane"},
                    {"badge": "M0694", "email" : "manish.goud@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0778", "email" : "manish.gupta@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0538", "email" : "manish.kumar@justo.co.in", "city": "Thane"},
                    {"badge": "M0765", "email" : "manish.singh@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS653", "email" : "manish.udutha@JUSTO.CO.IN", "city": "Mumbai"},
                    {"badge": "M0682", "email" : "manisha.more@justo.co.in", "city": "Bhiwandi"},
                    {"badge": "P0050", "email" : "manisha.pandey@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS1390", "email" : "manjiri.sawant@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0774", "email" : "manjiri.sawant@justto.co.in", "city": "Mumbai"},
                    {"badge": "P0475", "email" : "manoj.gutthe@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0705", "email" : "manoj.yadav@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS1125", "email" : "manojkumar.dhaygude@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS606", "email" : "mansoor.khan@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS1371", "email" : "manthan.dekate@justo.co.in", "city": "Pune"},
                    {"badge": "JUS1221", "email" : "mashak.lalmahammad@justo.co.in", "city": "Pune"},
                    {"badge": "P0493", "email" : "maya.pawar@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0553", "email" : "mayur.bartakke@justo.co.in", "city": "Pune"},
                    {"badge": "JUS0782", "email" : "mayur.gite@justo.co.in", "city": "Pune"},
                    {"badge": "M0488", "email" : "mayur.mohite@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS0175", "email" : "mayur.shinde@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0369", "email" : "mayuresh.asabe@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0657", "email" : "mayuri.shimpi@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0492", "email" : "meghana.gurav@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS0466", "email" : "meghesh.kulkarni@justo.co.in", "city": "Pune"},
                    {"badge": "JUS0394", "email" : "milind.patange@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0461", "email" : "minakshi.sonone@justo.co.in", "city": "Mumbai"},
                    {"badge": "B0026", "email" : "minoketan.samal@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0622", "email" : "misba.khan@justo.co.in", "city": "Bhubansewar "},
                    {"badge": "M0762", "email" : "mitali.jadhav@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS1515", "email" : "mitosh.navale@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0410", "email" : "mohammad.kaif@justo.co.in", "city": "Pune"},
                    {"badge": "M0715", "email" : "mohammad.shaikh@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0763", "email" : "hassan.shariff@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0820", "email" : "mohammed.rizwan@justo.co.in", "city": "mumbai"},
                    {"badge": "M0852", "email" : "rizwan.gothekar@justo.co.in", "city": "Thane"},
                    {"badge": "P0573", "email" : "mohan.dethe@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0737", "email" : "shaikh.mohdfzal@justo.co.in", "city": "Pune"},
                    {"badge": "M0667", "email" : "mohdahmed.azizi@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0574", "email" : "mohd.istiyaque@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0466", "email" : "", "city": "Mumbai"},
                    {"badge": "M0649", "email" : "mohit.vasudev@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0771", "email" : "mohsin.momin@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS639", "email" : "monali.chavan@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0376", "email" : "monika.walunj@justo.co.in", "city": "Pune"},
                    {"badge": "JUS616", "email" : "monish.chaudhari@justo.co.in", "city": "Pune"},
                    {"badge": "JUS678", "email" : "mrugesh.trivedi@justo.co.in", "city": "Thane"},
                    {"badge": "P0363", "email" : "Mugdha.Ambawale@justo.co.in", "city": "Pune"},
                    {"badge": "JUS1226", "email" : "mukesh.yadav@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0659", "email" : "muna.dadel@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0590", "email" : "muskan.budhrani@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0546", "email" : "nagesh.kamble@justo.co.in", "city": ""},
                    {"badge": "JUS702", "email" : "naman.singh@justo.co.in", "city": "Pune"},
                    {"badge": "P0415", "email" : "namrata.phatak@justo.co.in", "city": "Nashik"},
                    {"badge": "M0673", "email" : "", "city": "Mumbai"},
                    {"badge": "JUS1270", "email" : "nandita.barick@justo.co.in", "city": "khorda"},
                    {"badge": "M0776", "email" : "narendra.mishra@justo.co.in", "city": "khorda"},
                    {"badge": "M0748", "email" : "naresh.chandra@justo.co.in", "city": "Thane"},
                    {"badge": "P0534", "email" : "nasir.sayyed@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS0805", "email" : "navin.kataria@justo.co.in", "city": "Pune"},
                    {"badge": "JUS0807", "email" : "", "city": "Thane"},
                    {"badge": "P0506", "email" : "", "city": "Mumbai"},
                    {"badge": "M0646", "email" : "", "city": "Pune"},
                    {"badge": "M0758", "email" : "neha.sharma@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0633", "email" : "nehal.tripathi@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0166", "email" : "nihal.gupta@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0527", "email" : "niket.mule@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0094", "email" : "nikhil.barate@justo.co.in", "city": "Pune"},
                    {"badge": "M0680", "email" : "nikhil.dwivedi@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0383", "email" : "nikhil.kumbhar@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0638", "email" : "nikhil.mandke@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS0134", "email" : "nikhil.sisodiya@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS626", "email" : "nikhil.kulkarni@justo.co.in", "city": "Pune"},
                    {"badge": "M0642", "email" : "nilesh.jadhav@justo.co.in", "city": "Pune"},
                    {"badge": "P0249", "email" : "nilesh.pagar@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0603", "email" : "nilesh.sonar@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0334", "email" : "pune.admin@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0790", "email" : "nimit.dubey@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS0833", "email" : "nisha.bharti@justo.co.in", "city": "Thane"},
                    {"badge": "P0416", "email" : "nisha.samudre@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS667", "email" : "nishant.sharma@justo.co.in", "city": "Pune"},
                    {"badge": "P0388", "email" : "nishigandha.gaikwad@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0856", "email" : "nitesh.jadhav@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0586", "email" : "nithin.bhagath@justo.co.in", "city": "Thane"},
                    {"badge": "M0683", "email" : "nitika.yadav@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS0092", "email" : "nitin.pardeshi@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS1165", "email" : "nitin.sonawane@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0716", "email" : "nitish.jadhav@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0640", "email" : "nivedita.singh@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS692", "email" : "omkar.janekar@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0504", "email" : "omkar.kshirsagar@justo.co.in", "city": "Loni KD"},
                    {"badge": "M0745", "email" : "omkar.sarvankar@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS0887", "email" : "onkar.kulkarni@justo.co.in", "city": "Thane"},
                    {"badge": "JUS642", "email" : "onkarp.surve@justo.co.in", "city": "Pune"},
                    {"badge": "JUS0599", "email" : "ovez.shaikh@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0816", "email" : "palvi.phatangare@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0216", "email" : "paneri.hanawate@justo.co.in", "city": "Thane"},
                    {"badge": "P0547", "email" : "pankaj.singh@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0428", "email" : "pankaj.padol@justo.co.in", "city": "Pune"},
                    {"badge": "JUS596", "email" : "parag.bhoir@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS0762", "email" : "parag.chavaan@justo.co.in", "city": "Uran"},
                    {"badge": "P0556", "email" : "paras.pakhale@justo.co.in", "city": ""},
                    {"badge": "MM0829", "email" : "paresh.narvekar@justo.co.in", "city": "Pune"},
                    {"badge": "JUS0369", "email" : "parikshit.paunikar@justo.co.in", "city": "ratnagiri"},
                    {"badge": "P0359", "email" : "Pawan.Sharma@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0840", "email" : "payal.das@justo.co.in", "city": "Pune"},
                    {"badge": "M0720", "email" : "pervez.malik@justo.co.in", "city": "palghar"},
                    {"badge": "JUS0302", "email" : "pinank.salunke@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0389", "email" : "pinky.kalyani@justo.co.in", "city": ""},
                    {"badge": "JUS1000", "email" : "Piyush.Bagarecha@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0729", "email" : "pooja.tikude@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS661", "email" : "pooja.devkar@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0654", "email" : "pooja.bhatia@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS648", "email" : "pooja.patil@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0358", "email" : "pooja.karania@justo.co.in", "city": "Pune"},
                    {"badge": "P0469", "email" : "pooja.kumari@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0566", "email" : "pooja.singh@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0266", "email" : "poojan.ghaywat@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0265", "email" : "poonam.ahuja@justo.co", "city": "Mumbai"},
                    {"badge": "P0288", "email" : "pornima.jekte@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0359", "email" : "pradeep.sukumaran@justo.co.in", "city": ""},
                    {"badge": "JUS679", "email" : "pradipta.nayak@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS0409", "email" : "pradnyadip.wanjare@justo.co.in", "city": "Nayagarh"},
                    {"badge": "M0812", "email" : "pragati.munshi@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0600", "email" : "pragati.parab@justo.co.in", "city": "Thane"},
                    {"badge": "P0586", "email" : "pragati.kumbhar@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS0505", "email" : "prajay.khale@justo.co.in", "city": "Pune"},
                    {"badge": "M0366", "email" : "", "city": "Mumbai"},
                    {"badge": "P0180", "email" : "prajyot.pujari@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS0406", "email" : "prakhar.srivastava@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0804", "email" : "prakshi.sakaria@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0558", "email" : "pralhad.kapre@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0461", "email" : "pramod.surwade@justo.co.in", "city": ""},
                    {"badge": "M0639", "email" : "", "city": "Mumbai"},
                    {"badge": "M0629", "email" : "pranav.sakpal@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0505", "email" : "pranav.dixit@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS2000", "email" : "pranav.joshi@justo.co.in", "city": "Pune"},
                    {"badge": "JUS595", "email" : "pranav.samant@justo.co.in", "city": "Mumbai"},
                    {"badge": "m0818", "email" : "pranay.katkar@justo.co.in", "city": "Panvel"},
                    {"badge": "M0558", "email" : "pranoti.taware@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0697", "email" : "", "city": "Mumbai"},
                    {"badge": "JUS608", "email" : "prasad.palande@justo.co.in", "city": "Mumbai"},
                    {"badge": "WR1001", "email" : "parasad.workrig@workrig.com", "city": "Mumbai"},
                    {"badge": "P0338", "email" : "prasad.dhanorkar@justo.co.in", "city": "Pune"},
                    {"badge": "P0453", "email" : "prasad.naik@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0528", "email" : "prasad.wakhare@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0579", "email" : "prashant.gaikwad@justo.co.in", "city": "Nagpur"},
                    {"badge": "JUS00498", "email" : "prashant.bhide@justo.co.in", "city": "Kolhapur"},
                    {"badge": "JUS628", "email" : "prashant.fakatkar@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0326", "email" : "prashant.khairnar@justo.co.in", "city": "Pune"},
                    {"badge": "M0451", "email" : "prashant.pawar@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS1006", "email" : "Prashant.Tiwari@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS0912", "email" : "prateek.singh@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS0973", "email" : "pratik.jejurikar@justo.co.in", "city": ""},
                    {"badge": "JUS0248", "email" : "pratik.kolhapure@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0825", "email" : "pratik.patil@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS599", "email" : "pratik.shroff@justo.co.in", "city": "Dhule"},
                    {"badge": "JUS0971", "email" : "pratikshya.das@justo.co.in", "city": ""},
                    {"badge": "JUS0940", "email" : "praveen.kumar@justo.co.in", "city": "Bhubaneswar"},
                    {"badge": "JUS637", "email" : "praveen.apte@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0455", "email" : "", "city": "Pune"},
                    {"badge": "M0684", "email" : "", "city": "Mumbai"},
                    {"badge": "M0784", "email" : "pravin.parihar@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0652", "email" : "Pravin.Shinde@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0537", "email" : "pravin.tiwari@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0082", "email" : "preeta.gopalan@justo.co.in", "city": "Pune"},
                    {"badge": "M0358", "email" : "preetam.dhandore@justo.co.in", "city": "Thane"},
                    {"badge": "M0835", "email" : "preeti.kamble@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0507", "email" : "preeti.ahuja@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0417", "email" : "", "city": "Mumbai"},
                    {"badge": "M0713", "email" : "sample3@sample.com", "city": "Mumbai"},
                    {"badge": "M0756", "email" : "prithvi.ramar@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0418", "email" : "priti.kapse@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0529", "email" : "priyanka.masram@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS0329", "email" : "priyanka.bhadkwad@justo.co.in", "city": "Pune"},
                    {"badge": "P0173", "email" : "", "city": "Mumbai"},
                    {"badge": "JUS0259", "email" : "priyanka.hole@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0412", "email" : "priyanka.katkar@justo.co,in", "city": "Mumbai"},
                    {"badge": "JUS0572", "email" : "priyanshi.baghel@justo.co.in", "city": "Mumbai"},
                    {"badge": "JM1478", "email" : "qaz@workrig.com", "city": "Pune"},
                    {"badge": "JUS662", "email" : "purva.lipare@justo.co.in", "city": "Pune"},
                    {"badge": "JUS636", "email" : "Purva.sankalech@justo.co.in", "city": "Pune"},
                    {"badge": "M0599", "email" : "purvi.kha@justo.co.in", "city": "Jalgaon "},
                    {"badge": "P0372", "email" : "pushkar.ambekar@justo.co.in", "city": "Mumbai"},
                    {"badge": "MGM001", "email" : "pushp@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0725", "email" : "raaj.thakur@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0598", "email" : "", "city": "Mumbai"},
                    {"badge": "M0545", "email" : "radhakrishna.naidu@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0743", "email" : "Agaraees.razzak@justo.co.in", "city": "Mumbai"},
                    {"badge": "WR1401", "email" : "raghu.wr@wrmail.com", "city": "Mumbai"},
                    {"badge": "M0739", "email" : "rahul.ravindran@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0651", "email" : "rahul.arya@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0516", "email" : "rahul.gangan@justo.co.in", "city": "Mumbai"},
                    {"badge": "MGM002", "email" : "rahul@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS0884", "email" : "rahul.patil@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS0835", "email" : "rahul.tirmare@justo.co.in", "city": "Pune"},
                    {"badge": "P0557", "email" : "raj.thakur@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0386", "email" : "rajat.gaurav@justo.co.in", "city": "Pune"},
                    {"badge": "P0483", "email" : "rajesh.andhale@justo.co.in", "city": ""},
                    {"badge": "P0327", "email" : "rajesh.chavan@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS693", "email" : "rajesh.mayekar@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS694", "email" : "rajesh.roy@justo.co.in", "city": "Mumbai "},
                    {"badge": "P0381", "email" : "rajesh.surve@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS700", "email" : "rajesh.jha@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS680", "email" : "rajeshwar.patil@justo.co.in", "city": "Mumbai "},
                    {"badge": "M0534", "email" : "rajiv.ranjan@justo.co.in", "city": "Pune"},
                    {"badge": "P0581", "email" : "rajkeshwar.singh@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS1514", "email" : "Ram.Sharma@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0432", "email" : "ramanand.pandey@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0664", "email" : "ranjan.pratap@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS0343", "email" : "ranjan.sengupta@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS647", "email" : "ranjeet.kale@justo.co.on", "city": "Mumbai"},
                    {"badge": "JUS675", "email" : "ravi.ranjan@justo.co.in", "city": "Pune"},
                    {"badge": "P0399", "email" : "ravi.sharma@justo.co.in", "city": "Pune"},
                    {"badge": "JUS1336", "email" : "ravina.kumari@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0783", "email" : "reshu.kanojiya@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0742", "email" : "ria.bhamdi@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0574", "email" : "rishabh.sinha@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS0398", "email" : "rishi.sharma@justo.co.in", "city": "Pune"},
                    {"badge": "M0709", "email" : "rishikesh.ranga@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0247", "email" : "ritesh.chavan@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0832", "email" : "rithik.khatik@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0477", "email" : "ritik.wajage@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0734", "email" : "ritu.bhanushali@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0803", "email" : "ritu.pahuja@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0702", "email" : "riya.suvarna@justo.co.in", "city": "Thane"},
                    {"badge": "P0484", "email" : "riyathombare2000@gmail.com", "city": "Mumbai"},
                    {"badge": "JUS0101", "email" : "rizwan.shaikh@justo.co.in", "city": "Mumbai"},
                    {"badge": "JC000", "email" : "robert.lobo@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0443", "email" : "rohini.kumbhar@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0503", "email" : "rohit.patil@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0272", "email" : "rohit.doiphode@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0707", "email" : "rohit.jagtap@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0731", "email" : "rohit.jaiswal@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS676", "email" : "rohit.kanojia@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0347", "email" : "rohit.more@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0539", "email" : "rohit.sharma@justo.co.in", "city": "Pune"},
                    {"badge": "P0257", "email" : "rohit.uttekar@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0727", "email" : "romit.bose@justo.co.in", "city": "Thane"},
                    {"badge": "M0760", "email" : "ronit.kadwadkar@justo.co.in", "city": "mumbai"},
                    {"badge": "B0020", "email" : "rosalin.sahoo@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS0446", "email" : "roshni.chawla@justo.co.in", "city": "Thane"},
                    {"badge": "M0759", "email" : "rukaiya.surana@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0263", "email" : "rupali.kambale@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0480", "email" : "rupesh.kapadnis@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0626", "email" : "rupeshashok.jadhav@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0565", "email" : "rupesh.jadhav@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0515", "email" : "rupesh.katakdhond@justo.co.in", "city": "Pune"},
                    {"badge": "P0454", "email" : "rupesh.mhatre@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0671", "email" : "rupesh.nagare@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0384", "email" : "rushikesh.patil@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0474", "email" : "rushikesh.sawant@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0349", "email" : "rushikesh.thanedar@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0675", "email" : "rushikesh.varande@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0648", "email" : "rushiraj.ingawale@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0127", "email" : "rutuja.gawande@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS646", "email" : "shubham.chaudhary@justo.co.in", "city": "Pune"},
                    {"badge": "JUS683", "email" : "sabiya.mulani@justo.co.in", "city": "Nashik"},
                    {"badge": "P0518", "email" : "sachin.amrute@justo.co.in", "city": "Pune"},
                    {"badge": "JUS673", "email" : "sachin.vaishnav@justo.co.in", "city": "Mumbai "},
                    {"badge": "M0741", "email" : "sachin.shinde@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0122", "email" : "sachin.wani@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0420", "email" : "sadanand.dhumal@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS621", "email" : "sadhana.jagdale@justo.co.in", "city": "Mumbai "},
                    {"badge": "JC0005", "email" : "sagar.molake@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0836", "email" : "sagar.gopale@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS0476", "email" : "sagar.hundekari@justo.co.in", "city": "Pune"},
                    {"badge": "M0628", "email" : "sagar.mahale@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0421", "email" : "sagar.malhotra@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0501", "email" : "sagar.panchal@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS1330", "email" : "sagar.waichole@justo.co.in", "city": "Pune"},
                    {"badge": "JUS1028", "email" : "sagarika.das@justo.co.in", "city": "Pune"},
                    {"badge": "P0223", "email" : "sagnik.guha@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0512", "email" : "sahil.upadhyay@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0380", "email" : "sainath.pise@justo.co.in", "city": "Pune"},
                    {"badge": "M0575", "email" : "sajeev.nair@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0781", "email" : "sajid.shaikh@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS0485", "email" : "sakar.diwase@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0568", "email" : "saket.atkare@justo.co.in", "city": "Pune"},
                    {"badge": "P0559", "email" : "sakshi.gogawale@justo.co.in", "city": "Pune"},
                    {"badge": "M0813", "email" : "samad.shaikh@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0353", "email" : "samarth.agrawal@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0401", "email" : "samarth.bhandkar@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0732", "email" : "samidha.bhopi@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS615", "email" : "samina.mulla@justo.co.in", "city": "Pune"},
                    {"badge": "JUS0337", "email" : "samrat.sarkar@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0566", "email" : "samruddhi.patankar@justo.co.in", "city": "Pune"},
                    {"badge": "P0304", "email" : "samuel.pawar@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0747", "email" : "sandeep.gupta@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS0186", "email" : "sandeep.kulkarni@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0162", "email" : "sandeep.nayar@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS0625", "email" : "sandeep.kamat@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS0275", "email" : "sandesh.chavan@justo.co.in", "city": "Pune"},
                    {"badge": "P0350", "email" : "sandip.nande@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0611", "email" : "sangeeta.savardekar@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0509", "email" : "sangeetha.nambiar@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0333", "email" : "sangram.rout@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS597", "email" : "sanjay.chanda@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0711", "email" : "sanjay.tandalekar@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS0689", "email" : "sanjeev.thadani@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0489", "email" : "sanket.dighe@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0392", "email" : "sanket.bhagwat@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0425", "email" : "sanket.sanas@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS1029", "email" : "santlal.kannojia@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0782", "email" : "santosh.mishra@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS1030", "email" : "santosh.kadam@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0848", "email" : "santoshi.choudhary@justo.co.in", "city": "Thane"},
                    {"badge": "M0526", "email" : "saqlain.rakhe@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0631", "email" : "sarita.chandwadkar@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0777", "email" : "sarwan.sharma@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS0742", "email" : "satej.lokhande@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0821", "email" : "satish.kahar@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0810", "email" : "satish.malviya@justo.co.in", "city": "Mumbai"},
                    {"badge": "CON012", "email" : "satyamap@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS622", "email" : "satyajeet.nikam@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0487", "email" : "saud.shaikh@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0250", "email" : "", "city": "Mumbai"},
                    {"badge": "JUS1426", "email" : "saurabh.pandey@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0786", "email" : "savio.rego@justo.co.in", "city": "Thane"},
                    {"badge": "P0487", "email" : "sayali.pawar@justo.co.in", "city": "Sangli"},
                    {"badge": "JUS598", "email" : "sayan.chakraborty@justo.co.in", "city": "Pune"},
                    {"badge": "M0668", "email" : "seema.bhoir@justo.co.in", "city": "Thane"},
                    {"badge": "CON011", "email" : "seff.khomosi@justo.co.in", "city": "MUMBAI"},
                    {"badge": "M0621", "email" : "shabaz.khan@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS0901", "email" : "shahbaaz.khan@justo.co.in", "city": "Thane"},
                    {"badge": "M0548", "email" : "shahrukh.shaikh@justo.co.in", "city": "Mumbai"},
                    {"badge": "B0006", "email" : "shaikh.abdur@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0753", "email" : "shailendra.singh@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0164", "email" : "shailesh.jayswal@justo.co.in", "city": "Mumbai"},
                    {"badge": "CON010", "email" : "shailesh.karnik@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0491", "email" : "shailesh.sawkare@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0413", "email" : "", "city": "Mumbai"},
                    {"badge": "P0331", "email" : "shantanu.jain@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS1355", "email" : "sharad.pawar@justo.co.in", "city": "Pune"},
                    {"badge": "M0551", "email" : "sharfuddin.rehmani@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0826", "email" : "shashikant.mishra@justo.co.in", "city": "Thane"},
                    {"badge": "JUS0914", "email" : "shayad.sayyad@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0770", "email" : "Shehzad.khan@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0795", "email" : "shekhar.kulkarni@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS0213", "email" : "shivali.shinde@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS1199", "email" : "shivam.balap@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS627", "email" : "shivam.gupta@justo.co.in", "city": "Pune"},
                    {"badge": "M0679", "email" : "shivani.pandit@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0323", "email" : "shivcharan.rathod@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS632", "email" : "shobangi.suryavamshi@justo.co.in", "city": "Pune"},
                    {"badge": "JUS611", "email" : "Shreemant.suryawanshi@justo.co.in", "city": "Thane"},
                    {"badge": "P0531", "email" : "shreeraj.margale@justo.co.in", "city": "Pune"},
                    {"badge": "M0411", "email" : "shreya.jain@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS669", "email" : "shreyash.bangale@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0342", "email" : "shrija.patil@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0555", "email" : "shrikant.shinde@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS0178", "email" : "shrinivas.ugile@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS0260", "email" : "shriraj.patil@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0517", "email" : "shrishailya.deshpande@justo.co.in", "city": "Pune"},
                    {"badge": "P0532", "email" : "shruti.dekate@justo.co.in", "city": "Pune"},
                    {"badge": "P0465", "email" : "shruti.kodelwar@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0434", "email" : "shrutika.gaikwad@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0520", "email" : "shubham.nichal@justo.co.in", "city": "Pune"},
                    {"badge": "JUS658", "email" : "shubhamsuresh.patil@justo.co.in", "city": "Pune"},
                    {"badge": "P0580", "email" : "shubham.mali@justo.co.in", "city": "Pune"},
                    {"badge": "P0470", "email" : "shubham.doifode@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0519", "email" : "shubham.gupta@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0344", "email" : "shubham.jadhav@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS643", "email" : "Shubham.keservani@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0397", "email" : "shubham.sharma@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0317", "email" : "shubham.singh@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS633", "email" : "shubham.rawalkar@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS640", "email" : "shubham.patil@justo.co.in", "city": "Pune"},
                    {"badge": "P0387", "email" : "shubhanshu.gupta@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS1488", "email" : "shweta.bhardwaj@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS697", "email" : "Shweta.shinde@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0533", "email" : "shweta.garade@justo.co.in", "city": "Pune"},
                    {"badge": "JUS1212", "email" : "shweta.gawali@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS1370", "email" : "shweta.kamble@justo.co.in", "city": "mumbai"},
                    {"badge": "M0577", "email" : "shyam.bhagat@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0485", "email" : "siddhant.gaikwad@justo.co.in", "city": "Thane"},
                    {"badge": "M0775", "email" : "siddharth.visa@justo.co.in", "city": "Thane"},
                    {"badge": "P0570", "email" : "siddhesh.sakpal@justo.co.in", "city": "Pune"},
                    {"badge": "M0561", "email" : "siddhesh.shelar@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0587", "email" : "Siddheshwar.koli@justo.co.in", "city": "Solapur"},
                    {"badge": "M0717", "email" : "simar.dhir@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0296", "email" : "simran.chhangani@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0658", "email" : "simran.karara@justo.co.in", "city": "Mumbai"},
                    {"badge": "B0016", "email" : "simran.kaushal@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS0828", "email" : "simran.pange@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0788", "email" : "simranjit.singh@justo.co.in", "city": "Thane"},
                    {"badge": "P0562", "email" : "smita.singh@justo.co.in", "city": "Pune"},
                    {"badge": "JUS674", "email" : "smita.kudale@justo.co.in", "city": "Pune"},
                    {"badge": "P0427", "email" : "sneha.zine@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0754", "email" : "snehal.gaikwad@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0601", "email" : "snehal.waghule@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0688", "email" : "sohan.sawariya@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0422", "email" : "somesh.naikwade@justo.co.in", "city": "Pune"},
                    {"badge": "P0491", "email" : "jyoti.sutar@justo.co.in", "city": "Pune"},
                    {"badge": "JUS1264", "email" : "sonal.patil@justo.co.in", "city": "Pune"},
                    {"badge": "M0686", "email" : "sonal.panchal@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS0441", "email" : "sonam.thakur@justo.co.in", "city": "Pune"},
                    {"badge": "M0669", "email" : "soni.veduvar@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0606", "email" : "sonu.chabra@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0446", "email" : "sourabh.nevase@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS0249", "email" : "sourabh.ubale@justo.co.in", "city": "Mumbai"},
                    {"badge": "B0025", "email" : "srihar.rathor@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0735", "email" : "steffi.khose@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0761", "email" : "stuti.agarwal@justo.co.in", "city": "mumbai"},
                    {"badge": "P0184", "email" : "subhajeet.sinha@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0364", "email" : "subhendu.das@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS0866", "email" : "subhransu.sahoo@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0095", "email" : "subodh.adhari@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0263", "email" : "sudip.ghosh@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0414", "email" : "sujit.phatak@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0701", "email" : "", "city": ""},
                    {"badge": "P0577", "email" : "sumant.khandekar@justo.co.in", "city": "Pune"},
                    {"badge": "JUS0554", "email" : "sumit.dholey@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0109", "email" : "sumit.kumar@justo.co.in", "city": ""},
                    {"badge": "JUS0104", "email" : "sunil.naik@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0328", "email" : "sunil.nikam@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0625", "email" : "sunil.sapkal@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0602", "email" : "sunny.gerela@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS0238", "email" : "sunny.john@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0393", "email" : "", "city": "Mumbai"},
                    {"badge": "M0823", "email" : "supraja.katkam@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0500", "email" : "supriya.richhariya@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS1060", "email" : "suraj.bavkar@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0576", "email" : "suraj.jirage@justo.co.in", "city": "Pune"},
                    {"badge": "M0557", "email" : "suraj.pal@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0330", "email" : "suraj.sonkamble@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0178", "email" : "suraj.sujathan@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS618", "email" : "surajnath.upadhyay@justo.co.in", "city": "Mumbai "},
                    {"badge": "P0448", "email" : "surbhi.jagnani@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS603", "email" : "surya.rastogi@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS614", "email" : "sushil.mandge@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS1231", "email" : "susmita.chavan@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0390", "email" : "suyog.patil@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0619", "email" : "suyog.pawar@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0544", "email" : "sapna.sharma@justo.co.in", "city": "Pune"},
                    {"badge": "P0246", "email" : "swapnil.adhav@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS0311", "email" : "swapnil.bhalekar@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS0813", "email" : "swapnil.neman@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0354", "email" : "Swapnil.Rajguru@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS1067", "email" : "swapnil.sahani@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0620", "email" : "swapnil.sathe@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0484", "email" : "swati.fofaliya@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS1205", "email" : "sweta.kumari@justo.co.in", "city": "Mumbai"},
                    {"badge": "B0023", "email" : "swetankita.patra@justo.co.in", "city": "Mumbai"},
                    {"badge": "E001", "email" : "admin@workrig.com", "city": "Pune"},
                    {"badge": "P0447", "email" : "taniya.ahuja@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0637", "email" : "", "city": "Mumbai"},
                    {"badge": "JUS0548", "email" : "tanveer.pathan@justo.co.in", "city": "Pune"},
                    {"badge": "M0798", "email" : "tanvi.karande@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0311", "email" : "tanvi.lad@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0822", "email" : "tariq.mujib@justo.co.in", "city": "Thane"},
                    {"badge": "M0092", "email" : "tejal.hadawale@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0561", "email" : "tejas.giri@justo.co.in", "city": "Pune"},
                    {"badge": "M0791", "email" : "tejas.jadhav@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS0105", "email" : "tejashree.mhetre@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0244", "email" : "terrance.xavier@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0463", "email" : "tincy.chacko@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0615", "email" : "treeza.vaughan@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS0713", "email" : "tushar.bhadane@justo.co.in", "city": "Thane"},
                    {"badge": "JUS1034", "email" : "tushargiridhar.bhosale@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS0759", "email" : "tushar.bhosale@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS0461", "email" : "tushar.kore@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0568", "email" : "udit.sharma@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS696", "email" : "umang.joshi@justo.co.in", "city": "Pune"},
                    {"badge": "M0704", "email" : "umesh.shinde@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS604", "email" : "umesh.bhat@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS1516", "email" : "unnati.bhanushali@justo.co.in", "city": "Mumbai "},
                    {"badge": "P0449", "email" : "utkarsh.kale@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS688", "email" : "vishesh.sharma@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0385", "email" : "vaibhav.patil@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0678", "email" : "vaishali.mohite@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0596", "email" : "vaishali.naikar@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0653", "email" : "vaishali.shinde@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0210", "email" : "vaishnavi.gundawar@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0437", "email" : "vaishnavi.thete@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS634", "email" : "vaishnavi.kapale@justo.co.in", "city": "Nashik"},
                    {"badge": "P0563", "email" : "vandana.singh@justo.co.in", "city": "Pune"},
                    {"badge": "P0337", "email" : "varsha.punde@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0440", "email" : "veena.mhatre@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0406", "email" : "vidhi.malhotra@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0313", "email" : "vidyanand.rao@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS659", "email" : "vijay.vaidya@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS1304", "email" : "Vijay.mallishe@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0744", "email" : "vikas.ingole@justo.co.in", "city": "Thane"},
                    {"badge": "M0736", "email" : "", "city": "Mumbai"},
                    {"badge": "M0797", "email" : "vikas.shukla@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0656", "email" : "", "city": "Mumbai"},
                    {"badge": "JUS605", "email" : "vikram.mishra@justo.co.in", "city": "Mumbai "},
                    {"badge": "M0655", "email" : "vikram.salvekar@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0258", "email" : "vinayak.pillay@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0661", "email" : "vindhyachal.rastogi@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0726", "email" : "vinit.pawar@justo.co.in", "city": "Mumbai"},
                    {"badge": "JC0002", "email" : "vinod.agate@gmail.com", "city": "Mumbai"},
                    {"badge": "P0351", "email" : "", "city": "Mumbai"},
                    {"badge": "JC008", "email" : "Vipul.ovhal@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0604", "email" : "virendra.jaiswal@justo.co.in", "city": "Thane"},
                    {"badge": "M0383", "email" : "vishal.garud@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0368", "email" : "vishal.kawane@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0458", "email" : "vishal.khutwad@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0481", "email" : "", "city": "Pune"},
                    {"badge": "JUS0661", "email" : "vishal.thigale@justo.co.in", "city": "Pune"},
                    {"badge": "P0466", "email" : "vishweshwar.gadave@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS670", "email" : "vivek.yerande@justo.co.in", "city": "Pune"},
                    {"badge": "P0431", "email" : "vivek.k@justo.co.in", "city": "Pune"},
                    {"badge": "P0398", "email" : "vrashali.deshpande@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS623", "email" : "vrundavan.wagh@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS0738", "email" : "vyaprosh.kale@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0834", "email" : "wasim.patel@justo.co.in", "city": "Thane"},
                    {"badge": "JUS1080", "email" : "yakub.pathan@justo.co.in", "city": "Pune"},
                    {"badge": "M0610", "email" : "yash.jain@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0426", "email" : "yash.kajve@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0714", "email" : "yash.dubey@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS1053", "email" : "yashpal.singh@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0779", "email" : "yashraj.vyas@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS1458", "email" : "yasin.shaikh@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS654", "email" : "Yasmin.Chowdhury@justo.co.in", "city": "Mumbai "},
                    {"badge": "P0442", "email" : "yavi.bisen@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0336", "email" : "yogesh.damugade@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0696", "email" : "yogesh.duggal@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0495", "email" : "yogesh.somvanshi@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS671", "email" : "yogita.dalvi@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS0478", "email" : "yogita.karekar@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0593", "email" : "yusuf.khan@justo.co.in", "city": "Mumbai"},
                    {"badge": "M0752", "email" : "zeeshan.siddiqui@justo.co.in", "city": "Mumbai"},
                    {"badge": "P0585", "email" : "zubaid.shaikh@justo.co.in", "city": "Pune"},
                    {"badge": "M0809", "email" : "zulekha.shaikh@justo.co.in", "city": "Thane"},
                    {"badge": "JUS612", "email" : "komal.chandanshive@justo.co.in", "city": "Mumbai"},
                    {"badge": "JUS617", "email" : "manoj.chavan@justo.co.in", "city": "mumbai"},
                    {"badge": "M839", "email" : "pravin.kedar@justo.co.in", "city": "Mumbai"},
                    {"badge": "JC9", "email" : "sonali.das@justo.co.in", "city": "Mumbai"}]
            success = []
            failed = []
            for item in data:
                employee = request.env['hr.employee'].search([('barcode', '=', item['badge'])], limit=1)
                if employee:
                    request.env.cr.execute(f"update hr_employee set city = '{item['city']}' where id = {employee.id}")
                    if item['email']:
                        try:
                            request.env.cr.execute(f"update hr_employee set corporate_email = '{item['email']}' where id = {employee.id}")
                            success.append(employee.barcode)
                        except:
                            failed.append(employee.barcode)
            return 'Success : ' + str(success) + '  --- Failed : ' + str(failed)
        else:
            return 'Access Denied'