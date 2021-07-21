let
  pkgs = import (fetchTarball
    "https://github.com/NixOS/nixpkgs/archive/20.03.tar.gz") {};
  pyPkgs = pkgs.python3Packages;

in pkgs.mkShell {
  name = "OrToolsEnv";
  buildInputs = with pyPkgs; [
    # core
    python
    tkinter

    # development deps
    pkgs.mypy
    black
    python-language-server
    pyls-black
    pyls-mypy
    future
    importmagic
    epc
  ];

  # add dynamic libraries required by many dependencies
  # LD_LIBRARY_PATH = "${pkgs.pythonManylinuxPackages.manylinux2014Package}/lib";
}
