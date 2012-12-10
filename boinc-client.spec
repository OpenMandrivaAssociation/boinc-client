%define Werror_cflags %nil

Summary:	The BOINC client core
Name:		boinc-client
Version:	7.0.28
Release:	2
License:	LGPLv2+
Group:		Sciences/Other
URL:		http://boinc.berkeley.edu/
# The source for this package was pulled from upstream's vcs. Use the
# following commands to generate the tarball:
# svn export http://boinc.berkeley.edu/svn/tags/boinc_core_release_%{version_}
# pushd boinc_core_release_%{version_}
# ./_autosetup
# ../trim . Trim all binaries and other unnecessary things.
# popd
# tar -cvJf boinc-%{version}.tar.xz boinc_core_release_%{version_}/
Source0:	boinc-%{version}.tar.bz2
Source1:	boinc-client-init-d
Source2:	boinc-client-logrotate-d
Source3:	boinc-manager.desktop
Source4:	trim
#Create password file rw for group, this enables passwordless connection
#of manager from users of the boinc group.
#This won't be probably upstreamed as it might be unsafe for common usage
#without setting proper group ownership of the password file.
Patch0:		boinc-guirpcauth.patch
Patch1:		boinc-7.0.28-automake1.12.patch
BuildRequires:	python-mysql
BuildRequires:	curl-devel
BuildRequires:	desktop-file-utils
BuildRequires:	wxgtku-devel
BuildRequires:	gettext
BuildRequires:	mysql-devel
BuildRequires:	docbook-utils
BuildRequires:	sqlite3-devel
BuildRequires:	pkgconfig(glut)
BuildRequires:	libxmu-devel
BuildRequires:	libnotify-devel

Requires:	logrotate
Requires:	libxmu

%description
The Berkeley Open Infrastructure for Network Computing (BOINC) is an open-
source software platform which supports distributed computing, primarily in
the form of "volunteer" computing and "desktop Grid" computing.  It is well
suited for problems which are often described as "trivially parallel".  BOINC
is the underlying software used by projects such as SETI@home, Einstein@Home,
ClimatePrediciton.net, the World Community Grid, and many other distributed
computing projects.

This package installs the BOINC client software, which will allow your
computer to participate in one or more BOINC projects, using your spare
computer time to search for cures for diseases, model protein folding, study
global warming, discover sources of gravitational waves, and many other types
of scientific and mathematical research.

%package -n boinc-manager
Summary:	GUI to control and monitor %{name}
Group:		Sciences/Other
Requires:	%{name} = %{version}-%{release}

%description -n boinc-manager
The BOINC Manager is a graphical monitor and control utility for the BOINC
core client. It gives a detailed overview of the state of the client it is
monitoring. The BOINC Manager has two modes of operation, the "Simple View" in
which it only displays the most important information and the "Advanced View"
in which all information and all control elements are available.

%package devel
Summary:	Development files for %{name}
Group:		Development/Other

Requires:	%{name} = %{version}-%{release}
Requires:	openssl-devel
Requires:	mysql-devel
#Provides:	%{name}-static-devel = %{version}-%{release}

%description devel
This package contains development files for %{name}.

%package static
Summary:	Static libraries for %{name}
Group:		Sciences/Other

Requires:	%{name}-devel = %{version}-%{release}

%description static
This package contains static libraries for %{name}.

%package doc
Summary:	Documentation files for %{name}
Group:		Sciences/Other
BuildArch:	noarch

Requires:	%{name} = %{version}-%{release}

%description doc
This package contains documentation files for %{name}.

%prep
%setup -q -n boinc-%{version}
%patch0 -p0
%patch1 -p1

# fix utf8
iconv -f ISO88591 -t UTF8 < checkin_notes > checkin_notes.utf8
touch -r checkin_notes checkin_notes.utf8
mv checkin_notes.utf8 checkin_notes

iconv -f ISO88591 -t UTF8 < checkin_notes_2004 > checkin_notes_2004.utf8
touch -r checkin_notes_2004 checkin_notes_2004.utf8
mv checkin_notes_2004.utf8 checkin_notes_2004

iconv -f ISO88591 -t UTF8 < checkin_notes_2005 > checkin_notes_2005.utf8
touch -r checkin_notes_2005 checkin_notes_2005.utf8
mv checkin_notes_2005.utf8 checkin_notes_2005

iconv -f ISO88591 -t UTF8 < checkin_notes_2006 > checkin_notes_2006.utf8
touch -r checkin_notes_2006 checkin_notes_2006.utf8
mv checkin_notes_2006.utf8 checkin_notes_2006

# fix permissions and newlines on source files
chmod 644 clientgui/*.cpp  clientgui/*.h
sed -i 's/\r//' clientgui/DlgItemProperties.cpp

%build
%ifarch x86_64
%global boinc_platform x86_64-pc-linux-gnu
%else
%global boinc_platform i686-pc-linux-gnu
%endif

./_autosetup

%configure2_5x	--disable-dependency-tracking \
		--disable-fcgi \
		--disable-shared \
		--disable-server \
		--enable-client \
		--enable-manager \
		--enable-unicode \
		--enable-dynamic-client-linkage \
		--with-ssl \
		--with-x \
		--with-boinc-platform=%{boinc_platform}
#		STRIP=: DOCBOOK2X_MAN=/usr/bin/docbook2man \

# Disable rpaths
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

# Parallel make does not work, see upstream bugtracker at:
# http://boinc.berkeley.edu/trac/ticket/775
make

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/16x16/apps
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/32x32/apps
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/48x48/apps
mkdir -p %{buildroot}%{_initrddir}
mkdir -p %{buildroot}%{_localstatedir}/lib/boinc
mkdir -p %{buildroot}%{_mandir}/man1
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d/

%makeinstall_std

rm -rf %{buildroot}%{_bindir}/1sec
rm -rf %{buildroot}%{_bindir}/concat
rm -rf %{buildroot}%{_bindir}/create_work
rm -rf %{buildroot}%{_bindir}/dir_hier_move
rm -rf %{buildroot}%{_bindir}/dir_hier_path
rm -rf %{buildroot}%{_bindir}/sign_executable
rm -rf %{buildroot}%{_bindir}/start
rm -rf %{buildroot}%{_bindir}/status
rm -rf %{buildroot}%{_bindir}/stop
rm -rf %{buildroot}%{_bindir}/updater
rm -rf %{buildroot}%{_bindir}/upper_case

chmod a-x %{buildroot}%{_sysconfdir}/sysconfig/%{name}

pushd %{buildroot}%{_bindir}

# use symlink instead of hardlink
rm boinc
ln -s boinc_client boinc

# remove libtool archives
rm %{buildroot}%{_libdir}/*.la

# rename boincmgr and wrap it
mv %{buildroot}%{_bindir}/boincmgr %{buildroot}%{_bindir}/boinc_gui

cat > boincmgr <<EOF
#!/bin/bash
# wrapper script to allow passwordless manager connections from users of the boinc group

# Look for any local configuration settings of \$BOINCDIR
if [ -f %{_sysconfdir}/sysconfig/%{name} ]; then
	. %{_sysconfdir}/sysconfig/%{name} 
elif [ -f %{_sysconfdir}/default/%{name} ]; then
	. %{_sysconfdir}/default/%{name}
fi

# Otherwise pull \$BOINCDIR from the init script
if [ -z \$BOINCDIR ]; then
	BOINCDIR=\`grep 'BOINCDIR=' %{_sysconfdir}/init.d/%{name} | tr '"' ' ' | sed 's|BOINCDIR=||'\`;
fi

cd \$BOINCDIR
boinc_gui >& /dev/null
EOF
chmod a+x boincmgr
popd

# own init script and logrotate configuration file
rm -f %{buildroot}%{_sysconfdir}/init.d/%{name}
install -p -m755 %{SOURCE1} %{buildroot}%{_initrddir}/%{name}
install -p -m644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

# icon
cp clientgui/res/boincmgr.16x16.png %{buildroot}%{_datadir}/icons/hicolor/16x16/apps/boincmgr.png
cp clientgui/res/boincmgr.32x32.png %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/boincmgr.png
cp clientgui/res/boincmgr.48x48.png %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/boincmgr.png

%find_lang BOINC-Client
%find_lang BOINC-Manager

# bash-completion

install -Dp -m644 client/scripts/boinc.bash %{buildroot}%{_sysconfdir}/bash_completion.d/boinc-client
install -Dp -m644 %{SOURCE3} %{buildroot}%{_datadir}/applications/boinc-manager.desktop

%clean
rm -rf %{buildroot}

%pre
getent group boinc >/dev/null || groupadd -r boinc
getent passwd boinc >/dev/null || \
useradd -r -g boinc -d %{_localstatedir}/lib/boinc -s /sbin/nologin -c "BOINC client account." boinc
exit 0

%post
/sbin/chkconfig --add boinc-client

#correct wrong owner and group on files under /var/lib/boinc and log files
#caused by bug fixed in 5.10.45-8
chown --silent -R boinc:boinc %{_localstatedir}/log/boinc* \
%{_localstatedir}/lib/boinc/* 2>/dev/null || :

%preun
if [ $1 -eq 0 ]; then #if uninstalling, not only updating
	/sbin/service boinc-client stop
	/sbin/chkconfig --del boinc-client
fi

%postun
if [ "$1" -ge "1" ] ; then
        /sbin/service boinc-client condrestart >/dev/null 2>&1 || :
fi

%files -f BOINC-Client.lang
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/bash_completion.d/
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%doc COPYING COPYRIGHT
%{_bindir}/boinc
%{_bindir}/boinc_client
%{_bindir}/boinccmd
%{_bindir}/switcher
%{_initrddir}/%{name}
%attr(775,boinc,boinc) %{_localstatedir}/lib/boinc/

%files doc
%doc checkin_notes checkin_notes_2007 checkin_notes_2006 checkin_notes_2005 checkin_notes_2004 checkin_notes_2003 checkin_notes_2002

%files -n boinc-manager -f BOINC-Manager.lang
%{_bindir}/boinc_gui
%{_bindir}/boincmgr
%{_datadir}/applications/boinc-manager.desktop
%{_datadir}/icons/hicolor/16x16/apps/boincmgr.png
%{_datadir}/icons/hicolor/32x32/apps/boincmgr.png
%{_datadir}/icons/hicolor/48x48/apps/boincmgr.png

%files static
%{_libdir}/libboinc.a
%{_libdir}/libboinc_api.a
%{_libdir}/libboinc_crypt.a
%{_libdir}/libboinc_graphics2.a
%{_libdir}/libboinc_opencl.a
%{_libdir}/libboinc_zip.a

%files devel
%{_includedir}/boinc



%changelog
* Fri Jul 13 2012 Andrey Bondrov <abondrov@mandriva.org> 7.0.28-2
+ Revision: 809095
- Add patch1 to fix build with automake 1.12.x

* Sat May 19 2012 Andrey Bondrov <abondrov@mandriva.org> 7.0.28-1
+ Revision: 799643
- Update to 7.0.28, use some work that Mageia did on 7.0.6

* Sat Aug 14 2010 Tomas Kindl <supp@mandriva.org> 6.10.56-1mdv2011.0
+ Revision: 569795
- update to latest version - 6.10.56
- enable 'remote' GUI acces from localhost with random password
- preserve conf files

* Fri Mar 19 2010 Tomas Kindl <supp@mandriva.org> 6.10.17-1mdv2010.1
+ Revision: 525287
- fix underlinking issue
- fix missing BuildRequires
- fix manpages generation
- Now really drop that patch...
- bump to 6.10.17 release
- frop gcc4.4 patch as it's no longer needed

  + Thomas Backlund <tmb@mandriva.org>
    - fix typo in initscript

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

  + Emmanuel Andry <eandry@mandriva.org>
    - New version 6.6.37
    - use fedora spec and patches

* Sat Feb 28 2009 Guillaume Rousse <guillomovitch@mandriva.org> 6.6.1-1.svn20081217.2mdv2009.1
+ Revision: 345952
- rebuild

* Tue Feb 10 2009 Zombie Ryushu <ryushu@mandriva.org> 6.6.1-1.svn20081217.1mdv2009.1
+ Revision: 339118
- Upgrade to 6.6.1
- Upgrade to 6.6.1
- New Version 6.4.5
- New Version 6.4.5

* Sun Jun 15 2008 Funda Wang <fwang@mandriva.org> 5.10.45-1.svn20080315.1mdv2009.0
+ Revision: 219256
- BR unicode version of wxgtk2.8
- fix version
- disable server
- add missing files
- covert to mandriva style
- import boinc-client


* Sat May 17 2008 Milos Jakubicek <xjakub@fi.muni.cz> - 5.10.45-14.20080315svn
- Fixed opening locales by adding boinc-locales.patch

* Sat May 17 2008 Milos Jakubicek <xjakub@fi.muni.cz> - 5.10.45-13.20080315svn
- Fixed boincmgr segfaulting on F9/x86_64 (#445902) by adding
  boinc-parsecolor.patch (Patch2).

* Mon May 12 2008 Milos Jakubicek <xjakub@fi.muni.cz> - 5.10.45-12.20080315svn
- Do not ship ca-bundle.crt as it is already included in curl.
- Fixed the almost empty debuginfo package (do not strip anything).
- Patches documented according to the guidelines (PatchUpstreamStatus)

* Sun May 04 2008 Milos Jakubicek <xjakub@fi.muni.cz> - 5.10.45-11.20080315svn
- Fixed find command because starting with findutils-4.4.0-1.fc10, find 
  returns a non-zero value when "-delete" fails.
  (for more details on this see bug #20802 on savannah.gnu.org)

* Sat May 03 2008 Milos Jakubicek <xjakub@fi.muni.cz> - 5.10.45-10.20080315svn
- Fixed handling stale lockfiles (#444936).
- Initscript fixed to be compliant with current SysVInit guidelines
  (added condrestart, try-restart, force-reload actions).

* Wed Apr 23 2008 Lubomir Kundrak <lkundrak@redhat.com> - 5.10.45-9.20080315svn
- Do not expect chown of nonexistent files to succeed (#443568)

* Mon Apr 14 2008 Milos Jakubicek <xjakub@fi.muni.cz> - 5.10.45-8.20080315svn
- Fixed projects permissions (calling chown recursively).

* Mon Apr 14 2008 Milos Jakubicek <xjakub@fi.muni.cz> - 5.10.45-7.20080315svn
- Fixed running the boinc daemon as boinc user instead of root, file
  permissions changed accordingly.

* Mon Apr 07 2008 Milos Jakubicek <xjakub@fi.muni.cz> - 5.10.45-6.20080315svn
- Using --with-boinc-platform=i686-pc-linux-gnu on i386 instead of --build,
  --host, --target
- Added bash completion script.

* Fri Apr 04 2008 Milos Jakubicek <xjakub@fi.muni.cz> - 5.10.45-5.20080315svn
- Fixed build on i386 since it needs to be configured as i686-pc-linux-gnu 
  and not i386-pc-linux-gnu.

* Mon Mar 24 2008 Milos Jakubicek <xjakub@fi.muni.cz> - 5.10.45-4.20080315svn
- Removed unnecessary slash before the {_localstatedir} macro.

* Sun Mar 23 2008 Milos Jakubicek <xjakub@fi.muni.cz> - 5.10.45-3.20080315svn
- Logs moved to /var/log so that all SELinux related things could be removed.
- The error.log file has been renamed to boincerr.log.

* Sun Mar 16 2008 Milos Jakubicek <xjakub@fi.muni.cz> - 5.10.45-2.20080315svn
- Fixed typo in the semanage command (missing boinc subdirectory and quotes).
- Fixed installing empty log files.
- Fixed Patch1 (has been created before propagating the flags using the
  _autosetup script).

* Sat Mar 15 2008 Milos Jakubicek <xjakub@fi.muni.cz> - 5.10.45-1.20080315svn
- Updated to 5.10.45
- Added Patch1 removing -fomit-frame-pointer and -ffast-math compiler flags.
- Updated Patch0 (/lib/boinc_cmd.C changes have been merged in upstream).
- Log files (/var/lib/{boinc,error}.log) are touched during the installation
  so that correct(?) SELinux context can be set on them.
- Added Requires(post, postun): policycoreutils because of previous point.

* Sat Mar 08 2008 Milos Jakubicek <xjakub@fi.muni.cz> - 5.10.40-8.20080206svn
- Added missing Requires: mysql-devel for the -devel subpackage

* Fri Mar 07 2008 Milos Jakubicek <xjakub@fi.muni.cz> - 5.10.40-7.20080206svn
- Removed unnecessary client stopping when upgrading.
- Removed unnecessary ldconfig calls.
- A few changes unifying macros usage.
- Fixed missing directory ownership of {_localstatedir}/lib/boinc
- Added missing Requires: openssl-devel for the -devel subpackage

* Wed Feb 27 2008 Milos Jakubicek <xjakub@fi.muni.cz> - 5.10.40-6.20080206svn
- Added patch making the sources compatible with GCC4.3

* Mon Feb 25 2008 Milos Jakubicek <xjakub@fi.muni.cz> - 5.10.40-5.20080206svn
- Added the "stripchart" source directory to be trimmed.
- Removed all translations (will be added later through l10n specspo module).
- Fixed logrotate in case that boinc won't be running at the logrotate time.
- Changed summary and description according to upstream's choice.
- Fixed wrong SELinux context on error.log and boinc.log.
- Removed .svn directories from the source.
- Fixed missing Short-Description field in the init script.
- Service disabled by default.
- Fixed missing reload action in the init script.
- Changed the way of using the subsys directory for locking so that 
  rpmlint doesn't complain.
- Added script converting non-unicode files into UTF8.
- Added script removing execution rights on documentation files.
- Added documentation: checkin_notes_2007
- Init script behaves polite now when starting/stopping the service which
  has been already started/stopped (i.e. exits with 0).

* Fri Feb 16 2008 Milos Jakubicek <xjakub@fi.muni.cz> - 5.10.40-4.20080206svn
- Fixed locales installation path
- Fixed missing Provides: boinc-client-static in the -devel subpackage

* Thu Feb 14 2008 Milos Jakubicek <xjakub@fi.muni.cz> - 5.10.40-3.20080206svn
- Fixed the init script (now using the daemon function properly)
- Fixed missing chkconfig setup
- Added Requires: chkconfig

* Tue Feb 12 2008 Milos Jakubicek <xjakub@fi.muni.cz> - 5.10.40-2.20080206svn
- Fixed missing boinc user and group

* Tue Feb 06 2008 Milos Jakubicek <xjakub@fi.muni.cz> - 5.10.40-1.20080206svn
- Updated to 5.10.40.
- Fixed unpackaged files: libboinc_graphics*.
- Fixed missing BuildRequires: mysql-devel, libXmu-devel, libjpeg-devel.
- Added locales.
- Added script trimming binaries and other unnecessary code from the source.
- Added ldconfig call for the -devel subpackage.
- Added Czech and German translation.

* Wed Jan 09 2008 Debarshi Ray <rishi@fedoraproject.org> - 5.10.32-1.20080109svn
- Initial build. Imported SPEC written by Eric Myers and Milos Jakubicek.
- Disabled parallel make to prevent failure with -j3.
