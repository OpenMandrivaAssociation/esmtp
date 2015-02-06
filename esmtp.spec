Summary: 	User configurable relay-only Mail Transfer Agent (MTA)
Name:		esmtp
Version:	1.2
Release:	4
License:	GPLv2+
Group:		Networking/Mail
# http://flow.dl.sourceforge.net/sourceforge/esmtp/
URL:		http://esmtp.sourceforge.net
Source0:	http://heanet.dl.sourceforge.net/sourceforge/esmtp/%{name}-%{version}.tar.bz2
BuildRequires:	libesmtp-devel
Provides:	sendmail-command
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
ESMTP is a user configurable relay-only Mail Transfer Agent (MTA) with a
sendmail-compatible syntax. It's based on libESMTP supporting the AUTH
(including the CRAM-MD5 and NTLM SASL mechanisms) and the StartTLS SMTP
extensions.

So these are ESMTP features:

 * requires no administration privileges
 * individual user configuration
 * sendmail command line compatible
 * supports the AUTH SMTP extension, with the CRAM-MD5 and NTLM SASL
   mechanisms
 * support the StartTLS SMTP extension
 * does not receive mail, expand aliases or manage a queue


%prep
%setup -q


%build
# Avoid making symlinks, this is done  by make alternatives.
%__sed -i 's/\(.*LN_S.*\)/\#\1/' Makefile.in
%configure2_5x
%make


%install
%__rm -rf %buildroot
%makeinstall
%__install -d %buildroot%_sbindir

install -d %{buildroot}%{_sysconfdir}
install -m0644 sample.esmtprc %{buildroot}%{_sysconfdir}/esmtprc

%post
# sendmail-alternatives
update-alternatives --install %_sbindir/sendmail sendmail-command %_bindir/%name 20

%postun
# sendmail-alternatives
if [ "$1" = 0 ]; then
    update-alternatives --remove sendmail-command  %_bindir/%name
fi

%clean
%__rm -rf %buildroot

%files
%defattr(-,root,root)
%doc AUTHORS README TODO ChangeLog sample.esmtprc
%config(noreplace) %{_sysconfdir}/esmtprc
%_bindir/%name
%_mandir/man1/%name.1*
%_mandir/man5/%{name}rc.5*


%changelog
* Tue Jan 18 2011 Oden Eriksson <oeriksson@mandriva.com> 1.2-3mdv2011.0
+ Revision: 631584
- fix #56757 (Please provide a default esmtprc file in /etc allowing local delivery)

* Sun Dec 05 2010 Oden Eriksson <oeriksson@mandriva.com> 1.2-2mdv2011.0
+ Revision: 610385
- rebuild

* Sat Mar 20 2010 Emmanuel Andry <eandry@mandriva.org> 1.2-1mdv2010.1
+ Revision: 525506
- New version 1.2
- use configure2_5x

* Fri Feb 26 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0-3mdv2010.1
+ Revision: 511562
- rebuilt against openssl-0.9.8m

* Thu Sep 10 2009 Thierry Vignaud <tv@mandriva.org> 1.0-2mdv2010.0
+ Revision: 437483
- rebuild

* Sun Feb 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0-1mdv2009.1
+ Revision: 336142
- 1.0

* Wed Sep 17 2008 Michael Scherer <misc@mandriva.org> 0.6.0-2mdv2009.0
+ Revision: 285397
- add sendmail-command, fix #42207
- fix %%post and %%postun, people upgrading should remove the spurious link by hand, as %%postun was incorrect

* Fri Aug 15 2008 Emmanuel Andry <eandry@mandriva.org> 0.6.0-1mdv2009.0
+ Revision: 272336
- New version
- fix license

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild
    - fix spacing at top of description

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Mon Dec 17 2007 Thierry Vignaud <tv@mandriva.org> 0.5.1-1mdv2008.1
+ Revision: 124730
- kill re-definition of %%buildroot on Pixel's request
- do not hardcode man pages extension
- import esmtp


* Wed Mar 01 2006 Nicolas Lécureuil <neoclust@mandriva.org> 0.5.1-1mdk
- New release 0.5.1
- use mkrel

* Thu Jan 13 2005 Lenny Cartier <lenny@mandrakesoft.com> 0.5.0-2mdk
- rebuild

* Thu Dec 11 2003 Han Boetes <han@klama.mandrake.org> 0.5.0-1mdk
- bump and cleanup

* Wed Jul 16 2003 Han Boetes <han@linux-mandrake.com> 0.4.1-1mdk
- bump

* Mon Mar 24 2003 Lenny Cartier <lenny@mandrakesoft.com> 0.3-1mdk
- 0.3

* Fri Dec 27 2002 Han Boetes <han@linux-mandrake.com> 0.2-3mdk
- rebuild because of new rpm macros and new glibc

* Wed Dec 11 2002 Han Boetes <han@mijncomputer.nl> 0.2-2mdk
- Use alternative instead of provides, as suggested by B.Reser

* Sun Dec  8 2002 Han Boetes <han@linux-mandrake.com> 0.2-1mdk
- Initial Release for Mandrake
