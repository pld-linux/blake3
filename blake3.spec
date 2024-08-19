# TODO:
# - switch to rust implementation by  default?
# - package b3sum
#
Summary:	Official implementation of BLAKE3 cryptographic hash function
Name:		blake3
Version:	1.5.4
Release:	1
License:	CCO or Apache v2.0
Group:		Libraries
Source0:	https://github.com/BLAKE3-team/BLAKE3/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	5745700dfd8bbf665544e259ff4ebfc9
URL:		https://github.com/BLAKE3-team/BLAKE3
BuildRequires:	cmake >= 3.9
BuildRequires:	rpmbuild(macros) >= 2.007
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
BLAKE3 is a cryptographic hash function that is:
- Much faster than MD5, SHA-1, SHA-2, SHA-3, and BLAKE2.
- Secure, unlike MD5 and SHA-1. And secure against length extension,
  unlike SHA-2.
- Highly parallelizable across any number of threads and SIMD lanes,
  because it's a Merkle tree on the inside.
- Capable of verified streaming and incremental updates, again because
  it's a Merkle tree.
- A PRF, MAC, KDF, and XOF, as well as a regular hash.
- One algorithm with no variants, which is fast on x86-64 and also on
  smaller architectures.

%package devel
Summary:	Header files for blake3 library
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for blake3 library.

%prep
%setup -q -n BLAKE3-%{version}

%build
install -d c/build
cd c/build
%cmake .. \
%ifarch %arm_with_neon
	-DBLAKE3_USE_NEON_INTRINSICS:BOOL=ON \
	-DBLAKE3_CFLAGS_NEON=''
%endif

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C c/build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libblake3.so.0
%attr(755,root,root) %{_libdir}/libblake3.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libblake3.so
%{_includedir}/blake3.h
%{_pkgconfigdir}/libblake3.pc
%{_libdir}/cmake/blake3
