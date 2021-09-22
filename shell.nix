let
  pkgs = import (fetchTarball
    "https://github.com/NixOS/nixpkgs/archive/21.05.tar.gz") {};
  pyPkgs = pkgs.python3Packages;

in pkgs.mkShell {
  name = "OrToolsEnv";
  buildInputs = with pyPkgs; [
    # core
    python
    tkinter

    # broken in local install
    matplotlib
    pandas
    ortools
    pulp

    # development deps
    pkgs.jupyter
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
