# AAE Extension: Python sample

A supplier agent that declares the AAE extension in its Agent Card and verifies
an AAE before it runs a gated skill, and a buyer agent that presents one.

## Layout

| File | Role |
| :-- | :-- |
| `run.py` | starts the supplier and runs the buyer against it, six cases |
| `src/aae_a2a_ext/server.py` | supplier agent: Agent Card, challenge, verification, receipt |
| `src/aae_a2a_ext/buyer.py` | buyer agent: discovery, presentation, challenge response |
| `src/aae_a2a_ext/verifier.py` | the nine verification steps of the AAE draft |
| `src/aae_a2a_ext/enforce.py` | constraint checks (step 7) |
| `src/aae_a2a_ext/challenge.py` | nonce challenge and subject binding |
| `src/aae_a2a_ext/digest.py` | `request_digest` |
| `src/aae_a2a_ext/testkeys.py` | public test keys and example AAEs |
| `tests/` | in-process tests of the exchange and the digest vectors |

## Use

```bash
poetry install
poetry run python run.py
poetry run pytest
```

Expected output and a description of the six cases: [HOWTORUN.md](../../../HOWTORUN.md).

## Server side in short

```python
from aae_a2a_ext.server import create_supplier_app
from aae_a2a_ext.testkeys import demo_resolver, did_of, issue_supplier_aae
from aae_a2a_ext.challenge import utc_now

app, card, executor = create_supplier_app(
    "http://127.0.0.1:8000",
    resolver=demo_resolver(),
    accepted_issuers=[did_of("issuer")],
    own_aae=issue_supplier_aae(utc_now()),
)
```

`app` is a Starlette application with the Agent Card route and the JSON-RPC
route. The card lists the extension with `required: true` and the gated skills
with their mandate actions.

The keys in `testkeys.py` are public test keys for this sample only. See
[NOTICE](NOTICE).
