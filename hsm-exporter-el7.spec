Name:	  hsm-exporter
Version:  0.0.1
%global gittag 0.0.1
Release:  1%{?dist}
Summary:  Prometheus exporter for HSM stats on Lustre

License:  Apache License 2.0
URL:      https://github.com/guilbaults/hsm-exporter
Source0:  https://github.com/guilbaults/%{name}/archive/v%{gittag}/%{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:	systemd
Requires:       python2-prometheus_client

%description
Prometheus exporter for HSM stats on Lustre MDS. This is to add some missing data to https://github.com/HewlettPackard/lustre_exporter

%prep
%autosetup -n %{name}-%{gittag}
%setup -q

%build

%install
mkdir -p %{buildroot}/%{_bindir}
mkdir -p %{buildroot}/%{_unitdir}

sed -i -e '1i#!/usr/bin/python' hsm-exporter.py
install -m 0755 %{name}.py %{buildroot}/%{_bindir}/%{name}
install -m 0644 infiniband-exporter.service %{buildroot}/%{_unitdir}/hsm-exporter.service

%clean
rm -rf $RPM_BUILD_ROOT

%files
%{_bindir}/%{name}
%{_unitdir}/hsm-exporter.service

%changelog
* Thu Aug 27 2020 Simon Guilbault <simon.guilbault@calculquebec.ca> 0.0.1-1
- Initial release
