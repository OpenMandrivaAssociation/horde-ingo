%define module	ingo
%define name	horde-%{module}
%define version	1.2.4
%define release	%mkrel 1

%define _requires_exceptions pear(Horde.*)

Name:           %{name}
Version:        %{version}
Release:        %{release}
Summary:	The Horde email filter rules Manager
License:	GPL
Group: 		System/Servers
URL:		http://www.horde.org/%{module}
Source0:	ftp://ftp.horde.org/pub/%{module}/%{module}-h3-%{version}.tar.gz
Patch0:		%{module}-h3-1.2.1-fhs.patch
Requires(post):	rpm-helper
Requires:	horde >= 3.3.8
Requires: 	horde-imp >= 4.3
BuildArch:	noarch

%description
Ingo is an email filter rules manager.

Ingo currently supports the following filtering drivers:

    * Sieve (using timsieved)
    * procmail (using VFS FTP driver)
    * IMAP client-side filtering

Ingo has replaced IMP's internal filtering code and is the default filtering
agent in IMP H3 (4.0).

%prep
%setup -q -n %{module}-h3-%{version}
%patch0 -p 1

%build

%install
rm -rf %{buildroot}

# apache configuration
install -d -m 755 %{buildroot}%{_webappconfdir}
cat > %{buildroot}%{_webappconfdir}/%{name}.conf <<EOF
# %{name} Apache configuration file

<Directory %{_datadir}/horde/%{module}/lib>
    Order allow,deny
    Deny from all
</Directory>

<Directory %{_datadir}/horde/%{module}/locale>
    Order allow,deny
    Deny from all
</Directory>

<Directory %{_datadir}/horde/%{module}/scripts>
    Order allow,deny
    Deny from all
</Directory>

<Directory %{_datadir}/horde/%{module}/templates>
    Order allow,deny
    Deny from all
</Directory>
EOF

# horde configuration
install -d -m 755 %{buildroot}%{_sysconfdir}/horde/registry.d
cat > %{buildroot}%{_sysconfdir}/horde/registry.d/%{module}.php <<'EOF'
<?php
//
// Ingo Horde configuration file
//
 
$this->applications['ingo'] = array(
    'fileroot'    => $this->applications['horde']['fileroot'] . '/ingo',
    'webroot'     => $this->applications['horde']['webroot'] . '/ingo',
    'name'        => _("Filters"),
    'status'      => 'active',
    'provides'    => array('mail/blacklistFrom', 'mail/showBlacklist', 'mail/whitelistFrom', 'mail/showWhitelist', 'mail/applyFilters', 'mail/canApplyFilters', 'mail/showFilters'),
    'menu_parent' => 'imp'
);
EOF

# remove .htaccess files
find . -name .htaccess -exec rm -f {} \;

# install files
install -d -m 755 %{buildroot}%{_datadir}/horde/%{module}
cp -pR *.php %{buildroot}%{_datadir}/horde/%{module}
cp -pR js %{buildroot}%{_datadir}/horde/%{module}
cp -pR themes %{buildroot}%{_datadir}/horde/%{module}
cp -pR lib %{buildroot}%{_datadir}/horde/%{module}
cp -pR locale %{buildroot}%{_datadir}/horde/%{module}
cp -pR scripts %{buildroot}%{_datadir}/horde/%{module}
cp -pR templates %{buildroot}%{_datadir}/horde/%{module}
cp -pR config %{buildroot}%{_sysconfdir}/horde/%{module}

install -d -m 755 %{buildroot}%{_sysconfdir}/horde
pushd %{buildroot}%{_datadir}/horde/%{module}
ln -s ../../../..%{_sysconfdir}/horde/%{module} config
popd

# activate configuration files
for file in %{buildroot}%{_sysconfdir}/horde/%{module}/*.dist; do
	mv $file ${file%.dist}
done

# fix script shellbang
for file in `find %{buildroot}%{_datadir}/horde/%{module}/scripts`; do
	perl -pi -e 's|/usr/local/bin/php|/usr/bin/php|' $file
done

%clean
rm -rf %{buildroot}

%post
if [ $1 = 1 ]; then
	# configuration
	%create_ghostfile %{_sysconfdir}/horde/%{module}/conf.php apache apache 644
	%create_ghostfile %{_sysconfdir}/horde/%{module}/conf.php.bak apache apache 644
fi
%if %mdkversion < 201010
%_post_webapp
%endif

%postun
%if %mdkversion < 201010
%_postun_webapp
%endif

%files
%defattr(-,root,root)
%doc LICENSE README docs
%config(noreplace) %{_webappconfdir}/%{name}.conf
%config(noreplace) %{_sysconfdir}/horde/registry.d/%{module}.php
%config(noreplace) %{_sysconfdir}/horde/%{module}
%{_datadir}/horde/%{module}


%changelog
* Sun Aug 08 2010 Thomas Spuhler <tspuhler@mandriva.org> 1.2.4-1mdv2011.0
+ Revision: 567493
- Updated to version 1.2.4
- added version 1.2.4 source file

* Tue Aug 03 2010 Thomas Spuhler <tspuhler@mandriva.org> 1.2.3-3mdv2011.0
+ Revision: 565212
- Increased release for rebuild

* Mon Jan 18 2010 Guillaume Rousse <guillomovitch@mandriva.org> 1.2.3-2mdv2010.1
+ Revision: 493347
- rely on filetrigger for reloading apache configuration begining with 2010.1, rpm-helper macros otherwise

* Sat Dec 26 2009 Funda Wang <fwang@mandriva.org> 1.2.3-1mdv2010.1
+ Revision: 482413
- new version 1.2.3

  + Guillaume Rousse <guillomovitch@mandriva.org>
    - restrict default access permissions to localhost only, as per new policy

* Sun Sep 20 2009 Guillaume Rousse <guillomovitch@mandriva.org> 1.2.2-1mdv2010.0
+ Revision: 445974
- new version
- new setup (simpler is better)

* Fri Sep 11 2009 Thierry Vignaud <tv@mandriva.org> 1.2.1-2mdv2010.0
+ Revision: 437882
- rebuild

* Thu Feb 05 2009 Guillaume Rousse <guillomovitch@mandriva.org> 1.2.1-1mdv2009.1
+ Revision: 337793
- new release
- rediff FHS patch

* Thu Aug 07 2008 Thierry Vignaud <tv@mandriva.org> 1.2-2mdv2009.0
+ Revision: 267075
- rebuild early 2009.0 package (before pixel changes)

* Fri May 30 2008 Guillaume Rousse <guillomovitch@mandriva.org> 1.2-1mdv2009.0
+ Revision: 213380
- don't recompress sources
  don't duplicate spec-helper work
- update to new version 1.2

* Wed Jan 16 2008 Guillaume Rousse <guillomovitch@mandriva.org> 1.1.5-1mdv2008.1
+ Revision: 153779
- update to new version 1.1.5

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Wed Dec 19 2007 Guillaume Rousse <guillomovitch@mandriva.org> 1.1.4-1mdv2008.1
+ Revision: 133744
- update to new version 1.1.4

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Thu Sep 06 2007 Guillaume Rousse <guillomovitch@mandriva.org> 1.1.3-1mdv2008.0
+ Revision: 81171
- update to new version 1.1.3


* Mon Sep 04 2006 Andreas Hasenack <andreas@mandriva.com>
+ 2006-09-04 20:51:02 (59910)
- bump release

* Mon Sep 04 2006 Andreas Hasenack <andreas@mandriva.com>
+ 2006-09-04 20:45:02 (59899)
- added missing javascript directory

* Mon Sep 04 2006 Andreas Hasenack <andreas@mandriva.com>
+ 2006-09-04 16:14:35 (59828)
- Import horde-ingo

* Fri Aug 25 2006 Guillaume Rousse <guillomovitch@mandriva.org> 1.1.1-2mdv2007.0
- Rebuild

* Mon May 22 2006 Guillaume Rousse <guillomovitch@mandriva.org> 1.1.1-1mdk
- New release 1.1.1

* Tue Mar 07 2006 Guillaume Rousse <guillomovitch@mandriva.org> 1.1-1mdk
- new version

* Wed Jan 11 2006 Guillaume Rousse <guillomovitch@mandriva.org> 1.0.2-2mdk
- fix automatic dependencies

* Tue Dec 27 2005 Guillaume Rousse <guillomovitch@mandriva.org> 1.0.2-1mdk
- new version
- %%mkrel

* Thu Jun 30 2005 Guillaume Rousse <guillomovitch@mandriva.org> 1.0.1-3mdk 
- better fix encoding
- fix requires

* Fri Feb 18 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 1.0.1-2mdk
- spec file cleanups, remove the ADVX-build stuff
- strip away annoying ^M

* Thu Jan 27 2005 Guillaume Rousse <guillomovitch@mandrake.org> 1.0.1-1mdk 
- new version
- no automatic config generation, incorrect default values
- horde isn't a prereq
- spec cleanup

* Mon Jan 17 2005 Guillaume Rousse <guillomovitch@mandrake.org> 1.0-3mdk 
- fix inclusion path
- fix configuration perms
- generate configuration at postinstall
- horde and rpm-helper are now a prereq

* Sat Jan 15 2005 Guillaume Rousse <guillomovitch@mandrake.org> 1.0-2mdk 
- fix summary

* Fri Jan 14 2005 Guillaume Rousse <guillomovitch@mandrake.org> 1.0-1mdk 
- first mdk release

