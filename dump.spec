%bcond_without	uclibc

Summary:	Programs for backing up and restoring filesystems
Name:		dump
Version:	0.4b42
Release:	4
License:	BSD
Group:		Archiving/Backup

Source0: 	ftp://osdn.dl.sourceforge.net/pub/sourceforge/d/du/%{name}/%{name}-%{version}.tar.gz
Patch0:		dump-nonroot.patch
Patch2:		dump-0.4b34-check-systypes.patch
Patch3:		dump-0.4b37-compile-fix.patch
Patch4:		dump_progname_mips.patch
Patch5:		dump-rh507948.patch
Patch6:		build-without-selinux.patch
URL:		http://sourceforge.net/projects/dump/

Requires:	rmt = %{version}-%{release}
BuildRequires:	pkgconfig(blkid)
BuildRequires:	pkgconfig(ncursesw)
BuildRequires:	readline-devel
BuildRequires:	pkgconfig(zlib)
BuildRequires:	bzip2-devel
BuildRequires:	pkgconfig(ext2fs) 
%if %{with uclibc}
BuildRequires:	uClibc-devel >= 0.9.33.2-9
%endif

%description
The dump package contains both dump and restore.  Dump examines files in
a filesystem, determines which ones need to be backed up, and copies
those files to a specified disk, tape or other storage medium.  The
restore command performs the inverse function of dump; it can restore a
full backup of a filesystem.  Subsequent incremental backups can then be
layered on top of the full backup.  Single files and directory subtrees
may also be restored from full or partial backups.

%package -n	uclibc-%{name}
Summary:	uClibc linked build of %{name}
Group:		Archiving/Backup
Requires:	uclibc-rmt = %{version}-%{release}

%description -n	uclibc-%{name}
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

%package -n	uclibc-rmt
Summary:	uClibc linked build of rmt
Group:		Archiving/Backup

%description -n	uclibc-rmt
The rmt utility provides remote access to tape devices for programs
like dump (a filesystem backup program), restore (a program for
restoring files from a backup) and tar (an archiving program).

%prep
%setup -q
%patch0 -p0 -b .nonroot
%patch2 -p1 -b .check-systypes
%patch3 -p1 -b .compfix
%patch4 -p1 -b .progname
%patch5 -p1 -b .rh507948
%patch6 -p0 -b .selinux

autoconf

%if %{with uclibc}
mkdir .uclibc
cp -a * .uclibc
%endif

mkdir .system
cp -a * .system

%build
%if %{with uclibc}
pushd .uclibc
%configure2_5x \
	CC="%{uclibc_cc}" \
	CFLAGS="%{uclibc_cflags}" \
	--sbindir=%{uclibc_root}/sbin \
	--bindir=%{uclibc_root}/sbin \
	--with-manowner=root \
	--with-mangrp=root \
	--with-manmode=644 \
	--enable-ermt \
	--disable-kerberos \
	--disable-transselinux
%make top_builddir=$PWD
popd
%endif

pushd .system	
%configure2_5x \
	--with-manowner=root \
	--with-mangrp=root \
	--with-manmode=644 \
	--enable-ermt \
	--disable-kerberos \
	--disable-transselinux
	
%make
popd

%install
%if %{with uclibc}
%makeinstall_std -C .uclibc SBINDIR=%{buildroot}%{uclibc_root}/sbin BINDIR=%{buildroot}%{uclibc_root}/sbin MANDIR=%{buildroot}%{_mandir}/man8
for i in dump restore; do
  mv %{buildroot}%{uclibc_root}/sbin/$i %{buildroot}%{uclibc_root}/sbin/$i.ext3
  ln -s $i.ext3 %{buildroot}%{uclibc_root}/sbin/$i.ext2
  ln -s $i.ext3 %{buildroot}%{uclibc_root}/sbin/$i
done
%endif

make -C .system install SBINDIR=%{buildroot}/sbin BINDIR=%{buildroot}/sbin MANDIR=%{buildroot}%{_mandir}/man8

for i in dump restore; do
  mv %{buildroot}/sbin/$i %{buildroot}/sbin/$i.ext3
  ln -s $i.ext3 %{buildroot}/sbin/$i.ext2
  ln -s $i.ext3 %{buildroot}/sbin/$i
done

pushd %{buildroot}
  mkdir .%{_sysconfdir}
  > .%{_sysconfdir}/dumpdates
  ln -s ../sbin/rmt ./%{_sysconfdir}/rmt
popd

%files
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

%if %{with uclibc}
%files -n uclibc-%{name}
%{uclibc_root}/sbin/dump*
%{uclibc_root}/sbin/restore*
%{uclibc_root}/sbin/rdump
%{uclibc_root}/sbin/rrestore
%endif

%files -n rmt
%doc COPYRIGHT
/sbin/rmt
%{_sysconfdir}/rmt
%{_mandir}/man8/rmt.8*

%if %{with uclibc}
%files -n uclibc-rmt
%{uclibc_root}/sbin/rmt
%endif
