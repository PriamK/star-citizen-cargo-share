# 🚀 Star Citizen - Calculateur de Parts Cargo

<div align="center">
  
![Star Citizen Logo](https://img.shields.io/badge/Star_Citizen-Cargo_Share-0d1117?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KICA8cGF0aCBkPSJNMTIgMkMyMC40MSAyIDIyIDMuNTkgMjIgMTJDMjIgMjAuNDEgMjAuNDEgMjIgMTIgMjJDMy41OSAyMiAyIDIwLjQxIDIgMTJDMiAzLjU5IDMuNTkgMiAxMiAyWiIgZmlsbD0iIzAwN0FGRiIvPgo8L3N2Zz4K&color=007AFF)
![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-orange?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

🌌 Interface graphique moderne inspirée du style Star Citizen 🌌

*Calcul automatique et équitable de la répartition des bénéfices lors des runs cargo en groupe sur Star Citizen.*

## 📋 Description

Star Citizen Cargo Share est une application Windows avec interface graphique élégante qui calcule automatiquement la répartition des bénéfices entre investisseurs et équipiers lors de la vente de cargo en équipe.

### 🎯 Nouveau système de calcul :
- Part collective : Un pourcentage du bénéfice (ex : 25%) partagé équitablement entre tous les membres.
- Part investissement : Les % restants sont répartis selon la proportion investie par chaque participant.
*Exemple : Pour chaque run, tous les joueurs reçoivent un bonus de base, puis ceux qui investissent bénéficient d'un bonus proportionnel à leur mise.*

## 🛠️ Fonctionnalités principales
- 🧮 Répartition ultra-fair : part collective + part proportionnelle (configurable en quelques clics)
- 👥 Gestion avancée d'équipage : distinction automatique investisseurs / équipiers
- 📊 Affichage ultra détaillé : bénéfice, parts, investissement et total net affichés pour chaque membre
- 🔄 Résultats interactifs en temps réel : redimensionnement des panels, historique détaillé sur 10 runs
- 🎨 Interface moderne Star Citizen touch : styles, couleurs, ergonomie, responsive

## 🚀 Installation et lancement

### Prérequis
1. Python 3.7+ requis sur votre PC

### Installation rapide
1. Clonez le repository
   git clone https://github.com/PriamK/star-citizen-cargo-share.git
2. Accédez au dossier
   cd star-citizen-cargo-share
3. Lancez l'application
   python main.py

## 🎮 Utilisation

1. Ajoutez les membres et leur mise
2. Indiquez le coût et la revente
3. Réglez le % de bonus collectif (α)
4. Cliquez sur 'Calculer les Parts' et voyez le récap détaillé
5. Glissez la barre centrale pour ajuster l'affichage historique/résultat !

## 💡 Algorithme de calcul

Formule mathématique :

Part collective = (α × Bénéfice) / n
Part investissement = ((1-α) × Bénéfice) × (investissement individuel / somme des investissements)
Total reçu = Part collective + Part investissement

Où :
- α = pourcentage de la part collective (configurable de 10% à 40%)
- n = nombre total de membres dans l'équipe

## 📝 Exemple pratique

Scénario Quantanium à 4 joueurs :
- Alice investit 100,000 aUEC, Bob investit 50,000 aUEC
- Charlie et David sont équipiers (0 aUEC)
- Coût total : 150,000 aUEC, Revente : 200,000 aUEC
- Bénéfice : 50,000 aUEC
- α = 25% (part collective)

Répartition :
- Part collective : 12,500 aUEC pour chacun
- Alice : 12,500 + 25,000 = 37,500 aUEC
- Bob : 12,500 + 12,500 = 25,000 aUEC
- Charlie : 12,500 aUEC
- David : 12,500 aUEC

## 🔧 Fonctionnalités avancées
- Historique détaillé : Suivi des 10 derniers runs avec détails complets
- Interface redimensionnable : Ajustez les panels selon vos besoins
- Calculs en temps réel : Vérification automatique et normalisation
- Export possible : Sauvegarde des données en JSON

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- 🐛 Signaler des bugs
- 💡 Proposer de nouvelles fonctionnalités
- 🎨 Améliorer l'interface utilisateur
- 📝 Corriger la documentation

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

**✨ Bon trading et bon loot, commandants ! ✨**

*See you in the 'verse!*

[![Stars](https://img.shields.io/github/stars/PriamK/star-citizen-cargo-share?style=social)](https://github.com/PriamK/star-citizen-cargo-share/stargazers)
[![Forks](https://img.shields.io/github/forks/PriamK/star-citizen-cargo-share?style=social)](https://github.com/PriamK/star-citizen-cargo-share/network)

</div>
