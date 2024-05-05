Name: libsigscan
Version: 20240505
Release: 1
Summary: Library for binary signature scanning
Group: System Environment/Libraries
License: LGPL-3.0-or-later
Source: %{name}-%{version}.tar.gz
URL: https://github.com/libyal/libsigscan
          
BuildRequires: gcc          

%description -n libsigscan
Library for binary signature scanning

%package -n libsigscan-static
Summary: Library for binary signature scanning
Group: Development/Libraries
Requires: libsigscan = %{version}-%{release}

%description -n libsigscan-static
Static library version of libsigscan.

%package -n libsigscan-devel
Summary: Header files and libraries for developing applications for libsigscan
Group: Development/Libraries
Requires: libsigscan = %{version}-%{release}

%description -n libsigscan-devel
Header files and libraries for developing applications for libsigscan.

%package -n libsigscan-python3
Summary: Python 3 bindings for libsigscan
Group: System Environment/Libraries
Requires: libsigscan = %{version}-%{release} python3
BuildRequires: python3-devel python3-setuptools

%description -n libsigscan-python3
Python 3 bindings for libsigscan

%package -n libsigscan-tools
Summary: Several tools for binary signature scanning files
Group: Applications/System
Requires: libsigscan = %{version}-%{release}

%description -n libsigscan-tools
Several tools for binary signature scanning files

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

%files -n libsigscan
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.so.*

%files -n libsigscan-static
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.a

%files -n libsigscan-devel
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.so
%{_libdir}/pkgconfig/libsigscan.pc
%{_includedir}/*
%{_mandir}/man3/*

%files -n libsigscan-python3
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/python3*/site-packages/*.a
%{_libdir}/python3*/site-packages/*.so

%files -n libsigscan-tools
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_bindir}/*
%{_mandir}/man1/*
%config %{_sysconfdir}/sigscan.conf

%changelog
* Sun May  5 2024 Joachim Metz <joachim.metz@gmail.com> 20240505-1
- Auto-generated

