# Configurations

import logging

pylapi_json_indent = 2

default_api_url = "https://app.example.com/api/1.0"
default_api_auth_header_name = "Authorization"
default_api_auth_type = "Bearer"
default_api_base_headers = {}

############################################################
#
# Controls
#

# In the order of decreasing amount of logging
log_levels = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL,
}
log_level = logging.ERROR
deep_log_level = logging.ERROR
