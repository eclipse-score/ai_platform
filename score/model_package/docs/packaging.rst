..
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

Manifest and OCI/SPDX mapping
#############################

The JSON Schema (draft 2020-12) is in
``score/model_package/schema/manifest.schema.json``. The YAML example in
``score/model_package/examples/tiny-onnx.yaml`` describes a small ONNX
classifier. All digests are synthetic placeholders; no model binary, signature
or BOM is supplied. Schema validation is not cryptographic verification.

OCI profile
===========

Reuse the OCI Image Manifest structure with ``schemaVersion: 2`` and
``mediaType: application/vnd.oci.image.manifest.v1+json``. This draft proposes
``artifactType: application/vnd.eclipse.score.ai-model.v1`` (not a registered
media type). Store the model package manifest JSON as the config blob with
``mediaType: application/vnd.eclipse.score.ai-model.manifest.v1+json``.
Layers carry model files, the detached signature and SPDX BOM, each addressed
by OCI digest/size and annotated with ``org.opencontainers.image.title`` matching
its relative package path. Do not rely on mutable registry tags for identity.
Reject duplicate paths, missing referenced objects and path traversal.

The signature covers the exact UTF-8 JSON bytes of the config manifest, including
its signature reference, not the OCI envelope or YAML presentation. The detached
signature blob is outside those bytes, avoiding circular signing. Verify the
config digest before signature verification. OEM trust anchors are external.
The YAML example must be serialized to JSON before signing.

The ``files`` list is sorted lexicographically by ASCII path, with unique paths.
Each hash is SHA-256 of that file's raw bytes. The top-level ``hash`` is SHA-256
of UTF-8 records ``path + NUL + hash + LF`` concatenated in that order, with
the literal lowercase ``sha256:`` prefix included in each record.
This commits both names and contents. No model file may be omitted.

Schema syntax checks do not enforce ordering, path uniqueness, digest equality,
SemVer comparisons or object existence: verify these at the API boundary.
``runtime`` is a runtime ID followed by a minimum SemVer requirement, for example
``onnxruntime>=1.17.0``. Runtime compatibility also includes supported operators
and tensor types. Tensor shape entries are positive fixed dimensions or named
dynamic dimensions; an empty shape denotes a scalar. ``safety`` is QM in this
profile. No ASIL claim follows from package verification.

Mapping
=======

.. list-table::
   :header-rows: 1
   :widths: 25 35 40

   * - Package field/object
     - OCI representation
     - SPDX 3.0 AI / Dataset profile mapping
   * - name, version
     - Config identity; optional descriptive annotations
     - Reference to model AI package and its version
   * - hash, files
     - Config commitment; model file layers use OCI SHA-256 descriptors
     - Model artifact references and integrity identifiers
   * - runtime
     - Config constraint; runtime is not bundled by this profile
     - Reference to runtime software and dependency relationship
   * - interface
     - Config input/output tensor descriptors
     - Reference to model metadata; no new SPDX tensor vocabulary
   * - safety, rollback.min_version
     - Signed config policy fields
     - No safety argumentation in BOM
   * - signature
     - Reference to detached-signature layer
     - Not a replacement for API signature verification
   * - bom
     - Reference to SPDX JSON layer
     - SPDX 3.0 AI and Dataset profiles
   * - Dataset provenance
     - Referenced by BOM, not model payload
     - Dataset package references and model training/test relationships
   * - Training information
     - Referenced by BOM
     - AI model training metadata references
   * - Release status
     - Referenced by BOM
     - Reference to release record; OEM vocabulary pending review

The BOM contains references only to model, datasets, runtime, training information
and release status. Do not embed datasets, training records or a safety case.
Use SPDX 3.0 AI and Dataset profiles rather than inventing a parallel BOM format.
The table is a conceptual profile mapping, not a new SPDX serialization schema.

Local validation
================

With ``jsonschema==4.25.1`` and ``PyYAML==6.0.3`` installed, run from the repo root:

.. code-block:: console

   python -m unittest discover -s score/model_package/tests -v
