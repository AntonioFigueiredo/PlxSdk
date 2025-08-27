Name:           plxsdk
BuildRequires:  dkms, kernel-devel, gcc, make, udev
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
for kver in $(ls /usr/src/kernels); do
    mkdir -p obj/$kver
    cp -a COPYING Makefile PlxApi Samples obj/$kver/
    make -C /usr/src/kernels/$kver M=$PWD/obj/$kver modules EXTRA_CFLAGS='-DRHEL_KERNEL'
done

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/lib/modules
for kver in $(ls /usr/src/kernels); do
    make -C /usr/src/kernels/$kver M=$PWD/obj/$kver modules_install INSTALL_MOD_PATH=%{buildroot}
done

# Remove kernel-generated metadata files
find %{buildroot}/lib/modules -type f \
  \( -name 'modules.*' ! -name '*.ko' \) -delete

%files
%defattr(-,root,root)
/lib/modules/*/extra/plxsdk.ko


%changelog