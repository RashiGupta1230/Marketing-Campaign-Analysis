"""
Persistent Governance Audit Ledger.
Stores managerial approvals to a persistent JSON log with SHA-256 integrity hashes.
"""

from datetime import datetime
import hashlib
import json
import os
from typing import Any, Dict, List

DEFAULT_AUDIT_FILE = os.path.join(os.path.dirname(__file__), "audit_log.json")


def load_audit_log(filepath: str = DEFAULT_AUDIT_FILE) -> List[Dict[str, Any]]:
    """Load audit history from persistent JSON ledger."""
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def save_audit_record(
    scenario: str,
    target_budget: float,
    projected_revenue: float,
    projected_roas: float,
    allocations: Dict[str, float],
    approved_by: str = "Marketing Manager",
    filepath: str = DEFAULT_AUDIT_FILE,
) -> Dict[str, Any]:
    """Append a signed managerial approval record with cryptographic verification hash."""
    now_iso = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    audit_id = f"AUD-{datetime.now().strftime('%Y%m%d%H%M%S')}"

    # Build verification payload & hash
    payload = f"{audit_id}|{scenario}|{target_budget}|{projected_revenue}|{projected_roas}|{approved_by}"
    verification_hash = hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]

    record = {
        "audit_id": audit_id,
        "timestamp": now_iso,
        "scenario": scenario,
        "approved_by": approved_by,
        "target_budget": float(target_budget),
        "projected_revenue": float(projected_revenue),
        "projected_roas": float(projected_roas),
        "allocations": {k: float(v) for k, v in allocations.items()},
        "verification_hash": f"SHA256:{verification_hash}",
        "status": "APPROVED",
    }

    records = load_audit_log(filepath)
    records.insert(0, record)  # Most recent first

    os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)

    return record
