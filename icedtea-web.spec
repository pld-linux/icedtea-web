# TODO:
#	- separate netx.jar? I guess it contains the JNLP implementation

# Conditional build:
%bcond_without	javadoc		# don't build javadoc
%bcond_with	tests		# build with tests (interactive?)

%define	use_jdk	icedtea7

Summary:	Web browser Java plugin and an implementation of Java Web Start
Summary(pl.UTF-8):	Wtyczka Java dla przeglądarek WWW i implementacja Java Web Start
Name:		icedtea-web
Version:	1.6.1
Release:	1
License:	GPL v2
Group:		Applications
Source0:	http://icedtea.wildebeest.org/download/source/%{name}-%{version}.tar.gz
# Source0-md5:	35d6712a5d9db69e8bd14ab68f94d748
URL:		http://icedtea.classpath.org/wiki/IcedTea-Web
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gtk+2-devel
BuildRequires:	iceweasel-devel
%{?with_tests:BuildRequires:	java-junit}
BuildRequires:	java-rhino
BuildRequires:	jpackage-utils
BuildRequires:	libxslt-progs
BuildRequires:	rpm-javaprov
BuildRequires:	zlib-devel
%{?buildrequires_jdk}
Obsoletes:	icedtea6-jre-base-mozilla-plugin
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The IcedTea-Web project provides a Free Software web browser plugin
running applets written in the Java programming language and an
implementation of Java Web Start, originally based on the NetX
project.

%package -n browser-plugin-java-%{name}
Summary:	IceTea Java plugin for WWW browsers
Summary(pl.UTF-8):	Wtyczka Javy do przeglądarek WWW
Group:		Development/Languages/Java
Requires:	%{name} = %{version}-%{release}
Requires:	browser-plugins >= 2.0
Requires:	browser-plugins(%{_target_base_arch})
Obsoletes:	browser-plugin-java-icedtea6

%description -n browser-plugin-java-%{name}
Java plugin for WWW browsers.

%description -n browser-plugin-java-%{name} -l pl.UTF-8
Wtyczka z obsługą Javy dla przeglądarek WWW.

%package javadoc
Summary:	Online manual for %{name}
Summary(pl.UTF-8):	Dokumentacja online do %{name}
Group:		Documentation
Requires:	jpackage-utils
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description javadoc
Documentation for %{name}.

%description javadoc -l pl.UTF-8
Dokumentacja do %{name}.

%description javadoc -l fr.UTF-8
Javadoc pour %{name}.

%prep
%setup -q

%build
%{__aclocal}
%{__autoconf}
%{__automake}

%configure \
	--with-jdk-home="%{java_home}" \
	--docdir="%{_javadocdir}/%{name}-%{version}" \
	%{!?with_javadoc:--disable-docs}

%{__make}

%{?with_tests:%{__make} -j1 plugin-tests run-netx-unit-tests run-netx-dist-tests}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_browserpluginsdir}
ln -s %{_libdir}/IcedTeaPlugin.so $RPM_BUILD_ROOT%{_browserpluginsdir}/libjavaplugin.so

%if %{with javadoc}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{name}-%{version} %{_javadocdir}/%{name}

%post -n browser-plugin-java-%{name}
%update_browser_plugins

%postun -n browser-plugin-java-%{name}
if [ "$1" = 0 ]; then
	%update_browser_plugins
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/javaws
%attr(755,root,root) %{_bindir}/itweb-settings
%attr(755,root,root) %{_bindir}/policyeditor
%attr(755,root,root) %{_libdir}/IcedTeaPlugin.so
%{_datadir}/%{name}
%{_pixmapsdir}/javaws.png
%{_mandir}/man1/*.1*
%lang(cs) %{_mandir}/cs/man1/*.1*
%lang(de) %{_mandir}/de/man1/*.1*
%lang(pl) %{_mandir}/pl/man1/*.1*

%files -n browser-plugin-java-%{name}
%defattr(644,root,root,755)
%attr(755,root,root) %{_browserpluginsdir}/libjavaplugin.so

%if %{with javadoc}
%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{name}-%{version}
%ghost %{_javadocdir}/%{name}
%endif
