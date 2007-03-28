### RPM cms dbs-web v03_02_00
## INITENV +PATH PYTHONPATH %i/lib

%define cvstag %v
Source: cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e&module=DBS/Web/DataDiscovery&export=DBS/Web/DataDiscovery&tag=-r%{cvstag}&output=/dbs-web.tar.gz
Requires: python dls py2-sqlalchemy cherrypy mysql py2-mysqldb oracle py2-cx-oracle sqlite py2-pysqlite py2-cheetah webtools yui

%prep
%setup -n DBS
%build
(make DDHOME=%_builddir/DBS/Web/DataDiscovery )

%install
mkdir -p %{i}/bin
mkdir -p %{i}/etc/profile.d
mkdir -p %{i}/lib/Web/DataDiscovery
cp -r Web/DataDiscovery/* %{i}/lib/

ln -s $WEBTOOLS_ROOT %{i}/lib/Web/DataDiscovery/WEBTOOLS
ln -s $YUI_ROOT %{i}/lib/Web/DataDiscovery/yui

# here I use octal code \044 for $ sign since I want "$NAME" to be appear in 
# init.sh file, instead of interpreting it here.
(echo "#!/bin/sh"; \
 echo "source $PYTHON_ROOT/etc/profile.d/init.sh"; \
 echo "source $CHERRYPY_ROOT/etc/profile.d/init.sh"; \
 echo "source $PY2_CHEETAH_ROOT/etc/profile.d/init.sh"; \
 echo "source $PY2_SQLALCHEMY_ROOT/etc/profile.d/init.sh"; \
 echo "source $WEBTOOLS_ROOT/etc/profile.d/init.sh"; \
 echo "source $YUI_ROOT/etc/profile.d/init.sh"; \
 echo "source $ORACLE_ROOT/etc/profile.d/init.sh"; \
 echo "source $PY2_CX_ORACLE_ROOT/etc/profile.d/init.sh"; \
 echo "source $MYSQL_ROOT/etc/profile.d/init.sh"; \
 echo "source $DLS_ROOT/etc/profile.d/init.sh"; \
 echo -e "export DDHOME=\044DBS_WEB_ROOT/lib/Web/DataDiscovery/"; \
 echo "export DLSHOME=$DLS_ROOT"; \
 echo -e "export TNS_ADMIN=\044DBS_WEB_ROOT/lib/Web/DataDiscovery/"; \
 echo -e "export DBS_DBPARAM=\044DBS_WEB_ROOT/lib/Web/DataDiscovery/DBParam"; \
 ) > %{i}/etc/profile.d/dependencies-setup.sh

(echo "#!/bin/tcsh"; \
 echo "source $PYTHON_ROOT/etc/profile.d/init.csh"; \
 echo "source $CHERRYPY_ROOT/etc/profile.d/init.csh"; \
 echo "source $PY2_CHEETAH_ROOT/etc/profile.d/init.csh"; \
 echo "source $PY2_SQLALCHEMY_ROOT/etc/profile.d/init.csh"; \
 echo "source $WEBTOOLS_ROOT/etc/profile.d/init.csh"; \
 echo "source $YUI_ROOT/etc/profile.d/init.csh"; \
 echo "source $ORACLE_ROOT/etc/profile.d/init.csh"; \
 echo "source $PY2_CX_ORACLE_ROOT/etc/profile.d/init.csh"; \
 echo "source $MYSQL_ROOT/etc/profile.d/init.csh"; \
 echo "source $DLS_ROOT/etc/profile.d/init.csh"; \
 echo -e "setenv DDHOME \044DBS_WEB_ROOT/lib/Web/DataDiscovery/"; \
 echo "setenv DLSHOME $DLS_ROOT"; \
 echo -e "setenv TNS_ADMIN \044DBS_WEB_ROOT/lib/Web/DataDiscovery/"; \
 echo -e "setenv DBS_DBPARAM \044DBS_WEB_ROOT/lib/Web/DataDiscovery/DBParam"; \
 ) > %{i}/etc/profile.d/dependencies-setup.csh

# Generate python code from templates 
cd %{i}/lib/Web/DataDiscovery
./scripts/genTemplates.sh

%post
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh
