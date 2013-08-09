import os
import subprocess

SPEC = "openstack-packstack.spec"
SPEC = SPEC if os.path.isfile(SPEC) else  "%s/rpmbuild/SPECS/%s" % (os.getenv("HOME"), SPEC)


#VERSION = ['2013', '2', '1']
proc = subprocess.Popen(["cat  '%s' | grep Version | awk '{print $2}'" % SPEC ], stdout=subprocess.PIPE, shell=True)

(out, err) = proc.communicate()
VERSION = out.split(".")
print("VERSION= " + str(out))
FINAL=False

def version_string():
    if FINAL:
        return '.'.join(filter(None, VERSION))
    else:
        return '.'.join(filter(None, VERSION))
