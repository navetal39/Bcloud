# INFO: #
# ===================================

# Constants: #
## Pahts: ##
### Error paths: ###
ERROR_404_PATH = "Pages/Error404.htm"
ERROR_405_PATH = "Pages/Error405.htm"
ERROR_500_PATH = "Pages/Error500.htm"
NO_NAME_ERROR_PATH = "Pages/ErrorNoName.htm"
EMPTY_FOLDER_ERROR_PATH = "Pages/ErrorEmptyFolder.htm"
NAME_IN_USE_ERROR_PATH = "Pages/ErrorNameInUse.htm"
### General paths: ###
LAST_UPDATE_PLUS_PATH = "Pages/LastUpdatePlus.htm"
HE_GAVE_UP_PATH = "Pages/HeGaveUp.htm" #Useless
HE_SAID_YES_PATH = "Pages/ThanksFor.htm" #Useless
SIGN_UP_APPROVAL_PATH = "Pages/SignUpApproval.htm"

## Server-Server Communication: ##
from COM import MAIN_SERVER_PORT, MAIN_SERVER_IP


# Imports: #
import socket
from Main_Server_Com import Server
from os.path import isfile


def get_server_for_thread():
    return Server(MAIN_SERVER_IP, MAIN_SERVER_PORT)
    
def get_fields_values(cont):
    '''
    '''
    fields_values = dict()
    fields = cont.split('&')
    for field in fields:
        name, value = field.split('=')
        fields_values[name] = value

    return fields_values

def path_exists(path):
    ''' For conventions, :P.
    '''
    return isfile(path)

def download_or_register(main_server, params):
    folder_flag = False; last_update = None
    try:
        params_dict = get_fields_values(params)
    except:
        raise
    
    if len(params_dict.keys()) == 1 and "username" in params_dict.keys(): # Download - first part.
        name = params_dict["username"]
        stat, data = main_server.get_last_update(name, 'public')
        if stat == "NNM":
            path = NO_NAME_ERROR_PATH
            status = "200"
        elif stat == "EMP":
            path = EMPTY_FOLDER_ERROR_PATH
            status = "200"
        elif stat == "SCS":
            path = LAST_UPDATE_PLUS_PATH # Add last update...!
            status = "200"
            last_update = data
        else:
            raise
        
    elif len(params_dict.keys()) == 2 and "username" in params_dict.keys() and "is_approved" in params_dict.keys() : # Download - second part.
        value = params_dict["is_approved"]
        if value == "YES":
            path = HE_SAID_YES_PATH; status = "200" # Just in case
            folder_flag = True
        elif value == "NO":
            path = HE_GAVE_UP_PATH; status = "200"  # Just in case
        else: # If the user decides to try to be funny and put something else in the url rather than "YES/NO" thinking that he may crash our server by doing so...
            status = "404"
            path = ERROR_404_PATH

    elif len(params_dict.keys()) == 2 and "username" in params_dict.keys() and "password" in params_dict.keys() : # Sign Up
        status, path = register(main_server, params_dict)
        


    else: # Same shit again... If the user decides to try to be funny and put something else in the url rather than "username/is_approved" thinking that he may crash our server by doing so...
        status = "404"
        path = ERROR_404_PATH
        
    return status, path, folder_flag, params_dict["username"], last_update

def register(main_server, fields_dict):
    #form_content = parsed_request[2]
    #fields_dict = get_fields_values(form_content)
    stat = main_server.create_user(fields_dict['username'],  fields_dict['password'])
    if stat == "NIU": #deal with JS
        path = NAME_IN_USE_ERROR_PATH
        status = "200"
    elif stat == "SCS":
        path = SIGN_UP_APPROVAL_PATH
        status = "200"
    else:
        raise
    return status, path

def get_folder(main_server, name):
    return main_server.get_folder(name)


'''
Exciting. Satisfying. Period.
.
'''
