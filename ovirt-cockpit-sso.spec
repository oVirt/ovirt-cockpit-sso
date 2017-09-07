%global product oVirt

## %global use_rhev %( test -z @RHEV@ && echo 1 || echo 0)
## %define debug_package %{nil}

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
cp container/cockpit-auth-ovirt %{build_root_dir}/.
cp container/config/cockpit/cockpit.conf %{build_root_dir}/config/cockpit/cockpit.conf
echo Installation done ...

%post
HOSTNAME=$(hostname -f)
ROOT_DIR=$(echo %{app_root_dir} | sed -e 's/\\/\\\\/g; s/\//\\\//g; s/&/\\\&/g')

echo Post-installation configuration, setting engine FQDN to: ${HOSTNAME}
/bin/sed -i "s/\%\%ENGINE_URL\%\%/https:\/\/${HOSTNAME}\/ovirt-engine/g" %{app_root_dir}/config/cockpit/cockpit.conf
/bin/sed -i "s/\%\%INSTALL_DIR\%\%/${ROOT_DIR}/g" %{app_root_dir}/config/cockpit/cockpit.conf
/bin/ln -s /etc/cockpit/ws-certs.d %{app_root_dir}/config/cockpit/ws-certs.d

%preun
rm %{app_root_dir}/config/cockpit/ws-certs.d

# TODO:
# engine-setup - port 9000
# firewall - ??, open 9000 port
# start - use ovirt-cockpit-sso.service

%files
%doc README.md 
%license LICENSE
%{app_root_dir}/cockpit-auth-ovirt
%{app_root_dir}/config/cockpit/cockpit.conf

%changelog
* Wed Sep 06 2017 Marek Libra <mlibra@redhat.com> - 0.0.1
- Initial version

