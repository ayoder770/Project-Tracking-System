Name:
Version:
Release:        1%{?dist}
Summary:

Group:
License:
URL:
Source0:

BuildRequires:
Requires:

%description


%prep
%setup -q


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc
