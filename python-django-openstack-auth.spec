%global pypi_name django_openstack_auth


%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:           python-django-openstack-auth
Version:        2.2.0
Release:        1%{?dist}
Summary:        Django authentication backend for OpenStack Keystone

License:        BSD
URL:            http://pypi.python.org/pypi/django_openstack_auth/
Source0:        http://tarballs.openstack.org/django_openstack_auth/django_openstack_auth-%{version}%{?milestone}.tar.gz

BuildArch:      noarch
 
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-sphinx
BuildRequires:  python-mox
BuildRequires:  python-keystoneclient
BuildRequires:  python-iso8601
BuildRequires:  python-pbr
BuildRequires:  python-netaddr
BuildRequires:  python-oslo-sphinx >= 2.5.0
BuildRequires:  python-babel
BuildRequires:  python-django

Requires:   python-django
Requires:   python-pbr
Requires:   python-oslo-config >= 1.9.3
Requires:   python-keystoneclient >= 1.1.0
Requires:   python-six >= 1.9.0
Requires:   python-oslo-policy >= 0.3.1


%description
Django OpenStack Auth is a pluggable Django authentication backend that
works with Django's ``contrib.auth`` framework to authenticate a user against
OpenStack's Keystone Identity API.

The current version is designed to work with the
Keystone V2 API.

%prep
%setup -q -n %{pypi_name}-%{upstream_version}

%build
# compile message catalogs
%{__python2} setup.py compile_catalog
echo >> django_openstack_auth.egg-info/SOURCES.txt
ls */locale/*/LC_MESSAGES/django*mo >> django_openstack_auth.egg-info/SOURCES.txt

%{__python2} setup.py build

# generate html docs
PYTHONPATH=.:$PYTHONPATH sphinx-build doc/source html

%install
%{__python2} setup.py install --skip-build --root %{buildroot}

# remove unnecessary .po files
find %{buildroot} -name django.po -exec rm '{}' \;

%find_lang django
# don't include tests in the RPM
rm -rf %{buildroot}/%{python2_sitelib}/openstack_auth/tests

%check
#mox3 is missing
#%{__python} setup.py test

%files -f django.lang
%license LICENSE
%dir %{python2_sitelib}/openstack_auth/
%dir %{python2_sitelib}/openstack_auth/locale
%dir %{python2_sitelib}/openstack_auth/locale/??/
%dir %{python2_sitelib}/openstack_auth/locale/??_??/
%dir %{python2_sitelib}/openstack_auth/locale/??/LC_MESSAGES
%dir %{python2_sitelib}/openstack_auth/locale/??_??/LC_MESSAGES
%{python2_sitelib}/openstack_auth/locale/django.pot
%{python2_sitelib}/openstack_auth/*.py*
%{python2_sitelib}/openstack_auth/plugin/
%{python2_sitelib}/%{pypi_name}-*.egg-info

%changelog
* Thu Mar 24 2016 RDO <rdo-list@redhat.com> 2.2.0-1
- 2.2.0 Rebuild for Mitaka 
