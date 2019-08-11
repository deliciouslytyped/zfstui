{pkgs ? import <nixpkgs> {}}: rec {
  pkg = pkgs.callPackage ./nix/zfstui/default.nix {};
  inherit (pkg) upstream fork;
  }
