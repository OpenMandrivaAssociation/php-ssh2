%define modname ssh2
%define dirname %{modname}
%define soname %{modname}.so
%define inifile A36_%{modname}.ini

Summary:	PHP bindings for the libssh2 library
Name:		php-%{modname}
Version:	0.10
Release:	%mkrel 11
Group:		Development/PHP
License:	PHP License
URL:		http://pecl.php.net/package/ssh2
Source0:	ssh2-%{version}.tar.bz2
Patch0:		ssh2-0.4.1-lib64.diff
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	libssh-devel
Provides:	php5-ssh2
Obsoletes:	php5-ssh2
Epoch:		1
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
Provides bindings to the libssh2 library which provide access to resources
(shell, remote exec, tunneling, file transfer) on a remote machine using a
secure cryptographic transport.

%prep

%setup -q -n ssh2-%{version}
%patch0 -p0

%build

phpize
%configure2_5x --with-libdir=%{_lib} \
    --with-%{modname}=shared,%{_prefix}

%make
mv modules/*.so .

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m755 %{soname} %{buildroot}%{_libdir}/php/extensions/

cat > %{buildroot}%{_sysconfdir}/php.d/%{inifile} << EOF
extension = %{soname}
EOF

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}
[ "../package.xml" != "/" ] && rm -f ../package.xml

%files 
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}


