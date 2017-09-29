%global product oVirt

Name:           ovirt-cockpit-sso
Version:        0.0.1
Release:        1
Summary:        Provides SSO from oVirt Administration Portal to Cockpit running on an oVirt host.
License:        ASL 2.0
URL:            https://github.com/mareklibra/ovirt-cockpit-sso
Source0:        ovirt-cockpit-sso-%{version}.tar.gz

%define build_root_dir %{buildroot}%{_datadir}/%{name}
%define app_root_dir %{_datadir}/%{name}

BuildArch: noarch

# None of 4.2 features are reuiqred by this package but "Web Console" link is first introduced here
Requires: ovirt-engine > 4.2

Requires: cockpit-ws >= 140
Requires: cockpit-dashboard >= 140

%description
This package sets cockpit-ws service (see cockpit-project.org) to provide SSO (Single Sign On) from oVirt's Administration Portal to Cockpit running on an oVirt's host machine.

%prep
tar -xzf %{SOURCE0}

%build

%install
mkdir -p %{build_root_dir}/config/cockpit
mkdir -p %{buildroot}%{_usr}/lib/systemd/system/

mkdir -p %{buildroot}/var/run/ovirt-cockpit-sso
chown ovirt %{buildroot}/var/run/ovirt-cockpit-sso

cp container/config/cockpit/cockpit.conf %{build_root_dir}/config/cockpit/.

cp container/cockpit-auth-ovirt %{build_root_dir}/.
cp container/keygen.sh %{build_root_dir}/.
cp start.sh %{build_root_dir}/.
cp ovirt-cockpit-sso.xml %{build_root_dir}/.
cp ovirt-cockpit-sso.service %{buildroot}%{_usr}/lib/systemd/system/.

%post
HOSTNAME=$(hostname -f)
ROOT_DIR=$(echo %{app_root_dir} | sed -e 's/\\/\\\\/g; s/\//\\\//g; s/&/\\\&/g')

echo Post-installation configuration of %{name} - setting engine FQDN to: ${HOSTNAME}
/bin/sed -i "s/\%\%ENGINE_URL\%\%/https:\/\/${HOSTNAME}\/ovirt-engine/g" %{app_root_dir}/config/cockpit/cockpit.conf
/bin/sed -i "s/\%\%INSTALL_DIR\%\%/${ROOT_DIR}/g" %{app_root_dir}/config/cockpit/cockpit.conf
/bin/ln -s %{_sysconfdir}/cockpit/ws-certs.d %{app_root_dir}/config/cockpit/ws-certs.d

echo configuring firewall for ovirt-cockpit-sso service - accept 9986/tcp
/bin/firewall-cmd --permanent --zone=public --new-service-from-file=%{app_root_dir}/ovirt-cockpit-sso.xml
/bin/firewall-cmd --reload

# engine's ca.pem can be retrieved via 'https://[FQDN]/ovirt-engine/services/pki-resource?resource=ca-certificate&format=X509-PEM-CA'
# without any authorization so there's no harm in making a copy here to speed up processing later
# TODO: proper location of CA file is configured in /etc/ovirt-engine/engine.conf.d/10-setup-pki.conf : ENGINE_PKI_CA
/bin/cp %{_sysconfdir}/pki/ovirt-engine/ca.pem %{app_root_dir}/ca.pem
chown ovirt %{app_root_dir}/ca.pem

%preun
rm %{app_root_dir}/config/cockpit/ws-certs.d
rm %{app_root_dir}/ca.pem
/bin/firewall-cmd --permanent --zone=public --delete-service=ovirt-cockpit-sso
/bin/firewall-cmd --reload

%files
%doc README.md 
%license LICENSE
%{app_root_dir}/config/cockpit/cockpit.conf
%{app_root_dir}/cockpit-auth-ovirt
%{app_root_dir}/keygen.sh
%{app_root_dir}/start.sh
%{app_root_dir}/ovirt-cockpit-sso.xml
%{_usr}/lib/systemd/system/ovirt-cockpit-sso.service
/var/run/ovirt-cockpit-sso

%changelog
* Wed Sep 06 2017 Marek Libra <mlibra@redhat.com> - 0.0.1
- Initial version
