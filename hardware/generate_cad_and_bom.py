#!/usr/bin/env python3
"""Compatibility guard: the previous geometry generator is withdrawn."""
raise SystemExit(
    "No P0 fabrication geometry has been released. Read hardware/PROTOTYPE_SPEC.md "
    "and hardware/ASSEMBLY_BLUEPRINTS.md. The old generator is archived as reference "
    "text and must not be used to order structural parts. Run "
    "python3 tools/validate_repository.py to check the active quote register."
)
