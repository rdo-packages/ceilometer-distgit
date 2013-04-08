%global _without_doc 1
%global with_doc %{!?_without_doc:1}%{?_without_doc:0}
%global pypi_name ceilometer

Name:             openstack-ceilometer
Version:          2013.1
Release:          1%{?dist}
Summary:          OpenStack measurement collection service

Group:            Applications/System
License:          ASL 2.0
URL:              https://wiki.openstack.org/wiki/Ceilometer
Source0:          http://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-2013.1.tar.gz
Source1:          %{pypi_name}.conf
Source2:          %{pypi_name}.logrotate

Source10:         %{name}-api.service
Source11:         %{name}-collector.service
Source12:         %{name}-compute.service
Source13:         %{name}-central.service

#
# patches_base=2013.1
#
Patch0001: 0001-Ensure-we-don-t-access-the-net-when-building-docs.patch

BuildArch:        noarch
BuildRequires:    intltool
BuildRequires:    python-sphinx
BuildRequires:    python-setuptools
BuildRequires:    python2-devel

BuildRequires:    openstack-utils


%description
OpenStack ceilometer provides services to measure and
collect metrics from OpenStack components.


%package -n       python-ceilometer
Summary:          OpenStack ceilometer python libraries
Group:            Applications/System

Requires:         python-qpid
Requires:         python-kombu
Requires:         python-amqplib

Requires:         python-eventlet
Requires:         python-greenlet
Requires:         python-iso8601
Requires:         python-lxml
Requires:         python-anyjson
Requires:         python-stevedore

Requires:         python-sqlalchemy
Requires:         python-migrate

Requires:         python-webob
Requires:         python-oslo-config
Requires:         PyYAML

%description -n   python-ceilometer
OpenStack ceilometer provides services to measure and
collect metrics from OpenStack components.

This package contains the ceilometer python library.


%package common
Summary:          Components common to all OpenStack ceilometer services
Group:            Applications/System

Requires:         python-ceilometer = %{version}-%{release}
Requires:         openstack-utils

Requires(post):   systemd-units
Requires(preun):  systemd-units
Requires(postun): systemd-units
Requires(pre):    shadow-utils



%description common
OpenStack ceilometer provides services to measure and
collect metrics from OpenStack components.

This package contains components common to all OpenStack
ceilometer services.


%package compute
Summary:          OpenStack ceilometer compute agent
Group:            Applications/System

Requires:         %{name}-common = %{version}-%{release}

Requires:         python-novaclient
Requires:         python-keystoneclient
Requires:         libvirt-python

%description compute
OpenStack ceilometer provides services to measure and
collect metrics from OpenStack components.

This package contains the ceilometer agent for
running on OpenStack compute nodes.


%package central
Summary:          OpenStack ceilometer central agent
Group:            Applications/System

Requires:         %{name}-common = %{version}-%{release}

Requires:         python-novaclient
Requires:         python-keystoneclient
Requires:         python-glanceclient
Requires:         python-swiftclient

%description central
OpenStack ceilometer provides services to measure and
collect metrics from OpenStack components.

This package contains the central ceilometer agent.


%package collector
Summary:          OpenStack ceilometer collector agent
Group:            Applications/System

Requires:         %{name}-common = %{version}-%{release}

Requires:         pymongo

%description collector
OpenStack ceilometer provides services to measure and
collect metrics from OpenStack components.

This package contains the ceilometer collector agent.


%package api
Summary:          OpenStack ceilometer API service
Group:            Applications/System

Requires:         %{name}-common = %{version}-%{release}

Requires:         pymongo
Requires:         python-flask
Requires:         python-pecan
Requires:         python-wsme

%description api
OpenStack ceilometer provides services to measure and
collect metrics from OpenStack components.

This package contains the ceilometer API service.


%if 0%{?with_doc}
%package doc
Summary:          Documentation for OpenStack ceilometer
Group:            Documentation

# Required to build module documents
BuildRequires:    python-eventlet
BuildRequires:    python-sqlalchemy
BuildRequires:    python-webob
# while not strictly required, quiets the build down when building docs.
BuildRequires:    python-migrate, python-iso8601

%description      doc
OpenStack ceilometer provides services to measure and
collect metrics from OpenStack components.

This package contains documentation files for ceilometer.
%endif

%prep
%setup -q -n ceilometer-%{version}

%patch0001 -p1

find . \( -name .gitignore -o -name .placeholder \) -delete

find ceilometer -name \*.py -exec sed -i '/\/usr\/bin\/env python/{d;q}' {} +

# TODO: Have the following handle multi line entries
sed -i '/setup_requires/d; /install_requires/d; /dependency_links/d' setup.py

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# docs generation requires everything to be installed first
export PYTHONPATH="$( pwd ):$PYTHONPATH"

pushd doc

%if 0%{?with_doc}
SPHINX_DEBUG=1 sphinx-build -b html source build/html
# Fix hidden-file-or-dir warnings
rm -fr build/html/.doctrees build/html/.buildinfo
%endif

popd

# Setup directories
install -d -m 755 %{buildroot}%{_sharedstatedir}/ceilometer
install -d -m 755 %{buildroot}%{_sharedstatedir}/ceilometer/tmp
install -d -m 755 %{buildroot}%{_localstatedir}/log/ceilometer

# Install config files
install -d -m 755 %{buildroot}%{_sysconfdir}/ceilometer
install -p -D -m 640 %{SOURCE1} %{buildroot}%{_sysconfdir}/ceilometer/ceilometer.conf
install -p -D -m 640 etc/ceilometer/policy.json %{buildroot}%{_sysconfdir}/ceilometer/policy.json
install -p -D -m 640 etc/ceilometer/sources.json %{buildroot}%{_sysconfdir}/ceilometer/sources.json
install -p -D -m 640 etc/ceilometer/pipeline.yaml %{buildroot}%{_sysconfdir}/ceilometer/pipeline.yaml

# Install initscripts for services
install -p -D -m 644 %{SOURCE10} %{buildroot}%{_unitdir}/%{name}-api.service
install -p -D -m 644 %{SOURCE11} %{buildroot}%{_unitdir}/%{name}-collector.service
install -p -D -m 644 %{SOURCE12} %{buildroot}%{_unitdir}/%{name}-compute.service
install -p -D -m 644 %{SOURCE13} %{buildroot}%{_unitdir}/%{name}-central.service

# Install logrotate
install -p -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

# Remove unneeded in production stuff
rm -f %{buildroot}%{_bindir}/ceilometer-debug
rm -fr %{buildroot}%{python_sitelib}/tests/
rm -fr %{buildroot}%{python_sitelib}/run_tests.*
rm -f %{buildroot}/usr/share/doc/ceilometer/README*
rm -f %{buildroot}/%{python_sitelib}/ceilometer/api/v1/static/LICENSE.*


%pre common
getent group ceilometer >/dev/null || groupadd -r ceilometer --gid 166
if ! getent passwd ceilometer >/dev/null; then
  # Id reservation request: https://bugzilla.redhat.com/923891
  useradd -u 166 -r -g ceilometer -G ceilometer,nobody -d %{_sharedstatedir}/ceilometer -s /sbin/nologin -c "OpenStack ceilometer Daemons" ceilometer
fi
exit 0

%post compute
if [ $1 -eq 1 ] ; then
    # Initial installation
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

%post collector
if [ $1 -eq 1 ] ; then
    # Initial installation
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

%post api
if [ $1 -eq 1 ] ; then
    # Initial installation
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

%post central
if [ $1 -eq 1 ] ; then
    # Initial installation
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

%preun compute
if [ $1 -eq 0 ] ; then
    for svc in compute; do
        /bin/systemctl --no-reload disable %{name}-${svc}.service > /dev/null 2>&1 || :
        /bin/systemctl stop %{name}-${svc}.service > /dev/null 2>&1 || :
    done
fi

%preun collector
if [ $1 -eq 0 ] ; then
    for svc in collector; do
        /bin/systemctl --no-reload disable %{name}-${svc}.service > /dev/null 2>&1 || :
        /bin/systemctl stop %{name}-${svc}.service > /dev/null 2>&1 || :
    done
fi

%preun api
if [ $1 -eq 0 ] ; then
    for svc in api; do
        /bin/systemctl --no-reload disable %{name}-${svc}.service > /dev/null 2>&1 || :
        /bin/systemctl stop %{name}-${svc}.service > /dev/null 2>&1 || :
    done
fi

%preun central
if [ $1 -eq 0 ] ; then
    for svc in agent; do
        /bin/systemctl --no-reload disable %{name}-${svc}.service > /dev/null 2>&1 || :
        /bin/systemctl stop %{name}-${svc}.service > /dev/null 2>&1 || :
    done
fi

%postun compute
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    for svc in compute; do
        /bin/systemctl try-restart %{name}-${svc}.service >/dev/null 2>&1 || :
    done
fi

%postun collector
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    for svc in collector; do
        /bin/systemctl try-restart %{name}-${svc}.service >/dev/null 2>&1 || :
    done
fi

%postun api
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    for svc in api; do
        /bin/systemctl try-restart %{name}-${svc}.service >/dev/null 2>&1 || :
    done
fi

%postun central
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    for svc in central; do
        /bin/systemctl try-restart %{name}-${svc}.service >/dev/null 2>&1 || :
    done
fi


%files common
%doc LICENSE
%dir %{_sysconfdir}/ceilometer
%config(noreplace) %attr(-, root, ceilometer) %{_sysconfdir}/ceilometer/ceilometer.conf
%config(noreplace) %attr(-, root, ceilometer) %{_sysconfdir}/ceilometer/policy.json
%config(noreplace) %attr(-, root, ceilometer) %{_sysconfdir}/ceilometer/sources.json
%config(noreplace) %attr(-, root, ceilometer) %{_sysconfdir}/ceilometer/pipeline.yaml
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}

%dir %attr(0755, ceilometer, root) %{_localstatedir}/log/ceilometer

%{_bindir}/ceilometer-*

%defattr(-, ceilometer, ceilometer, -)
%dir %{_sharedstatedir}/ceilometer
%dir %{_sharedstatedir}/ceilometer/tmp


%files -n python-ceilometer
%{python_sitelib}/ceilometer
%{python_sitelib}/ceilometer-%{version}*.egg-info


%if 0%{?with_doc}
%files doc
%doc doc/build/html
%endif


%files compute
%{_bindir}/ceilometer-agent-compute
%{_unitdir}/%{name}-compute.service


%files collector
%{_bindir}/ceilometer-collector
%{_unitdir}/%{name}-collector.service


%files api
%doc ceilometer/api/v1/static/LICENSE.*
%{_bindir}/ceilometer-api
%{_unitdir}/%{name}-api.service


%files central
%{_bindir}/ceilometer-agent-central
%{_unitdir}/%{name}-central.service


%changelog
* Mon Apr  8 2013 Pádraig Brady <P@draigBrady.com> - 2013.1-1
- Grizzly release

* Tue Mar 26 2013 Pádraig Brady <P@draigBrady.com> - 2013.1-0.5.g3
- Initial package
