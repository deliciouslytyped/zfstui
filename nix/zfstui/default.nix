{pkgs ? import <nixpkgs> {}}: {
  fork = pkgs.callPackage ./fork.nix { py-libzfs = pkgs.callPackage ../py-libzfs {}; zfs = pkgs.zfs; }; #todo zfsunstable
  upstream = pkgs.callPackage ./upstream.nix { zfs = pkgs.zfs; }; #todo zfsunstable
  }
