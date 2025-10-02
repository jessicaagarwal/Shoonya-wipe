## Deploy to Render (Docker)

Prerequisites:
- A Render account
- This repo pushed to GitHub or GitLab

Steps:
1. Ensure `render.yaml` is present at the repo root (it is).
2. Push changes to your repository's default branch.
3. In Render, click New → Blueprint → select your repo.
4. Review and create resources.

Notes:
- The app runs via the `Dockerfile` and listens on `PORT` provided by Render.
- Safe defaults are set via env vars: no real device wipe in cloud.
- Persistent disks are mounted at `/app/out` and `/app/exports` for artifacts.

Preset environment variables (in `render.yaml`):
- `RUNNING_IN_DOCKER=1`
- `ENABLE_REAL_WIPE=0`
- `WEB_PRODUCTION_MODE=0`
- `SHOONYA_PRODUCTION_MODE=0`
- `SIM_TOTAL_SECONDS=90`

Enabling production wiping (not recommended in cloud):
- Set `WEB_PRODUCTION_MODE=1`, `SHOONYA_PRODUCTION_MODE=1`, and (in Docker) `DOCKER_PRODUCTION_ALLOWED=1`.
- Requires privileged access to devices (not available on Render).
