from pathlib import Path

from tech_pack_assistant import MeasurementSpec, Revision, TechPack, create_starter_pack


def test_starter_pack_contains_seed_data() -> None:
    pack = create_starter_pack()
    assert pack.style.style_name == "Classic Tee"
    assert len(pack.measurements) == 1
    assert len(pack.revisions) == 1


def test_serialization_roundtrip(tmp_path: Path) -> None:
    pack = create_starter_pack()
    pack.add_measurement(MeasurementSpec(pom="Chest", size="L", value=22.5, tolerance=0.25))
    pack.add_revision(Revision(version="v2", author="qa", summary="Adjusted chest"))

    out = tmp_path / "pack.json"
    pack.save_json(out)

    loaded = TechPack.load_json(out)
    assert loaded.style.style_number == "ST-001"
    assert len(loaded.measurements) == 2
    assert loaded.measurements[1].pom == "Chest"
    assert loaded.revisions[-1].version == "v2"


def test_markdown_export_contains_tables() -> None:
    pack = create_starter_pack()
    content = pack.export_markdown()

    assert "# Tech Pack - Classic Tee" in content
    assert "## Measurement Specs" in content
    assert "| POM | Size | Measurement | Tolerance | Notes |" in content
    assert "## Revision History" in content


def test_validate_finds_bad_measurements() -> None:
    pack = create_starter_pack()
    pack.add_measurement(MeasurementSpec(pom="Chest", size="M", value=-1.0, tolerance=-0.5))
    pack.add_measurement(MeasurementSpec(pom="Chest", size="M", value=20.0, tolerance=0.25))

    issues = pack.validate()
    assert any("measurement must be > 0" in issue for issue in issues)
    assert any("tolerance must be >= 0" in issue for issue in issues)
    assert any("duplicate POM + size combination" in issue for issue in issues)


def test_export_measurements_csv(tmp_path: Path) -> None:
    pack = create_starter_pack()
    out_path = tmp_path / "measurements.csv"

    pack.export_measurements_csv(out_path)

    exported = out_path.read_text(encoding="utf-8")
    assert "pom,size,value,tolerance,notes" in exported
    assert "Body Length (HPS),M,27.0,0.25" in exported
