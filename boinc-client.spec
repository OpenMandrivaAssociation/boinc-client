%define Werror_cflags %nil

Summary:	The BOINC client core
Name:		boinc-client
Version:	7.0.28
Release:	%mkrel 1
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
BuildRequires:	python-mysql
BuildRequires:	curl-devel
BuildRequires:	desktop-file-utils
BuildRequires:	wxgtku-devel
BuildRequires:	gettext
BuildRequires:	mysql-devel
BuildRequires:	docbook-utils
BuildRequires:	sqlite3-devel
%if %{mdvver} < 201100
BuildRequires:	mesaglut-devel
%else
BuildRequires:	glut-devel
%endif
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

