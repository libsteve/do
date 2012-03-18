from paramiko import SSHClient
from paramiko import SFTPClient

_CONNECTION = None

def connect(server, port=22, username=None, password=None):
	if _CONNECTION == None:
		client = SSHClient()
		client.load_system_host_keys()
		client.connect(server, port, username, password)
		_CONNECTION = client
	return _CONNECTION

def close_connection():
	if _CONNECTION != None:
		_CONNECTION.close()
		_CONNECTION = None



_TEMP_FOLDER = "temp_do"

def copy_to_server(connection, files):
	client = connection.open_sftp()
	if _is_str_in_lst(_TEMP_FOLDER, client.listdir()):
		# remove the folder and its contents (to remove possible conflicts)
		_remote_rmdir(client, _TEMP_FOLDER)
	client.mkdir(_TEMP_FOLDER) # create the folder if it does not exist

	destination = "./" + _TEMP_FOLDER + "/"
	for f in files:
		client.put(f, destination+f)

	client.close()

def rmdir_from_server(connection, folder=_TEMP_FOLDER):
	client = connection.open_sftp()
	_remote_rmdir(client, folder)
	client.close()

def _is_str_in_lst(str, lst):
	for item in lst:
		if item == str:
			return True
	return False

def _remote_rmdir(sftp_client, folder):
	files = sftp_client.listdir(folder)
	for f in files:
		try:
			sftp_client.remove(f)
		except IOError:
			_remote_rmdir(stfp_client, f)
	sftp.rmdir(folder)







