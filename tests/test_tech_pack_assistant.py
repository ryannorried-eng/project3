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
