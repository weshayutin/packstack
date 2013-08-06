import subprocess

#VERSION = ['2013', '2', '1']
proc = subprocess.Popen(["cat openstack-packstack.spec | grep Version | awk '{print $2}'"], stdout=subprocess.PIPE, shell=True)
#print('VERSION= ' + str(VERSION))
(out, err) = proc.communicate()
VERSION = out.split(".")
print("VERSION= " + str(out))
FINAL=False

def version_string():
    if FINAL:
        return '.'.join(filter(None, VERSION))
    else:
        return '.'.join(filter(None, VERSION))
        

