import os
from trexlib.utils.common.config_util import read_config


CREDENTIAL_CONFIG                                   = read_config('credential_config.txt')

SENDGRID_API_KEY                                    = CREDENTIAL_CONFIG.get('SENDGRID_API_KEY')


#MAILJET_API_KEY                                     = os.environ.get('MAILJET_API_KEY')
#MAILJET_SECRET_KEY                                  = os.environ.get('MAILJET_SECRET_KEY')

FLASK_MAIL_USERNAME                                 = CREDENTIAL_CONFIG.get('FLASK_MAIL_USERNAME')
FLASK_MAIL_PASSWORD                                 = CREDENTIAL_CONFIG.get('FLASK_MAIL_PASSWORD')
FLASK_MAIL_SERVER                                   = CREDENTIAL_CONFIG.get('FLASK_MAIL_SERVER')
FLASK_MAIL_SERVER_PORT                              = CREDENTIAL_CONFIG.get('FLASK_MAIL_SERVER_PORT')
FLASK_MAIL_USE_SSL                                  = CREDENTIAL_CONFIG.get('FLASK_MAIL_USE_SSL')

DEFAULT_SENDER                                      = os.environ.get('DEFAULT_SENDER')
DEFAULT_RECIPIENT_EMAIL                             = os.environ.get('DEFAULT_RECIPIENT_EMAIL')