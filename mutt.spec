Summary: A text mode mail user agent.
Name: mutt
%define uversion 0.9
Version: 1.4.2.1
Release: 2
Epoch: 5
License: GPL
Group: Applications/Internet
Source: ftp://ftp.mutt.org/pub/mutt/mutt-%{version}i.tar.gz
Source2: ftp://ftp.mutt.org/pub/mutt/contrib/urlview-%{uversion}.tar.gz
Source1: mutt_ldap_query
Source3: mutt-colors
Patch0: mutt-1.4-nosetgid.patch
Patch1: mutt-default.patch
Patch2: mutt-1.2.5-muttbug-tmp.patch
Patch4: mutt-1.4.1-muttrc.patch
Patch5: mutt-sasl.patch
Patch7: mutt-1.4.1-bcc.patch
Patch8: mutt-1.4-sasl2.patch
Patch10: urlview-0.9-default.patch
Patch11: urlview.diff
Patch12: urlview-0.9-ncursesw.patch
Patch13: mutt-1.4.1-plain.patch
Patch14: mutt-1.4.1-rfc1734.patch
Url: http://www.mutt.org/
Requires: smtpdaemon, webclient, mailcap, gettext
Obsoletes: urlview
Provides: urlview
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root
Conflicts: mutt-us
Provides: mutt-i
%{!?nossl:BuildPrereq: openssl-devel}
%{!?nokerberos:BuildPrereq: krb5-devel}
BuildPrereq: cyrus-sasl-devel
BuildPrereq: /usr/sbin/sendmail
BuildPrereq: ncurses-devel >= 5.3-5

%description
Mutt is a text-mode mail user agent. Mutt supports color, threading,
arbitrary key remapping, and a lot of customization.

You should install mutt if you have used it in the past and you prefer
it, or if you are new to mail programs and have not decided which one
you are going to use.

%prep
%setup -n mutt-%{version} -q -a 2
# Thou shalt use fcntl, and only fcntl
%patch0 -p1 -b .nosetgid
# Something to make default colors work right.
# fixme: make sure this is still needed
%patch1 -p1 -b .default
# use mktemp -d in muttbug
%patch2 -p1 -b .tmp
# make it recognize https urls too
%patch4 -p1 -b .https
# fix auth to windows KDCs (#98662)
%patch5 -p1 -b .sasl
%patch7 -p1 -b .bcc
%patch8 -p1 -b .sasl2
%patch10 -p0 -b .default
%patch11 -p0 -b .build
%patch12 -p0 -b .ncursesw
%patch13 -p1 -b .plain
%patch14 -p1 -b .rfc1734
install -m644 %{SOURCE1} mutt_ldap_query

%build
export -n LINGUAS
CFLAGS="$RPM_OPT_FLAGS" ./configure --prefix=%{_prefix} \
	--with-sharedir=/etc --sysconfdir=/etc \
	--with-docdir=%{_docdir}/mutt-%{version} \
	--with-mandir=%{_mandir} \
	--with-infodir=%{_infodir} \
	--enable-pop --enable-imap \
	--with-sasl \
%{!?nossl:--with-ssl} \
%{!?nokerberos:--with-gss} \
	--disable-warnings --with-ncursesw --disable-domain \
	--disable-flock --enable-fcntl
make

cd urlview-%{uversion}
%configure --with-ncursesw
make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall sharedir=$RPM_BUILD_ROOT/etc \
  sysconfdir=$RPM_BUILD_ROOT/etc \
  docdir=$RPM_BUILD_ROOT%{_docdir}/mutt-%{version} \
  install
mkdir -p $RPM_BUILD_ROOT/etc/X11/applnk/Internet

# we like GPG here
cat contrib/gpg.rc >> \
	$RPM_BUILD_ROOT/etc/Muttrc
grep -5 "^color" contrib/sample.muttrc >> \
	$RPM_BUILD_ROOT/etc/Muttrc
# and we use aspell

cat >> $RPM_BUILD_ROOT/etc/Muttrc <<EOF
# use aspell
set ispell="/usr/bin/aspell --mode=email check"
source /etc/Muttrc.local
EOF

touch $RPM_BUILD_ROOT/etc/Muttrc.local

cd urlview-%{uversion}
%makeinstall
install -m 755 url_handler.sh $RPM_BUILD_ROOT%{_bindir}/url_handler.sh
mkdir -p doc/urlview
cp AUTHORS ChangeLog COPYING INSTALL README sample.urlview urlview.sgml \
  doc/urlview
cd ..

# remove unpackaged files from the buildroot
rm -rf $RPM_BUILD_ROOT%{_sysconfdir}/X11
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/mime.types
rm -f $RPM_BUILD_ROOT%{_bindir}/muttbug
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/{muttbug.1,mutt_dotlock.1}*
rm -f $RPM_BUILD_ROOT%{_mandir}/man5/mbox.5*

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root)
%config(noreplace) /etc/Muttrc
%config(noreplace) /etc/Muttrc.local
%doc doc/*.txt
%doc contrib/*.rc README* contrib/sample.* NEWS
%doc COPYRIGHT doc/manual.txt contrib/language* mime.types mutt_ldap_query
%doc urlview-%{uversion}/doc/urlview
%{_bindir}/mutt
%{_bindir}/flea
%{_bindir}/pgpring
%{_bindir}/pgpewrap
%{_bindir}/urlview
%{_bindir}/url_handler.sh
%{_mandir}/man1/urlview.*
%{_mandir}/man1/mutt.*
%{_mandir}/man1/flea.*
%{_mandir}/man5/muttrc.*

%changelog
* Mon Mar  7 2005 Bill Nottingham <notting@redhat.com> 5:1.4.2.1-2
- rebuild against new openssl

* Thu Jan 27 2005 Bill Nottingham <notting@redhat.com> 5:1.4.2.1-1
- update to 1.4.2.1 (#141007, <moritz@barsnick.net>)
- include a /etc/Muttrc.local for site config (#123109)
- add <f2> as a additional help key for terminals that use <f1> internally
  (#139277)

* Wed Sep 15 2004 Nalin Dahyabhai <nalin@redhat.com> 5:1.4.1-10
- expect the server to prompt for additional auth data if we have some to
  send (#129961, upstream #1845)
- use "pop" as the service name instead of "pop-3" when using SASL for POP,
  per rfc1734

* Fri Aug 13 2004 Bill Nottingham <notting@redhat.com> 5:1.4.1-9
- set write_bcc to no by default (since we ship exim)
- build against sasl2 (#126724)

* Mon Jun 28 2004 Bill Nottingham <notting@redhat.com>
- remove autosplat patch (#116769)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun  8 2004 Bill Nottingham <notting@redhat.com> 5:1.4.1-7
- link urlview against ncursesw (fixes #125530, indirectly)

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jan 27 2004 Bill Nottingham <notting@redhat.com> 5:1.4.1-5
- add patch to fix menu padding (CAN-2004-0078, #109317)

* Mon Aug 18 2003 Bill Nottingham <notting@redhat.com> 5:1.4.1-4
- rebuild against ncursesw

* Tue Jul 22 2003 Nalin Dahyabhai <nalin@redhat.com> 5:1.4.1-3.2
- rebuild

* Mon Jul  7 2003 Bill Nottingham <notting@redhat.com> 5:1.4.1-3
- fix auth to windows KDCs (#98662)

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Mar 19 2003 Bill Nottingham <notting@redhat.com> 5:1.4.1-1
- update to 1.4.1, fixes buffer overflow in IMAP code

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Mon Jan 20 2003 Bill Nottingham <notting@redhat.com> 5:1.4-9
- add mailcap requires
- change urlview to htmlview as default browser

* Fri Jan 17 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- change urlview to mozilla as default browser

* Tue Jan 7 2003 Nalin Dahyabhai <nalin@redhat.com> 5:1.4-7
- rebuild

* Mon Dec 2 2002 Bill Nottingham <notting@redhat.com> 5:1.4-6
- ship flea

* Fri Nov 29 2002 Tim Powers <timp@redhat.com> 5:1.4-5
- remove unpackaged files from the buildroot

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Jun 14 2002 Bill Nottingham <notting@redhat.com> 1.4-3
- rebuild against new slang

* Wed May 29 2002 Nalin Dahyabhai <nalin@redhat.com> 1.4-2
- forcibly enable SSL and GSSAPI support

* Wed May 29 2002 Bill Nottingham <notting@redhat.com> 1.4-1
- whoa, 1.4.

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 16 2002 Bill Nottingham <notting@redhat.com>
- autoconf fun

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Jan  1 2002 Bill Nottingham <notting@redhat.com>
- update to 1.2.5.1

* Mon Jul 23 2001 Bill Nottingham <notting@redhat.com>
- don't explictly require krb5-libs, etc.; that's what find-requires is for
  (#49780, sort of)

* Sat Jul 21 2001 Tim Powers <timp@redhat.com>
- no more applnk entries, it's cluttering our menus

* Fri Jul 20 2001 Bill Nottingham <notting@redhat.com>
- add slang-devel to buildprereqs (#49531)

* Mon Jun 11 2001 Bill Nottingham <notting@redhat.com>
- add some sample color definitions (#19471)

* Thu May 24 2001 Bill Nottingham <notting@redhat.com>
- fix typo in muttrc.man (#41610)

* Mon May 14 2001 Bill Nottingham <notting@redhat.com>
- use mktemp in muttbug

* Wed May  2 2001 Nalin Dahyabhai <nalin@redhat.com>
- require webclient, not weclient

* Wed May  2 2001 Bill Nottingham <notting@redhat.com>
- build urlview here

* Fri Mar  2 2001 Nalin Dahyabhai <nalin@redhat.com>
- rebuild in new environment

* Tue Feb 13 2001 Bill Nottingham <notting@redhat.com>
- change buildprereq to /usr/sbin/sendmail (it's what it should have been
  originally)
- %langify

* Tue Feb 13 2001 Michael Stefaniuc <mstefani@redhat.com>
- changed buildprereq to smtpdaemon

* Tue Dec 19 2000 Bill Nottingham <notting@redhat.com>
- rebuild; it's just broken
- fix #13196
- buildprereq sendmail

* Fri Dec 01 2000 Bill Nottingham <notting@redhat.com>
- rebuild because of broken fileutils

* Fri Nov 10 2000 Nalin Dahyabhai <nalin@redhat.com>
- include a sample LDAP query script as a doc file

* Mon Nov  6 2000 Nalin Dahyabhai <nalin@redhat.com>
- patch for imap servers that like to volunteer information after AUTHENTICATE

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
