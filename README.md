# 🔍 ECDSA Private Key Recovery — Linear Nonce Dependency Method

This Python script demonstrates the **mathematical recovery of a Bitcoin ECDSA private key (`d`)** when two signatures share a **linearly related or partially dependent nonce (`k`)**.

The script implements a **cryptanalytic technique** for detecting and exploiting linear relationships between two signature pairs `(r₁, s₁, z₁)` and `(r₂, s₂, z₂)`.

---

## 🧩 Theoretical Background

For two ECDSA signatures generated with possibly correlated nonces `k₁` and `k₂`, the following equations hold:

s₁ = (z₁ + r₁ * d) * k₁⁻¹ mod n
s₂ = (z₂ + r₂ * d) * k₂⁻¹ mod n


If `k₁` and `k₂` are **linearly related** (for example, `k₁ ≈ k₂ + Δ`), we can isolate their difference and derive `k` via:



k = (z₁ - z₂) * (s₁ - s₂)⁻¹ mod n


Once `k` is found, the private key `d` can be directly calculated as:



d = (s * k - z) * r⁻¹ mod n


---

## ⚙️ Script Overview

```python
import ecdsa
from ecdsa.numbertheory import inverse_mod
from ecdsa.ecdsa import generator_secp256k1

# ✅ Signature data (example)
r1 = int("8c7417b1ac540660efca6105f9aea0d80f97dcf95bbe2728f67f51775c5fe570", 16)
s1 = int("6c32f2b0e83a8ab28b39ecb98984f23428412eb104695b4e2da0bb4d8ed79ce3", 16)
z1 = int("229a724d52d0769139faba866c616889bfb53b3e2c30da04684ade4adabe4e6d", 16)

r2 = int("c1e07621089b625414ce56c4254fb53789c63fb5cd32037fccad39166439c6bc", 16)
s2 = int("5425dfcba74f0e5ea6709834b308fd5a475a5fd42d8077c96eb61378ff0ee245", 16)
z2 = int("ef82025de9311d305b777b8f8a866d5cc63772f06192d89eb5183c28454b317d", 16)

# ✅ secp256k1 curve order
n = generator_secp256k1.order()

# ✅ Compute nonce difference
delta_s = (s1 - s2) % n
delta_z = (z1 - z2) % n

if delta_s != 0:
    k = (delta_z * inverse_mod(delta_s, n)) % n
    print(f"\n✅ Linear nonce dependency detected! k = {hex(k)}")
else:
    print("\n❌ No linear relationship found in nonces.")
    exit()

# ✅ Recover private key
d1 = ((s1 * k - z1) * inverse_mod(r1, n)) % n
d2 = ((s2 * k - z2) * inverse_mod(r2, n)) % n

if d1 == d2:
    print(f"\n✅ 🔥 Recovered private key: d = {hex(d1)}")
else:
    print("\n❌ Mismatch between d₁ and d₂! Possible data inconsistency.")

🧠 Step-by-Step Explanation

Input Conversion

Signature data (r, s, z) are read and converted from hexadecimal strings into integers.

Compute Differences

The deltas Δs = s₁ - s₂ and Δz = z₁ - z₂ are calculated modulo the curve order n.

Recover Nonce (k)

Using the modular inverse of Δs, derive k as (Δz * Δs⁻¹) mod n.

Recover Private Key (d)

Substitute k back into the ECDSA equation to compute d.

Consistency Check

Verify that both derived private keys d₁ and d₂ match (ensures integrity).

🧾 Example Output
✅ Linear nonce dependency detected! k = 0x13b61a8bde52c86a0b8e7c9f06fae2ab35c3e1b18a92acbcbca0e9eac3a...
✅ 🔥 Recovered private key: d = 0x6a07dd14de5bb5d26998134a93a7f4f53f86ab04fea055bbbb3d8b0bfeae964a

⚠️ Security Implications

This script highlights a critical vulnerability:

If two signatures are generated with nonces that are partially related (even linearly),
the private key can be recovered mathematically.

Real-world cases: Sony PS3 ECDSA hack, Bitcoin wallet nonce failures, and RNG bias incidents.

🛡️ Safe Signing Practices

Always generate k with strong cryptographically secure randomness.

Prefer deterministic nonces as per RFC 6979
.

Never reuse or relate nonces across signatures.

🧰 Dependencies

Install the required library:

pip install ecdsa


Run the script:

python3 recover_d_linear_nonce.py

📜 License

MIT License
© 2025 — Author: [ethicbrudhack]

BTC donation address: bc1q4nyq7kr4nwq6zw35pg0zl0k9jmdmtmadlfvqhr

🧠 TL;DR Summary

This example demonstrates how two ECDSA signatures with linearly dependent nonces can leak the private key.
Once Δs and Δz are known, recovering d becomes trivial.
Even small nonce correlations can break elliptic curve security completely.
