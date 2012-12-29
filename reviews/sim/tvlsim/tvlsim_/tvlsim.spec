#
%global mydocs __tmp_docdir
#
Name:           tvlsim
Version:        1.00.0
Release:        1%{?dist}

Summary:        Travel Market Simulator

Group:          System Environment/Libraries 
License:        LGPLv2+
URL:            http://%{name}.sourceforge.net
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:  cmake, python-devel
BuildRequires:  boost-devel, soci-mysql-devel, zeromq-devel, readline-devel
BuildRequires:  stdair-devel, airsched-devel, simfqt-devel, sevmgr-devel
BuildRequires:  airrac-devel, rmol-devel, airinv-devel, simcrs-devel
BuildRequires:  trademgen-devel, travelccm-devel


%description
The Travel Market Simulator project aims at providing reference implementation,
mainly in C++, of a travel market simulator, focusing on revenue management (RM)
for airlines. It is intended to be used for applied research activities only:
it is by no way intended to be used by production systems. It is a new breed of
software and aims to become the new generation PODS (http://podsresearch.com/),
which was instrumental in the inception of the Travel Market Simulator project.

Over a dozen components have been implemented and are fully functional,
encompassing for instance (but not limited to) traveller demand generation
(booking requests), travel distribution (GDS/CRS), low fare search (LFS),
price calculation and inventory availability calculation), customer choice
modelling (CCM), revenue management (RM), schedule and inventory management,
revenue accounting (RA).

The Travel Market Simulator can used in either batch or hosted mode. It is
the main component of the Travel Market Simulator:
http://www.travel-market-simulator

%{name} makes an extensive use of existing open-source libraries for
increased functionality, speed and accuracy. In particular the
Boost (C++ Standard Extensions: http://www.boost.org) library is used.

The %{name} component itself aims at providing a clean API and a simple
implementation, as a C++ library, of a travel market simulator, focusing
on revenue management (RM) for airlines. That library uses the Standard
Airline IT C++ object model (http://sf.net/projects/stdair).

Install the %{name} package if you need a library of basic C++ objects
for airline-related travel market simulator.

%package        devel
Summary:        Header files, libraries and development helper tools for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconfig

%description    devel
This package contains the header files, shared libraries and
development helper tools for %{name}. If you would like to develop
programs using %{name}, you will need to install %{name}-devel.

%package        doc
Summary:        HTML documentation for the %{name} library
Group:          Documentation
%if 0%{?fedora} || 0%{?rhel} > 5
BuildArch:      noarch
%endif
BuildRequires:  tex(latex)
BuildRequires:  doxygen, ghostscript

%description    doc
This package contains HTML pages, as well as a PDF reference manual,
for %{name}. All that documentation is generated thanks to Doxygen
(http://doxygen.org). The content is the same as what can be browsed
online (http://%{name}.org).


%prep
%setup -q


%build
%cmake .
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

mkdir -p %{mydocs}
mv $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/html %{mydocs}
rm -f %{mydocs}/html/installdox

%check
#ctest

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README
%{_bindir}/%{name}
%{_libdir}/lib%{name}.so.*
%{_mandir}/man1/%{name}.1.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/%{name}
%{_bindir}/%{name}-config
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_datadir}/aclocal/%{name}.m4
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/CMake
%{_mandir}/man1/%{name}-config.1.*
%{_mandir}/man3/%{name}-library.3.*

%files doc
%defattr(-,root,root,-)
%doc %{mydocs}/html
%doc COPYING


%changelog
* Sat Dec 29 2012 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 1.00.0-1
- First RPM release

