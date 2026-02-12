"""Streamlit web UI for the Tech Pack Assistant."""

from __future__ import annotations

from pathlib import Path

import streamlit as st

from tech_pack_assistant import (
    MeasurementSpec,
    Revision,
    StyleInfo,
    TechPack,
    create_starter_pack,
)

DATA_FILE = Path("tech_pack.json")


def _load_pack() -> TechPack:
    """Load the tech pack from disk, or create a starter if none exists."""
    if DATA_FILE.exists():
        return TechPack.load_json(DATA_FILE)
    pack = create_starter_pack()
    pack.save_json(DATA_FILE)
    return pack


def _save_pack(pack: TechPack) -> None:
    """Persist the tech pack to disk."""
    pack.save_json(DATA_FILE)


def _style_section(pack: TechPack) -> None:
    """Render the style details editor."""
    st.header("Style Details")

    with st.form("style_form"):
        style_number = st.text_input("Style Number", value=pack.style.style_number)
        style_name = st.text_input("Style Name", value=pack.style.style_name)
        season = st.text_input("Season", value=pack.style.season)
        brand = st.text_input("Brand", value=pack.style.brand)
        fabric = st.text_input("Fabric", value=pack.style.fabric)
        trims = st.text_input("Trims (comma-separated)", value=", ".join(pack.style.trims))

        if st.form_submit_button("Save Style Details"):
            pack.style = StyleInfo(
                style_number=style_number,
                style_name=style_name,
                season=season,
                brand=brand,
                fabric=fabric,
                trims=[t.strip() for t in trims.split(",") if t.strip()],
            )
            _save_pack(pack)
            st.success("Style details saved!")
            st.rerun()


def _measurements_section(pack: TechPack) -> None:
    """Render the measurement specs table and add form."""
    st.header("Measurement Specs")

    if pack.measurements:
        rows = [
            {
                "POM": m.pom,
                "Size": m.size,
                "Value": m.value,
                "Tolerance": m.tolerance,
                "Notes": m.notes,
            }
            for m in pack.measurements
        ]
        st.table(rows)

        # Delete buttons
        cols = st.columns(len(pack.measurements))
        for i, col in enumerate(cols):
            with col:
                if st.button(f"Delete row {i + 1}", key=f"del_spec_{i}"):
                    pack.measurements.pop(i)
                    _save_pack(pack)
                    st.rerun()
    else:
        st.info("No measurement specs yet. Add one below.")

    st.subheader("Add Measurement")
    with st.form("add_spec_form"):
        pom = st.text_input("Point of Measure (POM)")
        size = st.text_input("Size", value="M")
        value = st.number_input("Measurement Value", min_value=0.0, step=0.25, format="%.2f")
        tolerance = st.number_input("Tolerance (±)", min_value=0.0, step=0.125, format="%.3f")
        notes = st.text_input("Notes (optional)")

        if st.form_submit_button("Add Measurement"):
            if not pom:
                st.error("POM is required.")
            else:
                pack.add_measurement(
                    MeasurementSpec(
                        pom=pom,
                        size=size,
                        value=value,
                        tolerance=tolerance,
                        notes=notes,
                    )
                )
                _save_pack(pack)
                st.success(f"Added: {pom} ({size})")
                st.rerun()


def _revisions_section(pack: TechPack) -> None:
    """Render the revision history and add form."""
    st.header("Revision History")

    if pack.revisions:
        rows = [
            {
                "Version": r.version,
                "Author": r.author,
                "Summary": r.summary,
                "Timestamp": r.timestamp,
            }
            for r in pack.revisions
        ]
        st.table(rows)
    else:
        st.info("No revisions yet. Add one below.")

    st.subheader("Add Revision")
    with st.form("add_revision_form"):
        version = st.text_input("Version (e.g. v2)")
        author = st.text_input("Author")
        summary = st.text_input("Summary of changes")

        if st.form_submit_button("Add Revision"):
            if not version or not author or not summary:
                st.error("All fields are required.")
            else:
                pack.add_revision(Revision(version=version, author=author, summary=summary))
                _save_pack(pack)
                st.success(f"Added revision {version}")
                st.rerun()


def _export_section(pack: TechPack) -> None:
    """Render the export / download section."""
    st.header("Export")

    md_content = pack.export_markdown()

    st.download_button(
        label="Download as Markdown (.md)",
        data=md_content,
        file_name=f"tech_pack_{pack.style.style_number}.md",
        mime="text/markdown",
    )

    json_content = Path(DATA_FILE).read_text(encoding="utf-8") if DATA_FILE.exists() else "{}"
    st.download_button(
        label="Download as JSON",
        data=json_content,
        file_name=f"tech_pack_{pack.style.style_number}.json",
        mime="application/json",
    )

    with st.expander("Preview Markdown"):
        st.markdown(md_content)


def main() -> None:
    """Main Streamlit entry point."""
    st.set_page_config(page_title="Tech Pack Assistant", page_icon="🧵", layout="wide")
    st.title("Tech Pack Assistant")
    st.caption("Create and manage garment tech packs — no coding required.")

    pack = _load_pack()

    tab_style, tab_specs, tab_revisions, tab_export = st.tabs(
        ["Style Details", "Measurements", "Revisions", "Export & Download"]
    )

    with tab_style:
        _style_section(pack)

    with tab_specs:
        _measurements_section(pack)

    with tab_revisions:
        _revisions_section(pack)

    with tab_export:
        _export_section(pack)


if __name__ == "__main__":
    main()
