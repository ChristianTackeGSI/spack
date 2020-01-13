# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
#   Spack Project Developers. See the top-level COPYRIGHT file for details.
# Copyright 2020 GSI Helmholtz Centre for Heavy Ion Research GmbH,
#   Darmstadt, Germany
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Asiofi(CMakePackage):
    """C++ Boost.Asio language bindings for OFI libfabric"""

    homepage = 'https://github.com/FairRootGroup/asiofi'
    url = "https://github.com/FairRootGroup/asiofi/archive/v0.4.3.tar.gz"
    git = 'https://github.com/FairRootGroup/asiofi.git'
    maintainers = ['ChristianTackeGSI', 'dennisklein']

    version('develop', branch='dev')
    version('0.4.3', sha256='d2fc677f30b475d602db4c4e4cdfb54408c44fdcac1095e20c63ac5553cb884c')
    version('0.3.1', sha256='c18217634cf51c157ff3a21948245a9820eba3eb9d41d875ed6521dd85745fce')

    depends_on('pkgconfig')
    depends_on('boost@1.70:')
    # libfabric@1.9.0 doesn't work currently
    depends_on('libfabric@1.6.0:1.8')

    def patch(self):
        """asiofi gets its version number from git.
           But the tarball doesn't have that information, so
           we patch the spack version into CMakeLists.txt"""
        if not self.spec.satisfies("@develop"):
            filter_file(r'(get_git_version\(.*)\)',
                        r'\1 DEFAULT_VERSION %s)' % self.spec.version,
                        'CMakeLists.txt')

    def cmake_args(self):
        args = [
            "-DOFI_ROOT={}".format(self.spec["libfabric"].prefix),
            "-DBOOST_ROOT={}".format(self.spec["boost"].prefix),
        ]
        return args
