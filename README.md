
# oVirt-Cockpit SSO

Provides `cockpit-ws` service configured to handle SSO from oVirt's Administration Portal to Cockpit running on an oVirt host.

Distributed either as ``rpm`` or ``docker image`` (experimental).

Please note, the provided ``docker image`` is based on the Cockpit-Container project and is so far **experimental only** and work-in-progress.

## Instructions for rpm installation
The `ovirt-cockpit-sso.rpm` requires `ovirt-engine` package.

Requires `cockpit version >140`.

Verified against ovirt-engine 4.2.

Engine's hostname must be properly set (see `hostname -f`) before `rpm -i` is invoked.

RPM builds can be found in [Fedora Copr ovirt-cockpit-sso](https://copr.fedorainfracloud.org/coprs/mlibra/ovirt-cockpit-sso/)

Please download RPMs from [Project yum repository](http://people.redhat.com/mlibra/repos/ovirt-cockpit-sso/).

### To install:
```
# dnf install ovirt-cockpit-sso
# systemctl enable ovirt-cockpit-sso
# systemctl start ovirt-cockpit-sso
```

RPM installation without adding yum repository (please update version numbers):
```
# dnf install http://people.redhat.com/mlibra/repos/ovirt-cockpit-sso/fedora-27-x86_64/ovirt-cockpit-sso-0.0.1-1.noarch.rpm
```

### To try

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
https://[ENGINE_FQDN]:9986/=[OVIRT_HOST_UUID]/machines#access_token=[VALID_OVIRT_ACCESS_TOKEN]
```

If everything is ok, the browser shall end up with open Cockpit session for the `root` user on the specified host machine. 

## Docker
**Experimental only**, might be broken in favor of the rpm installation 

On the oVirt engine machine:

- allow port 9986
- ``docker run -v /:/host --rm --privileged -e "OVIRT_FQDN=$(hostname -f)" mareklibra/ovirt-cockpit-sso:latest``

## To Be Done
- Main use case (Web Admin part is missing): 
  - log into oVirt's Administration Portal (available for `admin` users only)
  - find particular host and select `Web Console` in the right-click menu
  - host's Cockpit session is opened while no password needs to be entered


## More Info

 * Based on [Cockpit/ws docker image](https://hub.docker.com/r/cockpit/ws/)
 * which is built using [Cockpit-Container project](https://github.com/cockpit-project/cockpit-container)
 * [oVirt project](http://www.ovirt.org)
 * [Cockpit Project](https://cockpit-project.org)
 * [Cockpit Development](https://github.com/cockpit-project/cockpit)
