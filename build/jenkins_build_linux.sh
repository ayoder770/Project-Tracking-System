#!/bin/bash
######################################################################
# File Name: jenkins_build_linux.sh
#
# Description: Build Linux packages from Jenkins
#
# File History
# 10/24/2021 - Andrew Yoder : Initial Release to build Linux rpm from
#                             Jenkins
# 11/06/2021 - Andrew Yoder : Build fpdf 1.7.2 and create tar file
#                           : Create tar file for Project Tracker source
#                           : Update to support both rpm and deb builds
######################################################################

# Which Linux distro to build. Supports 'rpm' and 'deb'
distro="$1"

# Version and Release of Build
version="$2"
release="$3"

if [ "$#" -ne 3 ]; then
  echo "Must supply three arguments: <rpm|deb> <version> <release>"
  exit 1
fi

# Build fpdf and create tar file
fpdf_dir="${WORKSPACE}/build/third-party-python/fpdf/"
rm -rf "${fpdf_dir}/build/"
rm -rf "${fpdf_dir}/install/"

mkdir -p "${fpdf_dir}/build/"
mkdir -p "${fpdf_dir}/install/"

tar xf "${fpdf_dir}/fpdf-1.7.2.tar.gz" -C "${fpdf_dir}/build/"
cd "${fpdf_dir}/build/fpdf-1.7.2/"

python3 setup.py build
python3 setup.py install --prefix=/usr/local --root="${fpdf_dir}/install/"

tar czf "${fpdf_dir}/fpdf-install-1.7.2.tar.gz" -C "${fpdf_dir}/install/" .


# Stage File Structure and create source tar file
staging="${WORKSPACE}/build/project-tracker-staging/"
rm -rf "$staging"
mkdir -p "$staging"

mkdir -p "${staging}/opt/project-tracker/"
mkdir -p "${staging}/opt/project-tracker/images/"
mkdir -p "${staging}/opt/project-tracker/database/"
mkdir -p "${staging}/usr/share/applications/"
mkdir -p "${staging}/etc/xdg/menus/applications-merged/"

cp ${WORKSPACE}/python/* ${WORKSPACE}/scripts/* "${staging}/opt/project-tracker/"
cp ${WORKSPACE}/linux/menu/*.desktop "${staging}/usr/share/applications/"
cp ${WORKSPACE}/linux/menu/*.menu "${staging}/etc/xdg/menus/applications-merged/"
cp ${WORKSPACE}/images/* "${staging}/opt/project-tracker/images/"
cp ${WORKSPACE}/configs/payPeriodStats.txt "${staging}/opt/project-tracker/"
cp ${WORKSPACE}/configs/project-tracker.sqlite "${staging}/opt/project-tracker/database/"

tar czf "${WORKSPACE}/build/project-tracker.tar.gz" -C "${WORKSPACE}/build/project-tracker-staging/" .

# Build rpm Package
if [ "$distro" == "rpm" ]; then

  # Clean the SOURCES and BUILD dir
  rm -rf "${WORKSPACE}/build/rpmbuild/SOURCES/"
  rm -rf "${WORKSPACE}/build/rpmbuild/BUILD/"

  # Set up rpmbuild area
  mkdir -p "${WORKSPACE}/build/rpmbuild/BUILD/"
  mkdir -p "${WORKSPACE}/build/rpmbuild/BUILDROOT/"
  mkdir -p "${WORKSPACE}/build/rpmbuild/RPMS/"
  mkdir -p "${WORKSPACE}/build/rpmbuild/SOURCES/"
  mkdir -p "${WORKSPACE}/build/rpmbuild/SPECS/"
  mkdir -p "${WORKSPACE}/build/rpmbuild/SRPMS/"

  # Stage the source tar files
  cp "${WORKSPACE}/build/project-tracker.tar.gz" "${WORKSPACE}/build/rpmbuild/SOURCES/"
  cp "${fpdf_dir}/fpdf-install-1.7.2.tar.gz" "${WORKSPACE}/build/rpmbuild/SOURCES/"

  # Build the rpm
  rpmbuild --define "_version ${version}" --define "_release ${release}" --define "_topdir ${WORKSPACE}/build/rpmbuild/" --target noarch -ba "${WORKSPACE}/build/rpmbuild/SPECS/project-tracker.spec"

  # Copy the rpm to Jenkins workspace
  cp ${WORKSPACE}/build/rpmbuild/RPMS/noarch/project-tracker*rpm "$WORKSPACE"

fi


# Build deb package
if [ "$distro" == "deb" ]; then

  rm -rf "${WORKSPACE}/build/deb/project-tracker_${version}-${release}_amd64/"
  mkdir -p "${WORKSPACE}/build/deb/project-tracker_${version}-${release}_amd64/DEBIAN/"

  # Copy and update the control file
  cp "${WORKSPACE}/build/deb/control" "${WORKSPACE}/build/deb/project-tracker_${version}-${release}_amd64/DEBIAN/"
  sed -i "s/__VERSION__/${version}-${release}/g" "${WORKSPACE}/build/deb/project-tracker_${version}-${release}_amd64/DEBIAN/control"

  # Untar source
  tar xf "${WORKSPACE}/build/project-tracker.tar.gz" -C "${WORKSPACE}/build/deb/project-tracker_${version}-${release}_amd64/"
  tar xf "${fpdf_dir}/fpdf-install-1.7.2.tar.gz" -C "${WORKSPACE}/build/deb/project-tracker_${version}-${release}_amd64/"

  dpkg-deb --build --root-owner-group "${WORKSPACE}/build/deb/project-tracker_${version}-${release}_amd64/"

fi