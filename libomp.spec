%ifarch ppc64le
%global libomp_arch ppc64
%else
%global libomp_arch %{_arch}
%endif


Name: libomp
Version: 6.0.0
Release: 2%{?dist}
Summary: OpenMP runtime for clang

License: NCSA
URL: http://openmp.llvm.org	
Source0: http://llvm.org/releases/%{version}/openmp-%{version}%{?rc_ver:rc%{rc_ver}}.src.tar.xz

Patch0: 0001-CMake-Make-LIBOMP_HEADERS_INSTALL_PATH-a-cache-varia.patch

BuildRequires: cmake
BuildRequires: elfutils-libelf-devel
BuildRequires: perl
BuildRequires: perl-Data-Dumper
BuildRequires: perl-Encode
BuildRequires: libffi-devel

Requires: elfutils-libelf%{?isa}

# libomp does not support s390x.
ExcludeArch: s390x

%description
OpenMP runtime for clang.

%package devel
Summary: OpenMP header files
Requires: clang-devel%{?isa} = %{version}

%description devel
OpenMP header files.

%prep
%autosetup -n openmp-%{version}%{?rc_ver:rc%{rc_ver}}.src -p1

%build
mkdir -p _build
cd _build

%cmake .. \
	-DLIBOMP_INSTALL_ALIASES=OFF \
	-DLIBOMP_HEADERS_INSTALL_PATH:PATH=%{_libdir}/clang/%{version}/include \
%if 0%{?__isa_bits} == 64
	-DOPENMP_LIBDIR_SUFFIX=64 \
%else
	-DOPENMP_LIBDIR_SUFFIX= \
%endif

%make_build


%install
%make_install -C _build


%files
%{_libdir}/libomp.so
%{_libdir}/libomptarget.so
%ifnarch %{arm} %{ix86}
%{_libdir}/libomptarget.rtl.%{libomp_arch}.so
%endif

%files devel
%{_libdir}/clang/%{version}/include/omp.h
%ifnarch %{arm}
%{_libdir}/clang/%{version}/include/ompt.h
%endif

%changelog
* Wed Mar 28 2018 Tom Stellard <tstellar@redhat.com> - 6.0.0-2
- Enable libomptarget plugins

* Fri Mar 09 2018 Tom Stellard <tstellar@redhat.com> - 6.0.0-1
- 6.0.0 Release

* Tue Feb 13 2018 Tom Stellard <tstellar@redhat.com> - 6.0.0-0.3.rc2
- 6.0.0-rc2 Release

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.0-0.2.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 25 2018 Tom Stellard <tstellar@redhat.com> - 6.0.0-0.1.rc1
- 6.0.0-rc1 Release

* Thu Dec 21 2017 Tom Stellard <tstellar@redhat.com> - 5.0.1-1
- 5.0.1 Release.

* Mon May 15 2017 Tom Stellard <tstellar@redhat.com> - 5.0.0-1
- Initial version.
