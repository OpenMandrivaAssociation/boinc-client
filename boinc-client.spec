%define snap 20080315
%define version_ 5_10_45

Summary:	The BOINC client core
Name:		boinc-client
Version:	5.10.45
Release:	14.%{snap}svn%{?dist}
License:	LGPLv2+
Group:		Applications/Engineering
URL:		http://boinc.berkeley.edu/
# The source for this package was pulled from upstream's vcs. Use the
# following commands to generate the tarball:
# svn export http://boinc.berkeley.edu/svn/tags/boinc_core_release_%{version_}
# pushd boinc_core_release_%{version_}
# ./_autosetup
# ./noexec . Fix unnecessary execute rights on documentation files
# ./unicode . Convert to UTF8
# ./trim . Trim all binaries and other unnecessary things.
# popd
# tar -czvf boinc-%{version}.tar.gz boinc_core_release_%{version_}/
Source0:	boinc-%{version}.tar.gz
Source1:	boinc-client-init-d
Source2:	boinc-client-logrotate-d
Source3:	boinc-manager.desktop
Source4:	boinc.1
Source5:	boinc_client.1
Source6:	boinc_cmd.1
Source7:	boincmgr.1
Source8:	trim
Source9:	noexec
Source10:	unicode
Source11:	boinc-client
#Changes necessary for GCC 3.4 should be already commited to CVS trunk
Patch0:		boinc-gcc43.patch
#http://boinc.berkeley.edu/trac/ticket/647 (patch commited to CVS trunk)
Patch1:		boinc-gccflags.patch
#http://boinc.berkeley.edu/trac/ticket/658 (patch commited to CVS trunk)
Patch2:		boinc-parsecolor.patch
#All the patches above should be removed by releasing boinc 6
Patch3:		boinc-locales.patch
#Not upstreamed yet, discussion in progress.
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

Requires:	logrotate
Requires:	chkconfig
Requires(pre):  shadow-utils

BuildRequires:	MySQL-python
BuildRequires:	curl-devel
BuildRequires:	desktop-file-utils
BuildRequires:	freeglut-devel
BuildRequires:	mesa-libGLU-devel
BuildRequires:	openssl-devel
BuildRequires:	wxGTK-devel
BuildRequires:  gettext
BuildRequires:  mysql-devel
BuildRequires:  libXmu-devel
BuildRequires:  libjpeg-devel

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
Group:		Applications/Engineering

Requires:	hicolor-icon-theme
Requires:	%{name} = %{version}-%{release}

%description -n boinc-manager
The BOINC Manager is a graphical monitor and control utility for the BOINC
core client. It gives a detailed overview of the state of the client it is
monitoring. The BOINC Manager has two modes of operation, the "Simple View" in
which it only displays the most important information and the "Advanced View"
in which all information and all control elements are available.

%package devel
Summary:	Development files for %{name}
Group:		Development/Libraries

Requires:	%{name} = %{version}-%{release}
Requires:	openssl-devel
Requires:	mysql-devel
Provides:	%{name}-static = %{version}-%{release}

%description devel
This package contains development files for %{name}.

%prep
%setup -q -n boinc_core_release_%{version_}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%ifarch i386
%configure --disable-static --enable-unicode --with-boinc-platform=i686-pc-linux-gnu STRIP=:
%else
%configure --disable-static --enable-unicode STRIP=:
%endif


# Parallel make does not work.
make -k

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/16x16/apps
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/32x32/apps
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/48x48/apps
mkdir -p $RPM_BUILD_ROOT%{_initrddir}
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/lib/boinc
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/

make install INSTALL="%{__install} -p" DESTDIR=$RPM_BUILD_ROOT

rm -rf $RPM_BUILD_ROOT%{_bindir}/1sec
rm -rf $RPM_BUILD_ROOT%{_bindir}/concat
rm -rf $RPM_BUILD_ROOT%{_bindir}/create_work
rm -rf $RPM_BUILD_ROOT%{_bindir}/dir_hier_move
rm -rf $RPM_BUILD_ROOT%{_bindir}/dir_hier_path
rm -rf $RPM_BUILD_ROOT%{_bindir}/sign_executable
rm -rf $RPM_BUILD_ROOT%{_bindir}/start
rm -rf $RPM_BUILD_ROOT%{_bindir}/status
rm -rf $RPM_BUILD_ROOT%{_bindir}/stop
rm -rf $RPM_BUILD_ROOT%{_bindir}/updater
rm -rf $RPM_BUILD_ROOT%{_bindir}/upper_case

pushd $RPM_BUILD_ROOT%{_bindir}
  ln -s boinc_client boinc
  mv boinc_gui boincmgr
popd

rm $RPM_BUILD_ROOT%{_bindir}/ca-bundle.crt
#because it's already included in curl

install -p -m755 %{SOURCE1} $RPM_BUILD_ROOT%{_initrddir}/%{name}
install -p -m644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/%{name}

# icon
install -p -m644 sea/boincmgr.16x16.png \
  $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/16x16/apps/boincmgr.png
install -p -m644 sea/boincmgr.32x32.png \
  $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/32x32/apps/boincmgr.png
install -p -m644 sea/boincmgr.48x48.png \
  $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/48x48/apps/boincmgr.png

# man page
install -p -m644 %{SOURCE4} $RPM_BUILD_ROOT%{_mandir}/man1
install -p -m644 %{SOURCE5} $RPM_BUILD_ROOT%{_mandir}/man1
install -p -m644 %{SOURCE6} $RPM_BUILD_ROOT%{_mandir}/man1
install -p -m644 %{SOURCE7} $RPM_BUILD_ROOT%{_mandir}/man1

desktop-file-install %{?_remove_encoding} --vendor fedora \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  %{SOURCE3}

# locales

mv locale/client/* locale
find locale -not -name "BOINC Manager.mo" -type f -delete
cp -rp locale $RPM_BUILD_ROOT%{_datadir}
find $RPM_BUILD_ROOT%{_datadir}/locale -name "BOINC Manager.mo" -execdir mv {} BOINC-Manager.mo \;

%find_lang BOINC-Manager

# bash-completion

install -Dp -m644 %{SOURCE11} $RPM_BUILD_ROOT%{_sysconfdir}/bash_completion.d/boinc-client

%clean
rm -rf $RPM_BUILD_ROOT

%pre

# Create BOINC user and group
getent group boinc >/dev/null || groupadd -r boinc
getent passwd boinc >/dev/null || \
useradd -r -g boinc -d %{_localstatedir}/lib/boinc -s /sbin/nologin \
	-c "BOINC client account." boinc
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

%post -n boinc-manager
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%postun -n boinc-manager
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/bash_completion.d/
%doc COPYING
%doc COPYRIGHT
%doc checkin_notes
%doc checkin_notes_2007
%doc checkin_notes_2006
%doc checkin_notes_2005
%doc checkin_notes_2004
%doc checkin_notes_2003
%doc checkin_notes_2002
%{_bindir}/boinc
%{_bindir}/boinc_client
%{_bindir}/boinc_cmd
%{_bindir}/crypt_prog
%{_bindir}/switcher
%{_initrddir}/%{name}
%{_mandir}/man1/boinc.1.gz
%{_mandir}/man1/boinc_client.1.gz
%{_mandir}/man1/boinc_cmd.1.gz
%{_mandir}/man1/boincmgr.1.gz
%defattr(-,boinc,boinc,-)
%{_localstatedir}/lib/boinc/

%files -n boinc-manager -f BOINC-Manager.lang
%defattr(-,root,root,-)
%{_bindir}/boincmgr
%{_datadir}/applications/fedora-boinc-manager.desktop
%{_datadir}/icons/hicolor/16x16/apps/boincmgr.png
%{_datadir}/icons/hicolor/32x32/apps/boincmgr.png
%{_datadir}/icons/hicolor/48x48/apps/boincmgr.png

%files devel
%defattr(-,root,root,-)
%{_libdir}/libboinc.a
%{_libdir}/libboinc_api.a
%{_libdir}/libboinc_zip.a
%{_libdir}/libsched.a
%{_libdir}/libboinc_graphics2.a
%{_libdir}/libboinc_graphics_api.a
%{_libdir}/libboinc_graphics_impl.a
%{_libdir}/libboinc_graphics_lib.a

%dir %{_includedir}/BOINC
%{_includedir}/BOINC/*

