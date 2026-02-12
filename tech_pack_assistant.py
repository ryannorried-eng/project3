"""Tech Pack Assistant MVP.

Provides a CLI and model helpers for creating a technical-design tech pack with:
- style metadata
- measurement specs (POM, size, value, tolerance, notes)
- revision history
- validation checks
- markdown and CSV export
"""

from __future__ import annotations

import csv
import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class StyleInfo:
    style_number: str
    style_name: str
    season: str
    brand: str
    fabric: str
    trims: list[str] = field(default_factory=list)


@dataclass(slots=True)
class MeasurementSpec:
    pom: str
    size: str
    value: float
    tolerance: float
    notes: str = ""


@dataclass(slots=True)
class Revision:
    version: str
    author: str
    summary: str
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass(slots=True)
class TechPack:
    style: StyleInfo
    measurements: list[MeasurementSpec] = field(default_factory=list)
    revisions: list[Revision] = field(default_factory=list)

    def add_measurement(self, measurement: MeasurementSpec) -> None:
        self.measurements.append(measurement)

    def add_revision(self, revision: Revision) -> None:
        self.revisions.append(revision)

    def to_dict(self) -> dict[str, Any]:
        return {
            "style": asdict(self.style),
            "measurements": [asdict(m) for m in self.measurements],
            "revisions": [asdict(r) for r in self.revisions],
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> TechPack:
        style = StyleInfo(**payload["style"])
        measurements = [MeasurementSpec(**item) for item in payload.get("measurements", [])]
        revisions = [Revision(**item) for item in payload.get("revisions", [])]
        return cls(style=style, measurements=measurements, revisions=revisions)

    def validate(self) -> list[str]:
        issues: list[str] = []
        seen_keys: set[tuple[str, str]] = set()

        for idx, spec in enumerate(self.measurements, start=1):
            row_ref = f"row {idx} ({spec.pom} / {spec.size})"
            if spec.value <= 0:
                issues.append(f"{row_ref}: measurement must be > 0")
            if spec.tolerance < 0:
                issues.append(f"{row_ref}: tolerance must be >= 0")

            key = (spec.pom.strip().lower(), spec.size.strip().lower())
            if key in seen_keys:
                issues.append(f"{row_ref}: duplicate POM + size combination")
            seen_keys.add(key)

        return issues

    def save_json(self, path: Path) -> None:
        path.write_text(json.dumps(self.to_dict(), indent=2), encoding="utf-8")

    @classmethod
    def load_json(cls, path: Path) -> TechPack:
        payload = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise ValueError("Invalid tech pack payload; expected JSON object")
        return cls.from_dict(payload)

    def export_markdown(self) -> str:
        lines: list[str] = []
        lines.append(f"# Tech Pack - {self.style.style_name}")
        lines.append("")
        lines.append("## Style Details")
        lines.append("")
        lines.append(f"- **Style Number:** {self.style.style_number}")
        lines.append(f"- **Season:** {self.style.season}")
        lines.append(f"- **Brand:** {self.style.brand}")
        lines.append(f"- **Fabric:** {self.style.fabric}")
        trims = ", ".join(self.style.trims) if self.style.trims else "None"
        lines.append(f"- **Trims:** {trims}")
        lines.append("")

        lines.append("## Measurement Specs")
        lines.append("")
        lines.append("| POM | Size | Measurement | Tolerance | Notes |")
        lines.append("| --- | --- | ---: | ---: | --- |")
        for spec in self.measurements:
            lines.append(
                f"| {spec.pom} | {spec.size} | {spec.value:.2f} | "
                f"±{spec.tolerance:.2f} | {spec.notes} |"
            )
        if not self.measurements:
            lines.append("| _No specs yet_ |  |  |  |  |")
        lines.append("")

        lines.append("## Revision History")
        lines.append("")
        lines.append("| Version | Timestamp (UTC) | Author | Summary |")
        lines.append("| --- | --- | --- | --- |")
        for rev in self.revisions:
            lines.append(f"| {rev.version} | {rev.timestamp} | {rev.author} | {rev.summary} |")
        if not self.revisions:
            lines.append("| _No revisions yet_ |  |  |  |")

        lines.append("")
        return "\n".join(lines)

    def export_measurements_csv(self, path: Path) -> None:
        field_names = ["pom", "size", "value", "tolerance", "notes"]
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=field_names)
            writer.writeheader()
            for spec in self.measurements:
                writer.writerow(asdict(spec))


def create_starter_pack() -> TechPack:
    """Generate a default starter tech pack with one base-size row and revision."""
    pack = TechPack(
        style=StyleInfo(
            style_number="ST-001",
            style_name="Classic Tee",
            season="FW26",
            brand="Sample Brand",
            fabric="100% Cotton Jersey",
            trims=["Neck rib", "Main label"],
        )
    )
    pack.add_measurement(
        MeasurementSpec(
            pom="Body Length (HPS)",
            size="M",
            value=27.0,
            tolerance=0.25,
            notes="Measure from high point shoulder",
        )
    )
    pack.add_revision(Revision(version="v1", author="designer", summary="Initial draft"))
    return pack


def _build_parser() -> Any:
    import argparse

    parser = argparse.ArgumentParser(description="Tech Pack Assistant MVP")
    sub = parser.add_subparsers(dest="command", required=True)

    init_cmd = sub.add_parser("init", help="Create a starter tech pack JSON")
    init_cmd.add_argument("--out", default="tech_pack.json", help="Output JSON path")

    add_spec = sub.add_parser("add-spec", help="Add a measurement spec row")
    add_spec.add_argument("--file", default="tech_pack.json", help="Existing tech pack JSON path")
    add_spec.add_argument("--pom", required=True)
    add_spec.add_argument("--size", required=True)
    add_spec.add_argument("--value", type=float, required=True)
    add_spec.add_argument("--tolerance", type=float, required=True)
    add_spec.add_argument("--notes", default="")

    add_revision = sub.add_parser("add-revision", help="Add a revision entry")
    add_revision.add_argument(
        "--file", default="tech_pack.json", help="Existing tech pack JSON path"
    )
    add_revision.add_argument("--version", required=True)
    add_revision.add_argument("--author", required=True)
    add_revision.add_argument("--summary", required=True)

    export_md = sub.add_parser("export-md", help="Export markdown tech pack")
    export_md.add_argument("--file", default="tech_pack.json", help="Existing tech pack JSON path")
    export_md.add_argument("--out", default="tech_pack.md", help="Output markdown path")

    export_csv = sub.add_parser("export-csv", help="Export measurement table to CSV")
    export_csv.add_argument("--file", default="tech_pack.json", help="Existing tech pack JSON path")
    export_csv.add_argument("--out", default="measurements.csv", help="Output CSV path")

    validate = sub.add_parser("validate", help="Validate tech pack measurement data")
    validate.add_argument("--file", default="tech_pack.json", help="Existing tech pack JSON path")

    return parser


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()

    if args.command == "init":
        pack = create_starter_pack()
        out = Path(args.out)
        pack.save_json(out)
        print(f"Created starter tech pack at {out}")
        return

    if args.command == "add-spec":
        path = Path(args.file)
        pack = TechPack.load_json(path)
        pack.add_measurement(
            MeasurementSpec(
                pom=args.pom,
                size=args.size,
                value=args.value,
                tolerance=args.tolerance,
                notes=args.notes,
            )
        )
        pack.save_json(path)
        print(f"Added spec row to {path}")
        return

    if args.command == "add-revision":
        path = Path(args.file)
        pack = TechPack.load_json(path)
        pack.add_revision(Revision(version=args.version, author=args.author, summary=args.summary))
        pack.save_json(path)
        print(f"Added revision to {path}")
        return

    if args.command == "export-md":
        in_path = Path(args.file)
        out_path = Path(args.out)
        pack = TechPack.load_json(in_path)
        out_path.write_text(pack.export_markdown(), encoding="utf-8")
        print(f"Exported markdown tech pack to {out_path}")
        return

    if args.command == "export-csv":
        in_path = Path(args.file)
        out_path = Path(args.out)
        pack = TechPack.load_json(in_path)
        pack.export_measurements_csv(out_path)
        print(f"Exported measurements CSV to {out_path}")
        return

    if args.command == "validate":
        path = Path(args.file)
        pack = TechPack.load_json(path)
        issues = pack.validate()
        if not issues:
            print("Tech pack validation passed")
            return

        print("Validation issues found:")
        for issue in issues:
            print(f"- {issue}")
        raise SystemExit(1)

    raise RuntimeError(f"Unsupported command: {args.command}")


if __name__ == "__main__":
    main()
