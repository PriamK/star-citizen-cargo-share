# 🚀 Star Citizen - Calculateur de Parts Cargo

<div align="center">
  
![Star Citizen Logo](https://img.shields.io/badge/Star_Citizen-Cargo_Share-0d1117?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KICA8cGF0aCBkPSJNMTIgMkMyMC40MSAyIDIyIDMuNTkgMjIgMTJDMjIgMjAuNDEgMjAuNDEgMjIgMTIgMjJDMy41OSAyMiAyIDIwLjQxIDIgMTJDMiAzLjU5IDMuNTkgMiAxMiAyWiIgZmlsbD0iIzAwN0FGRiIvPgo8L3N2Zz4K&color=007AFF)
![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-orange?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**🌌 Interface graphique moderne inspirée du style Star Citizen 🌌**

*Calcul automatique et équitable de la répartition des bénéfices cargo en groupe*

</div>

---

## 📋 Description

**Star Citizen Cargo Share Calculator** est une application Windows dotée d'une interface graphique élégante et moderne, spécialement conçue pour les pilotes de Star Citizen effectuant du trading en groupe. 

### 🎯 Fonctionnalités principales :

- 🧮 **Calcul automatique** des parts de bénéfices selon les investissements
- 👥 **Gestion des équipages** : distinction investisseurs/non-investisseurs
- 💰 **Répartition équitable** : 85% pour les investisseurs, 15% pour les participants
- 🎨 **Interface moderne** inspirée de l'esthétique Star Citizen
- 📊 **Rapports détaillés** avec récapitulatif complet
- 🔄 **Calculs en temps réel** avec vérification automatique

### 🌟 Design & Style

L'application arbore un design **futuriste et immersif** :
- 🔹 **Palette bleu foncé** rappelant l'interface Star Citizen
- ⭐ **Éléments sci-fi** avec touches cyan et argent
- 🖥️ **Interface claire et intuitive** pour une utilisation rapide
- 🎮 **Esthétique gaming** adaptée à la communauté

---

## 🚀 Installation Windows

### 📋 Prérequis

1. **Python 3.7+** installé sur votre système
   ```bash
   # Vérifiez votre version Python
   python --version
   ```

2. **Modules requis** (inclus avec Python par défaut) :
   - `tkinter` (Interface graphique)
   - `math` (Calculs)

### 💾 Installation rapide

```bash
# 1. Clonez le repository
git clone https://github.com/PriamK/star-citizen-cargo-share.git

# 2. Accédez au dossier
cd star-citizen-cargo-share

# 3. Lancez l'application
python main.py
```

### 🔧 Installation alternative (zip)

1. Téléchargez le fichier ZIP depuis GitHub
2. Extrayez dans un dossier de votre choix
3. Double-cliquez sur `main.py` ou lancez via terminal

---

## 🎮 Utilisation de l'Interface

### 🖥️ Interface principale

L'application se présente sous forme d'une fenêtre moderne avec trois sections principales :

#### 🔷 Section 1 : Gestion des Participants
```
┌─────────────────────────────────────┐
│  👨‍🚀 GESTION DES PERSONNES        │
├─────────────────────────────────────┤
│  Nom: [____________]               │
│  Montant investi: [____________]   │
│  [ Ajouter Personne ]              │
└─────────────────────────────────────┘
```

#### 🔷 Section 2 : Paramètres du Run Cargo
```
┌─────────────────────────────────────┐
│  💰 CALCUL DE RÉPARTITION          │
├─────────────────────────────────────┤
│  Coût total: [____________] aUEC   │
│  Revente totale: [____________]    │
│  [ Calculer les Parts ]            │
└─────────────────────────────────────┘
```

#### 🔷 Section 3 : Résultats Détaillés
```
┌─────────────────────────────────────┐
│  📊 RÉSULTATS                      │
├─────────────────────────────────────┤
│  ════════════════════════════════   │
│  BÉNÉFICE TOTAL: 50,000 aUEC       │
│  ════════════════════════════════   │
│                                     │
│  🚀 INVESTISSEURS (85%)            │
│    - Alice: 30,000 aUEC reçus      │
│    - Bob: 25,500 aUEC reçus        │
│                                     │
│  👥 ÉQUIPIERS (15%)                │
│    - Charlie: 7,500 aUEC           │
└─────────────────────────────────────┘
```

### 📝 Exemple d'utilisation pratique

**Scénario :** Run cargo Quantanium à 4 joueurs

1. **Ajout des participants :**
   - Alice (Investisseur) : 100,000 aUEC
   - Bob (Investisseur) : 50,000 aUEC  
   - Charlie (Équipier) : 0 aUEC
   - David (Équipier) : 0 aUEC

2. **Saisie des montants :**
   - Coût total : 150,000 aUEC
   - Revente : 200,000 aUEC
   - Bénéfice : 50,000 aUEC

3. **Répartition automatique :**
   - Alice : 28,333 aUEC (85% × 2/3)
   - Bob : 14,167 aUEC (85% × 1/3)
   - Charlie : 3,750 aUEC (15% ÷ 2)
   - David : 3,750 aUEC (15% ÷ 2)

---

## 📦 Création d'un Exécutable

### 🛠️ Avec PyInstaller

Pour créer un fichier `.exe` portable :

```bash
# Installation de PyInstaller
pip install pyinstaller

# Création de l'exécutable
pyinstaller --onefile --windowed --name="StarCitizen-CargoShare" main.py

# L'exécutable sera dans le dossier dist/
```

### ⚙️ Options avancées

```bash
# Avec icône personnalisée et optimisations
pyinstaller --onefile --windowed \
            --name="StarCitizen-CargoShare" \
            --icon="icon.ico" \
            --add-data="assets;assets" \
            main.py
```

---

## 🔧 Fonctionnalités Avancées

### 💡 Algorithme de Répartition

- **85% pour les investisseurs** (proportionnel à l'investissement)
- **15% pour les non-investisseurs** (répartition équitable)
- **Vérification automatique** des totaux
- **Gestion des cas limites** (divisions par zéro, etc.)

### 🎨 Personnalisation Interface

L'interface peut être étendue avec :
- Thèmes de couleurs personnalisés
- Sauvegarde/chargement des configurations
- Historique des runs précédents
- Export des résultats (CSV, PDF)

---

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- 🐛 Signaler des bugs
- 💡 Proposer de nouvelles fonctionnalités
- 🎨 Améliorer l'interface utilisateur
- 📝 Corriger la documentation

---

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

---

<div align="center">
  
**🌌 Bon trading, pilotes ! 🌌**

*See you in the 'verse!*

[![Stars](https://img.shields.io/github/stars/PriamK/star-citizen-cargo-share?style=social)](https://github.com/PriamK/star-citizen-cargo-share/stargazers)
[![Forks](https://img.shields.io/github/forks/PriamK/star-citizen-cargo-share?style=social)](https://github.com/PriamK/star-citizen-cargo-share/network)

</div>
