# Created by pyp2rpm-3.2.2
%global pypi_name dns-lexicon

Name:           python-%{pypi_name}
Version:        2.1.19
Release:        1%{?dist}
Summary:        Manipulate DNS records on various DNS providers in a standardized/agnostic way

License:        MIT
URL:            https://github.com/AnalogJ/lexicon
Source0:        https://files.pythonhosted.org/packages/source/d/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch
 
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
BuildRequires:  python2-future
BuildRequires:  python2-tldextract
 
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-future
BuildRequires:  python3-tldextract

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


%prep
%autosetup -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py2_build
%py3_build

%install
# Must do the subpackages' install first because the scripts in /usr/bin are
# overwritten with every setup.py install.
%py3_install
cp %{buildroot}/%{_bindir}/lexicon %{buildroot}/%{_bindir}/lexicon-%{python3_version}
ln -s %{_bindir}/lexicon-%{python3_version} %{buildroot}/%{_bindir}/lexicon-3

%py2_install
cp %{buildroot}/%{_bindir}/lexicon %{buildroot}/%{_bindir}/lexicon-%{python2_version}
ln -s %{_bindir}/lexicon-%{python2_version} %{buildroot}/%{_bindir}/lexicon-2

%files -n python2-%{pypi_name}
%license LICENSE
%doc README.md
%{_bindir}/lexicon
%{_bindir}/lexicon-2
%{_bindir}/lexicon-%{python2_version}
%{python2_sitelib}/lexicon
%{python2_sitelib}/dns_lexicon-%{version}-py?.?.egg-info

%files -n python3-%{pypi_name}
%license LICENSE
%doc README.md
%{_bindir}/lexicon-3
%{_bindir}/lexicon-%{python3_version}
%{python3_sitelib}/lexicon
%{python3_sitelib}/dns_lexicon-%{version}-py?.?.egg-info

%changelog
* Mon Feb 19 2018 Nick Bebout <nb@fedoraproject.org> - 2.1.19-1
- Initial package.
