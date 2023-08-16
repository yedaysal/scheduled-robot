### SMTP SPESIFIC VARIABLES ### 

# Put "smtp server address" here
smtp_server = "smtp.mail.yahoo.com"

# Put "smtp server port" here
smtp_server_port = 587

# Put "smtp server login username" here                                        
smtp_login_username = "someuser@yahoo.com"                           

# Put "smtp server login password" here
smtp_login_password = "somepassword"                             

### TEST AUTOMATION SPESIFIC VARIABLES ###

# Put "OPCO name" here
opco = "Uganda"                                        

api_dir = "/root/mtn-" + opco.lower() + "-test-automation/api/"
ussd_dir = "/root/mtn-" + opco.lower() + "-test-automation/ussd/"

# Put robot commands here
# robot_cmd =  "rm -f " + api_dir + "reports/*; cd " + api_dir + "; robot --loglevel debug -T  -o " + opco + "-output -l " + opco + "-log -r " + opco + "-report -d reports --skiponfailure noncritical -t \"CO Login Request - Agent\" ApiTestAutomationSuite/ ; chmod 777 -R reports/"
api_robot_cmd = "chmod 777 " + api_dir + "Resources/* ;" + "cd " + api_dir + "Resources" + "; robot --loglevel debug -T  -o MTN-" + opco + "-API-Test-output -l MTN-" + opco + "-API-Test-log -r MTN-" + opco + "-API-Test-report -d reports --skiponfailure noncritical ../ApiTestAutomationSuite/ ; chmod 777 -R reports/"
ussd_robot_cmd =  "chmod 777 " + ussd_dir + "Resources/* ;" + "cd " + ussd_dir + "Resources" + "; robot --loglevel debug -T  -o MTN-" + opco + "-USSD-Test-output -l MTN-" + opco + "-USSD-Test-log -r MTN-" + opco + "-USSD-Test-report -d reports --skiponfailure noncritical ../Tests/ ; chmod 777 -R reports/"

### MAIL SPESIFIC VARIABLES ###

# Put "email subject" here
mail_subject = "MTN " + opco + " Test Automation Report"         

# Put "email body" here
mail_text = "MTN " + opco + " Test Automation Execution Statistics"      

# Put "sender email address" here
mail_from = "someuser@yahoo.com"            

# Put "recipient addresses" here
mail_to = ["someuser1@yahoo.com", "someuser2@yahoo.com", "someuser3@yahoo.com"]
