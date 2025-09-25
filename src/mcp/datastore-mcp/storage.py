import os
import time
import threading
import msgpack
from typing import Any, Dict, Optional, Tuple

# In-memory structure: { namespace: { key: record_dict } }
# record_dict: {"v": value, "t": timestamp(int), "m": metadata(optional dict), "rev": int }

class DataStore:
    def __init__(self, base_dir: str, snapshot_name: str = "store.snapshot.msgpack", journal_name: str = "store.journal.msgpack"):
        self.base_dir = base_dir
        self.snapshot_path = os.path.join(base_dir, snapshot_name)
        self.journal_path = os.path.join(base_dir, journal_name)
        self._lock = threading.Lock()
        self._data: Dict[str, Dict[str, Dict[str, Any]]] = {}
        self._revisions: Dict[Tuple[str, str], int] = {}
        self._dirty = False
        self._last_compaction: Optional[int] = None
        self._corrupt_entries = 0
        os.makedirs(base_dir, exist_ok=True)
        self._load()

    # -------------- Persistence --------------
    def _load(self):
        # Load snapshot
        if os.path.exists(self.snapshot_path):
            try:
                with open(self.snapshot_path, 'rb') as f:
                    snapshot = msgpack.unpackb(f.read(), raw=False)
                if isinstance(snapshot, dict):
                    self._data = snapshot
                    for ns, mapping in self._data.items():
                        for k, rec in mapping.items():
                            self._revisions[(ns, k)] = int(rec.get("rev", 0))
            except Exception:
                # Corrupted snapshot -> start empty but keep file for debugging
                self._data = {}
        # Replay journal
        if os.path.exists(self.journal_path):
            try:
                with open(self.journal_path, 'rb') as f:
                    unpacker = msgpack.Unpacker(f, raw=False)
                    for entry in unpacker:
                        try:
                            if not isinstance(entry, dict):
                                self._corrupt_entries += 1
                                continue
                            op = entry.get("op")
                            ns = entry.get("ns")
                            k = entry.get("k")
                            if op == 1:  # write
                                v = entry.get("v")
                                t = entry.get("t")
                                m = entry.get("m")
                                rev = int(entry.get("rev", 0))
                                self._data.setdefault(ns, {})[k] = {"v": v, "t": t, "rev": rev}
                                if m is not None:
                                    self._data[ns][k]["m"] = m
                                self._revisions[(ns, k)] = rev
                            elif op == 0:  # delete
                                if ns in self._data and k in self._data[ns]:
                                    del self._data[ns][k]
                                    self._revisions[(ns, k)] = int(entry.get("rev", 0))
                        except Exception:
                            self._corrupt_entries += 1
                            continue
            except Exception:
                self._corrupt_entries += 1

    def _append_journal(self, entry: Dict[str, Any]):
        with open(self.journal_path, 'ab') as f:
            f.write(msgpack.packb(entry, use_bin_type=True))

    def compact(self) -> Dict[str, Any]:
        with self._lock:
            tmp_path = self.snapshot_path + ".tmp"
            with open(tmp_path, 'wb') as f:
                f.write(msgpack.packb(self._data, use_bin_type=True))
            os.replace(tmp_path, self.snapshot_path)
            # Reset journal
            open(self.journal_path, 'wb').close()
            self._last_compaction = int(time.time())
            snapshot_bytes = os.path.getsize(self.snapshot_path)
            journal_bytes = os.path.getsize(self.journal_path)
            return {"ok": True, "snapshot_bytes": snapshot_bytes, "journal_bytes": journal_bytes, "last_compaction": self._last_compaction}

    # -------------- CRUD Operations --------------
    def save(self, key: str, value: Any, namespace: str = "default", metadata: Optional[Dict[str, Any]] = None, replace: bool = True) -> Dict[str, Any]:
        ts = int(time.time())
        with self._lock:
            ns_map = self._data.setdefault(namespace, {})
            if not replace and key in ns_map:
                return {"error": "exists"}
            prev_rev = self._revisions.get((namespace, key), 0)
            rev = prev_rev + 1
            rec = {"v": value, "t": ts, "rev": rev}
            if metadata:
                rec["m"] = metadata
            ns_map[key] = rec
            self._revisions[(namespace, key)] = rev
            self._append_journal({"op": 1, "ns": namespace, "k": key, "v": value, "t": ts, "m": metadata, "rev": rev})
            return {"ok": True, "rev": rev, "timestamp": ts}

    def read(self, key: str, namespace: str = "default") -> Dict[str, Any]:
        with self._lock:
            rec = self._data.get(namespace, {}).get(key)
            if rec is None:
                return {"error": "not_found"}
            out = {"key": key, "namespace": namespace, "value": rec["v"], "timestamp": rec["t"], "rev": rec.get("rev", 0)}
            if "m" in rec:
                out["metadata"] = rec["m"]
            return out

    def list_keys(self, namespace: str = "default") -> Dict[str, Any]:
        with self._lock:
            ns_map = self._data.get(namespace, {})
            return {"namespace": namespace, "keys": list(ns_map.keys()), "count": len(ns_map)}

    def delete(self, key: str, namespace: str = "default") -> Dict[str, Any]:
        with self._lock:
            ns_map = self._data.get(namespace, {})
            if key not in ns_map:
                return {"error": "not_found"}
            prev_rev = self._revisions.get((namespace, key), 0)
            rev = prev_rev + 1
            del ns_map[key]
            self._revisions[(namespace, key)] = rev
            self._append_journal({"op": 0, "ns": namespace, "k": key, "rev": rev})
            return {"ok": True}

    def dump_namespace(self, namespace: str = "default", limit: Optional[int] = None, include_metadata: bool = False) -> Dict[str, Any]:
        with self._lock:
            ns_map = self._data.get(namespace, {})
            items = []
            for i, (k, rec) in enumerate(ns_map.items()):
                if limit is not None and i >= limit:
                    break
                entry = {"key": k, "value": rec["v"], "timestamp": rec["t"], "rev": rec.get("rev", 0)}
                if include_metadata and "m" in rec:
                    entry["metadata"] = rec["m"]
                items.append(entry)
            return {"namespace": namespace, "items": items, "count": len(ns_map)}

    def stats(self) -> Dict[str, Any]:
        with self._lock:
            namespaces = {ns: len(kvs) for ns, kvs in self._data.items()}
            total_keys = sum(namespaces.values())
            snapshot_bytes = os.path.getsize(self.snapshot_path) if os.path.exists(self.snapshot_path) else 0
            journal_bytes = os.path.getsize(self.journal_path) if os.path.exists(self.journal_path) else 0
            return {
                "namespaces": namespaces,
                "total_keys": total_keys,
                "snapshot_bytes": snapshot_bytes,
                "journal_bytes": journal_bytes,
                "last_compaction": self._last_compaction,
                "corrupt_entries": self._corrupt_entries,
            }
