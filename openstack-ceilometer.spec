%global _without_doc 1
%global with_doc %{!?_without_doc:1}%{?_without_doc:0}

%global release_name kilo
%global service ceilometer

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:             openstack-ceilometer
Version:          2015.1.0
Release:          6%{?milestone}%{?dist}
Summary:          OpenStack measurement collection service

Group:            Applications/System
License:          ASL 2.0
URL:              https://wiki.openstack.org/wiki/Ceilometer
Source0:          http://launchpad.net/%{service}/%{release_name}/%{version}/+download/%{service}-%{upstream_version}.tar.gz

Source1:          %{service}-dist.conf
Source2:          %{service}.logrotate
Source3:          %{service}.conf.sample
Source4:          ceilometer-rootwrap-sudoers
Source5:          openstack-ceilometer-polling

%if 0%{?rhel} && 0%{?rhel} <= 6
Source10:         %{name}-api.init
Source100:        %{name}-api.upstart
Source11:         %{name}-collector.init
Source110:        %{name}-collector.upstart
Source12:         %{name}-compute.init
Source120:        %{name}-compute.upstart
Source13:         %{name}-central.init
Source130:        %{name}-central.upstart
Source14:         %{name}-alarm-notifier.init
Source140:        %{name}-alarm-notifier.upstart
Source15:         %{name}-alarm-evaluator.init
Source150:        %{name}-alarm-evaluator.upstart
Source16:         %{name}-notification.init
Source160:        %{name}-notification.upstart
Source17:         %{name}-ipmi.init
Source170:        %{name}-ipmi.upstart
Source18:         %{name}-polling.init
Source180:        %{name}-polling.upstart
%else
Source10:         %{name}-api.service
Source11:         %{name}-collector.service
Source12:         %{name}-compute.service
Source13:         %{name}-central.service
Source14:         %{name}-alarm-notifier.service
Source15:         %{name}-alarm-evaluator.service
Source16:         %{name}-notification.service
Source17:         %{name}-ipmi.service
Source18:         %{name}-polling.service
%endif

BuildArch:        noarch
BuildRequires:    intltool
BuildRequires:    python-sphinx
BuildRequires:    python-setuptools
BuildRequires:    python-pbr
BuildRequires:    python-d2to1
BuildRequires:    python2-devel

%if ! (0%{?rhel} && 0%{?rhel} <= 6)
BuildRequires: systemd-units
%endif

%description
OpenStack ceilometer provides services to measure and
collect metrics from OpenStack components.


%package -n       python-ceilometer
Summary:          OpenStack ceilometer python libraries
Group:            Applications/System

Requires:         python-babel
Requires:         python-eventlet
Requires:         python-greenlet
Requires:         python-iso8601
Requires:         python-lxml
Requires:         python-anyjson
Requires:         python-jsonpath-rw
Requires:         python-stevedore >= 1.0.0
Requires:         python-msgpack
Requires:         python-six >= 1.6

Requires:         python-sqlalchemy
Requires:         python-alembic
Requires:         python-migrate

Requires:         python-webob
Requires:         python-oslo-config >= 2:1.4.0
Requires:         PyYAML
Requires:         python-netaddr
Requires:         python-oslo-config >= 2:1.4.0
Requires:         python-oslo-rootwrap
Requires:         python-oslo-vmware >= 0.6.0
Requires:         python-requests >= 1.2.1

Requires:         pysnmp
Requires:         pytz
Requires:         python-croniter

Requires:         python-retrying
Requires:         python-jsonschema
Requires:         python-werkzeug

Requires:         python-oslo-context
Requires:         python-oslo-concurrency
Requires:         python-oslo-i18n
Requires:         python-oslo-middleware


%description -n   python-ceilometer
OpenStack ceilometer provides services to measure and
collect metrics from OpenStack components.

This package contains the ceilometer python library.


%package common
Summary:          Components common to all OpenStack ceilometer services
Group:            Applications/System

Requires:         python-ceilometer = %{version}-%{release}
Requires:         openstack-utils
Requires:         python-oslo-messaging
Requires:         python-oslo-serialization
Requires:         python-oslo-utils
Requires:         python-posix_ipc

%if 0%{?rhel} && 0%{?rhel} <= 6
Requires(post):   chkconfig
Requires(postun): initscripts
Requires(preun):  chkconfig
%else
Requires(post):   systemd-units
Requires(preun):  systemd-units
Requires(postun): systemd-units
%endif
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
Requires:         python-tooz
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
Requires:         python-neutronclient
Requires:         python-tooz

%description central
OpenStack ceilometer provides services to measure and
collect metrics from OpenStack components.

This package contains the central ceilometer agent.


%package collector
Summary:          OpenStack ceilometer collector
Group:            Applications/System

Requires:         %{name}-common = %{version}-%{release}

# For compat with older provisioning tools.
# Remove when all reference the notification package explicitly
Requires:         %{name}-notification

Requires:         python-oslo-db
Requires:         python-pymongo

%description collector
OpenStack ceilometer provides services to measure and
collect metrics from OpenStack components.

This package contains the ceilometer collector service
which collects metrics from the various agents.


%package notification
Summary:          OpenStack ceilometer notification agent
Group:            Applications/System

Requires:         %{name}-common = %{version}-%{release}

%description notification
OpenStack ceilometer provides services to measure and
collect metrics from OpenStack components.

This package contains the ceilometer notification agent
which pushes metrics to the collector service from the
various OpenStack services.


%package api
Summary:          OpenStack ceilometer API service
Group:            Applications/System

Requires:         %{name}-common = %{version}-%{release}

Requires:         python-keystonemiddleware
Requires:         python-oslo-db
Requires:         python-pymongo
Requires:         python-pecan >= 0.4.5
Requires:         python-wsme >= 0.6
Requires:         python-paste-deploy
Requires:         python-ceilometerclient
Requires:         python-tooz

%description api
OpenStack ceilometer provides services to measure and
collect metrics from OpenStack components.

This package contains the ceilometer API service.


%package alarm
Summary:          OpenStack ceilometer alarm services
Group:            Applications/System

Requires:         %{name}-common = %{version}-%{release}
Requires:         python-ceilometerclient

%description alarm
OpenStack ceilometer provides services to measure and
collect metrics from OpenStack components.

This package contains the ceilometer alarm notification
and evaluation services.


%package ipmi
Summary:          OpenStack ceilometer ipmi agent
Group:            Applications/System

Requires:         %{name}-common = %{version}-%{release}

Requires:         python-novaclient
Requires:         python-keystoneclient
Requires:         python-neutronclient
Requires:         python-tooz
Requires:         python-oslo-rootwrap
Requires:         ipmitool

%description ipmi
OpenStack ceilometer provides services to measure and
collect metrics from OpenStack components.

This package contains the ipmi agent to be run on OpenStack
nodes from which IPMI sensor data is to be collected directly,
by-passing Ironic's management of baremetal.


%package polling
Summary:          OpenStack ceilometer polling agent
Group:            Applications/System

Requires:         %{name}-common = %{version}-%{release}

Requires:         python-novaclient >= 2.18.0
Requires:         python-keystoneclient >= 0.11.1
Requires:         python-glanceclient >= 0.14.0
Requires:         python-swiftclient >= 2.2.0
Requires:         libvirt-python

%description polling
Ceilometer aims to deliver a unique point of contact for billing systems to
aquire all counters they need to establish customer billing, across all
current and future OpenStack components. The delivery of counters must
be tracable and auditable, the counters must be easily extensible to support
new projects, and agents doing data collections should be
independent of the overall system.

This package contains the polling service.


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
%setup -q -n ceilometer-%{upstream_version}

find . \( -name .gitignore -o -name .placeholder \) -delete

find ceilometer -name \*.py -exec sed -i '/\/usr\/bin\/env python/{d;q}' {} +

# TODO: Have the following handle multi line entries
sed -i '/setup_requires/d; /install_requires/d; /dependency_links/d' setup.py

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
rm -rf {test-,}requirements.txt tools/{pip,test}-requires

%build
%{__python} setup.py build

install -p -D -m 640 %{SOURCE3} etc/ceilometer/ceilometer.conf.sample

# Programmatically update defaults in sample config
# which is installed at /etc/ceilometer/ceilometer.conf
# TODO: Make this more robust
# Note it only edits the first occurance, so assumes a section ordering in sample
# and also doesn't support multi-valued variables.
while read name eq value; do
  test "$name" && test "$value" || continue
  sed -i "0,/^# *$name=/{s!^# *$name=.*!#$name=$value!}" etc/ceilometer/ceilometer.conf.sample
done < %{SOURCE1}

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
install -d -m 755 %{buildroot}%{_sysconfdir}/ceilometer/rootwrap.d
install -d -m 755 %{buildroot}%{_sysconfdir}/sudoers.d
install -d -m 755 %{buildroot}%{_sysconfdir}/sysconfig/ceilometer
install -p -D -m 640 %{SOURCE1} %{buildroot}%{_datadir}/ceilometer/ceilometer-dist.conf
install -p -D -m 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/sudoers.d/ceilometer
install -p -D -m 644 %{SOURCE5} %{buildroot}%{_sysconfdir}/sysconfig/ceilometer/openstack-ceilometer-polling
install -p -D -m 640 etc/ceilometer/ceilometer.conf.sample %{buildroot}%{_sysconfdir}/ceilometer/ceilometer.conf
install -p -D -m 640 etc/ceilometer/policy.json %{buildroot}%{_sysconfdir}/ceilometer/policy.json
install -p -D -m 640 etc/ceilometer/pipeline.yaml %{buildroot}%{_sysconfdir}/ceilometer/pipeline.yaml
install -p -D -m 640 etc/ceilometer/event_pipeline.yaml %{buildroot}%{_sysconfdir}/ceilometer/event_pipeline.yaml
install -p -D -m 640 etc/ceilometer/event_definitions.yaml %{buildroot}%{_sysconfdir}/ceilometer/event_definitions.yaml
install -p -D -m 640 etc/ceilometer/api_paste.ini %{buildroot}%{_sysconfdir}/ceilometer/api_paste.ini
install -p -D -m 640 etc/ceilometer/rootwrap.conf %{buildroot}%{_sysconfdir}/ceilometer/rootwrap.conf
install -p -D -m 640 etc/ceilometer/rootwrap.d/ipmi.filters %{buildroot}/%{_sysconfdir}/ceilometer/rootwrap.d/ipmi.filters

# Install initscripts for services
%if 0%{?rhel} && 0%{?rhel} <= 6
install -p -D -m 755 %{SOURCE10} %{buildroot}%{_initrddir}/%{name}-api
install -p -D -m 755 %{SOURCE11} %{buildroot}%{_initrddir}/%{name}-collector
install -p -D -m 755 %{SOURCE12} %{buildroot}%{_initrddir}/%{name}-compute
install -p -D -m 755 %{SOURCE13} %{buildroot}%{_initrddir}/%{name}-central
install -p -D -m 755 %{SOURCE14} %{buildroot}%{_initrddir}/%{name}-alarm-notifier
install -p -D -m 755 %{SOURCE15} %{buildroot}%{_initrddir}/%{name}-alarm-evaluator
install -p -D -m 755 %{SOURCE16} %{buildroot}%{_initrddir}/%{name}-notification
install -p -D -m 755 %{SOURCE17} %{buildroot}%{_initrddir}/%{name}-ipmi
install -p -D -m 755 %{SOURCE18} %{buildroot}%{_initrddir}/%{name}-polling

# Install upstart jobs examples
install -d -m 755 %{buildroot}%{_datadir}/ceilometer
install -p -m 644 %{SOURCE100} %{buildroot}%{_datadir}/ceilometer/
install -p -m 644 %{SOURCE110} %{buildroot}%{_datadir}/ceilometer/
install -p -m 644 %{SOURCE120} %{buildroot}%{_datadir}/ceilometer/
install -p -m 644 %{SOURCE130} %{buildroot}%{_datadir}/ceilometer/
install -p -m 644 %{SOURCE140} %{buildroot}%{_datadir}/ceilometer/
install -p -m 644 %{SOURCE150} %{buildroot}%{_datadir}/ceilometer/
install -p -m 644 %{SOURCE160} %{buildroot}%{_datadir}/ceilometer/
install -p -m 644 %{SOURCE170} %{buildroot}%{_datadir}/ceilometer/
install -p -m 644 %{SOURCE180} %{buildroot}%{_datadir}/ceilometer/
%else
install -p -D -m 644 %{SOURCE10} %{buildroot}%{_unitdir}/%{name}-api.service
install -p -D -m 644 %{SOURCE11} %{buildroot}%{_unitdir}/%{name}-collector.service
install -p -D -m 644 %{SOURCE12} %{buildroot}%{_unitdir}/%{name}-compute.service
install -p -D -m 644 %{SOURCE13} %{buildroot}%{_unitdir}/%{name}-central.service
install -p -D -m 644 %{SOURCE14} %{buildroot}%{_unitdir}/%{name}-alarm-notifier.service
install -p -D -m 644 %{SOURCE15} %{buildroot}%{_unitdir}/%{name}-alarm-evaluator.service
install -p -D -m 644 %{SOURCE16} %{buildroot}%{_unitdir}/%{name}-notification.service
install -p -D -m 644 %{SOURCE17} %{buildroot}%{_unitdir}/%{name}-ipmi.service
install -p -D -m 644 %{SOURCE18} %{buildroot}%{_unitdir}/%{name}-polling.service
%endif

# Install logrotate
install -p -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

%if 0%{?rhel} && 0%{?rhel} <= 6
# Install pid directory
install -d -m 755 %{buildroot}%{_localstatedir}/run/ceilometer
%endif

# Remove unneeded in production stuff
rm -f %{buildroot}%{_bindir}/ceilometer-debug
rm -fr %{buildroot}%{python_sitelib}/tests/
rm -fr %{buildroot}%{python_sitelib}/run_tests.*
rm -f %{buildroot}/usr/share/doc/ceilometer/README*


%pre common
getent group ceilometer >/dev/null || groupadd -r ceilometer --gid 166
if ! getent passwd ceilometer >/dev/null; then
  # Id reservation request: https://bugzilla.redhat.com/923891
  useradd -u 166 -r -g ceilometer -G ceilometer,nobody -d %{_sharedstatedir}/ceilometer -s /sbin/nologin -c "OpenStack ceilometer Daemons" ceilometer
fi
exit 0

%post compute
%if 0%{?rhel} && 0%{?rhel} <= 6
if [ $1 -eq 1 ] ; then
    # Initial installation
    /sbin/chkconfig --add %{name}-compute
fi
%else
%systemd_post %{name}-compute.service
%endif

%post collector
%if 0%{?rhel} && 0%{?rhel} <= 6
if [ $1 -eq 1 ] ; then
    # Initial installation
    /sbin/chkconfig --add %{name}-collector
fi
%else
%systemd_post %{name}-collector.service
%endif

%post notification
%if 0%{?rhel} && 0%{?rhel} <= 6
if [ $1 -eq 1 ] ; then
    # Initial installation
    /sbin/chkconfig --add %{name}-notification
fi
%else
%systemd_post %{name}-notification.service
%endif

%post api
%if 0%{?rhel} && 0%{?rhel} <= 6
if [ $1 -eq 1 ] ; then
    # Initial installation
    /sbin/chkconfig --add %{name}-api
fi
%else
%systemd_post %{name}-api.service
%endif

%post central
%if 0%{?rhel} && 0%{?rhel} <= 6
if [ $1 -eq 1 ] ; then
    # Initial installation
    /sbin/chkconfig --add %{name}-central
fi
%else
%systemd_post %{name}-central.service
%endif

%post alarm
%if 0%{?rhel} && 0%{?rhel} <= 6
if [ $1 -eq 1 ] ; then
    # Initial installation
    for svc in alarm-notifier alarm-evaluator; do
        /sbin/chkconfig --add %{name}-${svc}
    done
fi
%else
%systemd_post %{name}-alarm-notifier.service %{name}-alarm-evaluator.service
%endif

%post ipmi
%if 0%{?rhel} && 0%{?rhel} <= 6
if [ $1 -eq 1 ] ; then
    # Initial installation
    /sbin/chkconfig --add %{name}-ipmi
fi
%else
%systemd_post %{name}-alarm-ipmi.service
%endif

%post polling
%if 0%{?rhel} && 0%{?rhel} <= 6
if [ $1 -eq 1 ] ; then
    # Initial installation
    /sbin/chkconfig --add %{name}-polling
fi
%else
%systemd_post %{name}-polling.service
%endif

%preun compute
%if 0%{?rhel} && 0%{?rhel} <= 6
if [ $1 -eq 0 ] ; then
    for svc in compute; do
        /sbin/service %{name}-${svc} stop > /dev/null 2>&1
        /sbin/chkconfig --del %{name}-${svc}
    done
fi
%else
%systemd_preun %{name}-compute.service
%endif

%preun collector
%if 0%{?rhel} && 0%{?rhel} <= 6
if [ $1 -eq 0 ] ; then
    for svc in collector; do
        /sbin/service %{name}-${svc} stop > /dev/null 2>&1
        /sbin/chkconfig --del %{name}-${svc}
    done
fi
%else
%systemd_preun %{name}-collector.service
%endif

%preun notification
%if 0%{?rhel} && 0%{?rhel} <= 6
if [ $1 -eq 0 ] ; then
    for svc in notification; do
        /sbin/service %{name}-${svc} stop > /dev/null 2>&1
        /sbin/chkconfig --del %{name}-${svc}
    done
fi
%else
%systemd_preun %{name}-notification.service
%endif

%preun api
%if 0%{?rhel} && 0%{?rhel} <= 6
if [ $1 -eq 0 ] ; then
    for svc in api; do
        /sbin/service %{name}-${svc} stop > /dev/null 2>&1
        /sbin/chkconfig --del %{name}-${svc}
    done
fi
%else
%systemd_preun %{name}-api.service
%endif

%preun central
%if 0%{?rhel} && 0%{?rhel} <= 6
if [ $1 -eq 0 ] ; then
    for svc in central; do
        /sbin/service %{name}-${svc} stop > /dev/null 2>&1
        /sbin/chkconfig --del %{name}-${svc}
    done
fi
%else
%systemd_preun %{name}-central.service
%endif

%preun alarm
%if 0%{?rhel} && 0%{?rhel} <= 6
if [ $1 -eq 0 ] ; then
    for svc in alarm-notifier alarm-evaluator; do
        /sbin/service %{name}-${svc} stop > /dev/null 2>&1
        /sbin/chkconfig --del %{name}-${svc}
    done
fi
%else
%systemd_preun %{name}-alarm-notifier.service %{name}-alarm-evaluator.service
%endif

%preun ipmi
%if 0%{?rhel} && 0%{?rhel} <= 6
if [ $1 -eq 0 ] ; then
    for svc in ipmi; do
        /sbin/service %{name}-${svc} stop > /dev/null 2>&1
        /sbin/chkconfig --del %{name}-${svc}
    done
fi
%else
%systemd_preun %{name}-ipmi.service
%endif

%preun polling
%if 0%{?rhel} && 0%{?rhel} <= 6
if [ $1 -eq 0 ] ; then
    for svc in polling; do
        /sbin/service %{name}-${svc} stop > /dev/null 2>&1
        /sbin/chkconfig --del %{name}-${svc}
    done
fi
%else
%systemd_preun %{name}-polling.service
%endif

%postun compute
%if 0%{?rhel} && 0%{?rhel} <= 6
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    for svc in compute; do
        /sbin/service %{name}-${svc} condrestart > /dev/null 2>&1 || :
    done
fi
%else
%systemd_postun_with_restart %{name}-compute.service
%endif

%postun collector
%if 0%{?rhel} && 0%{?rhel} <= 6
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    for svc in collector; do
        /sbin/service %{name}-${svc} condrestart > /dev/null 2>&1 || :
    done
fi
%else
%systemd_postun_with_restart %{name}-collector.service
%endif

%postun notification
%if 0%{?rhel} && 0%{?rhel} <= 6
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    for svc in notification; do
        /sbin/service %{name}-${svc} condrestart > /dev/null 2>&1 || :
    done
fi
%else
%systemd_postun_with_restart %{name}-notification.service
%endif

%postun api
%if 0%{?rhel} && 0%{?rhel} <= 6
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    for svc in api; do
        /sbin/service %{name}-${svc} condrestart > /dev/null 2>&1 || :
    done
fi
%else
%systemd_postun_with_restart %{name}-api.service
%endif

%postun central
%if 0%{?rhel} && 0%{?rhel} <= 6
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    for svc in central; do
        /sbin/service %{name}-${svc} condrestart > /dev/null 2>&1 || :
    done
fi
%else
%systemd_postun_with_restart %{name}-central.service
%endif

%postun alarm
%if 0%{?rhel} && 0%{?rhel} <= 6
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    for svc in alarm-notifier alarm-evaluator; do
        /sbin/service %{name}-${svc} condrestart > /dev/null 2>&1 || :
    done
fi
%else
%systemd_postun_with_restart %{name}-alarm-notifier.service %{name}-alarm-evaluator.service
%endif

%postun ipmi
%if 0%{?rhel} && 0%{?rhel} <= 6
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    for svc in ipmi; do
        /sbin/service %{name}-${svc} condrestart > /dev/null 2>&1 || :
    done
fi
%else
%systemd_postun_with_restart %{name}-ipmi.service
%endif


%postun polling
%if 0%{?rhel} && 0%{?rhel} <= 6
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    for svc in polling; do
        /sbin/service %{name}-${svc} condrestart > /dev/null 2>&1 || :
    done
fi
%else
%systemd_postun_with_restart %{name}-polling.service
%endif


%files common
%doc LICENSE
%dir %{_sysconfdir}/ceilometer
%attr(-, root, ceilometer) %{_datadir}/ceilometer/ceilometer-dist.conf
%config(noreplace) %attr(-, root, ceilometer) %{_sysconfdir}/ceilometer/ceilometer.conf
%config(noreplace) %attr(-, root, ceilometer) %{_sysconfdir}/ceilometer/policy.json
%config(noreplace) %attr(-, root, ceilometer) %{_sysconfdir}/ceilometer/pipeline.yaml
%config(noreplace) %attr(-, root, ceilometer) %{_sysconfdir}/ceilometer/api_paste.ini
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}

%dir %attr(0755, ceilometer, root) %{_localstatedir}/log/ceilometer
%if 0%{?rhel} && 0%{?rhel} <= 6
%dir %attr(0755, ceilometer, root) %{_localstatedir}/run/ceilometer
%endif

%{_bindir}/ceilometer-dbsync
%{_bindir}/ceilometer-expirer
%{_bindir}/ceilometer-send-sample


%defattr(-, ceilometer, ceilometer, -)
%dir %{_sharedstatedir}/ceilometer
%dir %{_sharedstatedir}/ceilometer/tmp


%files -n python-ceilometer
%{python_sitelib}/ceilometer
%{python_sitelib}/ceilometer-*.egg-info


%if 0%{?with_doc}
%files doc
%doc doc/build/html
%endif


%files compute
%{_bindir}/ceilometer-agent-compute
%if 0%{?rhel} && 0%{?rhel} <= 6
%{_initrddir}/%{name}-compute
%{_datarootdir}/ceilometer/%{name}-compute.upstart
%else
%{_unitdir}/%{name}-compute.service
%endif


%files collector
%{_bindir}/ceilometer-collector*
%if 0%{?rhel} && 0%{?rhel} <= 6
%{_initrddir}/%{name}-collector
%{_datarootdir}/ceilometer/%{name}-collector.upstart
%else
%{_unitdir}/%{name}-collector.service
%endif


%files notification
%config(noreplace) %attr(-, root, ceilometer) %{_sysconfdir}/ceilometer/event_pipeline.yaml
%config(noreplace) %attr(-, root, ceilometer) %{_sysconfdir}/ceilometer/event_definitions.yaml
%{_bindir}/ceilometer-agent-notification
%if 0%{?rhel} && 0%{?rhel} <= 6
%{_initrddir}/%{name}-notification
%{_datarootdir}/ceilometer/%{name}-notification.upstart
%else
%{_unitdir}/%{name}-notification.service
%endif


%files api
%{_bindir}/ceilometer-api
%if 0%{?rhel} && 0%{?rhel} <= 6
%{_initrddir}/%{name}-api
%{_datarootdir}/ceilometer/%{name}-api.upstart
%else
%{_unitdir}/%{name}-api.service
%endif


%files central
%{_bindir}/ceilometer-agent-central
%if 0%{?rhel} && 0%{?rhel} <= 6
%{_initrddir}/%{name}-central
%{_datarootdir}/ceilometer/%{name}-central.upstart
%else
%{_unitdir}/%{name}-central.service
%endif


%files alarm
%{_bindir}/ceilometer-alarm-notifier
%{_bindir}/ceilometer-alarm-evaluator
%if 0%{?rhel} && 0%{?rhel} <= 6
%{_initrddir}/%{name}-alarm-notifier
%{_datarootdir}/ceilometer/%{name}-alarm-notifier.upstart
%{_initrddir}/%{name}-alarm-evaluator
%{_datarootdir}/ceilometer/%{name}-alarm-evaluator.upstart
%else
%{_unitdir}/%{name}-alarm-notifier.service
%{_unitdir}/%{name}-alarm-evaluator.service
%endif


%files ipmi
%config(noreplace) %attr(-, root, ceilometer) %{_sysconfdir}/ceilometer/rootwrap.conf
%config(noreplace) %attr(-, root, ceilometer) %{_sysconfdir}/ceilometer/rootwrap.d/ipmi.filters
%{_bindir}/ceilometer-rootwrap
%{_bindir}/ceilometer-agent-ipmi
%{_sysconfdir}/sudoers.d/ceilometer
%if 0%{?rhel} && 0%{?rhel} <= 6
%{_initrddir}/%{name}-ipmi
%{_datarootdir}/ceilometer/%{name}-ipmi.upstart
%else
%{_unitdir}/%{name}-ipmi.service
%endif


%files polling
%{_bindir}/ceilometer-polling
%attr(-, root, ceilometer) %{_sysconfdir}/sysconfig/ceilometer/openstack-ceilometer-polling
%if 0%{?rhel} && 0%{?rhel} <= 6
%{_initrddir}/%{name}-polling
%{_datarootdir}/ceilometer/%{name}-polling.upstart
%else
%{_unitdir}/%{name}-polling.service
%endif


%changelog
* Mon Jul 13 2015 Pradeep Kilambi <pkilambi@redhat.com> 2015.1.0-6
- fix env file missing error in openstack-ceilometer-polling.service rhbz#1240740

* Tue Jul 07 2015 Pradeep Kilambi <pkilambi@redhat.com> 2015.1.0-5
- fix env file missing error in openstack-ceilometer-polling.service rhbz#1240740

* Wed Jun 24 2015 Pradeep Kilambi <pkilambi@redhat.com> 2015.1.0-4
- include event_definitions.yaml in notification sub-package rhbz#1221924

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2015.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri May 08 2015 Alan Pevec <alan.pevec@redhat.com> 2015.1.0-2
- include event_pipeline.yaml in notification sub-package rhbz#1219381

* Thu Apr 30 2015 Alan Pevec <alan.pevec@redhat.com> 2015.1.0-1
- OpenStack Kilo release
