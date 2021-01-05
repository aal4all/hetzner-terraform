#
# spec file for package python-parallax
#
# Copyright (c) 2016 SUSE LINUX GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


Name:           python3-parallax
Version:        1.0.6
Release:        0
Summary:        Execute commands and copy files over SSH to multiple machines at once
License:        BSD-3-Clause
Group:          Development/Languages/Python
Url:            https://github.com/krig/parallax/
Source:         https://pypi.python.org/packages/source/p/parallax/parallax-%{version}.tar.gz
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Requires:       openssh
BuildArch:      noarch
%if 0%{?suse_version}
Requires(post):   update-alternatives
Requires(postun): update-alternatives
%else
Requires(post):   /usr/sbin/update-alternatives
Requires(postun): /usr/sbin/update-alternatives
%endif

%description
Parallax SSH provides an interface to executing commands on multiple
nodes at once using SSH. It also provides commands for sending and receiving files to
multiple nodes using SCP.

%prep
%setup -q -n parallax-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

# create a dummy target for /etc/alternatives/parallax-askpass
mkdir -p %{buildroot}%{_sysconfdir}/alternatives
mv %{buildroot}%{_bindir}/parallax-askpass %{buildroot}%{_bindir}/parallax-askpass-%{py_ver}
ln -s -f %{_sysconfdir}/alternatives/parallax-askpass %{buildroot}%{_bindir}/parallax-askpass

%post
%_sbindir/update-alternatives \
   --install %{_bindir}/parallax-askpass parallax-askpass %{_bindir}/parallax-askpass-%{py_ver} 20

%preun
if [ "$1" = 0 ] ; then
   %_sbindir/update-alternatives --remove parallax-askpass %{_bindir}/parallax-askpass-%{py_ver}
fi

%files
%defattr(-,root,root,-)
%doc AUTHORS README.md COPYING
%{python3_sitelib}/parallax
%{python3_sitelib}/parallax-%{version}*.egg-info
%{_bindir}/parallax-askpass
%{_bindir}/parallax-askpass-%{py_ver}
%ghost %_sysconfdir/alternatives/parallax-askpass

%changelog
* Tue Jan  5 2021 Falko.Benthin@ZIT-BB.Brandenburg.de>
- update to version 1.0.6
* Thu Dec  8 2016 kgronlund@suse.com
- Fix broken build for non-SUSE distributions (again)
* Mon Aug 15 2016 toddrme2178@gmail.com
- Fix update-alternatives implementation.
* Wed Apr 27 2016 kgronlund@suse.com
- Fix broken package build for non-SUSE distributions
* Mon Mar  7 2016 kgronlund@suse.com
- Add alternatives entry for parallax-askpass
* Fri Jun 12 2015 kgronlund@suse.com
- Release 1.0.1
  + The host list expander function was not unicode-safe (bsc#934594)
  + Clean up and update documentation for Options.inline (#1)
  + Fix python3 error using askpass option (krig/parallel-ssh#1)
* Thu Feb 12 2015 kgronlund@suse.com
- Release 1.0.0a3
  - Be more accepting with format of limit argument
  - Fix incorrect name of options attribute
* Sat Jan  3 2015 p.drouand@gmail.com
- Fix license to be SPDX compliant; applied license is BSD3 derived
* Thu Dec 25 2014 kgronlund@suse.com
- Release 1.0.0a2
  - Prepend hostname on each line when -P is set (fate#318220)
  - Fix quiet option after API patch
* Thu Nov 20 2014 kgronlund@suse.com
- Revised packaging
- Removed dependency on xz
* Wed Oct 15 2014 kgronlund@suse.com
- Initial release.
