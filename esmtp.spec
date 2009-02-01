Summary: 	User configurable relay-only Mail Transfer Agent (MTA)
Name:		esmtp
Version:	1.0
Release:	%mkrel 1
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
%configure
%make


%install
%__rm -rf %buildroot
%makeinstall
%__install -d %buildroot%_sbindir

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
%_bindir/%name
%_mandir/man1/%name.1*
%_mandir/man5/%{name}rc.5*
