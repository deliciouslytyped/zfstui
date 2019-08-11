{ lib, python37, python37Packages, zfs, fetchFromGitHub, py-libzfs }:
 python37Packages.buildPythonPackage {
    pname = "zfstui";
    version = "master";

    doCheck = false; #TODO why does this segfault setuptools if false???

    propagatedBuildInputs = [ zfs py-libzfs ];

    src = ../../.; #TODO copy as git repo?
  }
