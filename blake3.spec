# TODO:
# - switch to rust implementation by default?
# - package b3sum
#
# Conditional build:
%bcond_without	tbb	# multithreading support with tbb library

Summary:	Official implementation of BLAKE3 cryptographic hash function
Summary(pl.UTF-8):	Oficjalna implementacja funkcji skrótu kryptograficznego BLAKE3
Name:		blake3
Version:	1.8.6
Release:	2
License:	CCO or Apache v2.0
Group:		Libraries
Source0:	https://github.com/BLAKE3-team/BLAKE3/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	76b5a080997967e451d99e6f1d1a480b
URL:		https://github.com/BLAKE3-team/BLAKE3
BuildRequires:	cmake >= 3.9
BuildRequires:	libstdc++-devel
BuildRequires:	rpmbuild(macros) >= 2.047
%{?with_tbb:BuildRequires:	tbb-devel >= 2021.11.0}
%{?with_tbb:Requires:	tbb >= 2021.11.0}
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

%description -l pl.UTF-8
BLAKE3 to funkcja skrótu kryptograficznego:
- znacznie szybsza niż MD5, SHA-1, SHA-2, SHA-3 i BLAKE2
- bezpieczna, w przeciwieństwie do MD5 i SHA-1; i bezpieczna względem
  rozszerzania długości, w przeciwieństwie do SHA-2.
- dająca się znacząco zrównoleglić na dowolną liczbę wątków i ścieżek
  SIMD ze względu na występujące wewnątrz drzewo Merkle'a
- pozwalająca na przesyłanie strumieni z weryfikacją i uaktualnieniami
  przyrostowymi, także ze względu na drzewo Merkle'a
- PRF, MAC, KDF, XOF, a także zwykła funkcja skrótu
- jeden algorytm bez wariantów, szybki na x86-64, jak i mniejszych
  architekturach.

%package devel
Summary:	Header files for blake3 library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki blake3
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%{?with_tbb:Requires:	libstdc++-devel}

%description devel
Header files for blake3 library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki blake3.

%prep
%setup -q -n BLAKE3-%{version}

%build
install -d c/build
cd c/build
%cmake .. \
	-DBLAKE3_USE_TBB:BOOL=%{__ON_OFF tbb} \
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
%doc README.md
%{_libdir}/libblake3.so.*.*.*
%ghost %{_libdir}/libblake3.so.0

%files devel
%defattr(644,root,root,755)
%{_libdir}/libblake3.so
%{_includedir}/blake3.h
%{_pkgconfigdir}/libblake3.pc
%{_libdir}/cmake/blake3
