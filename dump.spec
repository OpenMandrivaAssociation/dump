%define _disable_rebuild_configure 1

Summary:	Programs for backing up and restoring filesystems
Name:		dump
Version:	0.4b46
Release:	4
License:	BSD
Group:		Archiving/Backup
Url:		http://sourceforge.net/projects/dump/
Source0: 	ftp://osdn.dl.sourceforge.net/pub/sourceforge/d/du/%{name}/%{name}-%{version}.tar.gz
Patch0:		dump-0.4b37-compile-fix.patch
Patch1:		dump_progname_mips.patch
Patch2:		dump-0.4b46-openssl11.patch
Patch3:		dump-remove-lzo.patch
Patch4:		dump-glibc_xattr.patch
Patch5:		dump-0.4b46-fix-build-with-modern-compilers.patch
# Please do NOT import the "dump-buildfix.patch" Fedora applies here.
# It is badly broken and unneeded.
BuildRequires:	libtool
BuildRequires:	pkgconfig(bzip2)
BuildRequires:	pkgconfig(readline)
BuildRequires:	pkgconfig(blkid)
BuildRequires:	pkgconfig(ext2fs)
BuildRequires:	pkgconfig(com_err)
BuildRequires:	pkgconfig(ncursesw)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(lzo2)
Requires:	rmt = %{EVRD}
Requires:	setup

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
%autosetup -p1
rm -f compat/include/{lzoconf,minilzo}.h
rm -f compat/lib/minilzo.c

%build
autoreconf -fiv
%configure \
	--with-manowner=root \
	--with-mangrp=root \
	--with-manmode=644 \
	--enable-ermt \
	--disable-kerberos \
	--disable-transselinux

%make_build OPT="$RPM_OPT_FLAGS -fPIC -Wall -Wpointer-arith -Wstrict-prototypes -Wmissing-prototypes -Wno-char-subscripts -fno-strict-aliasing"

%install
%make_install

for i in dump restore; do
  mv %{buildroot}%{_sbindir}/$i %{buildroot}%{_sbindir}/$i.ext3
  ln -s $i.ext3 %{buildroot}%{_sbindir}/$i.ext2
  ln -s $i.ext3 %{buildroot}%{_sbindir}/$i
done

cd %{buildroot}
  mkdir .%{_sysconfdir}
  > .%{_sysconfdir}/dumpdates
  ln -s ..%{_sbindir}/rmt ./%{_sysconfdir}/rmt
cd ..

%files
%doc AUTHORS ChangeLog KNOWNBUGS NEWS README REPORTING-BUGS TODO MAINTAINERS dump.lsm
%license COPYING
%attr(0664,root,disk)	%config(noreplace) %{_sysconfdir}/dumpdates
#attr(6755,root,tty)	{_sbindir}/dump
%{_sbindir}/dump*
#attr(6755,root,tty)	{_sbindir}/restore
%{_sbindir}/restore*
%{_sbindir}/rdump
%{_sbindir}/rrestore
%doc %{_mandir}/man8/dump.8*
%doc %{_mandir}/man8/rdump.8*
%doc %{_mandir}/man8/restore.8*
%doc %{_mandir}/man8/rrestore.8*

%files -n rmt
%license COPYING
%{_sbindir}/ermt
%{_sbindir}/rmt
%{_sysconfdir}/rmt
%doc %{_mandir}/man8/rmt.8*
