Name: libvsgpt
Version: 20240504
Release: 1
Summary: Library to access the GUID Partition Table (GPT) volume system format
Group: System Environment/Libraries
License: LGPL-3.0-or-later
Source: %{name}-%{version}.tar.gz
URL: https://github.com/libyal/libvsgpt
             
BuildRequires: gcc             

%description -n libvsgpt
Library to access the GUID Partition Table (GPT) volume system format

%package -n libvsgpt-static
Summary: Library to access the GUID Partition Table (GPT) volume system format
Group: Development/Libraries
Requires: libvsgpt = %{version}-%{release}

%description -n libvsgpt-static
Static library version of libvsgpt.

%package -n libvsgpt-devel
Summary: Header files and libraries for developing applications for libvsgpt
Group: Development/Libraries
Requires: libvsgpt = %{version}-%{release}

%description -n libvsgpt-devel
Header files and libraries for developing applications for libvsgpt.

%package -n libvsgpt-python3
Summary: Python 3 bindings for libvsgpt
Group: System Environment/Libraries
Requires: libvsgpt = %{version}-%{release} python3
BuildRequires: python3-devel python3-setuptools

%description -n libvsgpt-python3
Python 3 bindings for libvsgpt

%package -n libvsgpt-tools
Summary: Several tools for Several tools for reading GUID Partition Table (GPT) volume systems
Group: Applications/System
Requires: libvsgpt = %{version}-%{release}

%description -n libvsgpt-tools
Several tools for Several tools for reading GUID Partition Table (GPT) volume systems

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

%files -n libvsgpt
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.so.*

%files -n libvsgpt-static
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.a

%files -n libvsgpt-devel
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.so
%{_libdir}/pkgconfig/libvsgpt.pc
%{_includedir}/*
%{_mandir}/man3/*

%files -n libvsgpt-python3
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/python3*/site-packages/*.a
%{_libdir}/python3*/site-packages/*.so

%files -n libvsgpt-tools
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_bindir}/*
%{_mandir}/man1/*

%changelog
* Sat May  4 2024 Joachim Metz <joachim.metz@gmail.com> 20240504-1
- Auto-generated

