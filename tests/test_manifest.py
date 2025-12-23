"""Tests for manifest.json validation."""
import json
from pathlib import Path


def test_manifest_valid():
    """Test manifest.json is valid JSON."""
    manifest_path = Path(__file__).parent.parent / "custom_components" / "ventilairsec2ha" / "manifest.json"

    assert manifest_path.exists(), f"manifest.json not found at {manifest_path}"

    with open(manifest_path, encoding="utf-8") as f:
        manifest = json.load(f)

    assert isinstance(manifest, dict), "manifest.json must be a dict"


def test_manifest_required_fields():
    """Test manifest.json has required fields."""
    manifest_path = Path(__file__).parent.parent / "custom_components" / "ventilairsec2ha" / "manifest.json"

    with open(manifest_path, encoding="utf-8") as f:
        manifest = json.load(f)

    required_fields = [
        "manifest_version",
        "domain",
        "name",
        "codeowners",
        "homeassistant",
        "version",
        "requirements",
    ]

    for field in required_fields:
        assert field in manifest, f"Missing required field: {field}"


def test_manifest_domain_format():
    """Test domain follows naming conventions."""
    manifest_path = Path(__file__).parent.parent / "custom_components" / "ventilairsec2ha" / "manifest.json"

    with open(manifest_path, encoding="utf-8") as f:
        manifest = json.load(f)

    domain = manifest["domain"]
    assert domain.islower(), "domain must be lowercase"
    assert "_" in domain or domain.isalnum(), "domain must use alphanumeric or underscores"
    assert domain == "ventilairsec2ha", "domain should match integration name"


def test_manifest_homeassistant_version():
    """Test homeassistant version is valid."""
    manifest_path = Path(__file__).parent.parent / "custom_components" / "ventilairsec2ha" / "manifest.json"

    with open(manifest_path, encoding="utf-8") as f:
        manifest = json.load(f)

    ha_version = manifest["homeassistant"]
    assert isinstance(ha_version, str), "homeassistant version must be string"
    assert len(ha_version.split(".")) >= 2, "invalid homeassistant version format"


def test_manifest_requirements():
    """Test requirements are properly formatted."""
    manifest_path = Path(__file__).parent.parent / "custom_components" / "ventilairsec2ha" / "manifest.json"

    with open(manifest_path, encoding="utf-8") as f:
        manifest = json.load(f)

    requirements = manifest.get("requirements", [])
    assert isinstance(requirements, list), "requirements must be a list"
    assert len(requirements) > 0, "should have at least one requirement"

    for req in requirements:
        assert isinstance(req, str), f"requirement '{req}' must be string"
        assert any(c in req for c in ["=", ">", "<"]), f"requirement '{req}' needs version specifier"
