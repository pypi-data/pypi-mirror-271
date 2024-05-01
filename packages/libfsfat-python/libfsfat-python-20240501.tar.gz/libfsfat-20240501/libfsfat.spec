Name: libfsfat
Version: 20240501
Release: 1
Summary: Library to support the File Allocation Table (FAT) file system format
Group: System Environment/Libraries
License: LGPL-3.0-or-later
Source: %{name}-%{version}.tar.gz
URL: https://github.com/libyal/libfsfat
              
BuildRequires: gcc              

%description -n libfsfat
Library to support the File Allocation Table (FAT) file system format

%package -n libfsfat-static
Summary: Library to support the File Allocation Table (FAT) file system format
Group: Development/Libraries
Requires: libfsfat = %{version}-%{release}

%description -n libfsfat-static
Static library version of libfsfat.

%package -n libfsfat-devel
Summary: Header files and libraries for developing applications for libfsfat
Group: Development/Libraries
Requires: libfsfat = %{version}-%{release}

%description -n libfsfat-devel
Header files and libraries for developing applications for libfsfat.

%package -n libfsfat-python3
Summary: Python 3 bindings for libfsfat
Group: System Environment/Libraries
Requires: libfsfat = %{version}-%{release} python3
BuildRequires: python3-devel python3-setuptools

%description -n libfsfat-python3
Python 3 bindings for libfsfat

%package -n libfsfat-tools
Summary: Several tools for reading File Allocation Table (FAT) file system volumes
Group: Applications/System
Requires: libfsfat = %{version}-%{release} openssl fuse3-libs 
BuildRequires: openssl-devel fuse3-devel 

%description -n libfsfat-tools
Several tools for reading File Allocation Table (FAT) file system volumes

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

%files -n libfsfat
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.so.*

%files -n libfsfat-static
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.a

%files -n libfsfat-devel
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.so
%{_libdir}/pkgconfig/libfsfat.pc
%{_includedir}/*
%{_mandir}/man3/*

%files -n libfsfat-python3
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/python3*/site-packages/*.a
%{_libdir}/python3*/site-packages/*.so

%files -n libfsfat-tools
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_bindir}/*
%{_mandir}/man1/*

%changelog
* Wed May  1 2024 Joachim Metz <joachim.metz@gmail.com> 20240501-1
- Auto-generated

