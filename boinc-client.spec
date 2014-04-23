%define Werror_cflags %nil

Summary:	The BOINC client core
Name:		boinc-client
Version:	7.2.42
Release:	3
License:	LGPLv2+
Group:		Sciences/Other
URL:		http://boinc.berkeley.edu/
# The source for this package was pulled from upstream's vcs. Use the
# following commands to generate the tarball:
# git clone git://boinc.berkeley.edu/boinc-v2.git boinc
# pushd boinc
# git checkout client_release/7.2/%{version}
# ./_autosetup
# ../trim . Trim all binaries and other unnecessary things.
# rm -rf .git*
# popd
# tar -cJvf boinc-%%{version}.tar.xz boinc
# Full changelog: http://boinc.berkeley.edu/dev/forum_thread.php?id=8378
Source0:	boinc-%{version}.tar.xz
Source1:	boinc-client-systemd
Source2:	boinc-client-logrotate-d
Source3:	boinc-manager.desktop
Source4:	trim
# Wrapper to fix GPU detection (fedora)
Source5:	boinc_gpu
# Create password file rw for group, this enables passwordless connection
# of manager from users of the boinc group.
# This won't be probably upstreamed as it might be unsafe for common usage
# without setting proper group ownership of the password file.
Patch0:		boinc-7.2.39-guirpcauth.patch
# Backport patch from 7.3 branch to fix idle time detection (fedora)
Patch1:		boinc-7.2.39-idledetect.patch
BuildRequires:	curl-devel
BuildRequires:	wxgtku-devel
BuildRequires:	gettext
BuildRequires:	jpeg-devel
BuildRequires:	openssl-devel
BuildRequires:	docbook2x
BuildRequires:	sqlite3-devel
BuildRequires:	pkgconfig(glut)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(xmu)
BuildRequires:	pkgconfig(xi)
BuildRequires:	libnotify-devel
BuildRequires:	xcb-util-devel
BuildRequires:	gtk+2.0-devel
BuildRequires:	libxscrnsaver-devel
BuildRequires:	icoutils
Requires:	logrotate

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
%setup -qn boinc
%apply_patches

# fix utf8
iconv -f ISO88591 -t UTF8 < checkin_notes_2004 > checkin_notes_2004.utf8
touch -r checkin_notes_2004 checkin_notes_2004.utf8
mv checkin_notes_2004.utf8 checkin_notes_2004

iconv -f ISO88591 -t UTF8 < checkin_notes_2005 > checkin_notes_2005.utf8
touch -r checkin_notes_2005 checkin_notes_2005.utf8
mv checkin_notes_2005.utf8 checkin_notes_2005

iconv -f ISO88591 -t UTF8 < checkin_notes_2009 > checkin_notes_2009.utf8
touch -r checkin_notes_2009 checkin_notes_2009.utf8
mv checkin_notes_2009.utf8 checkin_notes_2009

iconv -f ISO88591 -t UTF8 < checkin_notes_2010 > checkin_notes_2010.utf8
touch -r checkin_notes_2010 checkin_notes_2010.utf8
mv checkin_notes_2010.utf8 checkin_notes_2010

iconv -f ISO88591 -t UTF8 < checkin_notes_2011 > checkin_notes_2011.utf8
touch -r checkin_notes_2011 checkin_notes_2011.utf8
mv checkin_notes_2011.utf8 checkin_notes_2011

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

# Disable rpaths
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make

%install
mkdir -p %{buildroot}%{_iconsdir}/hicolor/256x256/apps
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_localstatedir}/lib/boinc
mkdir -p %{buildroot}%{_mandir}/man1
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d/

%makeinstall_std

chmod a-x %{buildroot}%{_sysconfdir}/sysconfig/%{name}

pushd %{buildroot}%{_bindir}

# use symlink instead of hardlink
rm boinc
cat > boinc <<EOF
#!/bin/bash
# wrapper script that redirects stdout/stderr to correct log paths

# we allow multiple clients so that the client does not think there is another instance running (namely this wrapper)
%{_bindir}/boinc_client --allow_multiple_clients \$@ >> %{_localstatedir}/log/boinc.log 2>> %{_localstatedir}/log/boincerr.log 
EOF
chmod a+x boinc

# remove libtool archives
rm %{buildroot}%{_libdir}/*.la

popd

# own systemd script and logrotate configuration file
rm -f %{buildroot}%{_sysconfdir}/init.d/%{name} %{buildroot}%{_sysconfdir}/sysconfig/%{name}
install -p -m 0755 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
install -p -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
install -p -m 0755 %{SOURCE5} %{buildroot}%{_bindir}

# create .png for app icon and install .desktop file
icotool -x -i 2 clientgui/res/BOINCGUIApp.ico -o %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/boincmgr.png
install -Dp -m 0644 %{SOURCE3} %{buildroot}%{_datadir}/applications/boinc-manager.desktop

%find_lang BOINC-Client
%find_lang BOINC-Manager

# bash-completion
install -Dp -m 0644 client/scripts/boinc.bash %{buildroot}%{_sysconfdir}/bash_completion.d/boinc-client

%pre
getent group boinc >/dev/null || groupadd -r boinc
getent passwd boinc >/dev/null || \
useradd -r -g boinc -d %{_localstatedir}/lib/boinc -s /sbin/nologin -c "BOINC client account." boinc
exit 0

%post
%_post_service %{name}

%preun
%_preun_service %{name}

%postun
%_postun_service %{name}

%files -f BOINC-Client.lang
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/bash_completion.d/
%doc COPYING COPYRIGHT
%{_bindir}/boinc
%{_bindir}/boinc_client
%{_bindir}/boinccmd
%{_bindir}/boinc_gpu
%{_bindir}/switcher
%{_unitdir}/%{name}.service
%{_mandir}/man?/boinccmd.?.*
%{_mandir}/man?/boinc.?.*
%defattr(-,boinc,boinc,-)
%{_localstatedir}/lib/boinc/

%files doc
%doc checkin_notes checkin_notes_*

%files -n boinc-manager -f BOINC-Manager.lang
%{_bindir}/boincmgr
%{_bindir}/boincscr
%{_datadir}/applications/boinc-manager.desktop
%{_iconsdir}/*/*/apps/boincmgr.*
%{_mandir}/man?/boincmgr.?.*

%files static
%{_libdir}/libboinc.a
%{_libdir}/libboinc_api.a
%{_libdir}/libboinc_crypt.a
%{_libdir}/libboinc_graphics2.a
%{_libdir}/libboinc_opencl.a

%files devel
%{_includedir}/boinc

