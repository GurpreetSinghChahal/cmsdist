### RPM external dd4hep v01-05

%define tag 9c2170c5cefa60dd034b7eec19dfb0a023fc64be
%define branch master
%define github_user AIDASoft

Source: git+https://github.com/%{github_user}/DD4hep.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz

BuildRequires: cmake

Requires: root boost clhep xerces-c py2-rootpy

%prep

%setup -n %{n}-%{realversion}

%build

rm -rf ../build
mkdir ../build
cd ../build

export BOOST_ROOT
cmake -DCMAKE_INSTALL_PREFIX="%{i}" \
      -DBoost_NO_BOOST_CMAKE=ON \
      -DCMAKE_PREFIX_PATH=${CLHEP_ROOT} \
      -DDD4HEP_USE_XERCESC=ON \
      -DXERCESC_ROOT_DIR=${XERCES_C_ROOT} \
      -DDD4HEP_USE_PYROOT=ON \
      -DCMAKE_BUILD_TYPE=Release \
      ../%{n}-%{realversion}

make %{makeprocesses} VERBOSE=1

%install

cd ../build
make install

%post
%{relocateConfig}*.cmake
%{relocateConfig}bin/*.sh
%{relocateConfig}bin/*.csh
