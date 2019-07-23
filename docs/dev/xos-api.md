# Prerequisites

```bash
sudo pip install python-consul twisted simplejson
```

Create the necessary certificates. Note: This file may be dependent
on the particular xos-core installation. You can find the correct file
at `helm-charts/xos-core/pki/xos-CA.pem`.

```bash
cat > local_certs.crt <<EOF
-----BEGIN CERTIFICATE-----
MIID1jCCAr6gAwIBAgIJAIWmwLL7nulVMA0GCSqGSIb3DQEBCwUAMHgxCzAJBgNV
BAYTAlVTMRMwEQYDVQQIDApDYWxpZm9ybmlhMRMwEQYDVQQHDApNZW5sbyBQYXJr
MQwwCgYDVQQKDANPTkYxFTATBgNVBAsMDFRlc3RpbmcgT25seTEaMBgGA1UEAwwR
Q09SRCBUZXN0IFJvb3QgQ0EwHhcNMTgxMjE0MTgyNTE5WhcNMTkxMjE1MTgyNTE5
WjB4MQswCQYDVQQGEwJVUzETMBEGA1UECAwKQ2FsaWZvcm5pYTETMBEGA1UEBwwK
TWVubG8gUGFyazEMMAoGA1UECgwDT05GMRUwEwYDVQQLDAxUZXN0aW5nIE9ubHkx
GjAYBgNVBAMMEUNPUkQgVGVzdCBSb290IENBMIIBIjANBgkqhkiG9w0BAQEFAAOC
AQ8AMIIBCgKCAQEAokxdd5vyy83NPQYQK/wsz6VLrunv/3FNSbUv9dC4MC5zZyMd
oxrYCfM38rypbrB5PIVlFdndfDzoYORmlC9gxJnFUmAztyU2JIZrcxk1sQ+lBWj+
Bytwh1TKT0OSfEWjB/LV1FGLAuspJGBn2T0E35bGhhzOL8Cgm0e8akeAfs2s9akO
Xcj+4osnAkXynKl+HhCTBkcrmg1YsTB3+0ug0vM5xuHMU5tVVKpn9DinZ3enuHle
ICyiMF8JyEibjGl0cjnGhw1lPzT7lsjxuoZhr3NaIlI/zUXBDTJbJ6T6gUa1Npa/
lurbEn/9pUMQcUIOnIfzbmzVjPmd0AL9fEcAlQIDAQABo2MwYTAdBgNVHQ4EFgQU
xYhJSu6N6DF7C39G1hAvF7JOC54wHwYDVR0jBBgwFoAUxYhJSu6N6DF7C39G1hAv
F7JOC54wDwYDVR0TAQH/BAUwAwEB/zAOBgNVHQ8BAf8EBAMCAYYwDQYJKoZIhvcN
AQELBQADggEBAJc7J+ZVhp7ti+YN2Smv/jtz79NyF1J6Eb3M/BC/A5Eo8Cp2hklC
NI00+con2Dvvbmj6lOgKXPL6C8LgxiZ5gVDtSvK8zuoIzkIDod4IovxcwLrvlIH4
BpG6Sm1d7EbwAHKFGc0qvVdRN48P884KnzW27eLtsdqrkUPuqz9Ph1JJmAzy3v5p
pKtL6zfn706pcad5NuAcoz0782T+wszHmBv0SBboLdo9NyUciJBQCjIDaSEOpqze
upzRp50aDMq3nxd7yZ3VGA52ECNQ4gWgWAHomDS22RdCHsedbUofnrl6TW88j+Aa
+4AJR9CmhoP1CnKHb5wVCBScw9T8gu3aLe0=
-----END CERTIFICATE-----
EOF
```

Setup a config file that at least configures logging:

```bash
cat > logging_config.yaml <<EOF
logging:
  version: 1
  handlers:
    console:
      class: logging.StreamHandler
EOF
```

The DNS name `xos-core` must map to an IP address:

```bash
sudo echo "<my-core-ip-address> xos-core" >> ~/etc/hosts
```

The following directories must be writeable:

```bash
sudo mkdir -p /var/run/xosapi
sudo chmod a+rwx /var/run/xosapi
```

# Starting the API

```python
import sys
import functools
from xosconfig import Config
from twisted.internet import reactor

Config.init("logging_config.yaml")

from xosapi.xos_grpc_client import SecureClient, InsecureClient

def connected(client):
    print "Connected!"
    print "Stopping!"
    reactor.stop()

client = SecureClient(endpoint="xos-core:30010", 
                      username="admin@opencord.org", 
                      password="letmein", 
                      cacert="local_certs.crt")
#client = InsecureClient(endpoint="198.0.0.57:30011")
client.set_reconnect_callback(functools.partial(connected, client))
client.start()
reactor.run()
```

If all works as it should, the above should print:

```test
Connected!
Stopping!
```

# Executing API commands

Everything you want to execute gets called from the `connected()` callback,
in between the `Connected!` and `Stopping!` lines. For example,

```python
def connected(client):
    print "Connected!"
    print client.orm.Site.objects.all()
    print "Stopping!"
```

This will print a list of sites known to the core.