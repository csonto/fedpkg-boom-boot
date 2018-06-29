%global summary A set of libraries and tools for managing boot loader entries
%global sphinx_docs 1

Name:		boom-boot
Version:	0.9
Release:	2%{?dist}
Summary:	%{summary}

License:	GPLv2
URL:		https://github.com/bmr-cymru/boom
Source0:	https://github.com/bmr-cymru/boom/archive/%{version}/boom-%{version}.tar.gz

BuildArch:	noarch

BuildRequires:	python3-setuptools
BuildRequires:	python3-devel
%if 0%{?sphinx_docs}
BuildRequires:	python3-sphinx
%endif

%description
Boom is a boot manager for Linux systems using boot loaders that support
the BootLoader Specification for boot entry configuration.

Boom requires a BLS compatible boot loader to function: either the
systemd-boot project, or Grub2 with the BLS patch (Red Hat Grub2 builds
include this support in both Red Hat Enterprise Linux 7 and Fedora).

%prep
%setup -q -n boom-%{version}
# NOTE: Do not use backup extension - MANIFEST.in is picking them

%build
%if 0%{?sphinx_docs}
make -C doc html
rm doc/_build/html/.buildinfo
mv doc/_build/html doc/html
rm -r doc/_build
%endif

%py3_build

%install
%py3_install

# Install Grub2 integration scripts
mkdir -p ${RPM_BUILD_ROOT}/etc/grub.d
mkdir -p ${RPM_BUILD_ROOT}/etc/default
install -m 755 etc/grub.d/42_boom ${RPM_BUILD_ROOT}/etc/grub.d
install -m 644 etc/default/boom ${RPM_BUILD_ROOT}/etc/default

# Make configuration directories
# mode 0700 - in line with /boot/grub2 directory:
install -d -m 700 ${RPM_BUILD_ROOT}/boot/boom/profiles
install -d -m 700 ${RPM_BUILD_ROOT}/boot/loader/entries
install -m 644 examples/boom.conf ${RPM_BUILD_ROOT}/boot/boom

mkdir -p ${RPM_BUILD_ROOT}/%{_mandir}/man8
mkdir -p ${RPM_BUILD_ROOT}/%{_mandir}/man5
install -m 644 man/man8/boom.8 ${RPM_BUILD_ROOT}/%{_mandir}/man8
install -m 644 man/man5/boom.5 ${RPM_BUILD_ROOT}/%{_mandir}/man5

rm doc/Makefile
rm doc/conf.py

# Test suite currently does not operate in rpmbuild environment
#%%check
#%%{__python3} setup.py test

%package -n python3-boom
Summary: %{summary}
%{?python_provide:%python_provide python3-boom}
Requires: python3
Recommends: (lvm2 or brtfs-progs)

# There used to be a boom package in fedora, and there is boom packaged in
# copr. How to tell which one is installed? We need python3-boom and no boom
# only.
Conflicts: boom

%package grub2
Summary: %{summary}
Supplements: (grub2 and python3-boom)

%description -n python3-boom
Boom is a boot manager for Linux systems using boot loaders that support
the BootLoader Specification for boot entry configuration.

Boom requires a BLS compatible boot loader to function: either the
systemd-boot project, or Grub2 with the BLS patch (Red Hat Grub2 builds
include this support in both Red Hat Enterprise Linux 7 and Fedora).

This package provides the python3 version of boom.

%description grub2
Boom is a boot manager for Linux systems using boot loaders that support
the BootLoader Specification for boot entry configuration.

Boom requires a BLS compatible boot loader to function: either the
systemd-boot project, or Grub2 with the BLS patch (Red Hat Grub2 builds
include this support in both Red Hat Enterprise Linux 7 and Fedora).

This package provides the integration scripts for grub2 bootloader.

%files -n python3-boom
%{_bindir}/boom
%license COPYING
%doc README.md
%doc %{_mandir}/man*/boom.*
%doc doc
%doc examples
%doc tests
%{python3_sitelib}/*
%dir /boot/boom
%config(noreplace) /boot/boom/boom.conf
%dir /boot/boom/profiles
%dir /boot/loader/entries

%files grub2
%license COPYING
%doc README.md
%{_sysconfdir}/grub.d/42_boom
%config(noreplace) %{_sysconfdir}/default/boom


%changelog
* Wed Jun 27 2018 Marian Csontos <mcsontos@redhat.com> 0.9-2
- Spin off grub2 into subpackage

* Wed Jun 27 2018 Marian Csontos <mcsontos@redhat.com> 0.9-1
- Update to new upstream 0.9.
- Fix boot_id caching.

* Fri Jun 08 2018 Marian Csontos <mcsontos@redhat.com> 0.8.5-6.2
- Remove example files from /boot/boom/profiles.

* Fri May 11 2018 Marian Csontos <mcsontos@redhat.com> 0.8.5-6.1
- Files in /boot are treated as configuration files.

* Thu Apr 26 2018 Marian Csontos <mcsontos@redhat.com> 0.8.5-6
- Package upstream version 0.8-5.6

