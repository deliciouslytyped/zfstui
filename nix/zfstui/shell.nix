{ lib, python37, python37Packages, zfs, fetchFromGitHub, py-libzfs }:
 python37Packages.buildPythonPackage {
    pname = "zfstui";
    version = "master";

    doCheck = false; #TODO why does this segfault setuptools if false???

    propagatedBuildInputs = [ zfs py-libzfs ];
    /*
    src = fetchFromGitHub {
      owner = "volkerp";
      repo = "zfstui";
      rev = "ef2cc86619dfcc79be477ba5d1e194f8f252a665";
      sha256 = "0nfmvcpk4svf34v2ljr1iknmilbly3cvv8r5f72v5pwx3g1i40vv";
      };
    */
    src = ../../.; #TODO copy as git repo?
  }
