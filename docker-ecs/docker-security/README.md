# Docker Security Best Practices

Hardening Docker containers using non-root users, read-only filesystems, capability dropping, AppArmor, and Content Trust.

---

## Files

| File | Purpose |
|---|---|
| `Dockerfile.insecure` | Baseline — runs as root |
| `Dockerfile.secure` | Non-root user |
| `Dockerfile.readonly` | Read-only filesystem |
| `Dockerfile.capabilities` | Capability drop testing |
| `Dockerfile.apparmor` | AppArmor profile testing |
| `Dockerfile.production` | All features combined |
| `app.py` | Shows running UID/GID |
| `logging-app.py` | Tests filesystem write permissions |
| `capability-test.py` | Tests Linux capabilities |
| `apparmor-test.py` | Tests AppArmor restrictions |
| `secure-production-app.py` | Final hardened app |
| `verify-signature.sh` | Content Trust demo |

---

## Tasks

### 1 — Non-Root User
```dockerfile
RUN groupadd -r appuser && useradd -r -g appuser appuser
USER appuser
```

### 2 — Read-Only Filesystem
```bash
docker run --read-only --tmpfs /tmp -p 5003:5000 readonly-test
```

### 3 — Drop Capabilities
```bash
docker run --cap-drop=ALL --cap-add=NET_BIND_SERVICE ...
```

### 4 — AppArmor Profile
```bash
sudo apparmor_parser -r /etc/apparmor.d/docker-secure-app
docker run --security-opt apparmor=docker-secure-app ...
```

> **Note:** Shared libraries need `mr` (read + mmap), not just `r`.  
> Diagnose denials: `sudo grep "apparmor.*DENIED" /var/log/kern.log`

### 5 — Content Trust
```bash
export DOCKER_CONTENT_TRUST=1
docker trust key generate mykey
```

### 6 — Production Run (All Features)
```bash
docker run -d --name production-secure \
  --tmpfs /tmp:rw,noexec,nosuid,size=50m \
  --cap-drop=ALL \
  --cap-add=NET_BIND_SERVICE \
  --security-opt apparmor=docker-secure-app \
  --security-opt no-new-privileges:true \
  --user 1001:1001 \
  --memory=256m \
  --cpus=0.5 \
  -p 5007:5000 \
  secure-production-app
```

---

## Results
```json
{ "uid": 1001, "gid": 1001 }
{ "app_write": "denied", "passwd_read": "denied", "tmp_write": "allowed" }
```

| Check | Status |
|---|---|
| Non-root user | ✅ |
| /app write blocked | ✅ |
| /etc/passwd blocked | ✅ |
| /tmp writable | ✅ |
| AppArmor active | ✅ |
| Memory 256MB | ✅ |
| CPU 0.5 cores | ✅ |
| no-new-privileges | ✅ |

---

## Quick Reference

| Flag | What it does |
|---|---|
| `--read-only` | Immutable root filesystem |
| `--tmpfs /tmp` | In-memory writable scratch space |
| `--cap-drop=ALL` | Remove all capabilities |
| `--security-opt apparmor=<profile>` | Mandatory access control |
| `--security-opt no-new-privileges:true` | Block privilege escalation |
| `--memory=256m` | Memory cap |
| `--cpus=0.5` | CPU cap |
| `DOCKER_CONTENT_TRUST=1` | Enforce signed images |
