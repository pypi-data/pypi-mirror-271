import pytest

from regscale.models.app_models.mapping import Mapping
import json


def test_mapping_validation():
    """
    Test the Mapping class validation
    """
    with open("./artifacts/mapping.json") as f:
        dat = json.load(f)

    expected_field_names = [
        "IP Address",
        "Hostname",
        "OS",
        "Vulnerability Title",
        "Vulnerability ID",
        "CVSSv2 Score",
        "CVSSv3 Score",
        "Description",
        "Proof",
        "Solution",
        "CVEs",
    ]
    mapping = Mapping(mapping=dat["mapping"], expected_field_names=expected_field_names)

    assert mapping


def test_mapping_no_validation():
    """
    Test the Mapping class validation
    """
    with open("./artifacts/mapping.json") as f:
        dat = json.load(f)

    expected_field_names = ["Pickles"]
    mapping = Mapping(mapping=dat["mapping"], expected_field_names=expected_field_names)

    assert mapping
