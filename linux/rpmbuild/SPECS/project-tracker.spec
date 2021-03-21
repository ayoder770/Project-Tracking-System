Name: project-tracker
Version: 1.0
Release: 1
Summary: System to track projects

#Group:
License: N/A
#URL:
#Source0:

#BuildRequires:
#Requires:

%description


%prep

# Clean up any remnants of previous build
rm -rf $RPM_BUILD_ROOT

# Set up the directories
mkdir -p $RPM_BUILD_ROOT/etc/xdg/menus/applications-merged/
mkdir -p $RPM_BUILD_ROOT/usr/share/applications/
mkdir -p $RPM_BUILD_ROOT/opt/project-tracker/database/
mkdir -p $RPM_BUILD_ROOT/opt/project-tracker/images/
mkdir -p $RPM_BUILD_ROOT/opt/project-tracker/spreadsheets/

cp ../../../python/* %{_sourcedir}
cp ../../../scripts/* %{_sourcedir}
cp ../../../linux/menu/* %{_sourcedir}
cp ../../../images/* %{_sourcedir}
cp ../../../configs/* %{_sourcedir}


%build
#%{make_build}


%install
rm -rf $RPM_BUILD_ROOT

install -d -m 0755 $RPM_BUILD_ROOT/opt/project-tracker/
install -d -m 0755 $RPM_BUILD_ROOT/opt/project-tracker/spreadsheets/
install -d -m 0755 $RPM_BUILD_ROOT/opt/project-tracker/images/
install -d -m 0755 $RPM_BUILD_ROOT/opt/project-tracker/database/
install -d -m 0755 $RPM_BUILD_ROOT/usr/share/applications/
install -d -m 0755 $RPM_BUILD_ROOT/etc/xdg/menus/applications-merged/

install -m 0644 %{_sourcedir}/*.desktop $RPM_BUILD_ROOT/usr/share/applications/
install -m 0644 %{_sourcedir}/*.menu $RPM_BUILD_ROOT/etc/xdg/menus/applications-merged/
install -m 0644 %{_sourcedir}/*.jpg $RPM_BUILD_ROOT/opt/project-tracker/images/
install -m 0644 %{_sourcedir}/*.py $RPM_BUILD_ROOT/opt/project-tracker/
install -m 0644 %{_sourcedir}/*.sh $RPM_BUILD_ROOT/opt/project-tracker/

install -m 0644 %{_sourcedir}/clients.xlsx $RPM_BUILD_ROOT/opt/project-tracker/spreadsheets/
install -m 0644 %{_sourcedir}/payPeriodStats.txt $RPM_BUILD_ROOT/opt/project-tracker/
install -m 0644 %{_sourcedir}/project-tracker.sqlite $RPM_BUILD_ROOT/opt/project-tracker/database/



# Cleanup after the build process
%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)

# Menu Files
%attr(0644, root, root) /usr/share/applications/project-tracker.desktop
%attr(0644, root, root) /usr/share/applications/project-tracker-build-invoice.desktop
%attr(0644, root, root) /etc/xdg/menus/applications-merged/project-tracker.menu

%attr(0755, root, root) /opt/project-tracker/
%attr(0755, root, root) /opt/project-tracker/freelance.py
%attr(0755, root, root) /opt/project-tracker/pay_time.py
%attr(0755, root, root) /opt/project-tracker/pdf.py
%attr(0755, root, root) /opt/project-tracker/platform_config.py
%attr(0755, root, root) /opt/project-tracker/buildInvoices.sh
%attr(0666, root, root) /opt/project-tracker/payPeriodStats.txt

%attr(0755, root, root) /opt/project-tracker/spreadsheets/
%config(noreplace) %attr(0666, root, root) /opt/project-tracker/spreadsheets/clients.xlsx

%attr(0755, root, root) /opt/project-tracker/images/
%attr(0644, root, root) /opt/project-tracker/images/paypal_button.jpg

%attr(0755, root, root) /opt/project-tracker/database/
%config(noreplace) %attr(0666, root, root) /opt/project-tracker/database/project-tracker.sqlite


%doc


%pre


%post



%changelog
* Sun Mar 21 2021 Andrew Yoder <ayoder770@gmail.com> 1.0
- Initial Release