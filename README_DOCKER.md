# 🎭 Docker Setup – Theater‑Light‑Controller

Dieses Docker‑Setup startet **alles** in Containern:
- **OLA (olad)** für DMX‑Ausgabe (USB/DMX Interface)
- **FastAPI Backend** (Port 8000)
- **Static Frontend** (Port 5500)

## Schnellstart
```bash
# 1) In diesen Ordner wechseln (da wo docker-compose.yml liegt)
docker compose build
docker compose up -d
```

**Danach:**
- Frontend: http://localhost:5500
- API:     http://localhost:8000
- OLA UI:  http://localhost:9090

## USB‑DMX Interface durchreichen
Das Enttec DMX USB Pro erscheint oft als `/dev/ttyUSB0` (Linux). 
In `docker-compose.yml` ist das bereits gemappt:
```yaml
devices:
  - "/dev/ttyUSB0:/dev/ttyUSB0"
privileged: true
```
> Falls dein Interface einen anderen Pfad hat, bitte anpassen (z. B. `/dev/ttyUSB1`).  
> Unter macOS/Windows mit Docker Desktop nutze den jeweiligen TTY‑Pfad (z. B. `/dev/tty.usbserial‑xxxx`).

## Datenstruktur im Container
- **/app/backend/** → `dmx_server.py` (FastAPI)
- **/app/frontend/** → `index.html` (Single‑Page‑App)

## OLA Hinweise
- OLA (olad) läuft **im Container** und steuert dein USB‑Interface direkt.
- OLA Web UI: http://localhost:9090 (Universe/Plugin‑Status prüfen)
- Wenn OLA dein Interface nicht sieht:
  1. Prüfe das Device‑Mapping (`devices:`) und `privileged: true`.
  2. Prüfe auf dem Host: `dmesg | grep -i tty` (richtiger Pfad?)
  3. Container‑Logs: `docker logs theater-light-controller`

## Stoppen/Entfernen
```bash
docker compose down
```

## Optional – Zwei‑Container‑Variante
Möchtest du Frontend separat (z. B. via Nginx) serven, kann man das Setup splitten. 
Dieses Paket nutzt absichtlich **eine** Container‑Instanz für Einfachheit.
