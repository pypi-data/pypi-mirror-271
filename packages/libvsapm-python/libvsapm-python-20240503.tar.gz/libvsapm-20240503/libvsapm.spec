Name: libvsapm
Version: 20240503
Release: 1
Summary: Library to access the Apple Partition Map (APM) volume system format
Group: System Environment/Libraries
License: LGPL-3.0-or-later
Source: %{name}-%{version}.tar.gz
URL: https://github.com/libyal/libvsapm
            
BuildRequires: gcc            

%description -n libvsapm
Library to access the Apple Partition Map (APM) volume system format

%package -n libvsapm-static
Summary: Library to access the Apple Partition Map (APM) volume system format
Group: Development/Libraries
Requires: libvsapm = %{version}-%{release}

%description -n libvsapm-static
Static library version of libvsapm.

%package -n libvsapm-devel
Summary: Header files and libraries for developing applications for libvsapm
Group: Development/Libraries
Requires: libvsapm = %{version}-%{release}

%description -n libvsapm-devel
Header files and libraries for developing applications for libvsapm.

%package -n libvsapm-python3
Summary: Python 3 bindings for libvsapm
Group: System Environment/Libraries
Requires: libvsapm = %{version}-%{release} python3
BuildRequires: python3-devel python3-setuptools

%description -n libvsapm-python3
Python 3 bindings for libvsapm

%package -n libvsapm-tools
Summary: Several tools for Several tools for reading Apple Partition Map (APM) volume systems
Group: Applications/System
Requires: libvsapm = %{version}-%{release}

%description -n libvsapm-tools
Several tools for Several tools for reading Apple Partition Map (APM) volume systems

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

%files -n libvsapm
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.so.*

%files -n libvsapm-static
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.a

%files -n libvsapm-devel
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.so
%{_libdir}/pkgconfig/libvsapm.pc
%{_includedir}/*
%{_mandir}/man3/*

%files -n libvsapm-python3
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/python3*/site-packages/*.a
%{_libdir}/python3*/site-packages/*.so

%files -n libvsapm-tools
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_bindir}/*
%{_mandir}/man1/*

%changelog
* Fri May  3 2024 Joachim Metz <joachim.metz@gmail.com> 20240503-1
- Auto-generated

