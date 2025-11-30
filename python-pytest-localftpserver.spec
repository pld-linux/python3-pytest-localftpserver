#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_with	python3 # CPython 3.x module (built from python3-pytest-localftpserver.spec)

Summary:	PyTest plugin which provides an FTP fixture for your tests
Summary(pl.UTF-8):	Wtyczka PyTesta udostępniająca wyposarzenie FTP dla testów
Name:		python-pytest-localftpserver
# keep 0.x here for python2 support
Version:	0.5.1
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/pytest-localftpserver/
Source0:	https://files.pythonhosted.org/packages/source/p/pytest-localftpserver/pytest_localftpserver-%{version}.tar.gz
# Source0-md5:	880f70dcba3c4b67026d30ccccd8c3da
URL:		https://pypi.org/project/pytest-localftpserver/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-pyftpdlib
BuildRequires:	python-pytest >= 3.0.5
BuildRequires:	python-wget >= 3.2
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.4
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-pyftpdlib
BuildRequires:	python3-pytest >= 3.0.5
BuildRequires:	python3-wget >= 3.2
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python-sphinx_rtd_theme >= 0.3.1
BuildRequires:	sphinx-pdg-2 >= 1.7.5
%endif
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
PyTest plugin which provides an FTP fixture for your tests.

%description -l pl.UTF-8
Wtyczka PyTesta udostępniająca wyposarzenie FTP dla testów.

%package -n python3-pytest-localftpserver
Summary:	PyTest plugin which provides an FTP fixture for your tests
Summary(pl.UTF-8):	Wtyczka PyTesta udostępniająca wyposarzenie FTP dla testów
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.4

%description -n python3-pytest-localftpserver
PyTest plugin which provides an FTP fixture for your tests.

%description -n python3-pytest-localftpserver -l pl.UTF-8
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
%if %{with python2}
%py_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=pytest_localftpserver.plugin \
%{__python} -m pytest tests/test_helper_functions.py tests/test_pytest_localftpserver.py

FTP_HOME=$(pwd)/tmp \
FTP_PASS=erni1 \
FTP_PORT=31175 \
FTP_USER=benz \
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=pytest_localftpserver.plugin \
%{__python} -m pytest tests/test_pytest_localftpserver_with_env_var.py
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=pytest_localftpserver.plugin \
%{__python3} -m pytest tests/test_helper_functions.py tests/test_pytest_localftpserver.py

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
%endif

%if %{with doc}
PYTHONPATH=$(pwd) \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-2
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc AUTHORS.rst HISTORY.rst LICENSE README.rst
%{py_sitescriptdir}/pytest_localftpserver
%{py_sitescriptdir}/pytest_localftpserver-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-pytest-localftpserver
%defattr(644,root,root,755)
%doc AUTHORS.rst HISTORY.rst LICENSE README.rst
%{py3_sitescriptdir}/pytest_localftpserver
%{py3_sitescriptdir}/pytest_localftpserver-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_modules,_static,api,*.html,*.js}
%endif
