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

"""Run the buyer and supplier agents against each other over A2A JSON-RPC.

The supplier listens on 127.0.0.1 on a free port, the buyer discovers its
Agent Card and sends six requests: two inside the mandate, one over the value
limit, and three protocol errors. The script exits 0 when every request
behaved as the specification says.
"""

from aae_a2a_ext.demo import main


if __name__ == '__main__':
    raise SystemExit(main())
