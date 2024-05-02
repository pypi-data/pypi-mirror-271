Name: libbde
Version: 20240502
Release: 1
Summary: Library to access the BitLocker Drive Encryption (BDE) format
Group: System Environment/Libraries
License: LGPL-3.0-or-later
Source: %{name}-%{version}.tar.gz
URL: https://github.com/libyal/libbde
Requires:         openssl        
BuildRequires: gcc         openssl-devel        

%description -n libbde
Library to access the BitLocker Drive Encryption (BDE) format

%package -n libbde-static
Summary: Library to access the BitLocker Drive Encryption (BDE) format
Group: Development/Libraries
Requires: libbde = %{version}-%{release}

%description -n libbde-static
Static library version of libbde.

%package -n libbde-devel
Summary: Header files and libraries for developing applications for libbde
Group: Development/Libraries
Requires: libbde = %{version}-%{release}

%description -n libbde-devel
Header files and libraries for developing applications for libbde.

%package -n libbde-python3
Summary: Python 3 bindings for libbde
Group: System Environment/Libraries
Requires: libbde = %{version}-%{release} python3
BuildRequires: python3-devel python3-setuptools

%description -n libbde-python3
Python 3 bindings for libbde

%package -n libbde-tools
Summary: Several tools for reading BitLocker Drive Encryption volumes
Group: Applications/System
Requires: libbde = %{version}-%{release} fuse3-libs
BuildRequires: fuse3-devel

%description -n libbde-tools
Several tools for reading BitLocker Drive Encryption volumes

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

%files -n libbde
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.so.*

%files -n libbde-static
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.a

%files -n libbde-devel
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.so
%{_libdir}/pkgconfig/libbde.pc
%{_includedir}/*
%{_mandir}/man3/*

%files -n libbde-python3
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/python3*/site-packages/*.a
%{_libdir}/python3*/site-packages/*.so

%files -n libbde-tools
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_bindir}/*
%{_mandir}/man1/*

%changelog
* Thu May  2 2024 Joachim Metz <joachim.metz@gmail.com> 20240502-1
- Auto-generated

