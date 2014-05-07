%global pypi_name django_openstack_auth

Name:           python-django-openstack-auth
Version:        1.1.5
Release:        2%{?dist}
Summary:        Django authentication backend for OpenStack Keystone 

License:        BSD
URL:            http://pypi.python.org/pypi/django_openstack_auth/
Source0:        http://pypi.python.org/packages/source/d/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
Patch0:         0001-remove-runtime-dep-to-python-pbr.patch
BuildArch:      noarch
 
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
%if 0%{?rhel}==6
BuildRequires:  python-sphinx10
%else
BuildRequires:  python-sphinx
%endif
BuildRequires:  python-mox
BuildRequires:  python-keystoneclient
BuildRequires:  python-iso8601
BuildRequires:  python-pbr
BuildRequires:  python-netaddr
BuildRequires:  python-oslo-sphinx

%if 0%{?rhel}<7 || 0%{?fedora} < 18
%if 0%{?rhel}==6
Requires:   Django14
BuildRequires: Django14
%else
Requires:   Django
BuildRequires:   Django
%endif
%else
Requires:   python-django
BuildRequires:   python-django
%endif
 
Requires:       python-keystoneclient

%description
Django OpenStack Auth is a pluggable Django authentication backend that
works with Django's ``contrib.auth`` framework to authenticate a user against
OpenStack's Keystone Identity API.

The current version is designed to work with the
Keystone V2 API.

%prep
%setup -q -n %{pypi_name}-%{version}
%patch0 -p1
# Remove bundled egg-info
# rm -rf %{pypi_name}.egg-info

# remove unnecessary .po files
find . -name "django.po" -exec rm -f '{}' \;

sed -i s/RPMVERSION/%{version}/ openstack_auth/__init__.py

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
rm -f {test-,}requirements.txt

# make doc build compatible with python-oslo-sphinx RPM
sed -i 's/oslosphinx/oslo.sphinx/' doc/source/conf.py

%build
%{__python} setup.py build

# generate html docs
%if 0%{?rhel}==6
PYTHONPATH=.:$PYTHONPATH sphinx-1.0-build doc/source html
%else
PYTHONPATH=.:$PYTHONPATH sphinx-build doc/source html
%endif

%install
%{__python} setup.py install --skip-build --root %{buildroot}

%if 0%{?rhel}==6
# Handling locale files
# This is adapted from the %%find_lang macro, which cannot be directly
# used since Django locale files are not located in %%{_datadir}
#
# The rest of the packaging guideline still apply -- do not list
# locale files by hand!
(cd $RPM_BUILD_ROOT && find . -name 'django*.mo') | %{__sed} -e 's|^.||' |
%{__sed} -e \
   's:\(.*/locale/\)\([^/_]\+\)\(.*\.mo$\):%lang(\2) \1\2\3:' \
      >> django.lang
%else
%find_lang django
%endif
# don't include tests in the RPM
rm -rf %{buildroot}/%{python_sitelib}/openstack_auth/tests

%check
%{__python} setup.py test

%files -f django.lang
%doc LICENSE
%dir %{python_sitelib}/openstack_auth
%{python_sitelib}/openstack_auth/*.py*
%{python_sitelib}/openstack_auth/locale/openstack_auth.pot
%{python_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

%changelog
* Thu Apr 03 2014 Matthias Runge <mrunge@redhat.com> - 1.1.5-1
- update to stable version 1.1.5 (rhbz#1082314)

* Tue Jan 14 2014 Matthias Runge <mrunge@redhat.com> - 1.1.4-1
- update to stable version 1.1.4 (rhbz#1051773) 

* Fri Oct 11 2013 Matthias Runge <mrunge@redhat.com> - 1.1.3-1
- update to stable version 1.1.3 (rhbz#1014494)

* Tue Sep 10 2013 Matthias Runge <mrunge@redhat.com> - 1.1.2-1
- update to stable version 1.1.2 (rhbz#1006012)

* Tue Aug 13 2013 Matthias Runge <mrunge@redhat.com> - 1.1.1-1
- update to stable version 1.1.1 (rhbz#991783)

* Fri Jul 26 2013 Matthias Runge <mrunge@redhat.com> - 1.1.0-1
- update to stable version 1.1.0 (rhbz#983007)

* Fri Jun 07 2013 Matthias Runge <mrunge@redhat.com> - 1.0.11-1
- update to django-openstack-auth-1.0.11 (rhbz#965249)

* Thu Apr 25 2013 Matthias Runge <mrunge@redhat.com> - 1.0.9-1
- update to 1.0.9 with more Django-1.5 fixes

* Wed Apr 24 2013 Matthias Runge <mrunge@redhat.com> - 1.0.8-1
- update to 1.0.8 for Django-1.5 compat

* Wed Mar 06 2013 Matthias Runge <mrunge@redhat.com> - 1.0.7-1
- update to 1.0.7 (rhbz#918435)

* Mon Feb 18 2013 Matthias Runge <mrunge@redhat.com> - 1.0.6-3
- BR python-iso8601

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Dec 10 2012 Matthias Runge <mrunge@redhat.com> - 1.0.6-1
- update to latest upstream version 1.0.6

* Tue Dec 04 2012 Matthias Runge <mrunge@redhat.com> - 1.0.4-1
- update to latest upstream version 1.0.4

* Mon Nov 05 2012 Matthias Runge <mrunge@redhat.com> - 1.0.3-1
- update latest upstream version 1.0.3

* Tue Oct 16 2012 Matthias Runge <mrunge@redhat.com> - 1.0.2-3
- fix build on EPEL6, require Django14 package on EPEL6
- handle languages by hand on EL6

* Mon Sep 24 2012 Matthias Runge <mrunge@redhat.com> - 1.0.2-2
- also support f17, el6

* Tue Sep 11 2012 Matthias Runge <mrunge@redhat.com> - 1.0.2-1
- Initial package.
