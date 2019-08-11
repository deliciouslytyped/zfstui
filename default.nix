{pkgs ? import <nixpkgs> {}}:
  pkgs.callPackage ./nix/zfstui/default.nix {}
