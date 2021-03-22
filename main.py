import paramiko, os
import time, datetime

datum = datetime.datetime.now().strftime("20%y%m%d")
putanja = '/backups/mikrotik/'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

router1 = {'hostname': '192.168.xx.1', 'port': '22', 'username': 'xx', 'password': 'xx'}
router2 = {'hostname': '192.168.xx.1', 'port': '22', 'username': 'xx', 'password': 'xx'}
router3 = {'hostname': '192.168.xx.1', 'port': '22', 'username': 'xx', 'password': 'xx'}
router4 = {'hostname': '192.168.xx.1', 'port': '22', 'username': 'xx', 'password': 'xx'}
router5 = {'hostname': '192.168.xx.1', 'port': '22', 'username': 'xx', 'password': 'xx'}

# creating a list of dictionaries (of devices)
routers = [router1, router2]

# Doing a loop
for router in routers:
    print(f'Connecting to {router["hostname"]}')
    client.connect(**router,look_for_keys=False)
    stdin, stdout, stderr = client.exec_command(':global idt [/system identity get name]; :put $idt')
    filename = stdout.read()
    # print (filename.decode())

    stdin, stdout, stderr = client.exec_command(' /export file=[/system identity get name]')

    stdin, stdout, stderr = client.exec_command('/system backup save dont-encrypt=yes name=[/system identity get name]')

    time.sleep(10)

    sftp = client.open_sftp()
    # Download
    filepath = filename.decode().strip() + ".rsc"
    print (filepath)
    localpath = os.path.join(putanja, datum+'-'+filepath )

    sftp.get(filepath, localpath)

    time.sleep(5)

    # sftp = client.open_sftp()
    # Download
    filepath = filename.decode().strip() + ".backup"
    print (filepath)
    localpath = os.path.join(putanja, datum+'-'+filepath)

    sftp.get(filepath, localpath)

    time.sleep(10)

client.close()
