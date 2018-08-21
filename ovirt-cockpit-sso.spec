Name:           ovirt-cockpit-sso
Version:        0.0.4
Release:        1%{?dist}
Summary:        Provides SSO from oVirt Administration Portal to Cockpit
License:        ASL 2.0
URL:            https://github.com/oVirt/ovirt-cockpit-sso
Source0:        https://github.com/oVirt/ovirt-cockpit-sso/archive/%{name}-%{version}.tar.gz

%define build_root_dir %{buildroot}%{_datadir}/%{name}
%define app_root_dir %{_datadir}/%{name}
%define logfile /var/log/ovirt-cockpit-sso.install.log

BuildArch: noarch

# None of the 4.2 features are reuiqred by this package but "Host Console" link is introduced here for the first time
# using conflicts instead of require because in CentOS Virt SIG repo we can't build ovirt-engine and the require
# breaks repository closure
Conflicts: ovirt-engine < 4.2

## TODO: increase to 140 once RHEL 7.5 is released
## In fact, cockpit 140 is required but this is eased to allow smooth
## deployment for testing in the meantime
## cockpit 140 is farther enforced in start.sh which is called by systemd
%if 0%{?fedora} >= 26
## fedora >26 is fine
Requires: cockpit-ws >= 140
Requires: cockpit-dashboard >= 140
%else
Requires: cockpit-ws >= 138
Requires: cockpit-dashboard >= 138
%endif

%description
This package sets cockpit-ws service (see cockpit-project.org) to provide
SSO (Single Sign On) from oVirt's Administration Portal to Cockpit running
on an oVirt's host machine.

%prep
%setup -q

%build

%install
mkdir -p %{build_root_dir}/config/cockpit
mkdir -p %{buildroot}%{_usr}/lib/systemd/system/

cp container/config/cockpit/cockpit.conf %{build_root_dir}/config/cockpit/.

cp container/cockpit-auth-ovirt %{build_root_dir}/.
cp container/keygen.sh %{build_root_dir}/.
cp start.sh %{build_root_dir}/.
cp prestart.sh %{build_root_dir}/.
cp ovirt-cockpit-sso.xml %{build_root_dir}/.
cp ovirt-cockpit-sso.service %{buildroot}%{_usr}/lib/systemd/system/.

%post
HOSTNAME=$(hostname -f)
ROOT_DIR=$(echo %{app_root_dir} | sed -e 's/\\/\\\\/g; s/\//\\\//g; s/&/\\\&/g')

case "$1" in
  1)
    echo configuring firewall for ovirt-cockpit-sso service - accept 9986/tcp > %{logfile}
    echo Post-installation configuration of %{name} - setting engine FQDN to: ${HOSTNAME} >> %{logfile}

    ## /bin/firewall-cmd --permanent --zone=public --new-service-from-file=%{app_root_dir}/ovirt-cockpit-sso.xml
    /bin/firewall-cmd --permanent --add-port 9986/tcp >> %{logfile}
    /bin/firewall-cmd --reload >> %{logfile}
  ;;
  2)
    ## This is an upgrade.
  ;;
esac

/bin/sed -i "s/\%\%ENGINE_URL\%\%/https:\/\/${HOSTNAME}\/ovirt-engine/g" %{app_root_dir}/config/cockpit/cockpit.conf
/bin/sed -i "s/\%\%INSTALL_DIR\%\%/${ROOT_DIR}/g" %{app_root_dir}/config/cockpit/cockpit.conf

%postun
case "$1" in
  0)
    ## package is being removed
    rm %{app_root_dir}/config/cockpit/ws-certs.d || true
    rm %{app_root_dir}/ca.pem || true

    ## TODO: this is not working but would be better approach:
    ## /bin/firewall-cmd --permanent --zone=public --delete-service=ovirt-cockpit-sso
    /bin/firewall-cmd --permanent --remove-port 9986/tcp >> %{logfile} || true
    /bin/firewall-cmd --reload >> %{logfile}
  ;;
  1)
     ## Package is being upgraded. Do nothing.
    :
  ;;
esac

# the .service file could be changed
systemctl daemon-reload

%files
%doc README.md
%license LICENSE
%{app_root_dir}/config/cockpit/cockpit.conf
%{app_root_dir}/cockpit-auth-ovirt
%{app_root_dir}/keygen.sh
%{app_root_dir}/start.sh
%{app_root_dir}/prestart.sh
%{app_root_dir}/ovirt-cockpit-sso.xml
%{_usr}/lib/systemd/system/ovirt-cockpit-sso.service

%config %{app_root_dir}/config/cockpit/cockpit.conf

%changelog
* Mon Nov 27 2017 Marek Libra <mlibra@redhat.com> - 0.0.4-1
- RPM installation fixes - https://github.com/oVirt/ovirt-cockpit-sso/pull/10

* Thu Nov 16 2017 Marek Libra <mlibra@redhat.com> - 0.0.3-3
- Spec file polishing

* Wed Nov 15 2017 Sandro Bonazzola <sbonazzo@redhat.com> - 0.0.3-2
- Fixing spec file for CentOS Virt SIG inclusion

* Wed Oct 25 2017 Marek Libra <mlibra@redhat.com> - 0.0.3
- Required cockpit-ws is 138 but the service is effectively
  disabled for lower than 140. So at least instlation is
  possible until RHEL 7.5 is released.

* Wed Oct 18 2017 Marek Libra <mlibra@redhat.com> - 0.0.2
- Fixes for package update

* Wed Sep 06 2017 Marek Libra <mlibra@redhat.com> - 0.0.1
- Initial version
