Name:           plxsdk
BuildRequires:  gcc, make
License:        GPL-2.0+
Summary:        plxsdk
Version:        0.1
Release:        0%{?dist}
URL:            https://github.com/AntonioFigueiredo/PlxSdk.git
Source0:        %{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%define debug_package %{nil}

%description
PlxSDK

%prep
%setup -q


%build
export TERM=dumb
make -C PlxApi PLX_SDK_DIR=$(pwd)

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}/usr/lib64
#cp PlxApi/libPlxApi.so %{buildroot}/usr/lib64/ || true
cp Library/PlxApi.a %{buildroot}/usr/lib64/ || true

#mkdir -p %{buildroot}/usr/share/plxsdk/examples
#cp -a Samples/* %{buildroot}/usr/share/plxsdk/examples/

%files
%defattr(-,root,root)

#/usr/lib64/PlxApi.so
/usr/lib64/PlxApi.a

/usr/include/plxsdk/*

/usr/share/plxsdk/examples/*

%changelog