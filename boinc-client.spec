%define snap 20081217
%define version_ 6_6_1
%define Werror_cflags %nil

Summary:	The BOINC client core
Name:		boinc-client
Version:	6.6.1
Release:	%mkrel 1.svn%{snap}.1
License:	LGPLv2+
Group:		Sciences/Other
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
Source0:	boinc-%{version}.tar.bz2
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
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires:	python-mysql
BuildRequires:	curl-devel
BuildRequires:	desktop-file-utils
BuildRequires:	mesaglut-devel
BuildRequires:	mesaglu-devel
BuildRequires:	openssl-devel
BuildRequires:	wxgtku2.8-devel
BuildRequires:  gettext
BuildRequires:  mysql-devel
BuildRequires:  libxmu-devel
BuildRequires:  libjpeg-devel libxslt-devel

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
Provides:	%{name}-static-devel = %{version}-%{release}

%description devel
This package contains development files for %{name}.

%prep
%setup -q -n boinc_core_release_%{version_}

%build

./_autosetup
%configure --disable-server --enable-client --enable-unicode
# %configure2_5x --disable-server --disable-static --enable-unicode STRIP=:
# Parallel make does not work.
make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/16x16/apps
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/32x32/apps
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/48x48/apps
mkdir -p $RPM_BUILD_ROOT%{_initrddir}
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/lib/boinc
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/

make DESTDIR=$RPM_BUILD_ROOT install

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

desktop-file-install --vendor="" \
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
%_pre_useradd boinc %{_localstatedir}/lib/boinc /sbin/nologin

%postun
%_postun_userdel boinc

%post
%_post_service %name

%preun
%_preun_service %name

%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/bash_completion.d/
%config %{_sysconfdir}/init.d/*
%config %{_sysconfdir}/sysconfig/boinc-client
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
%{_mandir}/man1/boinc.1.*
%{_mandir}/man1/boinc_client.1.*
%{_mandir}/man1/boinc_cmd.1.*
%defattr(-,boinc,boinc,-)
%{_localstatedir}/lib/boinc

%files -n boinc-manager -f BOINC-Manager.lang
%defattr(-,root,root,-)
%{_bindir}/boincmgr
%{_mandir}/man1/boincmgr.1.*
%{_datadir}/applications/*.desktop
%{_datadir}/boinc
%{_iconsdir}/hicolor/*/apps/boincmgr.png
%{_datadir}/locale/*

%files devel
%defattr(-,root,root,-)
%{_libdir}/*.a
%{_includedir}/boinc