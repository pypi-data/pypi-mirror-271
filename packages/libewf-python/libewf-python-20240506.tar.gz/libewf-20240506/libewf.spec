Name: libewf
Version: 20240506
Release: 1
Summary: Library to access the Expert Witness Compression Format (EWF) format
Group: System Environment/Libraries
License: LGPL-3.0-or-later
Source: %{name}-%{version}.tar.gz
URL: https://github.com/libyal/libewf
Requires: bzip2         openssl          zlib
BuildRequires: gcc bzip2-devel         openssl-devel          zlib-devel

%description -n libewf
Library to access the Expert Witness Compression Format (EWF) format

%package -n libewf-static
Summary: Library to access the Expert Witness Compression Format (EWF) format
Group: Development/Libraries
Requires: bzip2         openssl         

%description -n libewf-static
Static library version of libewf.

%package -n libewf-devel
Summary: Header files and libraries for developing applications for libewf
Group: Development/Libraries
Requires: libewf = %{version}-%{release}

%description -n libewf-devel
Header files and libraries for developing applications for libewf.

%package -n libewf-python3
Summary: Python 3 bindings for libewf
Group: System Environment/Libraries
Requires: libewf = %{version}-%{release} python3
BuildRequires: python3-devel python3-setuptools

%description -n libewf-python3
Python 3 bindings for libewf

%package -n libewf-tools
Summary: Several tools for reading and writing EWF files
Group: Applications/System
Requires: libewf = %{version}-%{release}  openssl fuse3-libs    libuuid
BuildRequires: byacc flex  openssl-devel fuse3-devel    libuuid-devel

%description -n libewf-tools
Several tools for reading and writing EWF files

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

%files -n libewf
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.so.*

%files -n libewf-static
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.a

%files -n libewf-devel
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.so
%{_libdir}/pkgconfig/libewf.pc
%{_includedir}/*
%{_mandir}/man3/*

%files -n libewf-python3
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/python3*/site-packages/*.a
%{_libdir}/python3*/site-packages/*.so

%files -n libewf-tools
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_bindir}/*
%{_mandir}/man1/*

# Exclude ewfdebug tool
%exclude %{_bindir}/ewfdebug

%changelog
* Mon May  6 2024 Joachim Metz <joachim.metz@gmail.com> 20240506-1
- Auto-generated

