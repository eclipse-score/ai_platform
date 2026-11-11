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

Component Requirements
######################

External feature IDs from eclipse-score/score issue #3260 are imported from
score_platform 0.7.4. Its docs-as-code 8.6.0 metamodel uses ``derived_from``
for component-to-feature requirement traceability (not ``satisfies``).
This specification still awaits partner review.

.. comp_req:: Manifest identity
   :id: comp_req__model_package__manifest
   :reqtype: Functional
   :security: YES
   :safety: QM
   :status: valid
   :version: 1
   :derived_from: feat_req__ai_platform__model_lifecycle
   :satisfied_by: comp__model_package

   The component shall accept only packages conforming to the manifest schema and OCI profile with immutable name and SemVer version identities.

   Derivation: ``feat_req__ai_platform__model_lifecycle``.

.. comp_req:: Stage without selection
   :id: comp_req__model_package__stage
   :reqtype: Functional
   :security: YES
   :safety: QM
   :status: valid
   :version: 1
   :derived_from: feat_req__ai_platform__model_lifecycle
   :satisfied_by: comp__model_package

   The component shall register packages without making them loadable or changing selection.

   Derivation: ``feat_req__ai_platform__model_lifecycle``.

.. comp_req:: Verify content
   :id: comp_req__model_package__verify
   :reqtype: Functional
   :security: YES
   :safety: QM
   :status: valid
   :version: 1
   :derived_from: feat_req__ai_platform__model_verification
   :satisfied_by: comp__model_package

   The component shall verify every model file digest, aggregate hash and runtime compatibility before marking a version verified.

   Derivation: ``feat_req__ai_platform__model_verification``.

.. comp_req:: Authenticate manifest
   :id: comp_req__model_package__signature
   :reqtype: Functional
   :security: YES
   :safety: QM
   :status: valid
   :version: 1
   :derived_from: feat_req__sec_crypt__sig_verification
   :satisfied_by: comp__model_package

   The component shall verify the detached manifest signature using the signature verification feature and OEM trust policy.

   Derivation: ``feat_req__sec_crypt__sig_verification``.

.. comp_req:: Atomic activation
   :id: comp_req__model_package__activate
   :reqtype: Functional
   :security: YES
   :safety: QM
   :status: valid
   :version: 1
   :derived_from: feat_req__ai_platform__model_lifecycle
   :satisfied_by: comp__model_package

   The component shall atomically activate only a currently verified version and preserve selection on failure.

   Derivation: ``feat_req__ai_platform__model_lifecycle``.

.. comp_req:: Bounded rollback
   :id: comp_req__model_package__rollback
   :reqtype: Functional
   :security: YES
   :safety: QM
   :status: valid
   :version: 1
   :derived_from: feat_req__ai_platform__model_lifecycle
   :satisfied_by: comp__model_package

   The component shall roll back only to a verified OEM-approved last-known-good predecessor respecting the active manifest's rollback.min_version.

   Derivation: ``feat_req__ai_platform__model_lifecycle``.

.. comp_req:: Active-only loading
   :id: comp_req__model_package__load
   :reqtype: Functional
   :security: YES
   :safety: QM
   :status: valid
   :version: 1
   :derived_from: feat_req__ai_platform__model_verification
   :satisfied_by: comp__model_package

   The component shall resolve Load only to the active verified version satisfying its constraint.

   Derivation: ``feat_req__ai_platform__model_verification``.

.. comp_req:: AI BOM reference
   :id: comp_req__model_package__bom
   :reqtype: Functional
   :security: YES
   :safety: QM
   :status: valid
   :version: 1
   :derived_from: feat_req__ai_platform__model_verification
   :satisfied_by: comp__model_package

   The component shall require a referenced SPDX 3.0 AI and Dataset profile BOM with references to model, datasets, runtime, training information and release status, excluding safety argumentation.

   Derivation: ``feat_req__ai_platform__model_verification``.
