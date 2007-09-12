%define fontdir %{_datadir}/fonts/liberation
%define catalogue %{_sysconfdir}/X11/fontpath.d

Summary: Fonts to replace commonly used Microsoft Windows Fonts
Name: liberation-fonts
Version: 0.2
Release: 3%{?dist}
License: GPLv2 with exceptions
Group: User Interface/X
URL: https://www.redhat.com/promo/fonts/
Source0: https://www.redhat.com/f/fonts/liberation-fonts-ttf-3.tar.gz
Source1: 59-liberation-fonts.conf
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: noarch
Buildrequires: xorg-x11-font-utils

%description
The Liberation Fonts are intended to be replacements for the three
most commonly used fonts on Microsoft systems: Times New Roman,
Arial, and Courier New.

%prep
%setup -q

%clean
rm -rf %{buildroot}

%build

%install
rm -rf %{buildroot}
# fonts
install -m 0755 -d %{buildroot}%{fontdir}
install -m 0644 *.ttf %{buildroot}%{fontdir}
# configuration
install -m 0755 -d %{buildroot}%{_sysconfdir}/fonts/conf.d
install -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/fonts/conf.d

install -d $RPM_BUILD_ROOT%{catalogue}
ln -sf %{fontdir} $RPM_BUILD_ROOT%{catalogue}/%{name}

# generate fonts.dir and fonts.scale
mkfontdir %{buildroot}%{fontdir}
mkfontscale %{buildroot}%{fontdir}

%post
if [ -x /usr/bin/fc-cache ]; then
  /usr/bin/fc-cache %{_datadir}/fonts
fi

%postun
if [ "$1" = "0" ]; then
  if [ -x /usr/bin/fc-cache ]; then
    /usr/bin/fc-cache %{_datadir}/fonts
  fi
fi

%files
%defattr(-,root,root)
%doc License.txt COPYING
%dir %{fontdir}
%config(noreplace) %{_sysconfdir}/fonts/conf.d/59-liberation-fonts.conf
%{fontdir}/*.ttf
%verify(not md5 size mtime) %{fontdir}/fonts.dir
%verify(not md5 size mtime) %{fontdir}/fonts.scale
%{catalogue}/%{name}

%changelog
* Wed Sep 12 2007 Jens Petersen <petersen@redhat.com> - 0.2-3.fc8
- add fontdir macro
- create fonts.dir and fonts.scale (reported by Mark Alford, #245961)
- add catalogue symlink

* Wed Sep 12 2007 Jens Petersen <petersen@redhat.com> - 0.2-2.fc8
- update license field to GPLv2

* Thu Jun 14 2007 Caius Chance <cchance@redhat.com> 0.2-1.fc8
- Updated new source tarball from upstream: '-3' (version 0.2).

* Tue May 15 2007 Matthias Clasen <mclasen@redhat.com> 0.1-9
- Bump revision

* Tue May 15 2007 Matthias Clasen <mclasen@redhat.com> 0.1-8
- Change the license tag to "GPL + font exception"

* Mon May 14 2007 Matthias Clasen <mclasen@redhat.com> 0.1-7
- Correct the source url 

* Mon May 14 2007 Matthias Clasen <mclasen@redhat.com> 0.1-6
- Incorporate package review feedback

* Fri May 11 2007 Matthias Clasen <mclasen@redhat.com> 0.1-5
- Bring the package in sync with Fedora packaging standards

* Wed Apr 25 2007 Meethune Bhowmick <bhowmick@redhat.com> 0.1-4
- Require fontconfig package for post and postun

* Tue Apr 24 2007 Meethune Bhowmick <bhowmick@redhat.com> 0.1-3
- Bump version to fix issue in RHEL4 RHN

* Thu Mar 29 2007 Richard Monk <rmonk@redhat.com> 0.1-2rhis
- New license file

* Thu Mar 29 2007 Richard Monk <rmonk@redhat.com> 0.1-1rhis
- Inital packaging
