{pkgs ? import <nixpkgs> {}}:
  pkgs.callPackage ./shell.nix { py-libzfs = pkgs.callPackage ../py-libzfs {}; zfs = pkgs.zfs; } #todo zfsunstable
