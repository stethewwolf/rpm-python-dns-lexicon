# Created by pyp2rpm-3.2.2
%global pypi_name dns-lexicon

%if 0%{?rhel} && 0%{?rhel} <= 7
%bcond_with python3
%else
%bcond_without python3
%endif

Name:           python-%{pypi_name}
Version:        2.4.4
Release:        2%{?dist}
Summary:        Manipulate DNS records on various DNS providers in a standardized/agnostic way

License:        MIT
URL:            https://github.com/AnalogJ/lexicon
Source0:        https://files.pythonhosted.org/packages/source/d/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

Patch0:         remove-shebang.patch

BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
BuildRequires:  python2-future
BuildRequires:  python2-tldextract

%if %{with python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-future
BuildRequires:  python3-tldextract
%endif

%description
Manipulate DNS records on various DNS providers in
a standardized/agnostic way. Introduction Lexicon provides a way to manipulate
DNS records on multiple DNS providers in a standardized way. Lexicon has a CLI
but it can also be used as a python library.Lexicon was designed to be used
in...

%package -n     python2-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{pypi_name}}

Requires:       python2-requests
Requires:       python2-tldextract
Requires:       python2-future
Requires:       python2-setuptools

%description -n python2-%{pypi_name}
Manipulate DNS records on various DNS providers in
a standardized/agnostic way. Introduction Lexicon provides a way to manipulate
DNS records on multiple DNS providers in a standardized way. Lexicon has a CLI
but it can also be used as a python library.Lexicon was designed to be used
in...

%if %{with python3}
%package -n     python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}

Requires:       python3-requests
Requires:       python3-tldextract
Requires:       python3-future
Requires:       python3-setuptools

%description -n python3-%{pypi_name}
Manipulate DNS records on various DNS providers in
a standardized/agnostic way. Introduction Lexicon provides a way to manipulate
DNS records on multiple DNS providers in a standardized way. Lexicon has a CLI
but it can also be used as a python library.Lexicon was designed to be used
in...
%endif

%prep
%autosetup -p1 -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py2_build
%if %{with python3}
%py3_build
%endif

%install
# Must do the subpackages' install first because the scripts in /usr/bin are
# overwritten with every setup.py install.

%py2_install
cp %{buildroot}/%{_bindir}/lexicon %{buildroot}/%{_bindir}/lexicon-%{python2_version}
ln -s %{_bindir}/lexicon-%{python2_version} %{buildroot}/%{_bindir}/lexicon-2

%if %{with python3}
%py3_install
cp %{buildroot}/%{_bindir}/lexicon %{buildroot}/%{_bindir}/lexicon-%{python3_version}
ln -s %{_bindir}/lexicon-%{python3_version} %{buildroot}/%{_bindir}/lexicon-3
%endif

%files -n python2-%{pypi_name}
%license LICENSE
%doc README.md
%if ! %{with python3}
%{_bindir}/lexicon
%endif
%{_bindir}/lexicon-2
%{_bindir}/lexicon-%{python2_version}
%{python2_sitelib}/lexicon
%{python2_sitelib}/dns_lexicon-%{version}-py?.?.egg-info

%if %{with python3}
%files -n python3-%{pypi_name}
%license LICENSE
%doc README.md
%{_bindir}/lexicon
%{_bindir}/lexicon-3
%{_bindir}/lexicon-%{python3_version}
%{python3_sitelib}/lexicon
%{python3_sitelib}/dns_lexicon-%{version}-py?.?.egg-info
%endif

%changelog
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
