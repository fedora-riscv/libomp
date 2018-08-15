%ifarch ppc64le
%global libomp_arch ppc64
%else
%global libomp_arch %{_arch}
%endif

%global rc_ver 1

Name: libomp
Version: 7.0.0
Release: 0.1.rc%{rc_ver}%{?dist}
Summary: OpenMP runtime for clang

License: NCSA
URL: http://openmp.llvm.org	
Source0: http://%{?rc_ver:pre}releases.llvm.org/%{version}/%{?rc_ver:rc%{rc_ver}}/openmp-%{version}%{?rc_ver:rc%{rc_ver}}.src.tar.xz
Source1: runtest.sh

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

%package test
Summary: OpenMP regression tests
Requires: %{name}%{?isa} = %{version}
Requires: %{name}-devel%{?isa} = %{version}
Requires: clang
Requires: llvm
Requires: gcc
Requires: gcc-c++
Requires: python3-lit

%description test
OpenMP regression tests

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

# Test package setup
%global libomp_srcdir %{_datadir}/libomp/src/
%global libomp_testdir %{libomp_srcdir}/runtime/test/
%global gcc_lit_cfg %{buildroot}%{libomp_testdir}/gcc.site.cfg
%global clang_lit_cfg %{buildroot}%{libomp_testdir}/clang.site.cfg

install -d %{buildroot}%{libomp_srcdir}/runtime
cp -R runtime/test  %{buildroot}%{libomp_srcdir}/runtime
cp -R runtime/src  %{buildroot}%{libomp_srcdir}/runtime

# Add symlinks to the libomp headers/library so gcc can find them.
ln -s %{_libdir}/clang/%{version}/include/omp.h %{buildroot}%{libomp_testdir}/omp.h
ln -s %{_libdir}/clang/%{version}/include/ompt.h %{buildroot}%{libomp_testdir}/ompt.h
ln -s %{_libdir}/libomp.so %{buildroot}%{libomp_testdir}/libgomp.so

# Generic test config
echo "import tempfile" > %{gcc_lit_cfg}
cat _build/runtime/test/lit.site.cfg >> %{gcc_lit_cfg}
sed -i 's~\(config.test_filecheck = \)""~\1"%{_libdir}/llvm/FileCheck"~' %{gcc_lit_cfg}
sed -i 's~\(config.omp_header_directory = \)"[^"]\+"~\1"%{_includedir}"~' %{gcc_lit_cfg}
sed -i 's~\(config.libomp_obj_root = \)"[^"]\+"~\1tempfile.mkdtemp()[1]~' %{gcc_lit_cfg}
sed -i 's~\(lit_config.load_config(config, \)"[^"]\+"~\1"%{libomp_testdir}/lit.cfg"~' %{gcc_lit_cfg}

# GCC config
# test_compiler_features was already populated with gcc information if gcc was used
# to compile libomp.
sed -i 's~\(config.test_c_compiler = \)"[^"]\+"~\1"%{_bindir}/gcc"~' %{gcc_lit_cfg}
sed -i 's~\(config.test_cxx_compiler = \)"[^"]\+"~\1"%{_bindir}/g++"~' %{gcc_lit_cfg}
sed -i 's~\(config.library_dir = \)"[^"]\+"~\1"%{libomp_testdir}"~' %{gcc_lit_cfg}

# Clang config
cp %{gcc_lit_cfg} %{clang_lit_cfg}
sed -i 's~\(config.test_compiler_features = \)\[[^\[]\+]~\1["clang"]~' %{clang_lit_cfg}
sed -i 's~\(config.test_c_compiler = \)"[^"]\+"~\1"%{_bindir}/clang"~' %{clang_lit_cfg}
sed -i 's~\(config.test_cxx_compiler = \)"[^"]\+"~\1"%{_bindir}/clang++"~' %{clang_lit_cfg}
sed -i 's~\(config.library_dir = \)"[^"]\+"~\1"%{_libdir}"~' %{clang_lit_cfg}

install -m 0755 %{SOURCE1} %{buildroot}%{_datadir}/libomp


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

%files test
%{_datadir}/libomp

%changelog
* Tue Aug 14 2018 Tom Stellard <tstellar@redhat.com> - 7.0.0-0.1.rc1
- 7.0.1-rc1 Release

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 02 2018 Tom Stellard <tstellar@redhat.com> - 6.0.1-2
- Add -threads option to runtest.sh

* Thu Jun 28 2018 Tom Stellard <tstellar@redhat.com> - 6.0.1-1
- 6.0.1 Release

* Fri May 11 2018 Tom Stellard <tstellar@redhat.com> - 6.0.0-0.1.rc1
- 6.0.1-rc1 Release

* Wed Mar 28 2018 Tom Stellard <tstellar@redhat.com> - 6.0.0-3
- Add test package

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
