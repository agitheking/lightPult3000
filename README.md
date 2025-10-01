
# 🎭 Theater‑Lichtsteuerung (Single‑Page + Python DMX)

## Inhalt
- `frontend/index.html` – Single‑File‑App (React + Babel + Tailwind via CDN)
- `backend/dmx_server.py` – FastAPI‑Server, spricht OLA (Open Lighting Architecture)
- `backend/requirements.txt` – Python‑Abhängigkeiten
- `config/stage_playlist_guest_scenes.json` – Beispiel‑Export (Szenen + Playlist)
- `start.sh` – Startskript (installiert Python‑Deps, startet Backend + Frontend)

## Voraussetzungen
- Linux/Ubuntu (empfohlen) oder macOS. Für DMX‑Ausgabe benötigst du **OLA** (Open Lighting Architecture).
- DMX‑Interface (z. B. **Enttec DMX USB Pro Mk2**), per USB angeschlossen.
- Python 3.10+

### OLA installieren (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install -y ola
sudo systemctl enable olad
sudo systemctl start olad
# Test: http://localhost:9090 (OLA Web UI)
```

> Hinweis: Das Python‑Paket `ola` kommt mit der OLA‑Installation (nicht via pip).

## Start
```bash
# im Projektverzeichnis
chmod +x start.sh
./start.sh
```

- Backend läuft auf **http://127.0.0.1:8000** (`/api/dmx`, `/api/scene`, `/api/status`).
- Frontend läuft auf **http://127.0.0.1:5500** (statischer Webserver).

Öffne die Frontend‑URL im Browser des Bühnensystems.

## Frontend‑Nutzung
- Tabs: **editor**, **probe**, **show**, **guest**
  - **editor**: Szenen bauen, Spots bearbeiten, Export/Import.
  - **probe**: Playlist bauen (Drag&Drop), Spots editierbar.
  - **show**: linkes Panel ausgeblendet, Bühne + Player groß, **nur abspielen**.
  - **guest**: 4 Kacheln (Party, Wohnzimmer Konzert 1, Rock Konzert, Arbeitslicht).
- **Export (alles)** speichert `theme`, `lights`, `scenes`, `playlist` in eine JSON.
- **Import** liest dieselben Felder.

### DMX‑Mapping
- **DIM**: 1 Kanal → `start` (0–255 basierend auf Helligkeit 0–100 %)
- **RGB**: 3 Kanäle → `start`=R, `start+1`=G, `start+2`=B, jeweils skaliert mit Helligkeit.

## API (Backend)
- `POST /api/dmx`
  ```json
  { "channels": [ {"address":1,"value":255}, {"address":2,"value":128} ] }
  ```
- `POST /api/scene`
  ```json
  { "dmx": [0, 255, 100, ... bis 512 Einträge] }
  ```
- `GET /api/status` → Universe / Vorschau erster 24 Kanäle

## Hardware‑Setup (Kurz)
1. Interface via USB an Rechner.
2. DMX OUT → Dimmerpacks/LED‑Fixtures → Daisy‑Chain, Terminator am Ende.
3. Adressierung: FR50Z je **1 Kanal**, RGB‑LEDs je **3 Kanäle** (Startadresse beachten).
4. In der App DMX‑Startkanäle der Spots an dein Patch anpassen.

## Tests
- Backend trocken testen (ohne OLA): `curl localhost:8000/api/status`
- Mit OLA: `ola_dmxconsole` oder OLA Web UI (Universe 0) prüfen.
