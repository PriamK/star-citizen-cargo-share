# 🚀 Build Instructions - Star Citizen Cargo Share

Guide complet pour créer un exécutable (.exe) de l'application.

## 📋 Prérequis

### Windows
- **Python 3.7+** installé ([Télécharger Python](https://www.python.org/downloads/))
  - ⚠️ Cocher "Add Python to PATH" lors de l'installation
- **pip** (inclus avec Python)

### Linux/macOS
- **Python 3.7+** (généralement pré-installé)
- **pip3**

## 🛠️ Méthode 1 : Build automatique (Recommandé)

### Windows

1. **Double-cliquez** sur `build.bat`

   OU ouvrez un terminal et exécutez :
   ```cmd
   build.bat
   ```

2. L'exécutable sera créé dans le dossier `dist/`
   ```
   dist/StarCitizenCargoShare.exe
   ```

### Linux/macOS

1. Ouvrez un terminal dans le dossier du projet

2. Exécutez le script de build :
   ```bash
   ./build.sh
   ```

3. L'exécutable sera créé dans le dossier `dist/`
   ```
   dist/StarCitizenCargoShare
   ```

## 🔧 Méthode 2 : Build manuel

### Étape 1 : Installer PyInstaller

```bash
pip install pyinstaller>=6.0.0
```

### Étape 2 : Générer l'exécutable

#### Option A : Utiliser le fichier .spec (Recommandé)
```bash
pyinstaller cargo-share.spec
```

#### Option B : Ligne de commande directe
```bash
pyinstaller --onefile --windowed --name StarCitizenCargoShare main.py
```

### Étape 3 : Récupérer l'exécutable

L'exécutable se trouve dans :
- **Windows** : `dist\StarCitizenCargoShare.exe`
- **Linux/macOS** : `dist/StarCitizenCargoShare`

## 📦 Structure après le build

```
star-citizen-cargo-share/
├── build/              # Fichiers temporaires (peut être supprimé)
├── dist/               # ⬢ EXÉCUTABLE ICI ⬢
│   └── StarCitizenCargoShare.exe
├── main.py
├── cargo-share.spec
├── build.bat
├── build.sh
└── ...
```

## 🎨 Personnalisation du build

### Ajouter une icône

1. Créez ou trouvez une icône `.ico` (Windows) ou `.icns` (macOS)

2. Modifiez `cargo-share.spec` :
   ```python
   icon='path/to/your/icon.ico'
   ```

3. Relancez le build

### Optimiser la taille

Dans `cargo-share.spec`, activez UPX :
```python
upx=True,
```

### Inclure des fichiers additionnels

Pour inclure des fichiers (images, config, etc.) :
```python
datas=[('fichier.txt', '.'), ('dossier/', 'dossier/')],
```

## ⚙️ Options PyInstaller

| Option | Description |
|--------|-------------|
| `--onefile` | Un seul fichier .exe (plus lent au démarrage) |
| `--windowed` | Pas de console (pour GUI) |
| `--console` | Affiche la console (pour debug) |
| `--name` | Nom de l'exécutable |
| `--icon` | Icône de l'application |
| `--add-data` | Ajouter des fichiers au build |

## 🐛 Dépannage

### Erreur : "Python not found"
- Vérifiez que Python est dans le PATH
- Réinstallez Python en cochant "Add to PATH"

### Erreur : "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### L'exécutable ne se lance pas
1. Testez avec `--console` pour voir les erreurs :
   ```bash
   pyinstaller --console --name StarCitizenCargoShare main.py
   ```

2. Vérifiez les antivirus (peuvent bloquer PyInstaller)

### Taille de l'exécutable trop grande
- Utilisez un environnement virtuel
- Activez UPX compression
- Utilisez `--onefile` avec prudence

## 📤 Distribution

### Fichiers à distribuer

**Version simple** :
- `StarCitizenCargoShare.exe` uniquement

**Version complète** :
- L'exécutable
- `README.md` (instructions pour l'utilisateur)
- `LICENSE` (si applicable)

### Créer un installateur (optionnel)

Utilisez **Inno Setup** (Windows) ou **NSIS** pour créer un installateur professionnel.

## 🚀 GitHub Release

Pour créer une release sur GitHub :

```bash
# Tag la version
git tag v1.0.0

# Push le tag
git push origin v1.0.0

# Sur GitHub : Create Release et uploadez l'exécutable
```

## ⬢ Support

En cas de problème :
1. Vérifiez les [Issues](https://github.com/PriamK/star-citizen-cargo-share/issues)
2. Créez une nouvelle issue avec :
   - OS et version Python
   - Message d'erreur complet
   - Commande utilisée

---

**See you in the 'verse, Commander!** 🌌
