{pkgs ? import <nixpkgs> {}}:
  pkgs.callPackage ./zfstui/default.nix {}
