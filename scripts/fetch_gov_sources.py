#!/usr/bin/env python3
"""Key-gated government source fetch stubs for the non-survey panel.

These sources require credentials or account-specific access. They are kept as
explicit stubs so the panel does not fabricate values while still documenting
where the future authenticated fetchers attach.
"""


def fetch_jta_overnight():
    """Fetch JTA overnight stays via e-Stat statsCode 00601020."""
    raise NotImplementedError("supply e-Stat appId — see docs/source_inventory.md")


def fetch_estat_generic(stats_code):
    """Fetch a generic e-Stat table by stats code."""
    raise NotImplementedError("supply e-Stat appId — see docs/source_inventory.md")


def fetch_ffdata():
    """Fetch FF-DATA, e-Stat toukei 00600466."""
    raise NotImplementedError("supply FF-DATA/e-Stat key — see docs/source_inventory.md")
