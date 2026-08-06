# Passwords2Bitwarden

Convert Nextcloud Passwords exports to Bitwarden / Vaultwarden JSON format.

## Requirements

- **Python 3.10+** (required for the primary, dependency-free workflow)
- **Docker or Podman** (optional, for a local containerized fallback)
- **Zero external dependencies** – the script relies solely on Python's standard library.

## How to Use

### 1. Export from Nextcloud Passwords

> ⚠️ Before exporting, switch your Nextcloud language to English: `Settings > Personal info > Language`. You can revert it afterward.

Go to `Passwords > More > Backup & Restore`, select `Backup or export`, and configure:
1. **Format**: `Predefined CSV`
2. **Options**: Check at least `Passwords` and `Folders`
3. **Run Export** → Download the ZIP archive

### 2. Convert to Bitwarden Format

#### 🔹 Primary Method: Single File (Zero Dependencies)
This fork is designed for maximum portability. No installation, no cloning, no external packages required.

1. Copy `main.py` directly into your working directory.
2. Run the script pointing to your exported ZIP:
   ```bash
   python main.py /path/to/nextcloud-export.zip
   ```
   Optionally specify an output directory:
   ```bash
   python main.py /path/to/nextcloud-export.zip ./output
   ```
3. The script extracts the ZIP locally, processes the CSVs, and generates `dump.json`.

💡 **Tip**: Use `python main.py --help` to see available options.

#### 🔸 Alternative: Docker / Podman (Local Build)
Prefer a containerized environment or don't have Python installed? You can run the script locally using Docker or Podman. No pre-built image is published; instead, you'll need the project files:

**Option A: Download as ZIP (Recommended)**
1. Click **Code → Download ZIP** on this repository.
2. Extract the archive and navigate to the folder.
3. Build and run locally:
   ```bash
   docker build -t p2b .
   docker run --rm -v ./<path-to-archive>/<archive-name>.zip:/app/archive.zip -v ./output:/app/output p2b
   ```

**Option B: Manual Copy**
If you only want the containerized workflow, copy just these three files into a new directory:
- `main.py`
- `Dockerfile`
- `.dockerignore`

Then run the same `docker build` and `docker run` commands as above. The converted file will be available in the `output` directory.

### 3. Import to Bitwarden / Vaultwarden

Go to your instance: `Tools > Import Data` → select `Bitwarden (json)` → upload `dump.json` → click `Import Data`.

## Why this fork?

The original project emphasizes Docker images and external dependencies. This fork prioritizes **portability and simplicity**:
- ✅ Single, self-contained Python file (`main.py`) for instant usage
- ✅ Zero external dependencies (standard library only)
- ✅ Local Docker/Podman fallback without published images
- ✅ Optimized for quick copy-paste or ZIP extraction workflows

This fork was created with the original author's approval following a PR discussion ([#12](https://github.com/facorazza/Passwords2Bitwarden/pull/12#issuecomment-5197595169)). Although I typically aim to keep projects unified to avoid fragmentation, this approach enables a more practical, zero-dependency workflow while fully respecting the original work.

## Code of Conduct

Please note that this project is released with a [Contributor Code of Conduct](CODE-OF-CONDUCT.md).
By participating in this project you agree to abide by its terms.

## Sponsoring

If you find this project useful, please consider giving it a **star ⭐ on GitHub** to show your support!

If you'd like to go a step further, you can also **buy me a coffee** ☕ via [Buy Me a Coffee](https://www.buymeacoffee.com/m1ck431). Your support helps me keep building great open-source projects like this one. Thank you! 🙏

<a href="https://www.buymeacoffee.com/m1ck431" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>
