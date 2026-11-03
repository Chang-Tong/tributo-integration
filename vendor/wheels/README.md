# Current Core dependency Wheels (0.3)

Both Broker profiles now use the current Core baseline. The previous Core
440da042, connector 0.1.0, and Broker 0.2 Wheel are retired from active build
inputs. Pure-Python Wheels below are installed by the Docker build; ordinary
third-party dependencies still come from the configured index.

| Wheel | Source and patch chain | SHA-256 |
| --- | --- | --- |
| `ray_clickhouse-1.0-py3-none-any.whl` | PyPI ray-clickhouse 1.0, unmodified distribution | `5ac258dd425ea9fa879b3429c57755f7948c1541bda5fc6f57f2c9605e3c63cb` |
| `tributo-1.0.0-py3-none-any.whl` | Chang-Tong/Tributo@1eaae848ef7f6acbd600c87771f91f9291f00b3e | `9493ecc3b791c184969e30b99ab367f27143c4a1e7703eb385c634088b4f9ce9` |
| `tributo_algorithms_boosting-0.1.0-py3-none-any.whl` | Chang-Tong/tributo-algorithms@6f39378d4d850cfd41e9510abc313efc6d4f209f + boosting-v2.7.patch + boosting-v2.8-onnx-schema.patch | `c8bbed6fd0c9f828b37de498113f578f93c4ccb2ba5811ff80ee8f4424d4e922` |
| `tributo_broker_redis-0.3.0-py3-none-any.whl` | Chang-Tong/tributo-broker-redis@e2973b2a7409fc72807bbec23388d13966c5c319 + broker-v0.3.0.patch | `2953d77288c1a1ee09f43d16368ff34a154fb9880a6576fcee05aa07f8839148` |

The complete [broker-v0.3.0.patch](../patches/broker-v0.3.0.patch) applies to a
clean e2973b2 archive and includes current-Core generic training and the V2
ownership migration, portable protocol contracts and admission fixes. Build with `uv build --wheel --offline`; compare its bytes
and all package Python sources to the bundled Wheel. Refresh the bundled file,
this table, and `uv lock --refresh-package tributo-broker-redis` together.

The Boosting Wheel retains its documented local patches. Its Git reference alone
does not reproduce the shipped Wheel; the two patch files and Apache-2.0 license
remain in this repository. Connector 1.0 is the unmodified published Wheel.

## Historical build evidence for 0.2 and earlier

The descriptions below concern previous distributions and do not select the
current build inputs. The complete current Broker patch is v0.3.0, applied on
its own to e2973b2.

## Reproducing the patched packages

Use a clean checkout of the source base in the table, apply the corresponding
patch with `git apply --check` and `git apply`, then build with Python 3.13.
For boosting, apply the cumulative v2.7 patch first, followed by the incremental
v2.8 ONNX schema patch (both paths are relative to the algorithms repository root):

```sh
uv build --wheel --no-sources --python 3.13 --out-dir /path/to/output .
```

Run that command at the broker repository root or in `packages/boosting` for
boosting. Add `--offline` when the build dependencies are already cached.
The Broker patch contains the runtime/package sources needed to reproduce its
Wheel; its regression suite lives in the Broker repository. The boosting
patches also retain their existing tests. No deployment environment files are
included. The boosting patch includes the earlier dataset-transform hook and
block-order randomization, the empty-shard fix, and the ONNX regression output
name alignment with the native checkpoint contract, plus binary evaluation
for either positive class encoding (training.positive_label=0 or 1). The v2.7
patch also converts binary logistic base_score probabilities to ONNX margins,
including constant zero-leaf trees. The v2.5 and v2.6 patches are retained
as historical provenance.

On 2026-09-24, applying the broker patch to a clean archive of its base and
building offline reproduced the shipped wheel byte-for-byte. All 13 broker
package Python files matched. The boosting patch also replayed cleanly; all
11 package Python files matched its shipped wheel. On 2026-09-25 (Asia/Shanghai),
the complete boosting v2.7 patch applied to a clean base archive and an offline
build reproduced the new wheel byte-for-byte; 40 targeted algorithm tests passed,
including imbalanced binary/multiclass and nonzero-mean regression intercepts.

On 2026-09-30, the broker v2.8 patch adds request receipt/deadline transport,
native Ray Jobs deadline stopping and recovery, cancellation before payload
validation, and per-delivery UTF-8 decoding. The v2.5 patch remains historical.
All 13 package Python files were compared byte-for-byte with the rebuilt wheel.

On 2026-09-30, the boosting v2.8 ONNX schema patch records the fitted input
column order in the ONNX file itself as JSON `feature_names`, together with
`task_type`, `objective`, `framework`, `num_features` and classification
`num_classes`. These facts come from the export source and trained Booster;
converter metadata and all v2.7 conversion fixes are preserved. The incremental
patch was checked and replayed against the v2.7 wheel source, and the resulting
`native.py` matched the repacked wheel byte-for-byte. The wheel was repacked with
a regenerated RECORD; every payload hash and size was checked. Its input wheel
SHA-256 was `4e6addbeca1f912e514fd73442c43e7d1551fbd2d334e0f53629a28f12f2da27`.
The 11 real binary/multiclass/regression exports in
`tests/test_boosting_wheel_metadata.py` verify opaque result-column metadata,
checkpoint output names and ONNX Runtime predictions against XGBoost, including
constant/imbalanced data. The test loads the checked-in wheel source directly,
so an older installed Boosting package cannot mask a regression.

Rebuild and update this table whenever the source base or a local patch changes.
Verify that every wheel filename still ends in `py3-none-any.whl`.

## Historical ray-clickhouse 0.1.0 provenance limitation

The retired 0.1.0 wheel must not be described as an unmodified build of the locked
`c162710...` reference. Its 13 package Python files match the existing local
`ray-clickhouse-auto-range` checkout at
`a5d6f99159aa7bc149ff2dbc463cec24dc56c7a2`, including uncommitted changes to
`src/ray_clickhouse/_schema.py` and `src/ray_clickhouse/datasink.py`.
The locked reference was unavailable in that checkout during this audit;
the complete portable patch chain and a byte-identical rebuild of this wheel
have not been established. This limitation does not apply to the current
unmodified PyPI 1.0 Wheel identified in the table above.

## Licenses

The other wheels carry their license file inside the wheel archive. The
boosting wheel currently omits it, so its upstream Apache-2.0 license is kept
next to the wheel as `tributo-algorithms-LICENSE`.

## Provider 0.2 protocol ownership migration

On 2026-10-27, the existing v2 parser, validators, reporter, request mappings,
and Ray driver moved from KnoVa into the provider's `profiles/aimodel_v2`.
The provider Wheel is now 0.2.0. The old 0.1 Wheel is removed from this build
input directory so wildcard offline installation cannot select both versions.

The complete `broker-v0.2.0.patch` applies directly to the clean `e2973b2` base;
do not apply the historical v2.8 patch first. It includes the preceding local
provider fixes as well as this migration. A clean archive plus that patch was
built offline and reproduced the new Wheel byte-for-byte. All provider Python
files were compared with the bundled Wheel payload.

To rebuild after provider changes, build its 0.2.0 Wheel from the sibling Broker
checkout, replace the bundled file, run `uv lock --refresh-package
tributo-broker-redis`, and update the hash in this table. Verify the lock's Wheel
hash before using `uv sync --frozen`. The source patch must be refreshed along
with the Wheel.
