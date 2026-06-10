#!/usr/bin/env python3
"""Project FAIRmat team emails into nomad.yaml's oasis.allowed_users.

This is a *host-side* deploy helper, NOT part of the plugin runtime. It keeps
the login gate (`oasis.allowed_users`, a flat email list NOMAD reads to allow
logins) in sync with the team roster (`fairmat_team.json`), which is the single
source of truth for who is on the FAIRmat team.

Design (intentional, do not "fix"):
  * Source of truth is fairmat_team.json. allowed_users is a SUBSET that may
    legitimately diverge: a deployer can manually add a guest email to
    allowed_users that is not in the team file.
  * The relationship is ONE-DIRECTIONAL and ADDITIVE (union, never subtract).
    This script only ADDS team emails missing from allowed_users. It NEVER
    removes or reorders existing entries, so manually-added guests survive.
  * Idempotent: running it again after a no-op change writes nothing.
  * Comments / key order / formatting in nomad.yaml are preserved (ruamel.yaml).

Usage:
    python sync_allowed_users.py \
        --team   /path/to/fairmat_team.json \
        --nomad  /path/to/nomad.yaml

    # preview without writing:
    python sync_allowed_users.py --team ... --nomad ... --dry-run

After running, restart the Oasis containers so NOMAD re-reads nomad.yaml.

Requires: ruamel.yaml  (pip install ruamel.yaml)
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from ruamel.yaml import YAML


def _load_team_emails(team_path: Path) -> list[str]:
    """Return emails from the team file, in file order, skipping blanks."""
    with team_path.open() as f:
        team = json.load(f)
    emails: list[str] = []
    for person in team:
        email = (person.get('email') or '').strip()
        if email:
            emails.append(email)
    return emails


def sync(team_path: Path, nomad_path: Path, dry_run: bool = False) -> int:
    """Add missing team emails into oasis.allowed_users. Returns count added."""
    yaml = YAML()
    yaml.preserve_quotes = True

    team_emails = _load_team_emails(team_path)

    with nomad_path.open() as f:
        doc = yaml.load(f)

    if doc is None:
        print(f'ERROR: {nomad_path} is empty or not valid YAML', file=sys.stderr)
        raise SystemExit(2)

    oasis = doc.get('oasis')
    if oasis is None:
        print(
            f"ERROR: no 'oasis' section in {nomad_path}; refusing to create it.",
            file=sys.stderr,
        )
        raise SystemExit(2)

    allowed = oasis.get('allowed_users')
    if allowed is None:
        # Section exists but no list yet — safe to start one.
        allowed = []
        oasis['allowed_users'] = allowed

    # Case-insensitive set of what is already gated, so we never add a dup
    # that differs only by case.
    existing_lower = {str(e).strip().lower() for e in allowed}

    added: list[str] = []
    for email in team_emails:
        if email.lower() not in existing_lower:
            allowed.append(email)
            existing_lower.add(email.lower())
            added.append(email)

    if not added:
        print('allowed_users already contains every team email — nothing to do.')
        return 0

    print(f'{"Would add" if dry_run else "Adding"} {len(added)} email(s):')
    for email in added:
        print(f'  + {email}')

    if dry_run:
        print('\n(dry-run: nomad.yaml NOT modified)')
        return len(added)

    with nomad_path.open('w') as f:
        yaml.dump(doc, f)
    print(f'\nWrote {nomad_path}. Restart the Oasis containers to apply.')
    return len(added)


def main() -> None:
    parser = argparse.ArgumentParser(
        description='Union FAIRmat team emails into nomad.yaml oasis.allowed_users '
        '(additive, never removes).'
    )
    parser.add_argument(
        '--team', required=True, type=Path, help='Path to fairmat_team.json'
    )
    parser.add_argument(
        '--nomad', required=True, type=Path, help='Path to nomad.yaml'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be added without writing the file.',
    )
    args = parser.parse_args()

    if not args.team.is_file():
        print(f'ERROR: team file not found: {args.team}', file=sys.stderr)
        raise SystemExit(2)
    if not args.nomad.is_file():
        print(f'ERROR: nomad.yaml not found: {args.nomad}', file=sys.stderr)
        raise SystemExit(2)

    sync(args.team, args.nomad, dry_run=args.dry_run)


if __name__ == '__main__':
    main()
