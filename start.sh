#!/bin/sh -

COCKPIT_VERSION=`rpm -q --queryformat '%{VERSION}' cockpit-ws`

echo Installed cockpit version: ${COCKPIT_VERSION}

# TODO: Following if-clause will be removed once rhel 7.5 is released, see comment in .spec file
if [ $(echo ""$COCKPIT_VERSION" >= 140" | bc) -ne 0 ] ; then
    echo Cockpit version check passed

    echo $$ > /var/run/ovirt-cockpit-sso/ovirt-cockpit-sso.pid

    # Add "G_MESSAGES_DEBUG=all" bellow to turn on debug messages in /var/log/messages
    OVIRT_FQDN=$(hostname -f) XDG_CONFIG_DIRS=/usr/share/ovirt-cockpit-sso/config /usr/libexec/cockpit-ws --port=9986
else
    # By skipping ovirt-cockpit-sso.pid here, the IsOvirtCockpitSSOStartedQuery check in engine will fail
    logger Installed cockpit-ws version is ${COCKPIT_VERSION} but at least 140 is required. Cockpit-ovirt-sso will be effectively disabled.

    # TODO: just for debugging:
    echo Installed Cockpit version ${COCKPIT_VERSION} is old, at least 140 is required for ovirt-cockpit SSO

    # Since SSO is disabled in this flow, do nothing but keep the service running
    tail -f /dev/null
fi
