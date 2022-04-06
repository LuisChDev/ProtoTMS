{
  description = "metaheuristic analysis with Google's or-tools software";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-21.11";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }: flake-utils.lib.eachDefaultSystem (system:
    let
      pkgs = nixpkgs.legacyPackages.${system};
      pyPkgs = pkgs.python3Packages;
      packageName = "or-tools-tms";

    in {
      devShell = (import ./shell.nix { inherit pkgs; });
    }
  );
}
