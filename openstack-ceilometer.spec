# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif

%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility
%global _without_doc 1
%global with_doc %{!?_without_doc:1}%{?_without_doc:0}
%global pypi_name ceilometer
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global common_desc \
OpenStack ceilometer provides services to measure and \
collect metrics from OpenStack components.

Name:             openstack-ceilometer
# Liberty semver reset
# https://review.openstack.org/#/q/I6a35fa0dda798fad93b804d00a46af80f08d475c,n,z
Epoch:            1
Version:          XXX
Release:          XXX
Summary:          OpenStack measurement collection service

Group:            Applications/System
License:          ASL 2.0
URL:              https://wiki.openstack.org/wiki/Ceilometer
Source0:          https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz
Source1:          %{pypi_name}-dist.conf
Source2:          %{pypi_name}.logrotate
Source4:          ceilometer-rootwrap-sudoers

Source11:         %{name}-compute.service
Source12:         %{name}-central.service
Source13:         %{name}-notification.service
Source14:         %{name}-ipmi.service
Source15:         %{name}-polling.service

Patch0001:        0001-Add-dummy-skip-metering-database-temporarily.patch

BuildArch:        noarch
BuildRequires:    intltool
BuildRequires:    openstack-macros
BuildRequires:    python%{pyver}-cotyledon
BuildRequires:    python%{pyver}-sphinx
BuildRequires:    python%{pyver}-setuptools
BuildRequires:    python%{pyver}-pbr >= 1.10.0
BuildRequires:    git
BuildRequires:    python%{pyver}-devel
# Required to compile translation files
BuildRequires:    python%{pyver}-babel

BuildRequires:    systemd

%description
%{common_desc}

%package -n       python%{pyver}-ceilometer
Summary:          OpenStack ceilometer python libraries
%{?python_provide:%python_provide python%{pyver}-ceilometer}
Group:            Applications/System

Requires:         python%{pyver}-babel
Requires:         python%{pyver}-cachetools >= 2.1.0
Requires:         python%{pyver}-eventlet
Requires:         python%{pyver}-futurist >= 1.8.0
Requires:         python%{pyver}-cotyledon
Requires:         python%{pyver}-greenlet
Requires:         python%{pyver}-iso8601
Requires:         python%{pyver}-keystoneauth1 >= 3.9.0
Requires:         python%{pyver}-jsonpath-rw-ext
Requires:         python%{pyver}-stevedore >= 1.20.0
Requires:         python%{pyver}-pbr
Requires:         python%{pyver}-six >= 1.9.0
Requires:         python%{pyver}-4.4.0

Requires:         python%{pyver}-alembic

Requires:         python%{pyver}-oslo-config >= 2:5.2.0
Requires:         python%{pyver}-netaddr
Requires:         python%{pyver}-oslo-rootwrap >= 2.0.0
Requires:         python%{pyver}-oslo-vmware >= 0.6.0
Requires:         python%{pyver}-requests >= 2.8.1

Requires:         python%{pyver}-pytz
Requires:         python%{pyver}-croniter

Requires:         python%{pyver}-werkzeug

Requires:         python%{pyver}-oslo-context
Requires:         python%{pyver}-oslo-concurrency >= 3.5.0
Requires:         python%{pyver}-oslo-i18n  >= 3.15.3
Requires:         python%{pyver}-oslo-log  >= 3.36.0
Requires:         python%{pyver}-oslo-privsep >= 1.32.0
Requires:         python%{pyver}-oslo-reports >= 1.18.0
Requires:         python%{pyver}-oslo-upgradecheck >= 0.1.1
Requires:         python%{pyver}-monotonic

# Handle python2 exception
%if %{pyver} == 2
Requires:         pysnmp
Requires:         PyYAML
Requires:         python-lxml
Requires:         python-anyjson
Requires:         python-jsonpath-rw
Requires:         python-msgpack >= 0.5.0
Requires:         python-retrying
Requires:         python%{pyver}-futures
%else
Requires:         python%{pyver}-pysnmp
Requires:         python%{pyver}-PyYAML
Requires:         python%{pyver}-lxml
Requires:         python%{pyver}-anyjson
Requires:         python%{pyver}-jsonpath-rw
Requires:         python%{pyver}-msgpack >= 0.5.0
Requires:         python%{pyver}-retrying
%endif


%description -n   python%{pyver}-ceilometer
%{common_desc}

This package contains the ceilometer python library.


%package common
Summary:          Components common to all OpenStack ceilometer services
Group:            Applications/System

# Collector service has been removed but not replaced
Provides:         openstack-ceilometer-collector = %{epoch}:%{version}-%{release}
Obsoletes:        openstack-ceilometer-collector < %{epoch}:%{version}-%{release}
# api service has been removed
Obsoletes:        openstack-ceilometer-api

Requires:         python%{pyver}-ceilometer = %{epoch}:%{version}-%{release}
Requires:         python%{pyver}-oslo-messaging >= 6.2.0
Requires:         python%{pyver}-oslo-serialization >= 1.10.0
Requires:         python%{pyver}-oslo-utils >= 3.37.0
Requires:         python%{pyver}-tooz
Requires:         python%{pyver}-gnocchiclient >= 7.0.0
Requires:         python%{pyver}-os-xenapi >= 0.3.3
Requires:         python%{pyver}-novaclient >= 1:9.1.0
Requires:         python%{pyver}-keystoneclient >= 1:3.15.0
Requires:         python%{pyver}-neutronclient >= 6.7.0
Requires:         python%{pyver}-glanceclient >= 1:2.8.0
Requires:         python%{pyver}-swiftclient
Requires:         python%{pyver}-cinderclient >= 3.3.0
Requires:         python%{pyver}-zaqarclient >= 1.3.0

# Handle python2 exception
%if %{pyver} == 2
Requires:         python-posix_ipc
%else
Requires:         python%{pyver}-posix_ipc
%endif


%if 0%{?rhel} && 0%{?rhel} < 8
%{?systemd_requires}
%else
%{?systemd_ordering} # does not exist on EL7
%endif
Requires(pre):    shadow-utils

# Config file generation
BuildRequires:    python%{pyver}-os-xenapi
BuildRequires:    python%{pyver}-oslo-config >= 2:5.2.0
BuildRequires:    python%{pyver}-oslo-concurrency
BuildRequires:    python%{pyver}-oslo-log
BuildRequires:    python%{pyver}-oslo-messaging
BuildRequires:    python%{pyver}-oslo-privsep
BuildRequires:    python%{pyver}-oslo-reports
BuildRequires:    python%{pyver}-oslo-vmware >= 0.6.0
BuildRequires:    python%{pyver}-glanceclient >= 1:2.8.0
BuildRequires:    python%{pyver}-neutronclient
BuildRequires:    python%{pyver}-novaclient  >= 1:9.1.0
BuildRequires:    python%{pyver}-swiftclient
BuildRequires:    python%{pyver}-croniter
BuildRequires:    python%{pyver}-jsonpath-rw-ext
BuildRequires:    python%{pyver}-tooz
BuildRequires:    python%{pyver}-werkzeug
BuildRequires:    python%{pyver}-gnocchiclient >= 7.0.0
BuildRequires:    python%{pyver}-cinderclient >= 3.3.0
BuildRequires:    python%{pyver}-zaqarclient >= 1.3.0

# Handle python2 exception
%if %{pyver} == 2
BuildRequires:    python-d2to1
BuildRequires:    python-jsonpath-rw
BuildRequires:    python-lxml
%else
BuildRequires:    python%{pyver}-d2to1
BuildRequires:    python%{pyver}-jsonpath-rw
BuildRequires:    python%{pyver}-lxml
%endif

%description common
%{common_desc}

This package contains components common to all OpenStack
ceilometer services.


%package compute
Summary:          OpenStack ceilometer compute agent
Group:            Applications/System

Requires:         %{name}-common = %{epoch}:%{version}-%{release}
Requires:         %{name}-polling = %{epoch}:%{version}-%{release}

%if %{pyver} == 2
Requires:         libvirt-python
%else
Requires:         python%{pyver}-libvirt
%endif


%description compute
%{common_desc}

This package contains the ceilometer agent for
running on OpenStack compute nodes.


%package central
Summary:          OpenStack ceilometer central agent
Group:            Applications/System

Requires:         %{name}-common = %{epoch}:%{version}-%{release}
Requires:         %{name}-polling = %{epoch}:%{version}-%{release}

%description central
%{common_desc}

This package contains the central ceilometer agent.


%package notification
Summary:          OpenStack ceilometer notification agent
Group:            Applications/System

Requires:         %{name}-common = %{epoch}:%{version}-%{release}

%description notification
%{common_desc}

This package contains the ceilometer notification agent
which pushes metrics to the collector service from the
various OpenStack services.


%package ipmi
Summary:          OpenStack ceilometer ipmi agent
Group:            Applications/System

Requires:         %{name}-common = %{epoch}:%{version}-%{release}
Requires:         %{name}-polling = %{epoch}:%{version}-%{release}

Requires:         ipmitool

%description ipmi
%{common_desc}

This package contains the ipmi agent to be run on OpenStack
nodes from which IPMI sensor data is to be collected directly,
by-passing Ironic's management of baremetal.


%package polling
Summary:          OpenStack ceilometer polling agent
Group:            Applications/System

Requires:         %{name}-common = %{epoch}:%{version}-%{release}

%if %{pyver} == 2
Requires:         libvirt-python
%else
Requires:         python%{pyver}-libvirt
%endif

%description polling
Ceilometer aims to deliver a unique point of contact for billing systems to
acquire all counters they need to establish customer billing, across all
current and future OpenStack components. The delivery of counters must
be tracable and auditable, the counters must be easily extensible to support
new projects, and agents doing data collections should be
independent of the overall system.

This package contains the polling service.

%package -n python%{pyver}-ceilometer-tests
Summary:        Ceilometer tests
%{?python_provide:%python_provide python%{pyver}-ceilometer-tests}
Requires:       python%{pyver}-ceilometer = %{epoch}:%{version}-%{release}
Requires:       python%{pyver}-gabbi >= 1.30.0

%description -n python%{pyver}-ceilometer-tests
%{common_desc}

This package contains the Ceilometer test files.

%if 0%{?with_doc}
%package doc
Summary:          Documentation for OpenStack ceilometer
Group:            Documentation

# Required to build module documents
BuildRequires:    python%{pyver}-eventlet
BuildRequires:    python%{pyver}-openstackdocstheme
# while not strictly required, quiets the build down when building docs.
BuildRequires:    python%{pyver}-iso8601

%description      doc
%{common_desc}

This package contains documentation files for ceilometer.
%endif

%prep
%autosetup -n ceilometer-%{upstream_version} -S git

find . \( -name .gitignore -o -name .placeholder \) -delete

find ceilometer -name \*.py -exec sed -i '/\/usr\/bin\/env python/{d;q}' {} +

# TODO: Have the following handle multi line entries
sed -i '/setup_requires/d; /install_requires/d; /dependency_links/d' setup.py

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
%py_req_cleanup

%build
# Generate config file
PYTHONPATH=. oslo-config-generator-%{pyver} --config-file=etc/ceilometer/ceilometer-config-generator.conf

%{pyver_build}

# Generate i18n files
%{pyver_bin} setup.py compile_catalog -d build/lib/%{pypi_name}/locale

# Programmatically update defaults in sample config
# which is installed at /etc/ceilometer/ceilometer.conf
# TODO: Make this more robust
# Note it only edits the first occurrence, so assumes a section ordering in sample
# and also doesn't support multi-valued variables.
while read name eq value; do
  test "$name" && test "$value" || continue
  sed -i "0,/^# *$name=/{s!^# *$name=.*!#$name=$value!}" etc/ceilometer/ceilometer.conf
done < %{SOURCE1}

%install
%{pyver_install}

%if 0%{?with_doc}
# docs generation requires everything to be installed first

%{pyver_build}
# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.doctrees doc/build/html/.buildinfo

%endif

# Setup directories
install -d -m 755 %{buildroot}%{_sharedstatedir}/ceilometer
install -d -m 755 %{buildroot}%{_sharedstatedir}/ceilometer/tmp
install -d -m 750 %{buildroot}%{_localstatedir}/log/ceilometer

# Install config files
install -d -m 755 %{buildroot}%{_sysconfdir}/ceilometer
install -d -m 755 %{buildroot}%{_sysconfdir}/ceilometer/rootwrap.d
install -d -m 755 %{buildroot}%{_sysconfdir}/sudoers.d
install -d -m 755 %{buildroot}%{_sysconfdir}/sysconfig
install -d -m 755 %{buildroot}%{_sysconfdir}/ceilometer/meters.d
install -p -D -m 640 %{SOURCE1} %{buildroot}%{_datadir}/ceilometer/ceilometer-dist.conf
install -p -D -m 440 %{SOURCE4} %{buildroot}%{_sysconfdir}/sudoers.d/ceilometer
install -p -D -m 640 etc/ceilometer/ceilometer.conf %{buildroot}%{_sysconfdir}/ceilometer/ceilometer.conf
install -p -D -m 640 ceilometer/pipeline/data/pipeline.yaml %{buildroot}%{_sysconfdir}/ceilometer/pipeline.yaml
install -p -D -m 640 etc/ceilometer/polling.yaml %{buildroot}%{_sysconfdir}/ceilometer/polling.yaml
install -p -D -m 640 ceilometer/pipeline/data/event_pipeline.yaml %{buildroot}%{_sysconfdir}/ceilometer/event_pipeline.yaml
install -p -D -m 640 ceilometer/pipeline/data/event_definitions.yaml %{buildroot}%{_sysconfdir}/ceilometer/event_definitions.yaml
install -p -D -m 640 etc/ceilometer/rootwrap.conf %{buildroot}%{_sysconfdir}/ceilometer/rootwrap.conf
install -p -D -m 640 etc/ceilometer/rootwrap.d/ipmi.filters %{buildroot}/%{_sysconfdir}/ceilometer/rootwrap.d/ipmi.filters
install -p -D -m 640 ceilometer/publisher/data/gnocchi_resources.yaml %{buildroot}%{_sysconfdir}/ceilometer/gnocchi_resources.yaml
install -p -D -m 640 ceilometer/data/meters.d/meters.yaml %{buildroot}%{_sysconfdir}/ceilometer/meters.d/meters.yaml

# Install systemd units for services
install -p -D -m 644 %{SOURCE11} %{buildroot}%{_unitdir}/%{name}-compute.service
install -p -D -m 644 %{SOURCE12} %{buildroot}%{_unitdir}/%{name}-central.service
install -p -D -m 644 %{SOURCE13} %{buildroot}%{_unitdir}/%{name}-notification.service
install -p -D -m 644 %{SOURCE14} %{buildroot}%{_unitdir}/%{name}-ipmi.service
install -p -D -m 644 %{SOURCE15} %{buildroot}%{_unitdir}/%{name}-polling.service

# Install logrotate
install -p -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

# Install i18n .mo files (.po and .pot are not required)
install -d -m 755 %{buildroot}%{_datadir}
rm -f %{buildroot}%{pyver_sitelib}/%{pypi_name}/locale/*/LC_*/%{pypi_name}*po
rm -f %{buildroot}%{pyver_sitelib}/%{pypi_name}/locale/*pot
mv %{buildroot}%{pyver_sitelib}/%{pypi_name}/locale %{buildroot}%{_datadir}/locale

# Find language files
%find_lang %{pypi_name} --all-name

# Remove unneeded in production stuff
rm -f %{buildroot}/usr/share/doc/ceilometer/README*

# Remove unused files
rm -fr %{buildroot}/usr/etc

%pre common
getent group ceilometer >/dev/null || groupadd -r ceilometer --gid 166
if ! getent passwd ceilometer >/dev/null; then
  # Id reservation request: https://bugzilla.redhat.com/923891
  useradd -u 166 -r -g ceilometer -G ceilometer,nobody -d %{_sharedstatedir}/ceilometer -s /sbin/nologin -c "OpenStack ceilometer Daemons" ceilometer
fi
exit 0

%post compute
%systemd_post %{name}-compute.service

%post notification
%systemd_post %{name}-notification.service

%post central
%systemd_post %{name}-central.service

%post ipmi
%systemd_post %{name}-alarm-ipmi.service

%post polling
%systemd_post %{name}-polling.service

%preun compute
%systemd_preun %{name}-compute.service

%preun notification
%systemd_preun %{name}-notification.service

%preun central
%systemd_preun %{name}-central.service

%preun ipmi
%systemd_preun %{name}-ipmi.service

%preun polling
%systemd_preun %{name}-polling.service

%postun compute
%systemd_postun_with_restart %{name}-compute.service

%postun notification
%systemd_postun_with_restart %{name}-notification.service

%postun central
%systemd_postun_with_restart %{name}-central.service

%postun ipmi
%systemd_postun_with_restart %{name}-ipmi.service


%postun polling
%systemd_postun_with_restart %{name}-polling.service


%files common -f %{pypi_name}.lang
%license LICENSE
%dir %{_sysconfdir}/ceilometer
%attr(-, root, ceilometer) %{_datadir}/ceilometer/ceilometer-dist.conf
%config(noreplace) %attr(-, root, ceilometer) %{_sysconfdir}/ceilometer/ceilometer.conf
%config(noreplace) %attr(-, root, ceilometer) %{_sysconfdir}/ceilometer/pipeline.yaml
%config(noreplace) %attr(-, root, ceilometer) %{_sysconfdir}/ceilometer/polling.yaml
%config(noreplace) %attr(-, root, ceilometer) %{_sysconfdir}/ceilometer/gnocchi_resources.yaml
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}

%dir %attr(0750, ceilometer, root) %{_localstatedir}/log/ceilometer

%{_bindir}/ceilometer-send-sample
%{_bindir}/ceilometer-upgrade
%{_bindir}/ceilometer-status

%defattr(-, ceilometer, ceilometer, -)
%dir %{_sharedstatedir}/ceilometer
%dir %{_sharedstatedir}/ceilometer/tmp


%files -n python%{pyver}-ceilometer
%{pyver_sitelib}/ceilometer
%{pyver_sitelib}/ceilometer-*.egg-info
%exclude %{pyver_sitelib}/ceilometer/tests

%files -n python%{pyver}-ceilometer-tests
%license LICENSE
%{pyver_sitelib}/ceilometer/tests

%if 0%{?with_doc}
%files doc
%doc doc/build/html
%endif


%files compute
%{_unitdir}/%{name}-compute.service


%files notification
%config(noreplace) %attr(-, root, ceilometer) %{_sysconfdir}/ceilometer/event_pipeline.yaml
%config(noreplace) %attr(-, root, ceilometer) %{_sysconfdir}/ceilometer/event_definitions.yaml
%dir %{_sysconfdir}/ceilometer/meters.d
%config(noreplace) %attr(-, root, ceilometer) %{_sysconfdir}/ceilometer/meters.d/meters.yaml
%{_bindir}/ceilometer-agent-notification
%{_unitdir}/%{name}-notification.service


%files central
%{_unitdir}/%{name}-central.service


%files ipmi
%config(noreplace) %attr(-, root, ceilometer) %{_sysconfdir}/ceilometer/rootwrap.conf
%config(noreplace) %attr(-, root, ceilometer) %{_sysconfdir}/ceilometer/rootwrap.d/ipmi.filters
%{_bindir}/ceilometer-rootwrap
%{_sysconfdir}/sudoers.d/ceilometer
%{_unitdir}/%{name}-ipmi.service

%files polling
%{_bindir}/ceilometer-polling
%{_unitdir}/%{name}-polling.service


%changelog
