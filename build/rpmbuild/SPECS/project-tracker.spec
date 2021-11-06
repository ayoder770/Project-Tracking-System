Name: project-tracker
Version: 2.1
Release: 1
Summary: System to track projects

#Group:
License: N/A
#URL:
Source0: fpdf-install-1.7.2.tar.gz
Source1: project-tracker.tar.gz

#BuildRequires:
Requires: python3

%description



%prep
echo "Prep"
rm -rf %{_builddir}/*

%autosetup -n project-tracker-staging -c
%autosetup -n project-tracker-staging -D -T -a 1



%build
echo "Build"



%install
echo "Install"
rm -rf %{buildroot}/*

cp -a %{_builddir}/project-tracker-staging/* %{buildroot}



# Cleanup after the build process
%clean
rm -rf %{buildroot}
rm -f %{_sourcedir}/*
rm -rf %{_builddir}/*



%files
%defattr(0644,root,root,0755)

# Menu Files
%attr(0644, root, root) /usr/share/applications/project-tracker.desktop
%attr(0644, root, root) /usr/share/applications/project-tracker-build-invoice.desktop
%attr(0644, root, root) /usr/share/applications/project-tracker-client-manager.desktop
%attr(0644, root, root) /etc/xdg/menus/applications-merged/project-tracker.menu

%attr(0755, root, root) /opt/project-tracker/
%attr(0755, root, root) /opt/project-tracker/project_tracker.py
%attr(0755, root, root) /opt/project-tracker/client_manager.py
%attr(0755, root, root) /opt/project-tracker/pay_time.py
%attr(0755, root, root) /opt/project-tracker/pdf.py
%config(noreplace) %attr(0755, root, root) /opt/project-tracker/platform_config.py
%config(noreplace) %attr(0755, root, root) /opt/project-tracker/config_vars.py
%attr(0755, root, root) /opt/project-tracker/buildInvoices.sh
%attr(0666, root, root) /opt/project-tracker/payPeriodStats.txt

%attr(0755, root, root) /opt/project-tracker/images/
%attr(0644, root, root) /opt/project-tracker/images/paypal_button.jpg

%attr(0777, root, root) /opt/project-tracker/database/
%config(noreplace) %attr(0666, root, root) /opt/project-tracker/database/project-tracker.sqlite

%attr(0755, root, root) /usr/local/lib/python3.6/site-packages/



%pre



%post



%changelog
* Sat Nov 06 2021 Andrew Yoder <ayoder770@gmail.com> 2.2
- Updated to include fpdf to rpm
- Get Project Tracker source from tar vs staging in spec
* Tue Sep 28 2021 Andrew Yoder <ayoder770@gmail.com> 2.1
- Removed spreadsheet directory and client workbook
- Added python3 as a dependency to the rpm
* Sun Sep 26 2021 Andrew Yoder <ayoder770@gmail.com> 2.0
- Added new desktop file and script for client manager utility
* Mon Mar 29 2021 Andrew Yoder <ayoder770@gmail.com> 1.1
- Added config_vars.py to spec file list
* Fri Mar 26 2021 Andrew Yoder <ayoder770@gmail.com> 1.1
- Changed name of "freelance.py" to "project_tracker.py"
* Sun Mar 21 2021 Andrew Yoder <ayoder770@gmail.com> 1.0
- Initial Release