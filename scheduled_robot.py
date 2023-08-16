from cProfile import runMIMEApplication
import schedule, time, smtplib, os, subprocess, config
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import xml.etree.cElementTree as et
import pandas as pd
from datetime import datetime


# Function to send mail
def mail():
    
    header = {'selector': 'th', 'props':
        [('background-color', '#87CEFA'), ('color', 'black'), ('text-align', 'center'), ('vertical-align', 'centre'),
         ('font-weight', 'bold')]}
    properties = {"border": "2px solid gray", "font-size": "16px"}

    BA = ['CHANGEME', 'CHANGEME']
    SI = ['CHANGEME', 'CHANGEME']

    project_team_members = pd.DataFrame(
        {'BA': BA, 'SI': SI})
    project_team_members_html = project_team_members.T.style.set_table_styles([header]) \
        .set_properties(**properties).hide(axis="columns").to_html()

    subscriber_profile = ['CHANGEME', 'CHANGEME', 'CHANGEME']
    agent_profile = ['CHANGEME', 'CHANGEME', 'CHANGEME']
    merchant_profile = ['CHANGEME', 'CHANGEME', 'CHANGEME']

    test_msisdn = pd.DataFrame(
        {'Subscriber Profile': subscriber_profile, 'Agent Profile': agent_profile,
         'Merchant Profile': merchant_profile})
    test_msisdn_html = test_msisdn.style.set_table_styles([header]).set_properties(**properties).hide(axis="index").to_html()

    # Create an array with the paths of api report files
    api_report_file_paths = api_robot()
    print(api_report_file_paths)

    # Create a dataframe with api test case names and their status
    output_xml = ""
    for i in range(len(api_report_file_paths)):
        if (api_report_file_paths[i].__contains__("xml")):
            output_xml = api_report_file_paths[i]
    tree = et.parse(output_xml)
    root = tree.getroot()
    test_name = []
    status = []
    for reg in root.iter('test'):
        root1 = et.Element('root')
        root1 = reg
        test_name.append(reg.attrib['name'])
        status.append(root1[-1].attrib['status'])
    api_df = pd.DataFrame({'Test Name': test_name, 'Status': status})

    def color_passed(value):
        if value == 'FAIL':
            color = 'red'
        elif value == 'PASS':
            color = 'green'
        else:
            return
        return f'color: {color}'

    api_execution_summary_html = api_df.style.applymap(color_passed, subset=['Status']) \
        .set_properties(**properties) \
        .set_table_styles([header]).to_html()

    # Create an html code with api test execution statistics to embed into the mail
    tree = et.parse(output_xml)
    root = tree.getroot()
    total_api = 0
    failed_api = 0
    skipped_api = 0
    passed_api = 0
    for reg in root.iter('statistics'):
        root1 = et.Element('root')
        root1 = reg
        failed_api = str(root1[0][0].attrib['fail'])
        skipped_api = str(root1[0][0].attrib['skip'])
        passed_api = str(root1[0][0].attrib['pass'])
        total_api = str(int(failed_api) + int(skipped_api) + int(passed_api))

    value1 = root[0][1].attrib['starttime']
    value2 = root[0][1].attrib['endtime']
    value3 = datetime.strptime(value1[9:], "%H:%M:%S.%f")
    value4 = datetime.strptime(value2[9:], "%H:%M:%S.%f")
    execution_time_api = value4 - value3
    execution_time_api = str(execution_time_api)[:7]

    # Create an array with the paths of ussd report files
    ussd_report_file_paths = ussd_robot()
    print(ussd_report_file_paths)

    # Create a dataframe with ussd test case names and their status
    output_xml = ""
    for i in range(len(ussd_report_file_paths)):
        if (ussd_report_file_paths[i].__contains__("xml")):
            output_xml = ussd_report_file_paths[i]
    tree = et.parse(output_xml)
    root = tree.getroot()
    test_name = []
    status = []
    for reg in root.iter('test'):
        root1 = et.Element('root')
        root1 = reg
        test_name.append(reg.attrib['name'])
        status.append(root1[-1].attrib['status'])
    ussd_df = pd.DataFrame({'Test Name': test_name, 'Status': status})

    ussd_execution_summary_html = ussd_df.style.applymap(color_passed, subset=['Status']) \
        .set_properties(**properties) \
        .set_table_styles([header]).to_html()

    # Create an html code with ussd test execution statistics to embed into the mail
    tree = et.parse(output_xml)
    root = tree.getroot()
    total_ussd = 0
    failed_ussd = 0
    skipped_ussd = 0
    passed_ussd = 0
    for reg in root.iter('statistics'):
        root1 = et.Element('root')
        root1 = reg
        failed_ussd = str(root1[0][0].attrib['fail'])
        skipped_ussd = str(root1[0][0].attrib['skip'])
        passed_ussd = str(root1[0][0].attrib['pass'])
        total_ussd = str(int(failed_ussd) + int(skipped_ussd) + int(passed_ussd))

    value1 = root[0][1].attrib['starttime']
    value2 = root[0][1].attrib['endtime']
    value3 = datetime.strptime(value1[9:], "%H:%M:%S.%f")
    value4 = datetime.strptime(value2[9:], "%H:%M:%S.%f")
    execution_time_ussd = value4 - value3
    execution_time_ussd = str(execution_time_ussd)[:7]

    channel = ['API', 'USSD']
    failed = [failed_api, failed_ussd]
    skipped = [skipped_api, skipped_ussd]
    passed = [passed_api, passed_ussd]
    total = [total_api, total_ussd]
    execution_time_list = [execution_time_api, execution_time_ussd]

    execution_stat = pd.DataFrame(
        {'Channel': channel, 'Failed': failed, 'Skipped': skipped, 'Passed': passed, 'Total': total, 'Execution Time': execution_time_list})

    def highlight_cols(s):
        color = 'indianred'
        return 'background-color: %s' % color

    def highlight_cols_2(s):
        color = 'palegreen'
        return 'background-color: %s' % color

    execution_stat_html = execution_stat.style.applymap(highlight_cols, subset=pd.IndexSlice[:, ['Failed']]) \
        .applymap(highlight_cols_2, subset=pd.IndexSlice[:, ['Passed']]) \
        .set_table_styles([header]) \
        .set_properties(**properties).hide(axis="index").to_html()

    all_report_file_paths = api_report_file_paths + ussd_report_file_paths
    execution_result_html = "<br> <strong>Project Team</strong> <br> " + project_team_members_html \
                            + "<br> <br>" + test_msisdn_html + "<br> <br>" \
                            + execution_stat_html + "<br> <br>" \
                            + "<br> <strong>API Test Summary</strong> <br> " + api_execution_summary_html \
                            + "<br> <strong>USSD Test Summary</strong> <br>" + ussd_execution_summary_html

    # Initialize connection to email server
    smtp = smtplib.SMTP(config.smtp_server, config.smtp_server_port)
    smtp.ehlo()
    smtp.starttls()

    # Login with email and password
    # if smtp.login(config.smtp_login_username, config.smtp_login_password):
    # print("SMTP LOGIN SUCCESSFUL")
    # os.system('echo "`date` --> SMTP LOGIN SUCCESSFUL" > output')
    # else:
    # os.system('echo "`date` --> SMTP LOGIN FAILED" > output')

    # Call the message function
    msg = message(config.mail_subject, execution_result_html, all_report_file_paths)

    # # Provide some data to the sendmail function
    # if smtp.sendmail(from_addr=config.mail_from, to_addrs=config.mail_to, msg=msg.as_string()):
    #     # print("MAIL SENT SUCCESSFULLY")
    #     subprocess.call('echo "`date` --> MAIL SENT SUCCESSFULLY" >> /root/scheduled_robot.log', shell=True)
    # else:
    #     subprocess.call('echo "`date` --> MAIL SENT FAILED" >> /root/scheduled_robot.log', shell=True)

    # Call the sendmail function and assign its output to a variable
    sendmail_result = smtp.sendmail(from_addr=config.mail_from, to_addrs=config.mail_to, msg=msg.as_string())

    # Check if the mail sent successfully
    if len(sendmail_result) == 0:
        subprocess.call('echo "`date` --> MAIL SENT SUCCESSFULLY" >> /root/scheduled_robot.log', shell=True)
    else:
        subprocess.call('echo "`date` --> MAIL SENT FAILED" >> /root/scheduled_robot.log', shell=True)

    # Close the smtp connection
    if smtp.quit():
        subprocess.call('echo "`date` --> SMTP CONNECTION CLOSED SUCCESSFULLY" >> /root/scheduled_robot.log',
                        shell=True)
    else:
        subprocess.call('echo "`date` --> SMTP CONNECTION CLOSE FAILED" >> /root/scheduled_robot.log', shell=True)

def message(subject, text, attachment=None):
    # build message contents
    msg = MIMEMultipart()

    # Add Subject
    msg['Subject'] = subject

    # Add text contents
    msg.attach(MIMEText(text, 'html'))

    # Check if we have anything
    # given in the attachment parameter
    if attachment is not None:

        # Check whether we have the
        # lists of attachments or not!
        if type(attachment) is not list:
            # if it isn't a list, make it one
            attachment = [attachment]

        for one_attachment in attachment:
            with open(one_attachment, 'rb') as f:
                # Read in the attachment using MIMEApplication
                file = MIMEApplication(
                    f.read(),
                    name=os.path.basename(one_attachment)
                )
            file['Content-Disposition'] = f'attachment;\
            filename="{os.path.basename(one_attachment)}"'

            # At last, Add the attachment to our message object
            msg.attach(file)
    return msg

# Function to run api robot command
def api_robot():

    api_cmd_output = subprocess.check_output(config.api_robot_cmd, shell=True).decode("utf-8").split("\n")
    api_report_path = api_cmd_output[-2].split(" ")
    api_log_path = api_cmd_output[-3].split(" ")
    api_output_path = api_cmd_output[-4].split(" ")
    api_report_file_paths = [api_report_path[-1], api_log_path[-1], api_output_path[-1]]
    return api_report_file_paths

# Function to run ussd robot command
def ussd_robot():

    ussd_cmd_output = subprocess.check_output(config.ussd_robot_cmd, shell=True).decode("utf-8").split("\n")
    ussd_report_path = ussd_cmd_output[-2].split(" ")
    ussd_log_path = ussd_cmd_output[-3].split(" ")
    ussd_output_path = ussd_cmd_output[-4].split(" ")
    ussd_report_file_paths = [ussd_report_path[-1], ussd_log_path[-1], ussd_output_path[-1]]
    return ussd_report_file_paths


# Every day at 12am or 00:00 time mail() is called.
schedule.every().day.at("20:40").do(mail)

# # Schedule the email to be sent every specified minutes
# schedule.every(config.test_execution_frequency + 12).minutes.do(mail)

# mail()

while True:
	schedule.run_pending()
	time.sleep(1)
