%define modname ssh2
%define soname %{modname}.so
%define inifile A36_%{modname}.ini

%define snap 20060607

Summary:	PHP bindings for the libssh2 library
Name:		php-%{modname}
Version:	0.11
Release:	%mkrel 0.%{snap}.3
Group:		Development/PHP
License:	PHP License
URL:		http://pecl.php.net/package/ssh2
Source0:	ssh2-%{version}-%{snap}.tar.bz2
Patch0:		php-ssh2-lib64.diff
Patch1:		php-ssh2-libssh2-0.16_fix.diff
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	libssh2-devel
Epoch:		1
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
Provides bindings to the libssh2 library which provide access to resources
(shell, remote exec, tunneling, file transfer) on a remote machine using a
secure cryptographic transport.

%prep

%setup -q -n ssh2
%patch0 -p0
%patch1 -p0

%build
%serverbuild

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
