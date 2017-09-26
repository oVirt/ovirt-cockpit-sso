#!/bin/sh -

OVIRT_FQDN=$(hostname -f) XDG_CONFIG_DIRS=/usr/share/ovirt-cockpit-sso/config /usr/libexec/cockpit-ws --port=9986
