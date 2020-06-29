let
  pkgs = import <nixpkgs> {};
  pyPkgs = pkgs.python3Packages;

in pkgs.mkShell rec {
  name = "OrToolsEnv";
  buildInputs = [
    pyPkgs.python
    pyPkgs.tkinter
  ];

  LD_LIBRARY_PATH = "/run/opengl-driver/lib:${pkgs.pythonManylinuxPackages.manylinux2014Package}/lib";
}
