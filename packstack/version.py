import os

#VERSION = ['2013', '2', '1']
VERSION = os.system("cat openstack-packstack.spec | grep Version | awk '{print $2}'")
FINAL=False

def version_string():
    if FINAL:
        return '.'.join(filter(None, VERSION))
    else:
        return VERSION
        

