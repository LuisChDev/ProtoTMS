{ pkgs ?
  import (fetchTarball "https://github.com/NixOS/nixpkgs/archive/21.11.tar.gz")
  { } }:
let pyPkgs = pkgs.python3Packages;

in pkgs.mkShell {
  name = "OrToolsEnv";
  buildInputs = with pyPkgs; [
    # core
    python
    poetry
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
    python-lsp-server
    pyls-black
    pyls-mypy
    future
    importmagic
    epc

    # testing
    pytest
    pytest-mock
    requests-mock
  ];

  # add dynamic libraries required by many dependencies
  # LD_LIBRARY_PATH = "${pkgs.pythonManylinuxPackages.manylinux2014Package}/lib";
}
