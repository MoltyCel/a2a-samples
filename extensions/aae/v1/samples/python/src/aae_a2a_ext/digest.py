# Copyright 2026 CryptoKRI GmbH (MolTrust)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""request_digest: the binding between a verification result and the request it
decided on (spec section 8.5).

The input is the request part {"skill", "transaction"} as the server froze it:
after the number mapping of section 6.4, before the skill runs. The output is
"sha256:" followed by the SHA-256 of its RFC 8785 (JCS) serialization in
lowercase hex, the same form as enforce.core_digest. There is no domain tag and
no nonce in the input, so anyone holding the request part can recompute it with
a JCS library and SHA-256 alone.

The digest identifies content, not an execution. Two tasks with byte-identical
request parts carry the same request_digest; the task id tells them apart.
"""
# ruff: noqa: D103, D205

from __future__ import annotations

import hashlib

import jcs


PREFIX = 'sha256:'


def request_bytes(part: dict) -> bytes:
    """The JCS serialization that request_digest hashes."""
    if not isinstance(part, dict) or set(part) != {'skill', 'transaction'}:
        raise ValueError('request part must be exactly {"skill", "transaction"}')
    return jcs.canonicalize(part)


def request_digest(part: dict) -> str:
    return PREFIX + hashlib.sha256(request_bytes(part)).hexdigest()
