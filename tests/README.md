# Gating testplans for libomp

The tests for libomp are in a separate repo: https://src.fedoraproject.org/tests/libomp
This directory should contain only fmf plans (such as build-gating.fmf) which import
the tests from the tests repo. This can be done using the "url" parameter of the
plan's "discover" step. Reference: https://tmt.readthedocs.io/en/stable/spec/plans.html#fmf
