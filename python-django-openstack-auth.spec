%global pypi_name django_openstack_auth

Name:           python-django-openstack-auth
Version:        1.0.2
Release:        1%{?dist}
Summary:        Django authentication backend for OpenStack Keystone 

License:        BSD
URL:            http://pypi.python.org/pypi/django_openstack_auth/1.0.2
Source0:        http://pypi.python.org/packages/source/d/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch
 
BuildRequires:  python2-devel
BuildRequires:  python-sphinx
BuildRequires:  python-mox
BuildRequires:  python-keystoneclient
BuildRequires:  python-django
 
Requires:       python-django >= 1.4
Requires:       python-keystoneclient

%description
Django OpenStack Auth is a pluggable Django authentication backend that
works with Django's ``contrib.auth`` framework to authenticate a user against
OpenStack's Keystone Identity API.

The current version is designed to work with the
Keystone V2 API.

%prep
%setup -q -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

# remove unnecessary .po files
find . -name "django.po" -exec rm -f '{}' \;


%build
%{__python} setup.py build

# generate html docs 
PYTHONPATH=.:$PYTHONPATH sphinx-build docs html
# remove the sphinx-build leftovers
#rm -rf html/.{doctrees,buildinfo}


%install
%{__python} setup.py install --skip-build --root %{buildroot}

%find_lang django

# don't include tests in the RPM
rm -rf %{buildroot}/%{python_sitelib}/openstack_auth/tests

%check
%{__python} setup.py test

%files -f django.lang
%doc README.rst LICENSE
%dir %{python_sitelib}/openstack_auth
%{python_sitelib}/openstack_auth/*.py*
%{python_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

%changelog
* Tue Sep 11 2012 Matthias Runge <mrunge@redhat.com> - 1.0.2-1
- Initial package.
