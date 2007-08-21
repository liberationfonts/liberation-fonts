%define srcname    liberation-fonts
%define srcver     0.2
%define srcdir     %{srcname}-%{srcver}

Summary:      Fonts to replace commonly used Microsoft Windows Fonts
Name:         liberation-fonts
Version:      0.2
Release:      1%{?dist}
License:      GPL + font exception
Group:        User Interface/X
URL:          https://www.redhat.com/promo/fonts/
Source0:      https://www.redhat.com/f/fonts/liberation-fonts-ttf-3.tar.gz 
Source1:      59-liberation-fonts.conf
BuildRoot:    %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:    noarch
Requires:     fontconfig


%description
The Liberation Fonts are intended to be replacements for the three most commonly used fonts on Microsoft systems: Times New Roman, Arial, and Courier New.


%prep
%setup -q -c


%clean
rm -rf %{buildroot}


%build


%install
rm -rf %{buildroot}
# fonts
install -m 0755 -d %{buildroot}%{_datadir}/fonts/liberation
install -m 0644 %{srcdir}/*.ttf %{buildroot}%{_datadir}/fonts/liberation
# configuration
install -m 0755 -d %{buildroot}%{_sysconfdir}/fonts/conf.d
install -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/fonts/conf.d


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
%doc %{srcdir}/License.txt %{srcdir}/COPYING
%{_datadir}/fonts/liberation
%config(noreplace) %{_sysconfdir}/fonts/conf.d/59-liberation-fonts.conf


%changelog
* Tue Aug 21 2007 Caius Chance <cchance@redhat.com> 0.2-1.fc7
- Resolves: rhbz#250753 Incorrect lincense file.
- Synchonized source tarball version with upstream (0.2).

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
