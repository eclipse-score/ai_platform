# *******************************************************************************
# Copyright (c) 2026 Contributors to the Eclipse Foundation
#
# See the NOTICE file(s) distributed with this work for additional
# information regarding copyright ownership.
#
# This program and the accompanying materials are made available under the
# terms of the Apache License Version 2.0 which is available at
# https://www.apache.org/licenses/LICENSE-2.0
#
# SPDX-License-Identifier: Apache-2.0
# *******************************************************************************
import copy
import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator
import yaml


ROOT = Path(__file__).resolve().parents[1]


class ManifestTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        schema = json.loads((ROOT / "schema/manifest.schema.json").read_text())
        Draft202012Validator.check_schema(schema)
        cls.validator = Draft202012Validator(schema)
        cls.example = yaml.safe_load((ROOT / "examples/tiny-onnx.yaml").read_text())

    def test_example(self):
        self.validator.validate(self.example)

    def test_empty(self):
        self.assertFalse(self.validator.is_valid({}))

    def test_missing_fields(self):
        for field in self.example:
            with self.subTest(field=field):
                manifest = copy.deepcopy(self.example)
                del manifest[field]
                self.assertFalse(self.validator.is_valid(manifest))

    def test_invalid_values(self):
        for field, value in [
            ("version", "01.0.0"),
            ("version", "1.0"),
            ("hash", "sha256:not-a-digest"),
            ("runtime", "onnxruntime"),
            ("files", []),
            ("safety", "ASIL_B"),
            ("signature", ""),
            ("bom", ""),
            ("rollback", {"min_version": "latest"}),
            ("interface", {"inputs": [], "outputs": []}),
            ("unexpected", True),
        ]:
            with self.subTest(field=field, value=value):
                manifest = copy.deepcopy(self.example)
                manifest[field] = value
                self.assertFalse(self.validator.is_valid(manifest))

    def test_invalid_tensor_and_path(self):
        for shape in [[0], [-1], [None]]:
            manifest = copy.deepcopy(self.example)
            manifest["interface"]["inputs"][0]["shape"] = shape
            self.assertFalse(self.validator.is_valid(manifest))
        for path in ["../tiny.onnx", "/tiny.onnx", "model/../tiny.onnx"]:
            manifest = copy.deepcopy(self.example)
            manifest["files"][0]["path"] = path
            self.assertFalse(self.validator.is_valid(manifest))


if __name__ == "__main__":
    unittest.main()
