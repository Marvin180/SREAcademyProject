# Contributing to SRE Observability Stack

Thank you for your interest in contributing to this project! Follow these guidelines to keep the codebase, Kubernetes manifests, and documentation clean and reliable.

---

## How to Contribute

1. **Fork the repository** and create a feature or fix branch from `main`:
   ```zsh
   git checkout -b feat/your-feature-name
   ```
2. **Make focused, well-tested changes** inside the appropriate directory (`src/App/`, `src/Prometheus/`, `src/Grafana/`, `src/Alertmanager/`, `src/scripts/`).
3. **Verify your changes locally** on Minikube before opening a Pull Request.
4. **Open a Pull Request** describing what changed, why it is needed, and how you tested it.

---

## Reporting Issues

When opening an issue, please include:
- A clear summary of the problem or enhancement proposal.
- Steps to reproduce the issue (including `kubectl` commands or traffic mode used).
- Relevant pod statuses (`kubectl get pods -A`) or container logs (`kubectl logs ...`).

---

## Coding & Repository Standards

- **Language:** Write all source code, comments, Kubernetes manifests, documentation, and commit messages in **English**.
- **Python Style (`src/main.py`, `src/scripts/`):**
  - Keep functions concise with clear docstrings and type annotations where helpful.
  - Validate Python syntax before committing (`python3 -m py_compile <file>`).
  - Avoid adding unnecessary third-party dependencies to CLI helper scripts.
- **Kubernetes Manifests (`src/*/*.yaml`):**
  - Keep components separated by folder and responsibility (`ConfigMap`, `Deployment`, `Service`, `RBAC`).
  - Include comments explaining *why* non-obvious settings exist (probes, resource limits, relabeling rules, provisioning paths).
  - Never commit plaintext credentials, API tokens, or webhook URLs; use Kubernetes `Secret` references for production integrations.
- **Documentation:** Update [README.md](README.md) whenever endpoints, ports, metrics, dashboards, or alerting rules change.

---

## Testing Checklist Before Submitting a PR

1. Confirm Python syntax compiles cleanly:
   ```zsh
   python3 -m py_compile src/main.py src/scripts/generate_traffic.py
   ```
2. Apply updated manifests in Minikube and verify rollouts succeed:
   ```zsh
   kubectl rollout status deployment/orders-app-deployment
   kubectl rollout status deployment/prometheus-deployment -n monitoring
   kubectl rollout status deployment/grafana-deployment -n monitoring
   kubectl rollout status deployment/alertmanager-deployment -n monitoring
   ```
3. Run the traffic generator against `orders-app` and confirm metrics, dashboards, and alerts respond as expected:
   ```zsh
   python3 src/scripts/generate_traffic.py --url <APP_URL> --mode mixed --duration 60
   ```
