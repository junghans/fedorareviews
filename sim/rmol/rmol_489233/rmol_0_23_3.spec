#
%define mydocs __tmp_docdir
#
Name:           rmol
Version:        0.23.0
Release:        3%{?dist}

Summary:        C++ library of Revenue Management and Optimisation classes and functions

Group:          System Environment/Libraries 
License:        LGPLv2
URL:            http://%{name}.sourceforge.net
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# Patch for g++ 4.5 compatibility. Already fixed by upstream.
Patch0:         rmol_fix_gcc_45_compilation_error.patch

BuildRequires:  gsl-devel
BuildRequires:  boost-devel
BuildRequires:  cppunit-devel
#Requires:       

%description
RMOL is a C++ library of Revenue Management and Optimisation classes 
and functions. Typically, that library may be used by service providers
(e.g., airlines offering flight seats, hotels offering rooms, rental car
companies offering rental days, broadcasting company offering advertisement 
slots, theaters offering seats, etc.) to help in optimising their revenues from
seat capacities.
Most of the algorithms implemented are public and documented in the following
book:
The Theory and practice of Revenue Management, by Kalyan T. Talluri and
Garrett J. van Ryzin, Kluwer Academic Publishers, 2004, ISBN 1-4020-7701-7

Install the %{name} package if you need a library for high-level
revenue management functionality.

%package        devel
Summary:        Header files, libraries and development documentation for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig
Requires(post): info
Requires(preun): info

%description    devel
This package contains the header files, static libraries and
development documentation for %{name}. If you would like to develop
programs using %{name}, you will need to install %{name}-devel.

%package doc
Summary:        HTML documentation for the RMOL library
Group:          Documentation
%if 0%{?fedora} >= 10
BuildArch:      noarch
BuildRequires:  texlive-latex
%endif
%if 0%{?fedora} < 10
BuildRequires:  tetex-latex
%endif
%{?el5:BuildRequires: tetex-latex}
BuildRequires:  doxygen, ghostscript

%description doc
This package contains the documentation in the HTML format of the RMOL
library. The documentation is the same as at the RMOL web page.


%prep
%setup -q

# Apply the g++ 4.5 compatibility patch
%patch0 -p0

# find ./doc -type f -perm 755 -exec chmod 644 {} \;
# Fix some permissions and formats
rm -f INSTALL
chmod -x ABOUT-NLS AUTHORS ChangeLog COPYING NEWS README TODO
find . -type f -name '*.[hc]pp' -exec chmod 644 {} \;


%build
%configure --disable-static
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
%find_lang %{name}
# remove unpackaged files from the buildroot
#rm -f $RPM_BUILD_ROOT%{_includedir}/%{name}/config.h
rm -f $RPM_BUILD_ROOT%{_infodir}/dir
rm -f $RPM_BUILD_ROOT%{_libdir}/lib%{name}.la
# chmod 644 doc/html/installdox doc/html/*.png doc/html/*.ico
rm -rf %{mydocs} && mkdir -p %{mydocs}
mv $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/html %{mydocs}

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post devel
/sbin/install-info %{_infodir}/%{name}-ref.info.* %{_infodir}/dir || :

%preun devel 
if [ "$1" = 0 ]; then
   /sbin/install-info --delete %{_infodir}/%{name}-ref.info.* %{_infodir}/dir || :
fi

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README
%{_bindir}/%{name}
%{_libdir}/lib*.so.*
%{_mandir}/man3/%{name}.3.*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/samples/*.csv

%files devel
%defattr(-,root,root,-)
%{_includedir}/%{name}
%{_bindir}/%{name}-config
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_datadir}/aclocal/%{name}.m4
%{_infodir}/%{name}-ref.info.*
%{_mandir}/man1/%{name}-config.1.*

%files doc
%defattr(-,root,root,-)
%doc %{mydocs}/html
%doc AUTHORS ChangeLog COPYING NEWS README


%changelog
* Wed Jul 28 2010 Denis Arnaud <denis.arnaud_fedora@m4x.org> 0.23.0-3
- Added a patch to fix Rawhide build error

* Fri Jan 22 2010 Rahul Sundaram <sundaram@fedoraproject.org> 0.23.0-2
- Rebuild for Boost soname bump

* Tue Sep 15 2009 Denis Arnaud <denis.arnaud_fedora@m4x.org> 0.23.0-1
- Upstream integration

* Mon May 11 2009 Denis Arnaud <denis.arnaud_fedora@m4x.org> 0.22.0-1
- Upstream integration

* Sun May 10 2009 Denis Arnaud <denis.arnaud_fedora@m4x.org> 0.21.0-3
- Removed dependencies on specific versions (for EL 5)

* Sat May 09 2009 Denis Arnaud <denis.arnaud_fedora@m4x.org> 0.21.0-2
- Removed dependencies on specific versions (for EL 5)

* Mon May 04 2009 Denis Arnaud <denis.arnaud_fedora@m4x.org> 0.21.0-1
- Upstream integration

* Sun May 03 2009 Denis Arnaud <denis.arnaud_fedora@m4x.org> 0.20.0-3
- Added dependency on libicu for Boost 1.37 (Fedora 11)

* Sun May 03 2009 Denis Arnaud <denis.arnaud_fedora@m4x.org> 0.20.0-2
- Added dependency on libicu-devel for Boost 1.37 (Fedora 11)

* Sun May 03 2009 Denis Arnaud <denis.arnaud_fedora@m4x.org> 0.20.0-1
- Upstream integration

* Sun Mar 25 2009 Denis Arnaud <denis.arnaud_fedora@m4x.org> 0.19.0-1
- RPM release for Fedora 10

* Wed Mar  4 2009 Denis Arnaud <denis.arnaud_fedora@m4x.org> 0.18.0-1
- Second RPM release
