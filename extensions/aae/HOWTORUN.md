# How to run the AAE Extension sample

The sample is in `v1/samples/python/`.

## 1. Prerequisites

- Python 3.12 or higher
- [Poetry](https://python-poetry.org/)

## 2. Setup

```bash
cd extensions/aae/v1/samples/python
poetry install
```

## 3. Run the agents

```bash
poetry run python run.py
```

`run.py` starts the supplier agent on `127.0.0.1` on a free port and runs the
buyer agent against it. The script exits with 0 when all six requests behaved
as the specification says, otherwise with 1.

Expected output (port, AAE id and digests change from run to run):

```text
Supplier agent listening on http://127.0.0.1:63773 (card at /.well-known/agent-card.json)

Supplier card: Example Supplier Agent; extension https://moltrust.ch/extensions/aae/v1 required=True
   params: draft=draft-kroehl-agentic-trust-aae-02 audience=http://127.0.0.1:63773/a2a/jsonrpc
           skills={"get-quote": {"action": "read"}, "place-order": {"action": "pay"}} accepted_issuers=['did:example:issuer']
   supplier's own AAE (steps 1-3 checked by buyer): subject=did:example:supplier actions=['write']

(a) place-order 120 EUR, inside the mandate (cap 500 EUR)
   task state : TASK_STATE_COMPLETED
   receipt    : verdict=ACCEPT steps=1,2,3,4,5,6,7 aae_id=urn:uuid:ebb191d2-40b7-4998-a7be-01a92b9f58b2
   digest     : sha256:84559612f1f46ec0a03f8c448905af075ba4edf66e529b15b50f69c85a68b59a (recomputed from the request: match)
   artifact   : {"amount": 120, "currency": "EUR", "items": [{"qty": 20, "sku": "PAPER-A4"}], "order_id": "PO-0001", "status": "confirmed"}

(a2) place-order 80 EUR for an item the supplier does not stock: the AAE check
     accepts, the skill fails. The receipt stays; the task state is the skill's.
   task state : TASK_STATE_FAILED
   receipt    : verdict=ACCEPT steps=1,2,3,4,5,6,7 aae_id=urn:uuid:ebb191d2-40b7-4998-a7be-01a92b9f58b2
   digest     : sha256:97ff82c176abd81ff1260c0885e3e25c2e651f153c6f4bcb8c6263e77d55198b (recomputed from the request: match)
   skill      : place-order failed: not in catalogue: DESK-02. AAE urn:uuid:ebb191d2-40b7-4998-a7be-01a92b9f58b2 was verified; the failure is the skill's, not the authorization's.

(b) place-order 900 EUR, over the max_transaction_value constraint
   task state : TASK_STATE_REJECTED
   rejected   : step 7 (constraints), reason_code=max_transaction_value_exceeded - amount 900 EUR > cap 500 EUR
   digest     : sha256:1681f33e6d117e299f95c5750c9c69b257a9264a32e430c1c147bf3e3233d2e5

(c1) extension not activated (no A2A-Extensions header), card says required
   JSON-RPC error -32008 ExtensionSupportRequiredError: Extension https://moltrust.ch/extensions/aae/v1 is required and was not activated
   ErrorInfo.metadata: {"extension": "https://moltrust.ch/extensions/aae/v1"}

(c2) extension activated, AAE missing
   JSON-RPC error -32602 InvalidParamsError: metadata[https://moltrust.ch/extensions/aae/v1].aae is required
   ErrorInfo.metadata: {"extension": "https://moltrust.ch/extensions/aae/v1", "reason_code": "aae_missing"}

(c3) forged AAE: claims the issuer's kid, signed with another key
   task state : TASK_STATE_REJECTED
   rejected   : step 1 (signature), reason_code=invalid_signature
   digest     : sha256:edf9dc35873b6b0f0c46f8aeead5193a7dc97bcdecc6116ae68899b75e0e86d6

6/6 scenarios behaved as specified
```

What the six requests show:

| Case | Request | Result |
| :-- | :-- | :-- |
| (a) | order of 120 EUR, inside the 500 EUR limit | accepted, task completed, receipt and order artifact |
| (a2) | order of 80 EUR for an item the supplier does not stock | accepted, the skill fails, task failed; the ACCEPT receipt stays |
| (b) | order of 900 EUR | rejected at step 7 (constraints), the skill is not invoked |
| (c1) | extension not activated, card says required | JSON-RPC error -32008 |
| (c2) | extension activated, AAE missing | JSON-RPC error -32602, `reason_code` `aae_missing` |
| (c3) | AAE that names the issuer's key but is signed with another key | rejected at step 1 (signature) |

In (a), (a2) and (c3) the buyer recomputes `request_digest` from the request it
sent and compares it with the one in the result.

## 4. Run the tests

```bash
poetry run pytest
```

The tests run the full exchange in process (no network), cover each
verification step that can reject a request, and check `request_digest`
against the vectors in `tests/vectors/request-digest.json` and Appendix B of
the specification.
