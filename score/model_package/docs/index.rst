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

AI Model Package
################

This draft defines a QM package and target-side lifecycle contract, not an
implementation. The OEM OTA client invokes the API; S-CORE implements no OTA.

.. comp:: AI Model Package
   :id: comp__model_package
   :security: YES
   :safety: QM
   :status: valid
   :version: 1
   :belongs_to: feat__ai_platform

.. toctree::
   :maxdepth: 2

   requirements/index
   lifecycle
   packaging

Out of scope
============

Store implementation, OTA backend, scheduling/resource budgets, ASIL-B, drift
monitoring and encryption are excluded.

Open questions
==============

* OCI versus plain tar fallback for constrained ECUs?
* One OEM signing key versus multiple signatures?
* Rollback on load failure only or also on health report? The OEM invokes
  rollback explicitly; this draft does not choose a trigger.
* Partner review of the package profile, trust and last-known-good policies.
