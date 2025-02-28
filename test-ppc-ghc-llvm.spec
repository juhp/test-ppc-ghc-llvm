Name:           test-ppc-ghc-llvm
Version:        0
Release:        1%{?dist}
Summary:        testing

License:        MIT

BuildRequires:  ghc9.12-compiler
BuildRequires:  ghc9.10-compiler
BuildRequires:  ghc9.8-compiler
BuildRequires:  ghc-compiler
BuildRequires:  ghc9.4-compiler
BuildRequires:  ghc9.2-compiler
BuildRequires:  ghc9.0-compiler
BuildRequires:  ghc8.10-compiler
BuildRequires:  llvm12
BuildRequires:  llvm14
BuildRequires:  llvm15
BuildRequires:  llvm17
BuildRequires:  clang15
BuildRequires:  clang17
BuildRequires:  numactl-devel

%description
123

%prep
echo 'main = putStrLn "foo"' > foo.hs

%build
%define test_foo() \
%define ghc_major %1\
%define llvm_ver %2\
ghc-%{ghc_major} foo.hs -o foo\
./foo\
[ "$(./foo)" = "foo" ]\
ghc-%{ghc_major} foo.hs -o foo -fllvm -pgmlc=%{_bindir}/llc-%{llvm_ver} -pgmlo=%{_bindir}/opt-%{llvm_ver} %{?3} -fforce-recomp && ./foo || failed=1\
[ "$(./foo)" = "foo" ] || failed=1

%test_foo 9.12 17 "-pgmlas=clang-17"
%test_foo 9.10 15 "-pgmlas=clang-15"
%test_foo 9.8 15
%test_foo 9.6.6 15
%test_foo 9.4 14
%test_foo 9.2 12
%test_foo 9.0 12
%test_foo 8.10 12

if [ "$failed" = "1" ]; then
  exit 1
fi

%install

%files

%changelog
* Mon Jan 20 2025 Jens Petersen <petersen@redhat.com>
- test https://gitlab.haskell.org/ghc/ghc/-/issues/25667
