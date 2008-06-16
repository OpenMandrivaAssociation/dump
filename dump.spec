%define	name	dump
%define version 0.4b41
%define release %mkrel 6

Summary:	Programs for backing up and restoring filesystems
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD
Group:		Archiving/Backup

Source: 	ftp://osdn.dl.sourceforge.net/pub/sourceforge/d/du/%{name}/%{name}-%{version}.tar.bz2
Patch0:		dump-nonroot.patch
Patch2:		dump-0.4b34-check-systypes.patch
Patch3:		dump-0.4b37-compile-fix.patch
Url:		http://sourceforge.net/projects/dump/

Requires:	rmt = %{version}-%{release}
BuildRequires:	e2fsprogs-devel >= 1.15
BuildRequires:	ncurses-devel
BuildRequires:	termcap-devel
BuildRequires:	readline-devel
BuildRequires:	zlib-devel
BuildRequires:	bzip2-devel
BuildRequires:	openssl-devel >= 0.9.7a
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The dump package contains both dump and restore.  Dump examines files in
a filesystem, determines which ones need to be backed up, and copies
those files to a specified disk, tape or other storage medium.  The
restore command performs the inverse function of dump; it can restore a
full backup of a filesystem.  Subsequent incremental backups can then be
layered on top of the full backup.  Single files and directory subtrees
may also be restored from full or partial backups.

%package -n	rmt
Summary:	Provides certain programs with access to remote tape devices
Group:		Archiving/Backup
Provides:	/sbin/rmt

%description -n	rmt
The rmt utility provides remote access to tape devices for programs
like dump (a filesystem backup program), restore (a program for
restoring files from a backup) and tar (an archiving program).

%prep
%setup -q
%patch0 -p0 -b .nonroot
%patch2 -p1 -b .check-systypes
%patch3 -p1 -b .compfix
autoconf

%build
%configure2_5x \
	--with-manowner=root \
	--with-mangrp=root \
	--with-manmode=644 \
	--enable-ermt \
	--disable-kerberos

%make OPT="$RPM_OPT_FLAGS -Wall -Wpointer-arith -Wstrict-prototypes -Wmissing-prototypes -Wno-char-subscripts"

%install
rm -rf $RPM_BUILD_ROOT

make install SBINDIR=$RPM_BUILD_ROOT/sbin BINDIR=$RPM_BUILD_ROOT/sbin MANDIR=${RPM_BUILD_ROOT}%{_mandir}/man8

for i in dump restore; do
  mv $RPM_BUILD_ROOT/sbin/$i $RPM_BUILD_ROOT/sbin/$i.ext3
  ln -s $i.ext3 $RPM_BUILD_ROOT/sbin/$i.ext2
  ln -s $i.ext3 $RPM_BUILD_ROOT/sbin/$i
done

pushd $RPM_BUILD_ROOT
  mkdir .%{_sysconfdir}
  > .%{_sysconfdir}/dumpdates
  ln -s ../sbin/rmt ./%{_sysconfdir}/rmt
popd

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc CHANGES COPYRIGHT KNOWNBUGS README THANKS TODO MAINTAINERS dump.lsm
%attr(0664,root,disk)	%config(noreplace) %{_sysconfdir}/dumpdates
#%attr(6755,root,tty)	/sbin/dump
/sbin/dump*
#%attr(6755,root,tty)	/sbin/restore
/sbin/restore*
/sbin/rdump
/sbin/rrestore
%{_mandir}/man8/dump.8*
%{_mandir}/man8/rdump.8*
%{_mandir}/man8/restore.8*
%{_mandir}/man8/rrestore.8*

%files -n rmt
%defattr(-,root,root)
%doc COPYRIGHT
/sbin/rmt
%{_sysconfdir}/rmt
%{_mandir}/man8/rmt.8*
