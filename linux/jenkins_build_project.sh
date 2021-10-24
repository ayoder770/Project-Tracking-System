#!/bin/bash
######################################################################
# File History
# 10/24/2021 - Andrew Yoder : Initial Release to build Linux rpm from
#                             Jenkins
######################################################################

# Set up rpmbuild area
mkdir -p "${WORKSPACE}/linux/rpmbuild/BUILD/"
mkdir -p "${WORKSPACE}/linux/rpmbuild/BUILDROOT/"
mkdir -p "${WORKSPACE}/linux/rpmbuild/RPMS/"
mkdir -p "${WORKSPACE}/linux/rpmbuild/SOURCES/"
mkdir -p "${WORKSPACE}/linux/rpmbuild/SPECS/"
mkdir -p "${WORKSPACE}/linux/rpmbuild/SRPMS/"

# Build the rpm
rpmbuild --define "_topdir ${WORKSPACE}/linux/rpmbuild/" --target noarch -ba "${WORKSPACE}/linux/rpmbuild/SPECS/project-tracker.spec"

# Copy the rpm to Jenkins workspace
cp "${WORKSPACE}/linux/rpmbuild/RPMS/noarch/project-tracker*.rpm" "$WORKSPACE"