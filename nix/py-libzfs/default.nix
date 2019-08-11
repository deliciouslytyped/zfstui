#{pkgs ? import <./pinned/nixpkgs.nix> {}}:
{pkgs ? import <nixpkgs> {}}:
  pkgs.callPackage ./shell.nix { zfs = pkgs.zfs; } #zfsUnstable
