{ lib, python37, python37Packages, fetchFromGitHub, zfs }:
let
  py-libzfs = python37Packages.buildPythonPackage {
    pname = "py-libzfs";
    version = "master";

    preBuild = ''
      substituteInPlace ./configure \
        --replace header_prefix=/usr/local header_prefix=${zfs.dev} 
      ./configure
      '';

    nativeBuildInputs = [ python37Packages.cython ];
    propagatedBuildInputs = [ zfs ];
    src = fetchFromGitHub {
      owner = "freenas";
      repo = "py-libzfs";
      rev = "9bf07db68bacee65cb0ae1aee66d92a0a6c36e21";
      sha256 = "08ndn2bpkq8ix5d6jyyn963jra0ifr8d2v09nv4by88wmbbah26k";
    };
  };
in
  python37.withPackages (p: [ py-libzfs ])
