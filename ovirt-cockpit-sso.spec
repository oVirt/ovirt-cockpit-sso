Name:           ovirt-cockpit-sso
Version:        0.1.4
Release:        2%{?dist}
Summary:        Provides SSO from oVirt Administration Portal to Cockpit
License:        ASL 2.0
URL:            https://github.com/oVirt/%{name}
Source0:        https://resources.ovirt.org/pub/src/%{name}/%{name}-%{version}.tar.gz

%define build_root_dir %{buildroot}%{_datadir}/%{name}
%define app_root_dir %{_datadir}/%{name}
%define logfile /var/log/ovirt-cockpit-sso.install.log

BuildArch: noarch

# None of the 4.2 features are reuiqred by this package but "Host Console" link is introduced here for the first time
# using conflicts instead of require because in CentOS Virt SIG repo we can't build ovirt-engine and the require
# breaks repository closure
Conflicts: ovirt-engine < 4.4

Requires: cockpit-ws >= 140
Requires: cockpit-system >= 224
Requires: python3

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

    ## /bin/firewall-cmd --permanent --zone=public --new-service-from-file=%%{app_root_dir}/ovirt-cockpit-sso.xml
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

%config %verify(not md5 size mtime) %{app_root_dir}/config/cockpit/cockpit.conf

%changelog
* Sun Jan 10 2021 - Yedidyah Bar David <didi@redhat.com> - 0.1.4-2
- spec: update cockpit requirements

* Thu Apr 23 2020 Lev Veyde <lveyde@redhat.com> - 0.1.4-1
- Fixed BZ1826248 - https://bugzilla.redhat.com/1826248

* Mon Apr 06 2020 Sandro Bonazzola <sbonazzo@redhat.com> - 0.1.3-2
- Fix spec file issues

* Thu Apr  2 2020 Sandro Bonazzola - 0.1.3-1
- Explicitly require Python 3

* Thu Dec 19 2019 Ryan Barry <rbarry@redhat.com> - 0.1.2
- Use python2 explicitly so we build on FC30

* Thu Nov 29 2018 Marek Libra <mlibra@redhat.com> - 0.1.1
- Exclude cockpit.conf from verification - https://github.com/oVirt/ovirt-cockpit-sso/pull/17

* Mon Sep  3 2018 Marek Libra <mlibra@redhat.com> - 0.1.0
- debug logging removed
- mark cockpit.conf as a config file - https://github.com/oVirt/ovirt-cockpit-sso/pull/15

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
