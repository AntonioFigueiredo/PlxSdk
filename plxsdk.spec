Name:           plxsdk
BuildRequires:  gcc, make, kernel-devel, elfutils-libelf-devel
License:        GPL-2.0+
Summary:        plxsdk
Version:        0.1
Release:        0%{?dist}
URL:            https://github.com/AntonioFigueiredo/PlxSdk.git
Source0:        %{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Requires(post): kmod
Requires(postun): kmod

%define debug_package %{nil}

%description
PlxSDK

%prep
%setup -q


%build
export TERM=dumb
make -C PlxApi PLX_SDK_DIR=$(pwd)

mkdir -p built-kmods
export PLX_SDK_DIR=$(pwd)

for kdir in /usr/src/kernels/*; do
    [ -d "$kdir" ] || continue
    krel=$(basename "$kdir")

    echo "Building PLX kernel modules for $krel"

    cd Driver
    for target in 8000n 8000d 6000n 9050 9030 9080 9054 9056 9656 8311 Svc; do
        sh ./builddriver "$target" cleanall
    done

    for target in 8000n 8000d 6000n 9050 9030 9080 9054 9056 9656 8311 Svc; do
        KDIR="$kdir" sh ./builddriver "$target"
    done
    cd ..

    mkdir -p "built-kmods/$krel"
    find Driver -maxdepth 2 -type f -name 'Plx*.ko' -exec cp -a {} "built-kmods/$krel/" \;
done

%install
rm -rf %{buildroot}

# Install complete SDK source tree for driver/module builds
mkdir -p %{buildroot}/usr/src/%{name}-%{version}/
cp -a Driver %{buildroot}/usr/src/%{name}-%{version}/
cp -a Include %{buildroot}/usr/src/%{name}-%{version}/
cp -a Makefiles %{buildroot}/usr/src/%{name}-%{version}/
cp -a PlxApi %{buildroot}/usr/src/%{name}-%{version}/
cp -a Bin %{buildroot}/usr/src/%{name}-%{version}/
cp -a Samples %{buildroot}/usr/src/%{name}-%{version}/
cp -a Makefile %{buildroot}/usr/src/%{name}-%{version}/

# Install static library
mkdir -p %{buildroot}/usr/lib64
cp PlxApi/Library/PlxApi.a %{buildroot}/usr/lib64/ || true

# Install headers
mkdir -p %{buildroot}/usr/include/plxsdk
cp -a Include/* %{buildroot}/usr/include/plxsdk/

# Install utility scripts/binaries
mkdir -p %{buildroot}/usr/bin
cp Bin/Plx_load %{buildroot}/usr/bin/
cp Bin/Plx_unload %{buildroot}/usr/bin/
cp Bin/startlog %{buildroot}/usr/bin/

# Install sample source code
mkdir -p %{buildroot}/usr/share/plxsdk/examples
cp -a Samples/* %{buildroot}/usr/share/plxsdk/examples/

# Install prebuilt kernel modules
for krel_dir in built-kmods/*; do
    [ -d "$krel_dir" ] || continue
    krel=$(basename "$krel_dir")
    mkdir -p %{buildroot}/lib/modules/$krel/extra/plxsdk
    cp -a "$krel_dir"/*.ko %{buildroot}/lib/modules/$krel/extra/plxsdk/
done

%post
for modules_dir in /lib/modules/*; do
    [ -d "$modules_dir/extra/plxsdk" ] || continue
    /usr/sbin/depmod "$(basename "$modules_dir")" >/dev/null 2>&1 || :
done

%postun
for modules_dir in /lib/modules/*; do
    [ -d "$modules_dir" ] || continue
    /usr/sbin/depmod "$(basename "$modules_dir")" >/dev/null 2>&1 || :
done

%files
%defattr(-,root,root)
/lib/modules/*/extra/plxsdk/*.ko
/usr/src/%{name}-%{version}
/usr/lib64/PlxApi.a
/usr/include/plxsdk/*
/usr/bin/Plx_load
/usr/bin/Plx_unload
/usr/bin/startlog
/usr/share/plxsdk/examples/*

%changelog
