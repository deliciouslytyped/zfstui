{ lib, python37, python37Packages, zfs, fetchFromGitHub }:
 python37Packages.buildPythonPackage {
    pname = "zfstui";
    version = "master";

    preBuild = ''
      substituteInPlace ./zfstui/zfs.py \
        --replace /sbin/ "" 
      substituteInPlace ./zfstui/dialogs.py \
        --replace "lines[0]" 'lines[0] if lines else ""' 
      '';

    propagatedBuildInputs = [ zfs ];
    src = fetchFromGitHub {
      owner = "volkerp";
      repo = "zfstui";
      rev = "ef2cc86619dfcc79be477ba5d1e194f8f252a665";
      sha256 = "0nfmvcpk4svf34v2ljr1iknmilbly3cvv8r5f72v5pwx3g1i40vv";
    };
  }
