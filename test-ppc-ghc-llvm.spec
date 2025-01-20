%global ghc_major 9.12
%global llvm_ver 15

Name:           test-ppc-ghc-llvm
Version:        0
Release:        1%{?dist}
Summary:        testing

License:        MIT

BuildRequires:  ghc%{ghc_major}-compiler
BuildRequires:  llvm%{llvm_ver}
%if v"%{ghc_major}" >= v"9.10"
BuildRequires:  clang%{llvm_ver}
BuildRequires:  numactl-devel
%endif

%description
123

%prep
echo 'main = putStrLn "foo"' > foo.hs

%build
ghc-%{ghc_major} foo.hs -o foo
./foo
[ "$(./foo)" = "foo" ]
touch foo.hs
ghc-%{ghc_major} foo.hs -o foo -fllvm -pgmlc=%{_bindir}/llc-%{llvm_ver} -pgmlo=%{_bindir}/opt-%{llvm_ver} -pgmlas=clang-%{llvm_ver} -fforce-recomp
./foo
[ "$(./foo)" = "foo" ]

%install

%files

%changelog
* Mon Jan 20 2025 Jens Petersen <petersen@redhat.com>
- test https://gitlab.haskell.org/ghc/ghc/-/issues/25667
