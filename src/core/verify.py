#!/usr/bin/env python3
"""
SafeErasePro - Signed Log Verifier (MVP)

Usage:
  python verify.py --log out/wipelog_signed.json --pub keys/public.pem

Verifies RSA-PSS-SHA256 signature embedded in the JSON under `signature`.
Returns exit code 0 on VALID, 1 on INVALID/error.
"""

import argparse
import base64
import json
import sys
import hashlib

from Crypto.PublicKey import RSA  # type: ignore
from Crypto.Signature import pss  # type: ignore
from Crypto.Hash import SHA256  # type: ignore


def canonical_bytes(obj: dict) -> bytes:
    return json.dumps(obj, separators=(",", ":"), sort_keys=True).encode("utf-8")


def verify(log_path: str, pub_path: str) -> bool:
    data = json.load(open(log_path, "r", encoding="utf-8"))
    sig_block = data.get("signature") or {}
    sig_b64 = sig_block.get("sig_b64")
    if not sig_b64:
        print("No signature present", file=sys.stderr)
        return False

    # Prepare unsigned payload
    unsigned = dict(data)
    unsigned.pop("signature", None)
    payload = canonical_bytes(unsigned)

    h = SHA256.new(payload)
    key = RSA.import_key(open(pub_path, "rb").read())
    verifier = pss.new(key)
    try:
        verifier.verify(h, base64.b64decode(sig_b64))
        # Optional: check fingerprint match if provided
        pub_fpr = hashlib.sha256(open(pub_path, "rb").read()).hexdigest()[:16]
        claimed = sig_block.get("pubkey_sha256_16", "")
        if claimed and claimed != pub_fpr:
            print("WARNING: Public key fingerprint mismatch")
        print("VALID: Signature verified")
        return True
    except (ValueError, TypeError):
        print("INVALID: Signature verification failed", file=sys.stderr)
        return False


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--log", required=True)
    ap.add_argument("--pub", required=True)
    args = ap.parse_args()
    return 0 if verify(args.log, args.pub) else 1


if __name__ == "__main__":
    sys.exit(main())




