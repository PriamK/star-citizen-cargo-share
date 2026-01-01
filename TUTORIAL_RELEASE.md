# 🎯 TUTORIEL : Créer une Release Automatique

## ⚡ VERSION ULTRA-RAPIDE (3 commandes)

Vous êtes sur la branche `claude/star-citizen-design-Vnq78`. Voici exactement quoi faire :

```bash
# 1️⃣ Créer le tag de version
git tag v1.0.0

# 2️⃣ Pousser le tag vers GitHub
git push origin v1.0.0

# 3️⃣ C'est tout ! ✨ Attendez 5-10 minutes
```

**Résultat** : GitHub Actions va automatiquement créer les .exe et publier la release !

---

## 📺 SUIVRE LE PROCESSUS EN DIRECT

### Étape 1 : Après avoir poussé le tag

Allez sur votre repository GitHub :
```
https://github.com/PriamK/star-citizen-cargo-share
```

### Étape 2 : Voir le workflow en action

1. Cliquez sur l'onglet **"Actions"** (en haut)
   ```
   https://github.com/PriamK/star-citizen-cargo-share/actions
   ```

2. Vous verrez apparaître : **"🚀 Build and Release"**

3. Cliquez dessus pour voir :
   - ✅ Build Windows (en cours...)
   - ✅ Build Linux (en cours...)
   - ✅ Build macOS (en cours...)
   - ✅ Create Release (après les builds)

### Étape 3 : Récupérer la release (après 5-10 min)

1. Allez sur l'onglet **"Releases"** (à droite sur GitHub)
   ```
   https://github.com/PriamK/star-citizen-cargo-share/releases
   ```

2. Vous verrez votre release **"Star Citizen Cargo Share v1.0.0"**

3. Téléchargez les fichiers :
   - `StarCitizenCargoShare-Windows.exe` ← pour Windows
   - `StarCitizenCargoShare-Linux` ← pour Linux
   - `StarCitizenCargoShare-macOS` ← pour macOS

---

## 🎬 GUIDE VISUEL PAS À PAS

### Option A : Depuis votre terminal (RECOMMANDÉ)

```bash
┌─────────────────────────────────────────────────┐
│  VOUS ÊTES ICI                                  │
│  Branche: claude/star-citizen-design-Vnq78      │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│  COMMANDE 1 : Créer le tag                      │
│  $ git tag v1.0.0                               │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│  COMMANDE 2 : Pousser le tag                    │
│  $ git push origin v1.0.0                       │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│  GITHUB ACTIONS SE DÉCLENCHE AUTOMATIQUEMENT    │
│  ⚙️  Building Windows.exe...                    │
│  ⚙️  Building Linux...                          │
│  ⚙️  Building macOS...                          │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│  RELEASE CRÉÉE AUTOMATIQUEMENT ! 🎉             │
│  📦 Tous les .exe sont uploadés                 │
└─────────────────────────────────────────────────┘
```

### Option B : Via l'interface GitHub (si vous préférez)

1. **Créer le tag sur GitHub** :
   - Allez sur : `https://github.com/PriamK/star-citizen-cargo-share/releases`
   - Cliquez sur **"Draft a new release"**
   - Dans **"Choose a tag"**, tapez : `v1.0.0` et cliquez "Create new tag"
   - Titre : `Star Citizen Cargo Share v1.0.0`
   - Cliquez **"Publish release"**

2. Le workflow se déclenchera automatiquement et ajoutera les .exe !

---

## 🔍 VÉRIFICATION : Le workflow fonctionne ?

Après avoir poussé le tag, vérifiez :

```bash
# Voir tous vos tags
git tag

# Voir les tags sur GitHub
git ls-remote --tags origin
```

Vous devriez voir `v1.0.0` dans les deux listes.

---

## 🆘 DÉPANNAGE EXPRESS

### Problème : "Le workflow ne démarre pas"

**Solution** : Vérifiez le format du tag
```bash
# ✅ BON (avec le 'v')
git tag v1.0.0

# ❌ MAUVAIS (sans le 'v')
git tag 1.0.0
```

### Problème : "Je veux refaire la release"

**Solution** : Supprimez et recréez le tag
```bash
# Supprimer localement
git tag -d v1.0.0

# Supprimer sur GitHub
git push origin :refs/tags/v1.0.0

# Recréer
git tag v1.0.0
git push origin v1.0.0
```

---

## 📊 APRÈS LA PREMIÈRE RELEASE

Pour les prochaines versions :

```bash
# Corriger un bug → v1.0.1
git tag v1.0.1
git push origin v1.0.1

# Nouvelle fonctionnalité → v1.1.0
git tag v1.1.0
git push origin v1.1.0

# Changement majeur → v2.0.0
git tag v2.0.0
git push origin v2.0.0
```

---

## ✅ CHECKLIST AVANT DE LANCER

- [ ] Tout est committé et pushé sur la branche
- [ ] Vous avez choisi un numéro de version (ex: v1.0.0)
- [ ] Vous êtes connecté à GitHub
- [ ] Prêt à attendre 5-10 minutes

---

## 🚀 COMMANDES À COPIER-COLLER

**Pour créer votre première release MAINTENANT** :

```bash
# Tout en une seule fois :
git tag v1.0.0 && git push origin v1.0.0

# Puis allez voir sur GitHub :
# https://github.com/PriamK/star-citizen-cargo-share/actions
```

**C'est aussi simple que ça !** 🎉

---

## 📱 LIENS UTILES

| Quoi | Lien |
|------|------|
| Voir les workflows | https://github.com/PriamK/star-citizen-cargo-share/actions |
| Voir les releases | https://github.com/PriamK/star-citizen-cargo-share/releases |
| Voir les tags | https://github.com/PriamK/star-citizen-cargo-share/tags |

---

**⬢ Prêt ? Lancez les commandes ci-dessus et observez la magie opérer ! 🚀**
