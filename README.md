
# oVirt-Cockpit SSO

Provides cockpit-ws service configured to handle SSO from oVirts Administration Portal to Cockpit running on an oVirt host.

Packed as either ``rpm`` or ``docker image``.

Please note, the provided ``docker image`` is based on the Cockpit-Container project and is so far **experimental only** and work-in-progress.

## Instructions for rpm installation
The `ovirt-cockpit-sso.rpm` is meant to be installed on an oVirt engine machine.

Required cockpit version: >140

Verified against ovirt-engine 4.2.

Engine's hostname must be properly set (see `hostname -f`) before `rpm -i`.

**TODO:** yum epository

To install:
```
dnf install ovirt-cockpit-sso
```


## Instructions for docker
**Experimental only**

On the oVirt engine machine:

- allow port 9000
- ``docker run -v /:/host --rm --privileged -e "OVIRT_FQDN=$(hostname -f)" mareklibra/ovirt-cockpit-sso:latest``

## To try

- Get the oVirt SSO access token, i.e. via:

```
curl -v -H "Accept: application/json" --data "grant_type=password&scope=ovirt-app-api&username=[YOUR_USER]%40[OVIRT_DOMAIN]&password=[YOUR_PWD]" https://[ENGINE_FQDN]/ovirt-engine/sso/oauth/token --insecure
```

- get host UUID (where the login shall lead to), i.e. via:

```
curl -v -i --insecure --header "Accept: application/xml" --header "Filter: true" --user "[YOUR_USER]@[OVIRT_DOMAIN]" "https://[ENGINE_FQDN]/ovirt-engine/api/hosts"
```

- in browser, enjoy ovirt-cockpit SSO by:
```
http://[OVIRT_FQDN]:9000/=[HOST_UUID]#access_token=[OVIRT_SSO_TOKEN]
```

If everything is ok, the browser shall end up with open Cockpit session for the `root` user on the specified host machine. 

**Not yet fully implemented:** Eventually, log into oVirt's Administration Portal, find particular host and select `Web Console` in the right-click menu to open host's Cockpit session using SSO.

## More Info

 * Based on [Cockpit/ws docker image](https://hub.docker.com/r/cockpit/ws/)
 * which is built using [Cockpit-Container project](https://github.com/cockpit-project/cockpit-container)
 * [oVirt project](www.ovirt.org)
 * [Cockpit Project](https://cockpit-project.org)
 * [Cockpit Development](https://github.com/cockpit-project/cockpit)
