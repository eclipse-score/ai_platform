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

Lifecycle API
#############

Names are model IDs; versions are exact SemVer strings. Operations for one name
are serialized. A (name, version) identity is immutable. Calls return success
with the affected identity or one of the errors below. Errors expose no
cryptographic details or internal paths.

States
======

.. code-block:: text

   absent --register--> registered --verify--> verified --activate--> active
                                                                  |
                                             inactive <--replace--+
                                                |
                                                +--activate--> active

Inactive means previously active and still verified. At most one version per
name is active. Failed calls preserve the active selection. Verification
records bind immutable content, runtime and trust policy; changes to any of
these invalidate verification, including for an active version.

register(package)
=================

Stage the OCI package on target. Validate manifest schema, identity and required
referenced objects before publishing a registered record. Partial staging is
invisible. Registration does not establish authenticity. Identical registration
is idempotent; different content with the same identity is rejected.

Errors: ``INVALID_PACKAGE``, ``IDENTITY_CONFLICT``, ``STORAGE_ERROR``.

verify(name, version)
=====================

Verify the detached manifest signature through
``feat_req__sec_crypt__sig_verification`` and OEM trust policy. Recompute every
model file digest and the aggregate hash and check the installed runtime against
the runtime constraint. Mark verified only after every check succeeds.
Re-verifying unchanged content is idempotent. Failure leaves registered content
unverified and invalidates any prior verification record for that version.

Errors: ``NOT_FOUND``, ``SIGNATURE_INVALID``, ``HASH_MISMATCH``,
``RUNTIME_INCOMPATIBLE``, ``STORAGE_ERROR``.

activate(name, version)
=======================

Require current verification. Atomically persist and switch selection; the
previous active version becomes inactive. New loads see either old or new
selection, never partial state; existing handles may finish on their pinned
version. After restart, selection and recovery metadata reflect the old or
new complete transaction. Activating the current verified selection is idempotent.

Errors: ``NOT_FOUND``, ``NOT_VERIFIED``, ``STORAGE_ERROR``.

rollback(name)
==============

Choose the most recent previously active, currently verified version approved
as last known good by OEM health policy. Activation alone does not prove health;
approval is integration policy, not a fifth lifecycle call. The candidate must
be at least the current active manifest's signed ``rollback.min_version``
using SemVer precedence. Never use only the candidate's floor. Switch using
activation's atomic semantics. No active selection or eligible predecessor
returns ``NO_ROLLBACK_TARGET``; a predecessor below the floor returns
``ROLLBACK_FORBIDDEN``.

Errors: ``NO_ROLLBACK_TARGET``, ``ROLLBACK_FORBIDDEN``, ``NOT_VERIFIED``,
``STORAGE_ERROR``.

Load integration
================

``Load(ModelId id, VersionConstraint constraint)`` resolves only the active,
currently verified version satisfying the constraint. No selection returns
``NO_ACTIVE_VERSION``; stale verification returns ``NOT_VERIFIED``; constraint
mismatch returns ``VERSION_UNSATISFIED``. Load never implicitly registers,
activates, rolls back or selects an inactive version.

Error codes
===========

* ``INVALID_PACKAGE``: malformed manifest, unsupported profile or missing object.
* ``IDENTITY_CONFLICT``: immutable identity already has different content.
* ``NOT_FOUND``: requested identity is not registered.
* ``SIGNATURE_INVALID``: missing, untrusted or invalid signature.
* ``HASH_MISMATCH``: model file or aggregate digest differs.
* ``RUNTIME_INCOMPATIBLE``: installed runtime cannot satisfy the constraint.
* ``NOT_VERIFIED``: no current successful verification.
* ``STORAGE_ERROR``: staging or atomic persistence failed.
* ``NO_ROLLBACK_TARGET``: no approved predecessor available.
* ``ROLLBACK_FORBIDDEN``: predecessor is below the signed floor.
* ``NO_ACTIVE_VERSION``: no selected version exists.
* ``VERSION_UNSATISFIED``: selected version fails the Load constraint.
* ``INVALID_ARGUMENT``: malformed name/version in non-register calls.
