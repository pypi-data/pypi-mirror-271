# Stinky noodle

Stiny noodle is a Python OpenAPI spec linter that can read `spectral` (https://github.com/stoplightio/spectral) rule sets. This project is very early stage and not stable at all. The main reason for creating this project is to make it much easier to use with Python projects.

## Getting started

Run `pip install stinky-noodle` and then run `noodle <path-to-spec-file>` to start linting.

## Rule sets

Stinky noodle fully relies on rule sets as defined in the `spectral` docs and does not have its own syntax:
https://meta.stoplight.io/docs/spectral/e5b9616d6d50c-rulesets

You can use a rule set by adding the following argument:

```bash
noodle -s <path-to-ruleset>[ -d <dir-containing-custom-module>][ -m <cusom-module-name>] <path-to-spec-file>
```

## Caveats

- Spectral linting rules can make use of custom functions written in js. There is currently no way of automatically converting those functions in python built into Stink noodle. Functions always have to be manually converted. See the `Custom callables` section on how to do that.

- Spectral's builtin `unreferencedReusableObjects`, named `unreferenced_reusable_objects` in `stinky-noodle`, has not yet been implemented due to its complexity (e.g. it depends on a dependency graph of the API spec document). It will be implemented in the near future.

## Custom callables

TODO

## Using stinky-noodle in pre-commit

TODO
