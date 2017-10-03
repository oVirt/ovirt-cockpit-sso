#!/bin/sh -

echo $$ > /var/run/ovirt-cockpit-sso/ovirt-cockpit-sso.pid

# Add "G_MESSAGES_DEBUG=all" bellow to turn on debug messages in /var/log/messages
OVIRT_FQDN=$(hostname -f) XDG_CONFIG_DIRS=/usr/share/ovirt-cockpit-sso/config /usr/libexec/cockpit-ws --port=9986
