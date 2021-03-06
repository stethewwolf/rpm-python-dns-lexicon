%global pypi_name dns-lexicon


%if 0%{?rhel} && 0%{?rhel} <= 7
%global rhel7 1
%endif

%bcond_with python3
%bcond_without python2

%if 0%{?rhel} >= 8
# EPEL8 is currently missing dependencies used by the extras metapackages
%bcond_with extras
%else
%bcond_without extras
%endif

Name:           python-%{pypi_name}
Version:        3.3.28
Release:        1%{?dist}
Summary:        Manipulate DNS records on various DNS providers in a standardized/agnostic way

License:        MIT
URL:            https://github.com/AnalogJ/lexicon
Source0:        https://files.pythonhosted.org/packages/source/d/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

Patch0:         0000-remove-shebang.patch

%if 0%{?rhel7}
#Patch1:         0001-fix-requirements.patch
BuildRequires:  python36-cryptography
BuildRequires:  python36-pyOpenSSL
BuildRequires:  python36-tldextract
%else
BuildRequires:  python3-cryptography
BuildRequires:  python3-pyOpenSSL
%endif

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-future

%if 0%{?fedora} && 0%{?fedora} <= 28
BuildRequires:  python3-PyYAML
%endif
%if 0%{?rhel7}
BuildRequires:  python36-PyYAML
%else
BuildRequires:  python3-pyyaml
%endif

# Extras requirements
# {{{
%if %{with extras}
%if 0%{?rhel7}
BuildRequires:  python36-beautifulsoup4
BuildRequires:  python-boto3
BuildRequires:  python36-xmltodict
%else
BuildRequires:  python3-beautifulsoup4
BuildRequires:  python3-boto3
BuildRequires:  python3-xmltodict
%endif
BuildRequires:  python3-dns
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

%if 0%{?fedora} && 0%{?fedora} <= 28
Requires:       python3-PyYAML
%else
Requires:       python3-pyyaml
%endif

# Both packages install a Python module named lexicon
# TODO: Remove this once resolved upstream (see upstream #222)
Conflicts:      python-lexicon

%description -n python3-%{pypi_name}
Lexicon provides a way to manipulate DNS records on multiple DNS providers in a
standardized way. Lexicon has a CLI but it can also be used as a python
library.

This is the Python 3 version of the package.

# Extras meta-packages
# {{{
%if %{with extras}

%package -n     python3-%{pypi_name}+easyname
Summary:        Meta-package for python3-%{pypi_name} and easyname provider
%{?python_provide:%python_provide python3-%{pypi_name}+easyname}

Requires:       python3-%{pypi_name} = %{version}-%{release}
Requires:       python3-beautifulsoup4

%description -n python3-%{pypi_name}+easyname
This package installs no files. It requires python3-%{pypi_name} and all
dependencies necessary to use the easyname provider.


%package -n     python3-%{pypi_name}+gratisdns
Summary:        Meta-package for python3-%{pypi_name} and gratisdns provider
%{?python_provide:%python_provide python3-%{pypi_name}+gratisdns}

Requires:       python3-%{pypi_name} = %{version}-%{release}
Requires:       python3-beautifulsoup4

%description -n python3-%{pypi_name}+gratisdns
This package installs no files. It requires python3-%{pypi_name} and all
dependencies necessary to use the gratisdns provider.

%package -n     python3-%{pypi_name}+henet
Summary:        Meta-package for python3-%{pypi_name} and Hurricane Electric provider
%{?python_provide:%python_provide python3-%{pypi_name}+henet}

Requires:       python3-%{pypi_name} = %{version}-%{release}
Requires:       python3-beautifulsoup4

%description -n python3-%{pypi_name}+henet
This package installs no files. It requires python3-%{pypi_name} and all
dependencies necessary to use the Hurricane Electric provider.

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

%if ! 0%{?rhel7}
# EL7 does not have the dependencies necessary for this meta-package
# {{{

%package -n     python3-%{pypi_name}+hetzner
Summary:        Meta-package for python3-%{pypi_name} and Hetzner provider
%{?python_provide:%python_provide python3-%{pypi_name}+hetzner}

Requires:       python3-%{pypi_name} = %{version}-%{release}
Requires:       python3-beautifulsoup4
Requires:       python3-dns

%description -n python3-%{pypi_name}+hetzner
This package installs no files. It requires python3-%{pypi_name} and all
dependencies necessary to use the Hetzner provider.
# }}}
%endif

%endif
# }}}

%prep
%autosetup -p1 -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py3_build

%install
%py3_install
install -pm 0755 %{buildroot}/%{_bindir}/lexicon %{buildroot}/%{_bindir}/lexicon-%{python3_version}
ln -s %{_bindir}/lexicon-%{python3_version} %{buildroot}/%{_bindir}/lexicon-3


%files -n python3-%{pypi_name}
%license LICENSE
#%doc README.md
%{_bindir}/lexicon
%{_bindir}/lexicon-3
%{_bindir}/lexicon-%{python3_version}
%{python3_sitelib}/lexicon
%{python3_sitelib}/dns_lexicon-%{version}-py?.?.egg-info

# Extras meta-packages
# {{{
%if %{with extras}
%files -n python3-%{pypi_name}+easyname
%files -n python3-%{pypi_name}+gratisdns
%files -n python3-%{pypi_name}+henet
%if ! 0%{?rhel7}
%files -n python3-%{pypi_name}+hetzner
%endif
%files -n python3-%{pypi_name}+plesk
%files -n python3-%{pypi_name}+route53
%endif
# }}}

%changelog
* Tue Oct 08 2019 Eli Young <elyscape@gmail.com> - 3.3.4-2
- Rebuild due to Koji issues

* Mon Oct 07 2019 Eli Young <elyscape@gmail.com> - 3.3.4-1
- Update to 3.3.4 (#1725208)
- Support EPEL8 builds

* Thu Oct 03 2019 Miro Hron??ok <mhroncok@redhat.com> - 3.2.8-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hron??ok <mhroncok@redhat.com> - 3.2.8-3
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

* Mon Jul 02 2018 Miro Hron??ok <mhroncok@redhat.com> - 2.4.4-3
- Rebuilt for Python 3.7

* Tue Jun 26 2018 Eli Young <elyscape@gmail.com> - 2.4.4-2
- Remove unnecessary shebang

* Tue Jun 26 2018 Eli Young <elyscape@gmail.com> - 2.4.4-1
- Update to 2.4.4 (#1594777)

* Tue Jun 19 2018 Eli Young <elyscape@gmail.com> - 2.4.3-1
- Update to 2.4.3 (#1592158)

* Tue Jun 19 2018 Miro Hron??ok <mhroncok@redhat.com> - 2.4.0-2
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
