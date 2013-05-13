%define modname ssh2
%define soname %{modname}.so
%define inifile A36_%{modname}.ini

Summary:	PHP bindings for the libssh2 library
Name:		php-%{modname}
Version:	0.11.3
%define subrel 1
Release:	1
Group:		Development/PHP
License:	PHP License
URL:		http://pecl.php.net/package/ssh2
Source0:	http://pecl.php.net/get/ssh2-%{version}.tgz
# svn checkout http://svn.php.net/repository/pecl/ssh2/trunk ssh2
Patch0:		php-ssh2-lib64.diff
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	openssl-devel
BuildRequires:	zlib-devel
BuildRequires:	pkgconfig(libssh2) >= 0.15
Epoch:		1

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
%configure2_5x --with-libdir=%{_lib} \
    --with-%{modname}=shared,%{_prefix}

make
mv modules/*.so .

%install
rm -rf %{buildroot}

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

%clean
rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc package*.xml
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}


%changelog
* Sun Jan 15 2012 Oden Eriksson <oeriksson@mandriva.com> 1:0.11.3-0.1
- 0.11.3

* Wed Aug 24 2011 Oden Eriksson <oeriksson@mandriva.com> 1:0.11.2-8mdv2011.0
+ Revision: 696373
- rebuilt for php-5.3.8

* Fri Aug 19 2011 Oden Eriksson <oeriksson@mandriva.com> 1:0.11.2-7
+ Revision: 695318
- rebuilt for php-5.3.7

* Thu May 05 2011 Oden Eriksson <oeriksson@mandriva.com> 1:0.11.2-6
+ Revision: 667721
- mass rebuild

* Sat Mar 19 2011 Oden Eriksson <oeriksson@mandriva.com> 1:0.11.2-5
+ Revision: 646557
- rebuilt for php-5.3.6

* Sat Jan 08 2011 Oden Eriksson <oeriksson@mandriva.com> 1:0.11.2-4mdv2011.0
+ Revision: 629745
- rebuilt for php-5.3.5

* Mon Jan 03 2011 Oden Eriksson <oeriksson@mandriva.com> 1:0.11.2-3mdv2011.0
+ Revision: 628051
- ensure it's built without automake1.7

* Tue Nov 23 2010 Oden Eriksson <oeriksson@mandriva.com> 1:0.11.2-2mdv2011.0
+ Revision: 600183
- rebuild

* Thu Nov 04 2010 Oden Eriksson <oeriksson@mandriva.com> 1:0.11.2-1mdv2011.0
+ Revision: 593189
- duh!
- 0.11.2

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1:0.11.1-0.20090208.9mdv2011.0
+ Revision: 588722
- rebuild

* Fri Mar 05 2010 Oden Eriksson <oeriksson@mandriva.com> 1:0.11.1-0.20090208.8mdv2010.1
+ Revision: 514657
- rebuilt for php-5.3.2

* Sun Feb 21 2010 Oden Eriksson <oeriksson@mandriva.com> 1:0.11.1-0.20090208.7mdv2010.1
+ Revision: 509091
- rebuild

* Sat Jan 02 2010 Oden Eriksson <oeriksson@mandriva.com> 1:0.11.1-0.20090208.6mdv2010.1
+ Revision: 485264
- rebuilt for php-5.3.2RC1

* Sat Nov 21 2009 Oden Eriksson <oeriksson@mandriva.com> 1:0.11.1-0.20090208.5mdv2010.1
+ Revision: 468091
- rebuilt against php-5.3.1

* Sun Oct 04 2009 Oden Eriksson <oeriksson@mandriva.com> 1:0.11.1-0.20090208.4mdv2010.0
+ Revision: 453378
- use the svn snapshot (they migrated from cvs -> svn)

* Wed Sep 30 2009 Oden Eriksson <oeriksson@mandriva.com> 1:0.11.1-0.20090208.3mdv2010.0
+ Revision: 451221
- rebuild

* Sun Jul 19 2009 Raphaël Gertz <rapsys@mandriva.org> 1:0.11.1-0.20090208.2mdv2010.0
+ Revision: 397605
- Rebuild

* Wed May 13 2009 Oden Eriksson <oeriksson@mandriva.com> 1:0.11.1-0.20090208.1mdv2010.0
+ Revision: 375449
- use a more recent cvs snapshot to make it build with php-5.3.x
- rebuilt against php-5.3.0RC2

* Sun Mar 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1:0.11.0-2mdv2009.1
+ Revision: 346635
- rebuilt for php-5.2.9

* Tue Feb 17 2009 Oden Eriksson <oeriksson@mandriva.com> 1:0.11.0-1mdv2009.1
+ Revision: 341498
- 0.11.0
- build against system libssh2

* Thu Jan 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1:0.11.0-0.20080515.3mdv2009.1
+ Revision: 321950
- rebuild

* Fri Dec 05 2008 Oden Eriksson <oeriksson@mandriva.com> 1:0.11.0-0.20080515.2mdv2009.1
+ Revision: 310223
- rebuilt against php-5.2.7

* Sun Jul 27 2008 Oden Eriksson <oeriksson@mandriva.com> 1:0.11.0-0.20080515.1mdv2009.0
+ Revision: 250652
- 0.11.0-20080515
- build it against private libssh2-0.14 code to make it work again

* Tue Jul 15 2008 Oden Eriksson <oeriksson@mandriva.com> 1:0.11-0.20071019.3mdv2009.0
+ Revision: 235881
- rebuild

* Fri May 02 2008 Oden Eriksson <oeriksson@mandriva.com> 1:0.11-0.20071019.2mdv2009.0
+ Revision: 200118
- rebuilt against php-5.2.6

* Tue Feb 05 2008 Oden Eriksson <oeriksson@mandriva.com> 1:0.11-0.20071019.1mdv2008.1
+ Revision: 162813
- new snap 20071019
- drop upstream patches

* Mon Feb 04 2008 Oden Eriksson <oeriksson@mandriva.com> 1:0.11-0.20060607.5mdv2008.1
+ Revision: 161957
- rebuild

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Nov 11 2007 Oden Eriksson <oeriksson@mandriva.com> 1:0.11-0.20060607.4mdv2008.1
+ Revision: 107576
- restart apache if needed

* Sat Sep 01 2007 Oden Eriksson <oeriksson@mandriva.com> 1:0.11-0.20060607.3mdv2008.0
+ Revision: 77580
- fixed empty release
- rebuilt against php-5.2.4

* Thu Aug 16 2007 Oden Eriksson <oeriksson@mandriva.com> 1:0.11-0.20060607.2mdv2008.0
+ Revision: 64305
- use the new %%serverbuild macro

* Tue Aug 07 2007 Oden Eriksson <oeriksson@mandriva.com> 1:0.11-0.20060607.1mdv2008.0
+ Revision: 59940
- use the latest cvs snapshot as of 20060607
- rediffed the lib64 patch (P0)
- make it build against libssh2 later than 0.16 (P1)
- rebuilt against new libssh2

* Thu Jun 14 2007 Oden Eriksson <oeriksson@mandriva.com> 1:0.10-15mdv2008.0
+ Revision: 39388
- use distro conditional -fstack-protector

* Fri Jun 01 2007 Oden Eriksson <oeriksson@mandriva.com> 1:0.10-14mdv2008.0
+ Revision: 33783
- rebuilt against new upstream version (5.2.3)

* Mon May 07 2007 Oden Eriksson <oeriksson@mandriva.com> 1:0.10-13mdv2008.0
+ Revision: 24428
- fix deps

* Thu May 03 2007 Oden Eriksson <oeriksson@mandriva.com> 1:0.10-12mdv2008.0
+ Revision: 21033
- rebuilt against new upstream version (5.2.2)


* Fri Feb 09 2007 Oden Eriksson <oeriksson@mandriva.com> 0.10-11mdv2007.0
+ Revision: 118557
- rebuilt against new upstream php version (5.2.1)

* Wed Nov 08 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.10-10mdv2007.0
+ Revision: 78318
- fix deps
- bunzip patches

* Tue Nov 07 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.10-9mdv2007.0
+ Revision: 77397
- rebuilt for php-5.2.0

* Thu Nov 02 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.10-8mdv2007.1
+ Revision: 75357
- Import php-ssh2

* Mon Aug 28 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.10-8
- rebuilt for php-5.1.6

* Thu Jul 27 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.10-7mdk
- rebuild

* Sat May 06 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.10-6mdk
- rebuilt for php-5.1.4

* Fri May 05 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.10-5mdk
- rebuilt for php-5.1.3

* Thu Feb 02 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.10-4mdk
- new group (Development/PHP) and iurt rebuild

* Sun Jan 15 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.10-3mdk
- rebuilt against php-5.1.2

* Tue Nov 29 2005 Oden Eriksson <oeriksson@mandriva.com> 1:0.10-2mdk
- rebuilt against php-5.1.1

* Sat Nov 26 2005 Oden Eriksson <oeriksson@mandriva.com> 1:0.10-1mdk
- 0.10
- drop upstream patch P1 (bug4756)
- rebuilt against php-5.1.0
- fix versioning

* Sun Oct 30 2005 Oden Eriksson <oeriksson@mandriva.com> 5.1.0_0.9-0.RC1.2mdk
- rebuilt to provide a -debug package too

* Sun Oct 02 2005 Oden Eriksson <oeriksson@mandriva.com> 5.1.0_0.9-0.RC1.1mdk
- 0.9
- rebuilt against php-5.1.0RC1
- fixed the lib64 patch
- added P1 to make it compile

* Wed Sep 07 2005 Oden Eriksson <oeriksson@mandriva.com> 5.0.5_0.6-1mdk
- rebuilt against php-5.0.5 (Major security fixes)

* Fri May 27 2005 Oden Eriksson <oeriksson@mandriva.com> 5.0.4_0.6-1mdk
- rename the package

* Sun Apr 17 2005 Oden Eriksson <oeriksson@mandriva.com> 5.0.4_0.6-1mdk
- 5.0.4

* Sun Mar 20 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 5.0.3_0.6-2mdk
- use the %%mkrel macro

* Sat Feb 12 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 5.0.3_0.6-1mdk
- initial Mandrakelinux package

* Sat Feb 12 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.10_0.6-1mdk
- 0.6
- rebuilt against a non hardened-php aware php lib

* Mon Jan 17 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.10_0.4.1-3mdk
- fix deps

* Sat Jan 15 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.10_0.4.1-2mdk
- rebuild due to hardened-php-0.2.6
- cleanups

* Sat Jan 08 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.10_0.4.1-1mdk
- initial mandrake package
- added P0

