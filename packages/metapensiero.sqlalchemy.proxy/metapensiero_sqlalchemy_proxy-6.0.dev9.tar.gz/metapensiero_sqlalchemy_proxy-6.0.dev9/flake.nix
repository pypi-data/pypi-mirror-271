# -*- coding: utf-8 -*-
# :Project:   metapensiero.sqlalchemy.proxy — Development environment
# :Created:   ven 24 giu 2022, 11:18:08
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2022, 2023, 2024 Lele Gaifax
#

{
  description = "metapensiero.sqlalchemy.proxy";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs";
    flake-utils.url = "github:numtide/flake-utils";
    gitignore = {
      url = "github:hercules-ci/gitignore.nix";
      # Use the same nixpkgs
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, flake-utils, gitignore }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        inherit (builtins) fromTOML getAttr listToAttrs map readFile replaceStrings splitVersion;
        pkgs = import nixpkgs { inherit system; };
        inherit (pkgs.lib) cartesianProductOfSets flip;
        inherit (gitignore.lib) gitignoreFilterWith;

        getSource = name: path: pkgs.lib.cleanSourceWith {
          name = name;
          src = path;
          filter = gitignoreFilterWith { basePath = path; };
        };

        # Python versions to test against, see also Makefile
        pyVersions = [
          "python310"
          "python311"
        ];

        # SQLAlchemy versions to try out
        saVersions = [
          { version = "1.4.51";
            hash = "sha256-55CMICXrGDlOMtZd0C0uN+F9czzb59eCMcK21+sgzbk="; }
          { version = "2.0.29";
            hash = "sha256-vZVmuOWMq9cAvDZ7YOkNk0nNFvCYSXP5ipoJ+cZOhvA="; }
        ];

        py-sa-pairs = cartesianProductOfSets { pyv = pyVersions; sav = saVersions; };

        mkSAPkg = python: saVersion:
          python.pkgs.buildPythonPackage rec {
            pname = "SQLAlchemy";
            version = saVersion.version;
            src = python.pkgs.fetchPypi {
              inherit pname version;
              hash = saVersion.hash;
            };
            doCheck = false;
            nativeBuildInputs = [ python.pkgs.cython ];
            propagatedBuildInputs = [
              python.pkgs.greenlet
              python.pkgs.typing-extensions
            ];
          };

        mkPkg = pyVersion: saVersion:
          let
            py = getAttr pyVersion pkgs;
            sqlalchemy' = mkSAPkg py saVersion;
            pinfo = (fromTOML (readFile ./pyproject.toml)).project;
          in
            py.pkgs.buildPythonPackage {
              pname = pinfo.name;
              version = pinfo.version;

              src = getSource "proxy" ./.;
              format = "pyproject";

              nativeBuildInputs = with py.pkgs; [
                pdm-backend
              ];

              propagatedBuildInputs = with py.pkgs; [
                sqlalchemy'
              ];
            };

        # Concatenate just the major and minor version parts: "1.2.3" -> "12"
        mamiVersion = v:
          let
            inherit (builtins) splitVersion;
            inherit (pkgs.lib.lists) take;
            inherit (pkgs.lib.strings) concatStrings;
          in
            concatStrings (take 2 (splitVersion v));

        proxyPkgs = flip map py-sa-pairs
          (pair: {
            name = "proxy-${mamiVersion pair.pyv}-sqlalchemy${mamiVersion pair.sav.version}";
            value = mkPkg pair.pyv pair.sav;
          });

        mkTestShell = pyVersion: saVersion:
         let
           py = getAttr pyVersion pkgs;
           pkg = mkPkg pyVersion saVersion;
           env = py.buildEnv.override {
             extraLibs = [
               pkg
               py.pkgs.psycopg2
             ];
           };
         in pkgs.mkShell {
           name = "Test Python ${py.version} SA ${saVersion.version}";
           packages = with pkgs; [
             env
             just
             postgresql_15
             yq-go
           ] ++ (with py.pkgs; [
             pytest
             pytest-cov
             python-rapidjson
           ]);

           shellHook = ''
             TOP_DIR=$(pwd)
             export PYTHONPATH="$TOP_DIR/src''${PYTHONPATH:+:}$PYTHONPATH"
             trap "$TOP_DIR/tests/postgresql stop" EXIT
           '';
         };

        testShells = flip map py-sa-pairs
          (pair: {
            name = "test-${mamiVersion pair.pyv}-sqlalchemy${mamiVersion pair.sav.version}";
            value = mkTestShell pair.pyv pair.sav;
          });
      in {
        devShells = {
          default = pkgs.mkShell {
            name = "Dev shell";

            packages = (with pkgs; [
              bump2version
              just
              python3
              sphinx
              twine
              yq-go
            ]) ++ (with pkgs.python3Packages; [
              build
              tomli
            ]);

            shellHook = ''
               TOP_DIR=$(pwd)
               export PYTHONPATH="$TOP_DIR/src''${PYTHONPATH:+:}$PYTHONPATH"
               trap "$TOP_DIR/tests/postgresql stop" EXIT
             '';
          };
        } // (listToAttrs testShells);

        packages = listToAttrs proxyPkgs;
      });
}
