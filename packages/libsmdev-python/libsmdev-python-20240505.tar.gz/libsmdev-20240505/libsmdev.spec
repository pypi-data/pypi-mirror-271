Name: libsmdev
Version: 20240505
Release: 1
Summary: Library to access and read storage media (SM) devices
Group: System Environment/Libraries
License: LGPL-3.0-or-later
Source: %{name}-%{version}.tar.gz
URL: https://github.com/libyal/libsmdev
       
BuildRequires: gcc       

%description -n libsmdev
Library to access and read storage media (SM) devices

%package -n libsmdev-static
Summary: Library to access and read storage media (SM) devices
Group: Development/Libraries
Requires: libsmdev = %{version}-%{release}

%description -n libsmdev-static
Static library version of libsmdev.

%package -n libsmdev-devel
Summary: Header files and libraries for developing applications for libsmdev
Group: Development/Libraries
Requires: libsmdev = %{version}-%{release}

%description -n libsmdev-devel
Header files and libraries for developing applications for libsmdev.

%package -n libsmdev-python3
Summary: Python 3 bindings for libsmdev
Group: System Environment/Libraries
Requires: libsmdev = %{version}-%{release} python3
BuildRequires: python3-devel python3-setuptools

%description -n libsmdev-python3
Python 3 bindings for libsmdev

%package -n libsmdev-tools
Summary: Several tools for accessing storage media (SM) devices
Group: Applications/System
Requires: libsmdev = %{version}-%{release}

%description -n libsmdev-tools
Several tools for accessing storage media (SM) devices

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

%files -n libsmdev
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.so.*

%files -n libsmdev-static
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.a

%files -n libsmdev-devel
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.so
%{_libdir}/pkgconfig/libsmdev.pc
%{_includedir}/*
%{_mandir}/man3/*

%files -n libsmdev-python3
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/python3*/site-packages/*.a
%{_libdir}/python3*/site-packages/*.so

%files -n libsmdev-tools
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_bindir}/*
%{_mandir}/man1/*

%changelog
* Sun May  5 2024 Joachim Metz <joachim.metz@gmail.com> 20240505-1
- Auto-generated

