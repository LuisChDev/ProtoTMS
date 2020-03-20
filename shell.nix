let
  # horrible workaround. FIXME
  pkgs = import ~/.nix-defexpr/channels/nixos-20.03 {};
  pyPkgs = pkgs.python3Packages;

in pkgs.mkShell rec {
  name = "OrToolsEnv";
  venvDir = "./.venv";
  buildInputs = [
    pyPkgs.python
    pyPkgs.venvShellHook

    # runtime
    pyPkgs.ortools
    pyPkgs.pony

    # development
    pyPkgs.python-language-server
    pyPkgs.flake8
    pyPkgs.pyls-mypy
    pyPkgs.black
  ];
}
