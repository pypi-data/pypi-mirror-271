Name: libvslvm
Version: 20240504
Release: 1
Summary: Library to access the Linux Logical Volume Manager (LVM) volume system
Group: System Environment/Libraries
License: LGPL-3.0-or-later
Source: %{name}-%{version}.tar.gz
URL: https://github.com/libyal/libvslvm
             
BuildRequires: gcc             

%description -n libvslvm
Library to access the Linux Logical Volume Manager (LVM) volume system

%package -n libvslvm-static
Summary: Library to access the Linux Logical Volume Manager (LVM) volume system
Group: Development/Libraries
Requires: libvslvm = %{version}-%{release}

%description -n libvslvm-static
Static library version of libvslvm.

%package -n libvslvm-devel
Summary: Header files and libraries for developing applications for libvslvm
Group: Development/Libraries
Requires: libvslvm = %{version}-%{release}

%description -n libvslvm-devel
Header files and libraries for developing applications for libvslvm.

%package -n libvslvm-python3
Summary: Python 3 bindings for libvslvm
Group: System Environment/Libraries
Requires: libvslvm = %{version}-%{release} python3
BuildRequires: python3-devel python3-setuptools

%description -n libvslvm-python3
Python 3 bindings for libvslvm

%package -n libvslvm-tools
Summary: Several tools for Several tools for reading Linux Logical Volume Manager (LVM) volume systems
Group: Applications/System
Requires: libvslvm = %{version}-%{release} fuse3-libs
BuildRequires: fuse3-devel

%description -n libvslvm-tools
Several tools for Several tools for reading Linux Logical Volume Manager (LVM) volume systems

%prep
%setup -q

%build
%configure --prefix=/usr --libdir=%{_libdir} --mandir=%{_mandir} --enable-python
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
%make_install

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -n libvslvm
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.so.*

%files -n libvslvm-static
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.a

%files -n libvslvm-devel
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.so
%{_libdir}/pkgconfig/libvslvm.pc
%{_includedir}/*
%{_mandir}/man3/*

%files -n libvslvm-python3
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/python3*/site-packages/*.a
%{_libdir}/python3*/site-packages/*.so

%files -n libvslvm-tools
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_bindir}/*
%{_mandir}/man1/*

%changelog
* Sat May  4 2024 Joachim Metz <joachim.metz@gmail.com> 20240504-1
- Auto-generated

