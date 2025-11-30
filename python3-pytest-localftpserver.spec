#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

Summary:	PyTest plugin which provides an FTP fixture for your tests
Summary(pl.UTF-8):	Wtyczka PyTesta udostępniająca wyposarzenie FTP dla testów
Name:		python3-pytest-localftpserver
Version:	1.5.0
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/pytest-localftpserver/
Source0:	https://files.pythonhosted.org/packages/source/p/pytest-localftpserver/pytest_localftpserver-%{version}.tar.gz
# Source0-md5:	cecd485afcaa9979612e3b60d9974efa
URL:		https://pypi.org/project/pytest-localftpserver/
BuildRequires:	python3-build
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.10
BuildRequires:	python3-setuptools >= 1:67.0.0
BuildRequires:	python3-setuptools_scm >= 6.2
%if %{with tests}
BuildRequires:	python3-cryptography >= 43
BuildRequires:	python3-pyOpenSSL >= 24.1.0
BuildRequires:	python3-pyftpdlib >= 1.5.8
BuildRequires:	python3-pytest >= 8.2.0
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
%if %{with doc}
BuildRequires:	python3-sphinx_copybutton >= 0.3.0
BuildRequires:	python3-sphinx_rtd_theme >= 0.5.0
BuildRequires:	sphinx-pdg-3 >= 1.8
%endif
Requires:	python3-modules >= 1:3.10
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
PyTest plugin which provides an FTP fixture for your tests.

%description -l pl.UTF-8
Wtyczka PyTesta udostępniająca wyposarzenie FTP dla testów.

%package apidocs
Summary:	API documentation for Python pytest_localftpserver module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona pytest_localftpserver
Group:		Documentation

%description apidocs
API documentation for Python pytest_localftpserver module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona pytest_localftpserver.

%prep
%setup -q -n pytest_localftpserver-%{version}

install -d tmp

%build
%py3_build_pyproject

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=pytest_localftpserver.plugin \
%{__python3} -m pytest tests/test_helper_functions.py tests/test_pytest_localftpserver.py tests/test_pytest_localftpserver_TLS.py

FTP_CERTFILE=$(pwd)/tests/test_keycert.pem \
FTP_FIXTURE_SCOPE=function \
FTP_HOME=$(pwd)/tmp \
FTP_HOME_TLS=$(pwd)/tmp \
FTP_PASS=erni1 \
FTP_PORT=31175 \
FTP_PORT_TLS=31176 \
FTP_USER=benz \
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=pytest_localftpserver.plugin \
%{__python3} -m pytest tests/test_pytest_localftpserver_with_env_var.py
%endif

%if %{with doc}
PYTHONPATH=$(pwd) \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS.rst HISTORY.rst LICENSE README.rst
%{py3_sitescriptdir}/pytest_localftpserver
%{py3_sitescriptdir}/pytest_localftpserver-%{version}.dist-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_modules,_static,api,*.html,*.js}
%endif
