%define modname	ssh2
%define soname	%{modname}.so
%define inifile	A36_%{modname}.ini

Summary:	PHP bindings for the libssh2 library
Name:		php-%{modname}
Epoch:		1
Version:	0.11.3
Release:	4
Group:		Development/PHP
License:	PHP License
Url:		http://pecl.php.net/package/ssh2
Source0:	http://pecl.php.net/get/ssh2-%{version}.tgz
# svn checkout http://svn.php.net/repository/pecl/ssh2/trunk ssh2
Patch0:		php-ssh2-lib64.diff
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	openssl-devel
BuildRequires:	zlib-devel
BuildRequires:	pkgconfig(libssh2) >= 0.15

%description
Provides bindings to the libssh2 library which provide access to resources
(shell, remote exec, tunneling, file transfer) on a remote machine using a
secure cryptographic transport.

%prep

%setup -q -n ssh2-%{version}
[ "../package*.xml" != "/" ] && mv ../package*.xml .

%patch0 -p0

%build
%serverbuild

phpize
%configure2_5x \
	--with-libdir=%{_lib} \
	--with-%{modname}=shared,%{_prefix}

make
mv modules/*.so .

%install
install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m0755 %{soname} %{buildroot}%{_libdir}/php/extensions/

cat > %{buildroot}%{_sysconfdir}/php.d/%{inifile} << EOF
extension = %{soname}
EOF

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart >/dev/null || :
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart >/dev/null || :
    fi
fi

%files 
%doc package*.xml
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}

