from engine_communicator import EngineCommunicator
import json


class EngineGlobalApi:
    def __init__(self, socket):
        self.engine_socket = socket

    # returns an array of doc objects. The doc object contains doc name, size, file time etc
    def get_doc_list(self):
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": -1, "method": "GetDocList", "params": []})
        response = self.engine_socket.send_call(self.engine_socket, msg)
        return json.loads(response)['result']['qDocList']

    # returns the os name (always windowsNT). Obsolete?
    def get_os_name(self):
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": -1, "method": "OSName", "params": []})
        response = self.engine_socket.send_call(self.engine_socket, msg)
        return json.loads(response)['result']['qReturn']

    # returns the app id. If desktop is used the app id is the same as the full path to qvf
    # if it's running against Enterprise, app id will be a guid
    def create_app(self, app_name):
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": -1, "method": "CreateApp", "params": [app_name]})
        response = json.loads(self.engine_socket.send_call(self.engine_socket, msg))
        if 'error' in response:
            error_msg = response["error"]["message"]
            code = response["error"]["code"]
            return "Error code - " + str(code) + ", Error Msg: " + error_msg
        else:
            return response['result']['qAppId']

    # DeleteApp Method Deletes an app from the Qlik Sense repository or from the file system. Qlik Sense Enterprise:
    # In addition to being removed from the repository, the app is removed from the directory as well:
    # <installation_directory>\Qlik\Sense\Apps The default installation directory is ProgramData. Qlik Sense Desktop:
    #  The app is deleted from the directory %userprofile%\Documents\Qlik\Sense\Apps. Parameters: qAppId.. Identifier
    #  of the app to delete. In Qlik Sense Enterprise, the identifier of the app is a GUID in the Qlik Sense
    # repository. In Qlik Sense Desktop, the identifier of the app is the name of the app, as defined in the apps
    # folder %userprofile%\Documents\Qlik\Sense\Apps. This parameter is mandatory.
    def delete_app(self, app_name):
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": -1, "method": "DeleteApp", "params": [app_name]})
        response = self.engine_socket.send_call(self.engine_socket, msg)
        return json.loads(response)['result']['qSuccess']

    # opens an app and returns an object with handle, generic id and type
    def open_doc(self, app_name, user_name='', password='', serial='', no_data=False):
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": -1, "method": "OpenDoc", "params": [app_name, user_name,
                                                                                                   password, serial,
                                                                                                   no_data]})
        response = self.engine_socket.send_call(self.engine_socket, msg)
        if "error" in response:
            error_msg = json.loads(response)["error"]["message"]
            code = json.loads(response)["error"]["code"]
            return "Error code: " + str(code) + ", Error Msg: " + error_msg
        else:
            return json.loads(response)['result']["qReturn"]

    # returns an object with handle, generic id and type for the active app
    def get_active_doc(self):
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": -1, "method": "GetActiveDoc", "params": []})
        response = self.engine_socket.send_call(self.engine_socket, msg)
        return json.loads(response)['result']['qReturn']

    @staticmethod
    def get_handle(obj):
        return obj["qHandle"]

    # Abort All commands
    def abort_all(self):
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": -1, "method": "AbortAll", "params": []})
        response = self.engine_socket.send_call(self.engine_socket, msg)
        response_json = json.loads(response)
        if 'error' in response_json:
            error_msg = response_json.error.message
            code = ''
            return "Error code - " + code + ", Error Msg: " + error_msg
        else:
            return json.loads(response)['result']  # ['qReturn']

    # Abort Specific Request
    def abort_request(self, request_id):
        msg = json.dumps(
            {"jsonrpc": "2.0", "id": 0, "handle": -1, "method": "AbortRequest", "params": {"qRequestId": request_id}})
        response = self.engine_socket.send_call(self.engine_socket, msg)
        response_json = json.loads(response)
        if 'error' in response_json:
            error_msg = response_json.error.message
            code = ''
            return "Error code - " + code + ", Error Msg: " + error_msg
        else:
            return response_json['result']  # ['qReturn']

    # Configure Reload - This is done before doing a reload qCancelOnScriptError: If set to true, the script
    # execution is halted on error. Otherwise, the engine continues the script execution. This parameter is relevant
    # only if the variable ErrorMode is set to 1. qUseErrorData: If set to true, any script execution error is
    # returned in qErrorData by the GetProgress method. qInteractOnError: If set to true, the script execution is
    # halted on error and the engine is waiting for an interaction to be performed. If the result from the
    # interaction is 1 (qDef.qResult is 1), the engine continues the script execution otherwise the execution is
    # halted. This parameter is relevant only if the variable ErrorMode is set to 1 and the script is run in debug
    # mode (qDebug is set to true when calling the DoReload method).
    def configure_reload(self, cancel_on_error=False, use_error_data=True, interact_on_error=False):
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": -1, "method": "ConfigureReload",
                          "params": {"qCancelOnScriptError": cancel_on_error, "qUseErrorData": use_error_data,
                                     "qInteractOnError": interact_on_error}})
        response = self.engine_socket.send_call(self.engine_socket, msg)
        response_json = json.loads(response)
        if 'error' in response_json:
            error_msg = response_json['error']['message']
            code = str(response_json['error']['code'])
            return "Error code: " + code + ", Error Msg: " + error_msg
        else:
            return response_json['result']  # ['qReturn']

    # Copy app - This is done before doing a reload qTargetAppId (MANDATORY):  Identifier (GUID) of the app
    # entity in the Qlik Sense repository. The app entity must have been previously created by the repository (via
    # the REST API). qSrcAppId (MANDATORY): Identifier (GUID) of the source app in the Qlik Sense repository. Array
    # of QRS identifiers. The list of all the objects in the app to be copied must be given. This list must contain
    # the GUIDs of all these objects. If the list of the QRS identifiers is empty, the CopyApp method copies all
    # objects to the target app. Script-defined variables are automatically copied when copying an app. To be able to
    #  copy variables not created via script, the GUID of each variable must be provided in the list of QRS
    # identifiers. To get the QRS identifiers of the objects in an app, you can use the QRS API. The GET method (from
    #  the QRS API) returns the identifiers of the objects in the app. The following example returns the QRS
    # identifiers of all the objects in a specified app: GET /qrs/app/9c3f8634-6191-4a34-a114-a39102058d13 Where
    # 9c3f8634-6191-4a34-a114-a39102058d13 is the identifier of the app.

    # BUG - Does not work in September 2017 release
    def copy_app(self, target_app_id, src_app_id, qIds=[""]):
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": -1, "method": "CopyApp",
                          "params": {"qTargetAppId": target_app_id, "qSrcAppId": src_app_id, "qIds": qIds}})
        response = self.engine_socket.send_call(self.engine_socket, msg)
        response_json = json.loads(response)
        if 'error' in response_json:
            error_msg = response_json['error']['message']
            code = str(response_json['error']['code'])
            return "Error code - " + code + ", Error Msg: " + error_msg
        elif response_json['result']['qSuccess']:
            return "Success?: " + response_json['result'].qSuccess

    # Creates an empty session app. The following applies: The name of a session app cannot be chosen. The engine
    # automatically assigns a unique identifier to the session app. A session app is not persisted and cannot be
    # saved. Everything created during a session app is non-persisted; for example: objects, data connections.
    def create_session_app(self):
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": -1, "method": "CreateSessionApp", "params": {}})
        response = self.engine_socket.send_call(self.engine_socket, msg)
        response_json = json.loads(response)
        if 'error' in response_json:
            error_msg = response_json['error']['message']
            code = str(response_json['error']['code'])
            return "Error code - " + code + ", Error Msg: " + error_msg
        else:
            # Return the session App Id to use for subsequent calls
            # The identifier of the session app is composed of the prefix SessionApp_ and of a GUID.
            return response_json['result']['qSessionAppId']  # ['qReturn']

    # Create an empty session app from an Existing App The objects in the source app are copied into the session app
    # but contain no data. The script of the session app can be edited and reloaded. The name of a session app cannot
    #  be chosen. The engine automatically assigns a unique identifier to the session app. A session app is not
    # persisted and cannot be saved. Everything created during a session app is non-persisted; for example: objects,
    # data connections.
    def create_session_app_from_app(self, src_app_id):
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": -1, "method": "CreateSessionAppFromApp",
                          "params": {"qSrcAppId": src_app_id}})
        response = self.engine_socket.send_call(self.engine_socket, msg)
        response_json = json.loads(response)
        if 'error' in response_json:
            error_msg = response_json['error']['message']
            code = str(response_json['error']['code'])
            return "Error code - " + code + ", Error Msg: " + error_msg
        else:
            # Return the session App Id to use for subsequent calls
            # The identifier of the session app is composed of the prefix SessionApp_ and of a GUID.
            return response_json['result']['qSessionAppId']  # ['qReturn']

    # ExportApp method: Exports an app from the Qlik Sense repository to the file system. !!! This operation is
    # possible only in Qlik Sense Enterprise. !!! Parameters: qTargetPath (MANDATORY) - Path and name of the target
    # app qSrcAppId (MANDATORY) - Identifier of the source app. The identifier is a GUID from the Qlik Sense
    # repository. qIds - Array of identifiers.. The list of all the objects in the app to be exported must be given.
    # This list must contain the GUIDs of all these objects.
    def export_app(self, target_path, src_app_id, qIds=[""]):
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": -1, "method": "ExportApp",
                          "params": {"qTargetPath": target_path, "qSrcAppId": src_app_id, "qIds": qIds}})
        response = self.engine_socket.send_call(self.engine_socket, msg)
        response_json = json.loads(response)
        if 'error' in response_json:
            error_msg = response_json['error']['message']
            code = str(response_json['error']['code'])
            return "Error code - " + code + ", Error Msg: " + error_msg
        elif response_json["result"]["qSuccess"]:
            return "Success?: " + response_json['result'].qSuccess

    # ReplaceAppFromID method: Replaces an app with the objects from a source app. The list of objects in the app to
    # be replaced must be defined in qIds. !!! This operation is possible only in Qlik Sense Enterprise. !!!
    # Parameters: qTargetAppId (MANDATORY) - Identifier (GUID) of the target app. The target app is the app to be
    # replaced. qSrcAppId (MANDATORY) - Identifier of the source app. The identifier is a GUID from the Qlik Sense
    # repository. qIds - QRS identifiers (GUID) of the objects in the target app to be replaced. Only QRS-approved
    # GUIDs are applicable. An object that is QRS-approved, is for example an object that has been published (i.e not
    #  private anymore). If an object is private, it should not be included in this list.  If qIds is empty,
    # the engine automatically creates a list that contains all QRS-approved objects. If the array of identifiers
    # contains objects that are not present in the source app, the objects related to these identifiers are removed
    # from the target app.
    def replace_app_from_id(self, target_path, src_app_id, qIds=[""]):
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": -1, "method": "ReplaceAppFromID",
                          "params": {"qTargetAppId": target_path, "qSrcAppId": src_app_id, "qIds": qIds}})
        response = self.engine_socket.send_call(self.engine_socket, msg)
        response_json = json.loads(response)
        if 'error' in response_json:
            error_msg = response_json['error']['message']
            code = str(response_json['error']['code'])
            return "Error code - " + code + ", Error Msg: " + error_msg
        elif response_json["result"]["qSuccess"]:
            return "Success?: " + response_json['result'].qSuccess

    # GetAuthenticatedUser
    # No parameters
    def get_auth_user(self):
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": -1, "method": "GetAuthenticatedUser", "params": {}})
        response = self.engine_socket.send_call(self.engine_socket, msg)
        response_json = json.loads(response)
        return response_json["result"]

    # GetDatabasesFromConnectionString Lists the databases in a ODBC, OLEDB or CUSTOM data source (global level)
    # Parameters: qConnection (object - has several fields) qId: Identifier of the connection. Is generated by
    # the engine and is unique. qName (MANDATORY): Name of the connection. This parameter is mandatory and must
    # be set when creating or modifying a connection. qConnectionString (MANDATORY): One of: ODBC CONNECT TO [
    # <provider name>], OLEDB CONNECT TO [<provider name>], CUSTOM CONNECT TO [<provider name>], "<local absolute
    #  or relative path,UNC path >", "<URL>" Connection string. qType (MANDATORY): Type of the connection. One
    # of- ODBC, OLEDB, <Name of the custom connection file>, folder, internet. For ODBC, OLEDB and custom
    # connections, the engine checks that the connection type matches the connection string. The type is not case
    #  sensitive. qUserName: Name of the user who creates the connection. This parameter is optional; it is only
    # used for OLEDB, ODBC and CUSTOM connections. A call to GetConnection method does not return the user name.
    # qPassword: Password of the user who creates the connection. This parameter is optional; it is only used for
    #  OLEDB, ODBC and CUSTOM connections. A call to GetConnection method does not return the password.
    # qModifiedDate: Is generated by the engine. Creation date of the connection or last modification date of the
    #  connection. qMeta: Information about the connection. qLogOn (SSO Passthrough or not): Select which user
        # credentials to use to connect to the source. LOG_ON_SERVICE_USER: Disables, LOG_ON_CURRENT_USER: Enables
    def list_databases_from_odbc(self, connect_name, connect_string, connect_type, user_name, password, mod_date="",
                                 meta="", sso_passthrough="LOG_ON_SERVICE_USER"):
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": -1, "method": "GetDatabasesFromConnectionString",
                          "params": [{"qId": "", "qName": connect_name, "qConnectionString": connect_string,
                                      "qType": connect_type, "qUserName": user_name, "qPassword": password,
                                      "qModifiedDate": mod_date, "qMeta": meta, "qLogOn": sso_passthrough}]})
        response = self.engine_socket.send_call(self.engine_socket, msg)
        response_json = json.loads(response)
        if 'error' in response_json:
            error_msg = response_json['error']['message']
            code = str(response_json['error']['code'])
            return "Error code - " + code + ", Error Msg: " + error_msg
        elif response_json["result"]["qSuccess"]:
            return response_json['result'].qDatabases  # Returns an array of databases

    # IsValidConnectionString method: Checks if a connection string is valid.
    def is_valid_connect_string(self, connect_name, connect_string, connect_type, user_name, password, mod_date="",
                                meta="", sso_passthrough="LOG_ON_SERVICE_USER"):
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": -1, "method": "IsValidConnectionString", "params": [
            {"qId": "", "qName": connect_name, "qConnectionString": connect_string, "qType": connect_type,
             "qUserName": user_name, "qPassword": password, "qModifiedDate": mod_date, "qMeta": meta,
             "qLogOn": sso_passthrough}]})
        response = self.engine_socket.send_call(self.engine_socket, msg)
        response_json = json.loads(response)
        if 'error' in response_json:
            error_msg = response_json['error']['message']
            code = str(response_json['error']['code'])
            return "Error code - " + code + ", Error Msg: " + error_msg
        elif response_json["result"]["qSuccess"]:
            return response_json['result'].qDatabases  # Returns an array of databases

    # GetOdbcDsns: List all the ODBC connectors installed on the Sense server machine in Windows
    def get_odbc_dsns(self):
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": -1, "method": "GetOdbcDsns", "params": {}})
        response = self.engine_socket.send_call(self.engine_socket, msg)
        response_json = json.loads(response)
        if 'error' in response_json:
            error_msg = response_json['error']['message']
            code = str(response_json['error']['code'])
            return "Error code - " + code + ", Error Msg: " + error_msg
        elif response_json["result"]["qSuccess"]:
            return response_json['result'].qOdbcDsns  # Returns an array of DSN's

    # GetOleDbProviders: Returns the list of the OLEDB providers installed on the system.
    def get_ole_dbs(self):
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": -1, "method": "GetOleDbProviders", "params": {}})
        response = self.engine_socket.send_call(self.engine_socket, msg)
        response_json = json.loads(response)
        if 'error' in response_json:
            error_msg = response_json['error']['message']
            code = str(response_json['error']['code'])
            return "Error code - " + code + ", Error Msg: " + error_msg
        elif response_json["result"]["qSuccess"]:
            return response_json['result'].qOleDbProviders  # Returns an array of OLE db's

    # GetProgress: Gives information about the progress of the DoReload and DoSave calls. Parameters: qRequestId:
    # Identifier of the DoReload or DoSave request or 0. Complete information is returned if the identifier of the
    # request is given. If the identifier is 0, less information is given. Progress messages and error messages are
    # returned but information like when the request started and finished is not returned.

    def get_progress(self, request_id):
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": -1, "method": "GetProgress", "params": {}})
        response = self.engine_socket.send_call(self.engine_socket, msg)
        response_json = json.loads(response)
        if 'error' in response_json:
            error_msg = response_json['error']['message']
            code = str(response_json['error']['code'])
            return "Error code - " + code + ", Error Msg: " + error_msg
        elif response_json["result"]["qSuccess"]:
            return response_json['result'].qProgressData

    # IsDesktopMode: Indicates whether the user is working in Qlik Sense Desktop.
    # No parameters
    def is_desktop_mode(self, request_id):
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": -1, "method": "IsDesktopMode", "params": {}})
        response = self.engine_socket.send_call(self.engine_socket, msg)
        response_json = json.loads(response)
        if 'error' in response_json:
            error_msg = response_json['error']['message']
            code = str(response_json['error']['code'])
            return "Error code - " + code + ", Error Msg: " + error_msg
        else:
            return response_json["result"]["qReturn"] # Returns true or false

    @staticmethod
    def get_doc_handle(doc_object):
        return doc_object['qHandle']

    # ## NOT IMPLEMENTED, perceived out of use case scope: ## CreateDocEx, GetBaseBNFHash, GetBaseBNF, GetBNF,
        # GetCustomConnectors, GetDefaultAppFolder, GetFunctions, GetInteract, GetLogicalDriveStrings,
        # ## GetStreamList, GetSupportedCodePages, GetUniqueID, InteractDone, IsPersonalMode (deprecated), OSVersion,
        #  ProductVersion (depr), QTProduct, QvVersion (depr), ## ReloadExtensionList, ReplaceAppFromID,
