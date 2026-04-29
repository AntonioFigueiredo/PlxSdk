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
make -C src/PlxApi PLX_SDK_DIR=$(pwd)/src

%install
rm -rf %{buildroot}

# Install complete SDK source tree for driver/module builds
mkdir -p %{buildroot}/usr/src/%{name}-%{version}/

# Install DKMS config if present
if [ -f debian/plxsdk-dkms.dkms ]; then
    cp debian/plxsdk-dkms.dkms %{buildroot}/usr/src/%{name}-%{version}/dkms.conf
fi

# Install static library
mkdir -p %{buildroot}/usr/lib64
cp src/PlxApi/Library/PlxApi.a %{buildroot}/usr/lib64/ || true

# Install headers
mkdir -p %{buildroot}/usr/include/plxsdk
cp -a src/Include/* %{buildroot}/usr/include/plxsdk/

# Install utility scripts/binaries
mkdir -p %{buildroot}/usr/bin
cp src/Bin/Plx_load %{buildroot}/usr/bin/
cp src/Bin/Plx_unload %{buildroot}/usr/bin/
cp src/Bin/startlog %{buildroot}/usr/bin/

# Install sample source code
mkdir -p %{buildroot}/usr/share/plxsdk/examples
cp -a src/Samples/* %{buildroot}/usr/share/plxsdk/examples/

%files
%defattr(-,root,root)
/usr/src/%{name}-%{version}
/usr/lib64/PlxApi.a
/usr/include/plxsdk/*
/usr/bin/Plx_load
/usr/bin/Plx_unload
/usr/bin/startlog
/usr/share/plxsdk/examples/*

%changelog