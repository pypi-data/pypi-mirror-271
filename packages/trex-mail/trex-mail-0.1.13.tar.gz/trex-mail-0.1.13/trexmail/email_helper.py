'''
Created on 15 Jul 2022

@author: jacklok
'''
from trexlib.utils.google.cloud_tasks_util import create_task 
import logging, re
from trexmail.flask_mail import send_email
from flask import current_app
from trexconf.conf import SEND_EMAIL_TASK_URL 
from trexconf.conf import DEPLOYMENT_MODE, LOCAL_MODE, SYSTEM_TASK_SERVICE_CREDENTIAL_PATH, SYSTEM_TASK_GCLOUD_PROJECT_ID, SYSTEM_TASK_GCLOUD_LOCATION, SYSTEM_TASK_SERVICE_ACCOUNT_EMAIL 
from trexmail.conf import DEFAULT_SENDER

logger = logging.getLogger('helper')
#logger = logging.getLogger('debug')

def trigger_send_email(sender_address=DEFAULT_SENDER, recipient_address=None, subject=None, message=None, cc_address=None):
    
    logger.debug('sender_address=%s', sender_address)
    logger.debug('recipient_address=%s', recipient_address)
    logger.debug('DEPLOYMENT_MODE=%s', DEPLOYMENT_MODE)
    
    if DEPLOYMENT_MODE == LOCAL_MODE:
    #if False:
        logger.debug('send email directly')
        
        send_email(
                   sender       = sender_address, 
                   to_address   = [recipient_address], 
                   subject      = subject, 
                   body         = message,
                   app          = current_app
                   )
    
    else:
        logger.debug('send email to task queue')
        queue_name      = 'send-email' 
        payload         = {
                                'sender_address'    : sender_address,
                                'recipient_address' : recipient_address,
                                'subject'           : subject,
                                'message'           : message,
                                'cc_address'        : cc_address,
                            }
        logger.info('payload=%s', payload)
        logger.info('SEND_EMAIL_TASK_URL=%s', SEND_EMAIL_TASK_URL)
                        
        create_task(SEND_EMAIL_TASK_URL, queue_name, payload=payload, 
                        in_seconds      = 1, 
                        http_method     = 'POST',
                        credential_path = SYSTEM_TASK_SERVICE_CREDENTIAL_PATH, 
                        project_id      = SYSTEM_TASK_GCLOUD_PROJECT_ID,
                        location        = SYSTEM_TASK_GCLOUD_LOCATION,
                        service_email   = SYSTEM_TASK_SERVICE_ACCOUNT_EMAIL
                        )
     
    return True

def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None
