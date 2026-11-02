# AAE Extension

This directory contains the specification and a Python sample for the **AAE
extension v1** for the Agent2Agent (A2A) protocol.

## Purpose

An AAE (Agent Authorization Envelope) is a W3C Verifiable Credential, signed as
an EdDSA compact JWS, that states what an agent may do: the actions it may take
(mandate), the limits on them (constraints, for example a maximum transaction
value) and the time window (validity). The extension carries an AAE in an A2A
message and has the receiving agent verify it before a gated skill runs.

- The server declares the extension in its Agent Card, lists which skills it
  gates and which mandate action each one needs, and names the issuers it
  accepts.
- The client sends the AAE in `message.metadata`. The server answers with
  `TASK_STATE_AUTH_REQUIRED` and a nonce; the client signs the nonce with the
  key of the AAE's subject DID, which shows it controls that DID.
- The server runs the nine verification steps of the AAE draft. If one fails,
  the task ends in `TASK_STATE_REJECTED` with the failing step and a reason
  code, and the skill is never invoked. If all pass, the skill runs and the
  task carries an ACCEPT receipt.
- Every result carries a `request_digest` (SHA-256 over the JCS form of the
  request part), so the client can check that the decision refers to the
  request it sent.

The extension defines no new RPC methods, task states or core fields. It uses
the in-task authorization pattern of A2A section 7.6.

- Extension URI: `https://moltrust.ch/extensions/aae/v1`
- AAE baseline:
  [draft-kroehl-agentic-trust-aae-02](https://datatracker.ietf.org/doc/draft-kroehl-agentic-trust-aae/02/)
- Status: draft v1. Proposed as an A2A extension in
  [a2aproject/A2A#2391](https://github.com/a2aproject/A2A/issues/2391).

## Specification

➡️ **[Full Specification (v1)](./v1/spec.md)**

The specification is maintained in
[MoltyCel/aae-a2a-extension](https://github.com/MoltyCel/aae-a2a-extension),
together with conformance vectors and a guide for running another
implementation against this one.

## Sample Implementation

A buyer agent and a supplier agent run against each other over A2A JSON-RPC on
localhost. The buyer holds an AAE with a 500 EUR order limit and places six
orders; the sample prints what the supplier decided for each.

➡️ **[Python Sample Usage Guide](./v1/samples/python/README.md)**

➡️ **[How to run](./HOWTORUN.md)**
