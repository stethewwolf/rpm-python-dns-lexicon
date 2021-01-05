
%global forgeurl    https://github.com/AnalogJ/lexicon
Version:            3.5.3
%forgemeta

%global pypi_name dns-lexicon

%if 0%{?rhel} && 0%{?rhel} == 7
%global rhel7 1
%endif

%if 0%{?rhel} >= 8
# EPEL8 is currently missing dependencies used by the extras metapackages
%bcond_with extras
%else
%bcond_without extras
%endif

Name:           python-%{pypi_name}
Release:        1%{?dist}
Summary:        Manipulate DNS records on various DNS providers in a standardized/agnostic way

License:        MIT
URL:            %{forgeurl}
# pypi releases don't contain necessary data to run the tests
Source0:        %{forgesource}
BuildArch:      noarch

Patch0:         0000-remove-shebang.patch

BuildRequires:  pyproject-rpm-macros
BuildRequires:  poetry >= 0.12
BuildRequires:  python3-pyparsing >= 2.0.2
BuildRequires:  python3-six

# required to run the test suite
BuildRequires:  python3-mock
BuildRequires:  python3-pytest
BuildRequires:  python3-pytest-vcr

# Extras requirements
# {{{
%if %{with extras}
BuildRequires:  python3-boto3
%endif
# }}}


%description
Lexicon provides a way to manipulate DNS records on multiple DNS providers in a
standardized way. Lexicon has a CLI but it can also be used as a python
library.

%package -n     python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}

Requires:       python3-cryptography
Requires:       python3-future
Requires:       python3-requests
Requires:       python3-setuptools
Requires:       python3-pyOpenSSL
Requires:       python3-tldextract
Requires:       python3-pyyaml

# Both packages install a Python module named lexicon
# TODO: Remove this once resolved upstream (see upstream #222)
Conflicts:      python3-lexicon

# These "extras" were previously present in upstream lexicon but are not there
# anymore.
# {{{
%if %{with extras}
Obsoletes: python3-%{pypi_name}+easyname < 3.4
Provides: python3dist(%{pypi_name}[easyname]) = %{version}
Provides: python%{python3_version}dist(%{pypi_name}[easyname]) = %{version}

Obsoletes: python3-%{pypi_name}+gratisdns < 3.4
Provides: python3dist(%{pypi_name}[gratisdns]) = %{version}
Provides: python%{python3_version}dist(%{pypi_name}[gratisdns]) = %{version}

Obsoletes: python3-%{pypi_name}+henet < 3.4
Provides: python3dist(%{pypi_name}[henet]) = %{version}
Provides: python%{python3_version}dist(%{pypi_name}[henet]) = %{version}

Obsoletes: python3-%{pypi_name}+hetzner < 3.4
Provides: python3dist(%{pypi_name}[hetzner]) = %{version}
Provides: python%{python3_version}dist(%{pypi_name}[hetzner]) = %{version}
%endif
# }}}

%description -n python3-%{pypi_name}
Lexicon provides a way to manipulate DNS records on multiple DNS providers in a
standardized way. Lexicon has a CLI but it can also be used as a python
library.

This is the Python 3 version of the package.


%package -n     python3-%{pypi_name}+plesk
Summary:        Meta-package for python3-%{pypi_name} and Plesk provider
%{?python_provide:%python_provide python3-%{pypi_name}+plesk}

Requires:       python3-%{pypi_name} = %{version}-%{release}
Requires:       python3-xmltodict

%description -n python3-%{pypi_name}+plesk
This package installs no files. It requires python3-%{pypi_name} and all
dependencies necessary to use the Plesk provider.


%package -n     python3-%{pypi_name}+route53
Summary:        Meta-package for python3-%{pypi_name} and Route 53 provider
%{?python_provide:%python_provide python3-%{pypi_name}+route53}

Requires:       python3-%{pypi_name} = %{version}-%{release}
Requires:       python3-boto3

%description -n python3-%{pypi_name}+route53
This package installs no files. It requires python3-%{pypi_name} and all
dependencies necessary to use the Route 53 provider.

%prep
%autosetup -n lexicon-%{version} -p1
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info
rm setup.py

%generate_buildrequires
%pyproject_buildrequires -r -t -e light -x route53,plesk


%build
%pyproject_wheel

%check
# AutoProviderTests: unknown failure - exclude to get suite passing for now
# GoDaddyProviderTests: unknown failure - just get the suite passing for now
#   TypeError: __init__() got an unexpected keyword argument 'allowed_methods'
#
# lexicon providers which do not work in Fedora due to missing dependencies:
# - TransipProviderTests
# - SoftLayerProviderTests
# - NamecheapProviderTests
# - NamecheapManagedProviderTests
# - GransyProviderTests
# - LocalzoneProviderTests
TEST_SELECTOR="not AutoProviderTests and not GoDaddyProviderTests and not TransipProviderTests and not SoftLayerProviderTests and not NamecheapProviderTests and not NamecheapManagedProviderTests and not GransyProviderTests and not LocalzoneProviderTests"
# EPEL 8 does not provide the python3-pytest-vcr package
%if 0%{?fedora}
# The %%tox macro lacks features so we need to use pytest directly:
# Miro Hrončok, 2020-09-11:
# > I am afraid the %%tox macro can only work with "static" deps declaration,
# > not with arbitrary installers invoked as commands, sorry about that.
py.test-3 -v -k "${TEST_SELECTOR}" lexicon
%endif

%install
%pyproject_install
install -pm 0755 %{buildroot}/%{_bindir}/lexicon %{buildroot}/%{_bindir}/lexicon-%{python3_version}
cd %{buildroot}/%{_bindir}
ln -s lexicon-%{python3_version} lexicon-3
rm -rf %{buildroot}%{python3_sitelib}/lexicon/tests


%files -n python3-%{pypi_name}
%license LICENSE
%doc README.rst
%{_bindir}/lexicon
%{_bindir}/lexicon-3
%{_bindir}/lexicon-%{python3_version}
%{python3_sitelib}/lexicon
%{python3_sitelib}/dns_lexicon-%{version}.dist-info

# Extras meta-packages
# {{{
%if %{with extras}
%files -n python3-%{pypi_name}+plesk
%{?python_extras_subpkg:%ghost %{python3_sitelib}/dns_lexicon-%{version}.dist-info}

%files -n python3-%{pypi_name}+route53
%{?python_extras_subpkg:%ghost %{python3_sitelib}/dns_lexicon-%{version}.dist-info}

%endif
# }}}

%changelog
* Tue Jan  5 2021 Felix Schwarz <fschwarz@fedoraproject.org> - 3.5.3-1
- update to 3.5.3

* Tue Nov 24 2020 Felix Schwarz <fschwarz@fedoraproject.org> - 3.5.2-1
- update to 3.5.2

* Mon Nov 16 2020 Felix Schwarz <fschwarz@fedoraproject.org> - 3.5.1-1
- update to 3.5.1

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.17-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 10 2020 Miro Hrončok <mhroncok@redhat.com> - 3.3.17-4
- Add metadata for Python extras subpackages

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 3.3.17-3
- Rebuilt for Python 3.9

* Wed Mar 04 2020 Felix Schwarz <fschwarz@fedoraproject.org> - 3.3.17-2
- add missing sources

* Tue Mar 03 2020 Felix Schwarz <fschwarz@fedoraproject.org> - 3.3.17-1
- Update to 3.3.17 (#1764339)

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Oct 08 2019 Eli Young <elyscape@gmail.com> - 3.3.4-2
- Rebuild due to Koji issues

* Mon Oct 07 2019 Eli Young <elyscape@gmail.com> - 3.3.4-1
- Update to 3.3.4 (#1725208)
- Support EPEL8 builds

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 3.2.8-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 3.2.8-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jun 27 2019 Eli Young <elyscape@gmail.com> - 3.2.8-1
- Update to 3.2.8 (#1722190)

* Tue May 28 2019 Eli Young <elyscape@gmail.com> - 3.2.6-1
- Update to 3.2.6 (#1685778)

* Fri Feb 15 2019 Eli Young <elyscape@gmail.com> - 3.1.5-1
- Update to 3.1.5 (#1671162)
- Add meta-subpackages for specific providers

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Dec 14 2018 Eli Young <elyscape@gmail.com> - 3.0.6-1
- Update to 3.0.6
- Declare conflict with python-lexicon
- Remove Python 2 package in Fedora 30+

* Wed Nov 14 2018 Eli Young <elyscape@gmail.com> - 3.0.2-2
- Fix dependencies on Fedora 28

* Wed Nov 14 2018 Eli Young <elyscape@gmail.com> - 3.0.2-1
- Update to 3.0.2

* Mon Oct 08 2018 Eli Young <elyscape@gmail.com> - 2.7.9-1
- Update to 2.7.9 (#1637142)

* Mon Aug 27 2018 Eli Young <elyscape@gmail.com> - 2.7.0-2
- Add dependency on python-cryptography (#1622418)

* Mon Jul 23 2018 Nick Bebout <nb@fedoraproject.org> - 2.7.0-1
- Update to 2.7.0

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 10 2018 Eli Young <elyscape@gmail.com> - 2.4.5-1
- Update to 2.4.5 (#1599479)

* Mon Jul 02 2018 Miro Hrončok <mhroncok@redhat.com> - 2.4.4-3
- Rebuilt for Python 3.7

* Tue Jun 26 2018 Eli Young <elyscape@gmail.com> - 2.4.4-2
- Remove unnecessary shebang

* Tue Jun 26 2018 Eli Young <elyscape@gmail.com> - 2.4.4-1
- Update to 2.4.4 (#1594777)

* Tue Jun 19 2018 Eli Young <elyscape@gmail.com> - 2.4.3-1
- Update to 2.4.3 (#1592158)

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 2.4.0-2
- Rebuilt for Python 3.7

* Mon Jun 11 2018 Eli Young <elyscape@gmail.com> - 2.4.0-1
- Update to 2.4.0 (#1589596)

* Tue May 29 2018 Eli Young <elyscape@gmail.com> - 2.3.0-1
- Update to 2.3.0 (#1582799)

* Mon May 07 2018 Eli Young <elyscape@gmail.com> - 2.2.3-1
- Update to 2.2.3 (#1575598)

* Thu May 03 2018 Eli Young <elyscape@gmail.com> - 2.2.2-1
- Update to 2.2.2 (#1574265)

* Sat Mar 24 2018 Eli Young <elyscape@gmail.com> - 2.2.1-1
- Update to 2.2.1
- Use Python 3 by default when available

* Mon Feb 19 2018 Nick Bebout <nb@fedoraproject.org> - 2.1.19-1
- Initial package.
