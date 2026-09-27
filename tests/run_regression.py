#!/usr/bin/env python3
'''Golden-log regression test for the CLI engine (dbz-play).

Runs a fixed set of deterministic games (see SCENARIOS below) - some
non-interactive (AI vs AI), some interactive with a scripted P1 (matching
how a real interactive session, or the browser's P1, is actually driven) -
and diffs the full captured output against checked-in golden files in
tests/golden/. Any change to engine behavior (narration text, AI decisions,
prompts, table formatting, win/loss outcome) shows up as a diff instead of
passing silently.

Usage (run from anywhere, with the project's venv active):
    python tests/run_regression.py              # run all scenarios
    python tests/run_regression.py --scenario NAME
    python tests/run_regression.py --update      # regenerate all goldens
    python tests/run_regression.py --update --scenario NAME
'''
import argparse
import dataclasses
import difflib
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DECKS_DIR = REPO_ROOT / 'dbz' / 'decks'
GOLDEN_DIR = Path(__file__).resolve().parent / 'golden'

# A real game only ever consumes ~190 answers with the "always pick the
# first available option" policy (confirmed empirically) - this is a
# generous, bounded amount of headroom that avoids needing an unbounded
# `yes`-style pipe.
INTERACTIVE_SCRIPT = '1\n' * 500


@dataclasses.dataclass
class Scenario:
    name: str
    deck1: str
    deck2: str
    seed: int
    interactive: bool


SCENARIOS = [
    # Non-interactive (AI vs AI) - one pass over all 7 Saiyan Saga decks.
    Scenario('ai_goku_vs_vegeta', 'goku', 'vegeta', seed=1, interactive=False),
    Scenario('ai_goku_vs_piccolo', 'goku', 'piccolo', seed=2, interactive=False),
    Scenario('ai_goku_survival_vs_vegeta_db', 'goku_survival', 'vegeta_db', seed=1, interactive=False),
    Scenario('ai_gohan_vs_gohan_anger', 'gohan', 'gohan_anger', seed=3, interactive=False),
    Scenario('ai_piccolo_vs_vegeta_db', 'piccolo', 'vegeta_db', seed=4, interactive=False),
    Scenario('ai_vegeta_vs_goku_survival', 'vegeta', 'goku_survival', seed=5, interactive=False),

    # Interactive (scripted P1 vs AI P2) - exercises Player.choose()'s
    # human branch: prompts, hand display, numbered options.
    Scenario('interactive_goku_survival_vs_vegeta_db', 'goku_survival', 'vegeta_db', seed=1, interactive=True),
    Scenario('interactive_goku_vs_vegeta', 'goku', 'vegeta', seed=1, interactive=True),
    Scenario('interactive_gohan_anger_vs_piccolo', 'gohan_anger', 'piccolo', seed=2, interactive=True),
]


def run_scenario(scenario):
    deck1 = DECKS_DIR / scenario.deck1
    deck2 = DECKS_DIR / scenario.deck2
    cmd = [sys.executable, '-m', 'dbz.play',
           '-d', str(deck1), '-d', str(deck2),
           '-s', str(scenario.seed), '-pw', '100']
    stdin_text = None
    if scenario.interactive:
        cmd += ['-pf', '100000']
        stdin_text = INTERACTIVE_SCRIPT
    else:
        cmd += ['-ni']

    result = subprocess.run(
        cmd, cwd=REPO_ROOT, input=stdin_text,
        capture_output=True, text=True)
    return f'{result.stdout}{result.stderr}[exit code: {result.returncode}]\n'


def golden_path(scenario):
    return GOLDEN_DIR / f'{scenario.name}.txt'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--update', action='store_true',
                         help='regenerate golden files from current output instead of comparing')
    parser.add_argument('--scenario', help='only run/update the named scenario')
    args = parser.parse_args()

    scenarios = SCENARIOS
    if args.scenario:
        scenarios = [s for s in scenarios if s.name == args.scenario]
        if not scenarios:
            print(f'No such scenario: {args.scenario}')
            return 1

    GOLDEN_DIR.mkdir(parents=True, exist_ok=True)

    failures = []
    for scenario in scenarios:
        output = run_scenario(scenario)
        path = golden_path(scenario)

        if args.update:
            path.write_text(output)
            print(f'UPDATED  {scenario.name}')
            continue

        if not path.exists():
            print(f'MISSING  {scenario.name} (no golden file - run with --update first)')
            failures.append(scenario.name)
            continue

        expected = path.read_text()
        if output == expected:
            print(f'PASS     {scenario.name}')
        else:
            print(f'FAIL     {scenario.name}')
            diff = difflib.unified_diff(
                expected.splitlines(keepends=True),
                output.splitlines(keepends=True),
                fromfile=f'{scenario.name} (golden)',
                tofile=f'{scenario.name} (actual)')
            sys.stdout.writelines(diff)
            failures.append(scenario.name)

    if args.update:
        return 0

    print()
    if failures:
        print(f'{len(failures)}/{len(scenarios)} scenario(s) failed: {", ".join(failures)}')
        return 1
    print(f'All {len(scenarios)} scenario(s) passed.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
