%global with_doc %{!?_without_doc:1}%{?_without_doc:0}

# openstack-packstack package -------------------------------------------------

Name:           openstack-packstack
Version:        2013.2.8
Release:        3%{?dist}
Summary:        Openstack Install Utility

Group:          Applications/System
License:        ASL 2.0 and GPLv2
URL:            https://github.com/stackforge/packstack
Source0:        http://mmagr.fedorapeople.org/downloads/packstack/openstack-packstack-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-setuptools

Requires:       openssh-clients

%description
Packstack is a utility that uses puppet modules to install openstack
packstack can be used to deploy various parts of openstack on multiple
pre installed servers over ssh. It does this by using puppet manifests to
apply Puppet Labs modules (https://github.com/puppetlabs/)

# packstack-modules-puppet package --------------------------------------------

%package -n packstack-modules-puppet
Summary:        Set of Puppet modules for OpenStack

%description -n packstack-modules-puppet
Set of Puppet modules used by Packstack to install OpenStack

# packstack-modules-puppet package --------------------------------------------

%if 0%{?with_doc}
%package doc
Summary:          Documentation for Packstack
Group:            Documentation

# packstack documentation package --------------------------------------------

%if 0%{?rhel}
BuildRequires:  python-sphinx10
%else
BuildRequires:  python-sphinx
%endif

%description      doc
Documentation for Packstack

This package contains documentation files for Packstack.
%endif

# Begin Prep ------------------------------------------------------------------

%prep
%setup -n openstack-packstack-%{version}

# RDO build: enabled EPEL and RDO repos on all hosts by default
#%patch1 -p1

# Sanitizing a lot of the files in the puppet modules, they come from seperate upstream projects
find packstack/puppet/modules \( -name .fixtures.yml -o -name .gemfile -o -name ".travis.yml" -o -name .rspec \) -exec rm {} +
find packstack/puppet/modules \( -name "*.py" -o -name "*.rb" -o -name "*.pl" \) -exec sed -i '/^#!/{d;q}' {} + -exec chmod -x {} +
find packstack/puppet/modules \( -name "*.sh" \) -exec sed -i 's/^#!.*/#!\/bin\/bash/g' {} + -exec chmod +x {} +
find packstack/puppet/modules -name site.pp -size 0 -exec rm {} +
find packstack/puppet/modules \( -name spec -o -name ext \) | xargs rm -rf

# Moving this data directory out temporarily as it causes setup.py to throw errors
rm -rf %{_builddir}/puppet
mv packstack/puppet %{_builddir}/puppet


%build
# puppet on fedora already has this module, using this one causes problems
%if 0%{?fedora}
    rm -rf %{_builddir}/puppet/modules/create_resources
%endif

#%{__python} setup.py build
%{__python} setup.py sdist

%if 0%{?with_doc}
cd docs
%if 0%{?rhel}
make man SPHINXBUILD=sphinx-1.0-build
%else
make man
%endif
%endif


%install
%{__python} setup.py install --skip-build --root %{buildroot}

# Delete tests
rm -fr %{buildroot}%{python_sitelib}/tests

mkdir -p %{buildroot}/%{_datadir}/packstack/
mv %{_builddir}/puppet %{buildroot}/%{python_sitelib}/packstack/puppet
cp -r %{buildroot}/%{python_sitelib}/packstack/puppet/modules  %{buildroot}/%{_datadir}/packstack/modules

%if 0%{?with_doc}
mkdir -p %{buildroot}%{_mandir}/man1
install -p -D -m 644 docs/_build/man/*.1 %{buildroot}%{_mandir}/man1/
%endif


%files
%doc LICENSE
%{_bindir}/packstack
%{python_sitelib}/packstack
%{python_sitelib}/openstack_packstack-%{version}*.egg-info

%if 0%{?with_doc}
%{_mandir}/man1/packstack.1.gz
%endif


%files -n packstack-modules-puppet
%defattr(644,root,root,755)
%{_datadir}/packstack/modules/


%changelog
* Mon Aug 12 2013 wes hayutin <whayutin@redhat.com> 2013.2.8-3
- little clean up (whayutin@redhat.com)
- get the correct dir for spec file (whayutin@redhat.com)
- firestack moves the src around a bit, spec file is removed from the root dir,
  find it in SPECS dir (whayutin@redhat.com)
- underscore vs hyphen (whayutin@redhat.com)
- oops.. don't use bash fi (whayutin@redhat.com)
- fix a few build errors while building in smokestack (whayutin@redhat.com)
- have to change the name of tarball to openstack-packstack for it to build in
  smokestack (whayutin@redhat.com)
- attempt to make packstack spec more like openstack spec files regarding doc
  (whayutin@redhat.com)
- not sure why an extra hyphen is added to the end of the version
  (whayutin@redhat.com)

* Thu Aug 08 2013 wes hayutin <whayutin@redhat.com> 2013.2.8-2
- testing upstream builder and release tagger (whayutin@redhat.com)

* Wed Aug 07 2013 wes hayutin <whayutin@redhat.com> 2013.2.8-1
- manually bump rev (whayutin@redhat.com)
- change source line in spec (whayutin@redhat.com)

* Wed Aug 07 2013 wes hayutin <whayutin@redhat.com>
- change source line in spec (whayutin@redhat.com)

* Wed Aug 07 2013 wes hayutin <whayutin@redhat.com> 2013.2.5-1
- change setup name from packstack to openstack-packstack (whayutin@redhat.com)

* Wed Aug 07 2013 wes hayutin <whayutin@redhat.com> 2013.2.4-1
- version.py is hardcoding the version, will now take it from the spec
  (whayutin@redhat.com)
- remove patch line in spec (whayutin@redhat.com)

* Wed Aug 07 2013 wes hayutin <whayutin@redhat.com> 2013.2.3-1
- updated spec (whayutin@redhat.com)

* Wed Aug 07 2013 wes hayutin <whayutin@redhat.com> 2013.2.2-1.dev691
- new package built with tito

* Thu Aug 01 2013 Martin Mágr <mmagr@redhat.com> - 2013.2.1-0.1.dev691
- Added support for Cinder GlusterFS backend configuration (#919607)
- Added support for linuxbridge (#971770)
- Service names made more descriptive (#947381)
- Increased timeout of kernel update (#973217)
- Set debug=true for Nova to have some logs (#958152)
- kvm.modules is loaded only if it exists (#979041)
- Enable qpidd on boot (#988803)
- Switched to https://github.com/packstack/puppet-qpid (#977786)
- If allinone and quantum selected, install basic network (#986024)

* Mon Jul 15 2013 Pádraig Brady <pbrady@redhat.com> - 2013.2.1-0.1.dev642
- Initial Havana release

* Wed Jul 10 2013 Martin Mágr <mmagr@redhat.com> - 2013.1.1-0.20.dev642
- Fixed provider network option (#976380)
- Made token_format configurable (#978853)
- Enable LVM snap autoextend (#975894)
- MariaDB support (#981116)

* Tue Jun 18 2013 Martin Mágr <mmagr@redhat.com> - 2013.1.1-0.19.dev632
- Restart openstack-cinder-volume service (#975007)

* Wed Jun 12 2013 Martin Mágr <mmagr@redhat.com> - 2013.1.1-0.17.dev631
- Updated Keystone puppet module to have token_format=PKI as default

* Tue Jun 11 2013 Martin Mágr <mmagr@redhat.com> - 2013.1.1-0.16.dev630
- Always update kernel package (#972960)

* Mon Jun 10 2013 Martin Mágr <mmagr@redhat.com> - 2013.1.1-0.15.dev625
- Omit Nova DB password only on compute nodes (#966325)
- Find free device during host startup (#971145)

* Mon Jun 10 2013 Martin Mágr <mmagr@redhat.com> - 2013.1.1-0.14.dev622
- Reverted Nova sql_connection changes because of introduced regression (#966325, #972365)

* Thu Jun 06 2013 Martin Mágr <mmagr@redhat.com> - 2013.1.1-0.12.dev621
- Install qemu-kvm before libvirt (#957632)
- Add template for quantum API server (#968513)
- Removed SQL password in sql_connection for compute hosts (#966325)
- Fixed color usage (#971075)
- Activate cinder-volumes VG and scan PVs after reboot (#971145)

* Tue Jun 05 2013 Martin Mágr <mmagr@redhat.com> - 2013.1.1-0.9.dev605
- Added whitespace filter to Nova and Quantum plugins (rhbz#970674)
- Removed RDO repo installation procedure

* Tue Jun 04 2013 Martin Mágr <mmagr@redhat.com> - 2013.1.1-0.8.dev601
- Updated to packstack-2013.1.1dev601
- Fixes: rhbz#953157, rhbz#966560, rhbz#967291, rhbz#967306, rhbz#967307,
         rhbz#967344, rhbz#967348, rhbz#969975, rhbz#965787

* Thu May 23 2013 Martin Mágr <mmagr@redhat.com> - 2013.1.1-0.7.dev580
- Removing call to setenforce (rhbz#954188)
- Synchronize time using all ntp servers (rhbz#956939)
- Fix for nagios multiple installation failures (rhbz#957006)

* Mon Apr 15 2013 Alan Pevec <apevec@redhat.com> 2013.1.1-0.5.dev538
- enable EPEL and el6-grizzly by default

* Tue Apr 09 2013 Martin Mágr <mmagr@redhat.com> - 2013.1.1-0.4.dev538
- Updated to  packstack-2013.1.1dev538.tar.gz
- Fixes: rhbz#946915, rhbz#947427

* Sun Mar 31 2013 Derek Higgins <derekh@redhat.com> - 2013.1.1-0.3.dev527
- update to packstack-2013.1.1dev527.tar.gz
- no longer require openstack-utils
- packstack now has its own copy of the puppet modules, the symbolic link
  causes problems with package updates

* Fri Mar 15 2013 Derek Higgins <derekh@redhat.com> - 2013.1.1-0.2.dev502
- remove tests

* Fri Mar 15 2013 Derek Higgins <derekh@redhat.com> - 2013.1.1-0.1.dev502
- Udated to grizzly (packstack-2013.1.1dev502.tar.gz)

* Wed Mar 13 2013 Martin Magr <mmagr@redhat.com> - 2012.2.3-0.5.dev475
- Updated to version 2012.2.3dev475

* Wed Feb 27 2013 Martin Magr <mmagr@redhat.com> - 2012.2.3-0.1.dev454
- Updated to version 2012.2.3dev454
- Fixes: rhbz#865347, rhbz#888725, rhbz#892247, rhbz#893107, rhbz#894733,
         rhbz#896618, rhbz#903545, rhbz#903813, rhbz#904670, rhbz#905081,
         rhbz#905368, rhbz#908695, rhbz#908771, rhbz#908846, rhbz#908900,
         rhbz#910089, rhbz#910210, rhbz#911626, rhbz#912006, rhbz#912702,
         rhbz#912745, rhbz#912768, rhbz#915382

* Mon Feb 18 2013 Martin Magr <mmagr@redhat.com> - 2012.2.2-1.0.dev408
- Updated to version 2012.2.2dev408

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2012.2.2-0.9.dev406
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 13 2013 Martin Magr <mmagr@redhat.com> - 2012.2.2-0.8.dev406
- Updated to version 2012.2.2dev406

* Tue Jan 29 2013 Martin Magr <mmagr@redhat.com> - 2012.2.2-0.7.dev346
- Updated to version 2012.2.2dev346

* Mon Jan 28 2013 Martin Magr <mmagr@redhat.com> - 2012.2.2-0.6.dev345
- Updated to version 2012.2.2dev345

* Mon Jan 21 2013 Martin Magr <mmagr@redhat.com> - 2012.2.2-0.5.dev318
- Updated to version 2012.2.2dev318

* Fri Jan 18 2013 Martin Magr <mmagr@redhat.com> - 2012.2.2-0.4.dev315
- Added openstack-utils to Requires
- Updated to version 2012.2.2dev315

* Fri Jan 11 2013 Derek Higgins <derekh@redhat.com> - 2012.2.2-0.3.dev281
- updated to version 2012.2.2dev281

* Fri Dec 07 2012 Derek Higgins <derekh@redhat.com> - 2012.2.2-0.2.dev211
- Fixed packaging, shebang in .sh files was being removed
- updated to version 2012.2.2dev211

* Wed Dec 05 2012 Derek Higgins <derekh@redhat.com> - 2012.2.2-0.1.dev205
- Fixing pre release versioning
- updated to version 2012.2.2dev205

* Fri Nov 30 2012 Derek Higgins <derekh@redhat.com> - 2012.2.1-1dev197
- cleaning up spec file
- updated to version 2012.2.1-1dev197

* Wed Nov 28 2012 Derek Higgins <derekh@redhat.com> - 2012.2.1-1dev186
- example packaging for Fedora / Redhat
