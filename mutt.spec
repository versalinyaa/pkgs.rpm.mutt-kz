Summary: A text mode mail user agent.
Name: mutt
%define pversion 1.2.5
Version: %{pversion}i
Release: 3
Serial: 4
Copyright: GPL
Group: Applications/Internet
Source: ftp://ftp.mutt.org/pub/mutt/mutt-%{pversion}i.tar.gz
Patch0: mutt-nosetgid.patch
Patch1: mutt-default.patch
Patch4: mutt-md5.patch
Url: http://www.mutt.org/
Requires: slang >= 0.99.38, smtpdaemon, urlview
BuildPrereq: openssl-devel
Buildroot: %{_tmppath}/mutt-root
Conflicts: mutt-us
Provides: mutt-i
%{!?nokerberos:Requires: krb5-libs}
%{!?nokerberos:BuildPrereq: krb5-devel}

%description
Mutt is a text mode mail user agent. Mutt supports color, threading,
arbitrary key remapping, and a lot of customization.

You should install mutt if you've used mutt in the past and you prefer
it, or if you're new to mail programs and you haven't decided which
one you're going to use.

%prep
%setup -n mutt-%{pversion} -q
%patch0 -p1 -b .nosetgid
%patch1 -p1 -b .default
%patch4 -p1 -b .md5-argh

%build
export -n LINGUAS
CFLAGS="$RPM_OPT_FLAGS" ./prepare --prefix=%{_prefix} \
	--with-sharedir=/etc --sysconfdir=/etc \
	--with-docdir=%{_docdir}/mutt-%{version} \
	--with-mandir=%{_mandir} \
	--with-infodir=%{_infodir} \
	--enable-pop --enable-imap \
	--with-ssl \
%{!?nokerberos:--with-gss=/usr/kerberos} \
	--disable-warnings --with-slang --disable-domain \
	--disable-flock --enable-fcntl
make
%install
rm -rf $RPM_BUILD_ROOT
%makeinstall sharedir=$RPM_BUILD_ROOT/etc \
  sysconfdir=$RPM_BUILD_ROOT/etc \
  docdir=$RPM_BUILD_ROOT%{_docdir}/mutt-%{version} \
  install
mkdir -p $RPM_BUILD_ROOT/etc/X11/applnk/Internet

cat > $RPM_BUILD_ROOT/etc/X11/applnk/Internet/mutt.desktop <<EOF
[Desktop Entry]
Name=Mutt
Name[sv]=Mutt
Type=Application
Comment=Mail reader
Comment[sv]=E-postläsare
Icon=mail2.xpm
MiniIcon=mini-mail.xpm
Exec=mutt
Terminal=true
EOF

# we like GPG here
cat contrib/gpg.rc >> \
	$RPM_BUILD_ROOT/etc/Muttrc

# and we use aspell

cat >> $RPM_BUILD_ROOT/etc/Muttrc <<EOF
# use aspell
set ispell="/usr/bin/aspell --mode=email check"

EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%config /etc/Muttrc
%config (missingok) /etc/X11/applnk/Internet/mutt.desktop
%doc contrib/*.rc README* contrib/sample.* NEWS
%doc COPYRIGHT doc/manual.txt contrib/language* mime.types
%{_bindir}/mutt
%{_bindir}/muttbug
%{_bindir}/pgpring
%{_bindir}/pgpewrap
%{_mandir}/man1/mutt.*
%{_mandir}/man5/muttrc.*
%{_prefix}/share/locale/*/LC_MESSAGES/mutt.mo

%changelog
* Thu Aug 24 2000 Nalin Dahyabhai <nalin@redhat.com>
- rebuild in new environment
- force flock() off and fcntl() on in case defaults change

* Tue Aug  8 2000 Nalin Dahyabhai <nalin@redhat.com>
- enable SSL support

* Fri Aug  4 2000 Bill Nottingham <notting@redhat.com>
- add translation to desktop entry

* Fri Jul 28 2000 Bill Nottingham <notting@redhat.com>
- update to 1.2.5i - fixes IMAP bugs

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Fri Jul  7 2000 Bill Nottingham <notting@redhat.com>
- 1.2.4i

* Tue Jun 27 2000 Nalin Dahyabhai <nalin@redhat.com>
- rebuild in new environment (release 3)
- adjust GSSAPI build logic

* Thu Jun 22 2000 Bill Nottingham <notting@redhat.com>
- fix MD5 code

* Wed Jun 21 2000 Bill Nottingham <notting@redhat.com>
- update to 1.2.2i

* Mon Jun 19 2000 Trond Eivind Glomsrød <teg@redhat.com>
- use aspell

* Sat Jun 10 2000 Bill Nottingham <notting@redhat.com>
- FHS fixes

* Wed May 10 2000 Bill Nottingham <notting@redhat.com>
- add some files

* Tue May  9 2000 Bill Nottingham <notting@redhat.com>
- update to 1.2i

* Tue Apr  4 2000 Bill Nottingham <notting@redhat.com>
- eliminate explicit krb5-configs dependency

* Wed Mar 22 2000 Bill Nottingham <notting@redhat.com>
- auto<foo> is so much fun.

* Wed Mar 01 2000 Nalin Dahyabhai <nalin@redhat.com>
- make kerberos support conditional at compile-time

* Mon Feb 07 2000 Preston Brown <pbrown@redhat.com>
- wmconfig -> desktop

* Fri Feb  4 2000 Bill Nottingham <notting@redhat.com>
- keep the makefiles from re-running autoheader, automake, etc.

* Thu Feb  3 2000 Nalin Dahyabhai <nalin@redhat.com>
- add forward-ported sasl patch

* Thu Feb  3 2000 Bill Nottingham <notting@redhat.com>
- handle compressed man pages, other cleanups

* Wed Jan 19 2000 Bill Nottingham <notting@redhat.com>
- 1.0.1

* Mon Jan  3 2000 Bill Nottingham <notting@redhat.com>
- add the sample mime.types to /usr/doc

* Sat Jan  1 2000 Bill Nottingham <notting@redhat.com>
- fix an odd y2k issue on receiving mail from ancient clients

* Fri Oct 21 1999 Bill Nottingham <notting@redhat.com>
- one-point-oh.

* Fri Sep 25 1999 Bill Nottingham <notting@redhat.com>
- add a buffer overflow patch

* Tue Aug 31 1999 Bill Nottingham <notting@redhat.com>
- update to 1.0pre2

* Tue Aug 17 1999 Bill Nottingham <notting@redhat.com>
- update to 0.95.7
- require urlview since the default muttrc uses it

* Mon Jun 21 1999 Bill Nottingham <notting@redhat.com>
- get correct manual path the Right Way(tm)
- make it so it uses default colors even if COLORFGBG isn't set

* Mon Jun 14 1999 Bill Nottingham <notting@redhat.com>
- update to 0.95.6

* Mon Apr 26 1999 Bill Nottingham <notting@redhat.com>
- try and make sure $RPM_OPT_FLAGS gets passed through

* Fri Apr 23 1999 Bill Nottingham <notting@redhat.com>
- update to 0.95.5

* Mon Mar 29 1999 Bill Nottingham <notting@redhat.com>
- sed correct doc path into /etc/Muttrc for viewing manual

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 3)

* Thu Mar 18 1999 Bill Nottingham <notting@redhat.com>
- strip binary

* Mon Mar  8 1999 Bill Nottingham <notting@redhat.com>
-  update to 0.95.4 - fixes a /tmp race

* Wed Feb 24 1999 Bill Nottingham <notting@redhat.com>
- the RETURN OF WMCONFIG! Aiyeee!

* Fri Feb 12 1999 Bill Nottingham <notting@redhat.com>
- 0.95.3 - fixes mailcap handling

* Mon Jan  4 1999 Bill Nottingham <notting@redhat.com>
- 0.95.1

* Sat Dec 12 1998 Bill Nottingham <notting@redhat.com>
- 0.95

* Fri Jul 31 1998 Bill Nottingham <notting@redhat.com>
- backport some 0.94.2 security fixes
- fix un-setgid
- update to 0.93.2

* Tue Jul 28 1998 Jeff Johnson <jbj@redhat.com>
- security fix
- update to 0.93.1.
- turn off setgid mail.

* Thu May 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Tue Apr 21 1998 Cristian Gafton <gafton@redhat.com>
- updated to 0.91.1

* Fri Apr 10 1998 Cristian Gafton <gafton@redhat.com>
- updated to mutt-0.89.1

* Thu Oct 16 1997 Otto Hammersmith <otto@redhat.com>
- Updated to mutt 0.85.
- added wmconfig entries.
- removed mime.types

* Mon Sep 1 1997 Donnie Barnes <djb@redhat.com>
- Rebuilt to insure all sources were fresh and patches were clean.

* Wed Aug 6 1997 Manoj Kasichainula <manojk@io.com>
 - Initial version for 0.81(e)
