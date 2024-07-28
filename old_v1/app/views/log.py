from flask import current_app as app
from flask import request
from datetime import datetime

cLoggedEndpoints       = ['endpoint_games', 'endpoint_detailed_stats', 'user_stats', 
                          'endpoint_batter_position', 'request_password_change', 'key']
cLoggedEndpointsNoArgs = ['register', 'change_password', 'login', 'verify_email']

# @app.after_request
# def after_request_func(response):    
#     now = datetime.now()
#     # dd/mm/YY H:M:S
#     dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    
#     #If HTTP request was not successful for any reason log a warning
#     try:
#         if (response.status_code >= 300):
#             app.logger.warning(f'WARNING Datetime: {dt_string}  Endpoint: {request.endpoint:15}  RC: {response.status:15}  IP: {request.remote_addr:13}')
#         elif (request.endpoint in cLoggedEndpoints):
#             app.logger.info(f'INFO    Datetime: {dt_string}  Endpoint: {request.endpoint:15}  RC: {response.status:15}  IP: {request.remote_addr:13}  Args: {request.args} ')
#         elif (request.endpoint in cLoggedEndpointsNoArgs):
#             app.logger.info(f' INFO    Datetime: {dt_string}  Endpoint: {request.endpoint:15}  RC: {response.status:15}  IP: {request.remote_addr:13} ')
#         return response
#     except:
#         app.logger.error(f' ERROR  Datetime: {dt_string}  Endpoint: {request.endpoint:15}')