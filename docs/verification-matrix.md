# Verification matrix

Current 0.3 baseline: Core `1eaae848ef7f6acbd600c87771f91f9291f00b3e`,
Broker 0.3, connector 1.0. Retired trainer/config APIs are rejected. The former
eight generic/current-Core failures are resolved; both protocols were tested
on the same Core. See the [current acceptance](https://github.com/Chang-Tong/tributo-broker-redis/blob/a4ccddda20ec942c3e62276db4b901c7bdad3d2b/docs/test-reports/2026-10-27-current-core-compatibility.md).
Earlier pinned-assembly evidence below is historical.

The implementation is now owned by `tributo-broker-redis.profiles.aimodel_v2`;
its protocol/mapping/driver tests moved to the Broker repository. KnoVa retains
compatibility, CLI, and deployment tests. Historical integration evidence below
remains separate from the current migration evidence.

On 2026-10-27, the final Broker 0.2 Wheel passed the pinned KnoVa assembly's
real training, inference, and exact-SHAP smoke (3/3), through the thin KnoVa
wrapper. The Broker-only current-Core assembly passed 54 business cases,
11 failure/recovery cases, and 8 real Sentinel cases after fixes. KnoVa's
132 tests passed. See the [complete local acceptance report](https://github.com/Chang-Tong/tributo-broker-redis/blob/a4ccddda20ec942c3e62276db4b901c7bdad3d2b/docs/test-reports/2026-10-27-aimodel-v2-acceptance.md)
for exact dependencies, first-run failures, fixes, artifacts, and remaining
generic-v1/current-Core release blockers.

The repository keeps one implementation path: KnoVa protocol v2 is adapted to
the public Tributo, Redis Broker, and official boosting contracts. Credentials
are supplied only through the process environment.

| Area | Verified path | Evidence |
| --- | --- | --- |
| Protocol | Training `job_id`; inference `execution_id`; required tenant/model/version/task identities; v2 lifecycle events | Unit suite |
| Broker | Redis Streams admission, ACK, retry, idempotency, queued cancellation, watchdog and one terminal event | Unit suite |
| Restart recovery | `XAUTOCLAIM` pending delivery recovery and active Ray Job cancellation state reconstruction | Unit suite and `--exercise-recovery` smoke |
| ClickHouse input | Tributo's official Ray ClickHouse Binding; connector-owned physical partitions; residual equality transforms; 200k-row/64 MiB inference blocks | Unit suite and KnoVa devbox integration |
| Training | Ray-native ClickHouse input, lossless train/validation/test split, two-worker distributed XGBoost and live per-round metrics | Unit suite and KnoVa devbox integration |
| Evaluation | Full test-set metrics, confusion matrix, ROC, threshold analysis, gain importance and distributed Pearson feature correlation | Unit suite and KnoVa devbox integration |
| Checkpoint | Official `model.ubj` and `feature_names.json` checkpoint on shared NAS/NFS path | Local integration smoke |
| Bundle | Official ONNX and UBJ artifacts, content digest and Bundle identity validation | Unit suite and local/S3 smoke |
| Protocol projection | Training `artifact_manifest` is passed directly into inference with exact paths, sizes and SHA-256 hashes | Local S3 smoke |
| Inference | ONNX prediction plus exact or explicitly approximate UBJ TreeSHAP | Local integration smoke |
| Output | KnoVa result projection followed by Tributo `WriteGateway` ClickHouse append, dynamic measured-row batching and bounded pre-write retry | Unit suite and local integration smoke |
| Deployment | Non-root image, Redis/Ray/Consumer Compose health, hardened systemd unit | Compose smoke |
| Offline | `docker save` + `zstd -19 -T0`, archive test, SHA-256 and platform record | Packaging script and generated package verification |

## Explicit upstream limits

- The pinned official boosting package persists a checkpoint but explicitly
  rejects `resume_from`; cross-process training resume waits for its recovery
  gate.
- Direct UBJ-only prediction is not enabled because the current official native
  predictor drops feature names. The supported complete Bundle path is ONNX
  prediction plus UBJ attribution.
- Dependencies are pinned to immutable commits until compatible releases are
  tagged.
