from paramiko import SSHClient
from paramiko import SFTPClient

_CONNECTION = None

def connect(server, port=22, username=None, password=None):
	global _CONNECTION
	if _CONNECTION != None:
		close_connection()
	try:
		client = SSHClient()
		client.load_system_host_keys()
		client.connect(server, port, username, password)
		_CONNECTION = client
	except:
		_CONNECTION = None
		print("Connection Failure")
	return _CONNECTION

def close_connection():
	global _CONNECTION
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
	connection.exec_command("rm -Rf " + folder)

def _is_str_in_lst(str, lst):
	for item in lst:
		if item == str:
			return True
	return False



def exec_on_server(connection, command="", args=[], show_output=True):
	if command != "":
		cmd = command
		for arg in args:
			cmd += " " + arg
		(stdin, stdout, sterr) = connection.exec_command(cmd)
		if show_output:
			out = stdout.readline()
			for line in stdout:
				out += line
			print(out)




