%define fontdir %{_datadir}/fonts/liberation
%define catalogue %{_sysconfdir}/X11/fontpath.d

Summary: Fonts to replace commonly used Microsoft Windows Fonts
Name: liberation-fonts
Version: 1.0
Release: 2%{?dist}
License: GPLv2 with exceptions
Group: User Interface/X
URL: https://www.redhat.com/promo/fonts/
Source0: liberation-fonts.tar.gz
Source1: COPYING
Source2: License.txt
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: noarch
Buildrequires: xorg-x11-font-utils

%description
The Liberation Fonts are intended to be replacements for the three
most commonly used fonts on Microsoft systems: Times New Roman,
Arial, and Courier New.

%prep
%setup -q -n %{name} -a 0
%{__cp} %{SOURCE1} %{SOURCE2} %{_builddir}/%{name}

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
# catalogue
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
%{fontdir}/*.ttf
%verify(not md5 size mtime) %{fontdir}/fonts.dir
%verify(not md5 size mtime) %{fontdir}/fonts.scale
%{catalogue}/%{name}

%changelog
* Wed Jan 16 2008 Caius Chance <cchance@redhat.com> - 1.0-2.fc9
- Moved source tarball from cvs to separated storage.

* Mon Jan 14 2008 Caius Chance <cchance@redhat.com> - 1.0-1.fc9
- Resolves: rhbz#428596 (Liberation fonts need to be updated to latest font.)

* Wed Nov 28 2007 Caius Chance <cchance@redhat.com> - 0.2-4.fc9
- Resolves: rhbz#367791 (remove 59-liberation-fonts.conf)

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
