#!/bin/sh -

APP_ROOT="/usr/share/ovirt-cockpit-sso"

# ensure the cockpit's WS certificate is present and accessible by ovirt:ovirt user:group
/usr/sbin/remotectl certificate --ensure --user=ovirt --group=ovirt --selinux-type=etc_t

# link cockpit's WS certificate to ovirt-cockpit-sso config dir which will be passed to the cockpit-ws later
/bin/ln -s /etc/cockpit/ws-certs.d ${APP_ROOT}/config/cockpit/ws-certs.d || true

## Engine's ca.pem should be properly retrieved via 'https://[FQDN]/ovirt-engine/services/pki-resource?resource=ca-certificate&format=X509-PEM-CA'
## but without any authorization - so there's no harm in making a copy here to speed up processing later
## TODO: retrieve location of CA file from /etc/ovirt-engine/engine.conf.d/10-setup-pki.conf : ENGINE_PKI_CA
/bin/cp /etc/pki/ovirt-engine/ca.pem ${APP_ROOT}/ca.pem
chown ovirt:ovirt ${APP_ROOT}/ca.pem

