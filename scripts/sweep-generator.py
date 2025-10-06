#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# /// script
# requires-python = ">=3.12"
# dependencies = [ "foamlib>=1.3.11", "pymadcad>=0.19.1", "numpy-stl>=3.2.0" ]
# ///

import json
import math
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

try:
    import numpy as np
except ImportError:
    print("This script requires numpy. Please install it (e.g., pip install numpy)", file=sys.stderr)
    raise

try:
    from foamlib import FoamFile
except Exception as e:
    print("Warning: foamlib not importable here; reading base cadDict will fail.", file=sys.stderr)
    raise

ROOT = Path(__file__).resolve().parent
BASE_CAD = ROOT / "constant" / "cadDict"
GENERATE = ROOT / "generate.py"
SWEEPS_DIR = ROOT / "sweeps"

# Defaults per user's confirmation
RADIUS_GRID = np.linspace(0.01, 0.02, 4).tolist()
HEIGHT_GRID = np.linspace(0.03, 0.05, 4).tolist()
TILT_GRID = list(range(0, 15, 5))
N_ROTOR_BLADES = [3, 4, 5, 6]
ANGULAR_VELOCITY = 35  # recorded only
MAX_WORKERS = 16


def read_base_params():
    cad = FoamFile(str(BASE_CAD))
    base = {
        "shaft": {
            "radius": float(cad["shaft"]["radius"]),
            "height": float(cad["shaft"]["height"]),
        },
        "stator": {
            "blades": {
                "radius": float(cad["stator"]["blades"]["radius"]),
                "height": float(cad["stator"]["blades"]["height"]),
                "distanceFromCenter": float(cad["stator"]["blades"]["distanceFromCenter"]),
                "n": int(cad["stator"]["blades"]["n"]),
            }
        },
    }
    return base


def format_of_dict(base, rotor):
    header = (
        "/*--------------------------------*- C++ -*----------------------------------*\\n"
        "| =========                 |                                                 |\n"
        "| \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |\n"
        "|  \\    /   O peration     |                                             |\n"
        "|   \\  /    A nd           |                                             |\n"
        "|    \\/     M anipulation  |                                                 |\n"
        "*---------------------------------------------------------------------------*/\n"
        "FoamFile\n{\n    version     2.0;\n    format      ascii;\n    class       dictionary;\n    object      cadSettings;\n}\n\n"
    )
    s = []
    s.append("shaft\n{")
    s.append(f"    radius {base['shaft']['radius']};")
    s.append(f"    height {base['shaft']['height']};")
    s.append("}\n")

    s.append("stator\n{")
    s.append("    blades")
    s.append("    {")
    s.append(f"        radius {base['stator']['blades']['radius']};")
    s.append(f"        height {base['stator']['blades']['height']};")
    s.append(f"        distanceFromCenter {base['stator']['blades']['distanceFromCenter']};")
    s.append(f"        n {base['stator']['blades']['n']};")
    s.append("    }")
    s.append("}\n")

    s.append("rotor\n{")
    s.append("    blades")
    s.append("    {")
    s.append(f"        radius {rotor['radius']};")
    s.append(f"        height {rotor['height']};")
    s.append(f"        tiltAngle {rotor['tiltAngle']};")
    s.append(f"        n {rotor['n']};")
    s.append("    }")
    s.append("}\n")

    s.append("// ************************************************************************* //\n")
    return header + "\n".join(s)


def make_case_dir(idx, rotor):
    # Create a readable name
    name = (
        f"case_{idx:04d}_n{rotor['n']}_R{rotor['radius']:.5f}_H{rotor['height']:.5f}_T{int(rotor['tiltAngle'])}"
    )
    case_dir = SWEEPS_DIR / name
    (case_dir / "constant" / "triSurface").mkdir(parents=True, exist_ok=True)
    return case_dir


def write_cad_dict(case_dir, base, rotor):
    text = format_of_dict(base, rotor)
    out = case_dir / "constant" / "cadDict"
    out.write_text(text)


def run_generate(case_dir):
    # Run generate.py with CWD=case_dir
    cmd = [sys.executable, str(GENERATE)]
    proc = subprocess.run(
        cmd,
        cwd=str(case_dir),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return proc


def collect_artifacts(case_dir):
    tri = case_dir / "constant" / "triSurface"
    artifacts = list(
        p for p in tri.glob("*.stl") if p.name.endswith(".stl")
    )
    return [str(p.relative_to(case_dir)) for p in artifacts]


def feasible_max_angle_deg(base_shaft_radius, rotor_height):
    return math.degrees(math.atan(base_shaft_radius / rotor_height))


def process_one(idx, base, rotor):
    case_dir = make_case_dir(idx, rotor)
    write_cad_dict(case_dir, base, rotor)

    # Pre-check feasibility window to avoid obvious failures (same as in generate.py)
    max_angle = feasible_max_angle_deg(base["shaft"]["radius"], rotor["height"])
    prechecked_infeasible = rotor["tiltAngle"] < 0 or rotor["tiltAngle"] > max_angle

    started_at = datetime.utcnow().isoformat() + "Z"
    proc = run_generate(case_dir)
    ended_at = datetime.utcnow().isoformat() + "Z"

    success = proc.returncode == 0 and not prechecked_infeasible

    # Determine failure reason/category when not successful
    failure_category = None
    failure_reason = None
    if not success:
        if prechecked_infeasible:
            failure_category = "PrecheckedInfeasibleTilt"
            failure_reason = (
                f"Requested tilt {rotor['tiltAngle']:.2f} exceeds feasible max angle {max_angle:.2f}"
            )
        # Parse stderr/stdout for Python exceptions or known messages
        text = (proc.stderr or "") + "\n" + (proc.stdout or "")
        # Try to find the last line that looks like an Exception line: "XxxError: ..." or "Exception: ..."
        lines = [ln.strip() for ln in text.strip().splitlines() if ln.strip()]
        for ln in reversed(lines):
            # Specific known message from generate.py
            if "Rotation around X for rotor blades exceeds the feasible max angle" in ln:
                failure_category = failure_category or "ExceedsMaxTiltAngle"
                # Capture the numeric part if present
                m = re.search(r"max angle: ([0-9]+\.[0-9]+)", ln)
                if m:
                    failure_reason = failure_reason or (
                        f"Rotation exceeds feasible max angle: {m.group(1)}"
                    )
                else:
                    failure_reason = failure_reason or ln
                break
            # Generic Exception/Error line (e.g., "ValueError: msg", "ModuleNotFoundError: msg", "Exception: msg")
            m = re.match(r"^(?P<etype>[A-Za-z_][A-Za-z0-9_]*)(?:\s*):\s*(?P<msg>.+)$", ln)
            if m:
                etype = m.group("etype")
                emsg = m.group("msg")
                failure_category = failure_category or etype
                failure_reason = failure_reason or emsg
                break
        if not failure_category:
            if proc.returncode != 0:
                failure_category = "NonZeroExit"
                failure_reason = failure_reason or f"Process exited with code {proc.returncode}"
            else:
                failure_category = "UnknownFailure"
                failure_reason = failure_reason or "Unknown failure"

    manifest = {
        "parameters": {
            "angularVelocity": ANGULAR_VELOCITY,
            "nRotorBlades": rotor["n"],
            "rotorBladeRadius": rotor["radius"],
            "rotorBladeHeight": rotor["height"],
            "rotorBladeTiltAngle": rotor["tiltAngle"],
        },
        "feasible": success,
        "feasibilityCheck": {
            "runnerMaxAngleDeg": max_angle,
            "precheckedInfeasible": prechecked_infeasible,
        },
        "returncode": proc.returncode,
        "stdout": proc.stdout[-8000:],  # tail
        "stderr": proc.stderr[-8000:],  # tail
        "artifacts": collect_artifacts(case_dir) if success else [],
        "startedAt": started_at,
        "endedAt": ended_at,
    }
    if not success:
        manifest["failure"] = {"category": failure_category, "reason": failure_reason}
    (case_dir / "manifest.json").write_text(json.dumps(manifest, indent=2))
    return case_dir, success, failure_category, failure_reason


def main():
    SWEEPS_DIR.mkdir(exist_ok=True)

    base = read_base_params()

    combos = []
    idx = 0
    for n in N_ROTOR_BLADES:
        for r in RADIUS_GRID:
            for h in HEIGHT_GRID:
                for t in TILT_GRID:
                    combos.append(
                        (
                            idx,
                            {
                                "n": int(n),
                                "radius": float(r),
                                "height": float(h),
                                "tiltAngle": float(t),
                            },
                        )
                    )
                    idx += 1

    print(f"Total combinations: {len(combos)}")

    successes = 0
    failure_counts = {}
    failure_samples = {}
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        futs = [ex.submit(process_one, i, base, rotor) for i, rotor in combos]
        for fut in as_completed(futs):
            case_dir, ok, fcat, freason = fut.result()
            print(f"[{ 'OK' if ok else 'FAIL' }] {case_dir.name}")
            if ok:
                successes += 1
            else:
                failure_counts[fcat] = failure_counts.get(fcat, 0) + 1
                # keep one sample reason per category
                failure_samples.setdefault(fcat, freason)

    print(f"Finished. Successes: {successes}/{len(combos)}. Results under {SWEEPS_DIR}")
    if failure_counts:
        print("Failure summary (by category):")
        for cat, cnt in sorted(failure_counts.items(), key=lambda x: (-x[1], x[0])):
            sample = failure_samples.get(cat, "")
            print(f"  - {cat}: {cnt} failures" + (f" | e.g., {sample}" if sample else ""))


if __name__ == "__main__":
    main()
