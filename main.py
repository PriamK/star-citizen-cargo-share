import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
from datetime import datetime

HISTORY_FILE = "trade_history.json"

class CargoShareApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🚀 Star Citizen - Calculateur de Parts Cargo")
        self.root.geometry("900x980")
        # Couleurs thème Star Citizen
        self.bg_color = "#0a1628"
        self.fg_color = "#00d9ff"
        self.button_color = "#1a3a52"
        self.text_color = "#e0f7fa"
        self.panel_color = "#0f2138"
        self.root.configure(bg=self.bg_color)
        # Données
        self.personnes = {}  # nom -> montant investi (0 si équipier)
        self.percent_equipier = tk.IntVar(value=15)  # pourcentage pour non-investisseurs
        self.history = self.load_history()
        # Frame pour les personnes
        frame_personnes = tk.Frame(root, bg=self.panel_color, padx=20, pady=20, bd=1, relief=tk.GROOVE)
        frame_personnes.pack(fill=tk.X, padx=16, pady=(16, 10))
        title_label = tk.Label(frame_personnes, text="👨‍🚀 GESTION DES PERSONNES",
                               font=("Segoe UI", 14, "bold"), bg=self.panel_color, fg=self.fg_color)
        title_label.grid(row=0, column=0, columnspan=8, sticky="w", pady=(0, 10))
        tk.Label(frame_personnes, text="Nom:", bg=self.panel_color, fg=self.text_color, font=("Segoe UI", 10)).grid(row=1, column=0, sticky="w")
        self.nom_entry = tk.Entry(frame_personnes, width=24, font=("Segoe UI", 10))
        self.nom_entry.grid(row=1, column=1, padx=(6, 18), pady=4, sticky="w")
        tk.Label(frame_personnes, text="Montant investi (0 = équipier):",
                 bg=self.panel_color, fg=self.text_color, font=("Segoe UI", 10)).grid(row=1, column=2, sticky="w")
        self.montant_entry = tk.Entry(frame_personnes, width=18, font=("Segoe UI", 10))
        self.montant_entry.grid(row=1, column=3, padx=(6, 18), pady=4, sticky="w")
        btn_ajouter = tk.Button(frame_personnes, text="➕ Ajouter", command=self.ajouter_personne,
                                bg=self.button_color, fg=self.fg_color, font=("Segoe UI", 10, "bold"),
                                cursor="hand2", relief=tk.RAISED)
        btn_ajouter.grid(row=1, column=4, padx=(0, 8))
        # Bouton supprimer une personne + sélection déroulante
        tk.Label(frame_personnes, text="Supprimer:", bg=self.panel_color, fg=self.text_color, font=("Segoe UI", 10)).grid(row=2, column=0, sticky="w", pady=(10,0))
        self.combo_supprimer = ttk.Combobox(frame_personnes, state="readonly", width=22, values=[])
        self.combo_supprimer.grid(row=2, column=1, padx=(6, 18), pady=(10,0), sticky="w")
        btn_supprimer = tk.Button(frame_personnes, text="🗑️ Supprimer", command=self.supprimer_selection,
                                  bg="#742a2a", fg="#ffecec", font=("Segoe UI", 10, "bold"), cursor="hand2")
        btn_supprimer.grid(row=2, column=2, pady=(10,0), sticky="w")
        # Liste affichée
        self.liste_label = tk.Label(frame_personnes, text="", bg=self.panel_color, fg=self.text_color,
                                    font=("Consolas", 9), justify=tk.LEFT)
        self.liste_label.grid(row=3, column=0, columnspan=8, sticky="w", pady=(12,0))
        # Frame pour calcul et paramètres
        frame_calcul = tk.Frame(root, bg=self.panel_color, padx=20, pady=20, bd=1, relief=tk.GROOVE)
        frame_calcul.pack(fill=tk.X, padx=16, pady=10)
        calc_title = tk.Label(frame_calcul, text="💰 CALCUL DE RÉPARTITION",
                              font=("Segoe UI", 14, "bold"), bg=self.panel_color, fg=self.fg_color)
        calc_title.grid(row=0, column=0, columnspan=8, sticky="w", pady=(0, 10))
        tk.Label(frame_calcul, text="Coût total cargo (aUEC):",
                 bg=self.panel_color, fg=self.text_color, font=("Segoe UI", 10)).grid(row=1, column=0, sticky="w")
        self.cout_entry = tk.Entry(frame_calcul, width=18, font=("Segoe UI", 10))
        self.cout_entry.grid(row=1, column=1, padx=(6, 24), pady=4, sticky="w")
        self.cout_entry.bind('<keyrelease>', self.update_cout_total)
        tk.Label(frame_calcul, text="Revente totale (aUEC):",
                 bg=self.panel_color, fg=self.text_color, font=("Segoe UI", 10)).grid(row=1, column=2, sticky="w")
        self.revente_entry = tk.Entry(frame_calcul, width=18, font=("Segoe UI", 10))
        self.revente_entry.grid(row=1, column=3, padx=(6, 24), pady=4, sticky="w")
        # Curseur pour % équipier (5% à 30%)
        tk.Label(frame_calcul, text="% Équipiers (non-investisseurs):",
                 bg=self.panel_color, fg=self.text_color, font=("Segoe UI", 10, "bold")).grid(row=2, column=0, sticky="w", pady=(10, 0))
        self.scale_equipier = tk.Scale(frame_calcul, from_=5, to=30, orient=tk.HORIZONTAL, variable=self.percent_equipier,
                                       length=240, bg=self.panel_color, fg=self.text_color, troughcolor="#123456",
                                       highlightthickness=0, sliderrelief=tk.RAISED, command=self.on_percent_change)
        self.scale_equipier.grid(row=2, column=1, padx=(6, 24), pady=(10, 0), sticky="w")
        self.label_percent = tk.Label(frame_calcul, text="15%", bg=self.panel_color, fg=self.fg_color, font=("Segoe UI", 10, "bold"))
        self.label_percent.grid(row=2, column=2, sticky="w", pady=(10,0))
        btn_calculer = tk.Button(frame_calcul, text="🧮 Calculer les Parts",
                                 command=self.calculer_parts, bg=self.button_color,
                                 fg=self.fg_color, font=("Segoe UI", 10, "bold"),
                                 cursor="hand2", relief=tk.RAISED)
        btn_calculer.grid(row=3, column=0, columnspan=4, pady=12, sticky="w")
        # Frame pour résultats + historique
        container = tk.Frame(root, bg=self.bg_color)
        container.pack(fill=tk.BOTH, expand=True, padx=16, pady=(10, 16))
        frame_resultats = tk.Frame(container, bg=self.panel_color, padx=20, pady=12, bd=1, relief=tk.GROOVE)
        frame_resultats.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        result_title = tk.Label(frame_resultats, text="📊 RÉSULTATS",
                                font=("Segoe UI", 14, "bold"), bg=self.panel_color, fg=self.fg_color)
        result_title.pack(pady=(0,10), anchor="w")
        self.resultat_text = tk.Text(frame_resultats, height=22, width=68,
                                     font=("Consolas", 10), bg="#051020",
                                     fg=self.text_color, relief=tk.SUNKEN, bd=2)
        self.resultat_text.pack(fill=tk.BOTH, expand=True)
        # Historique
        frame_history = tk.Frame(container, bg=self.panel_color, padx=14, pady=12, bd=1, relief=tk.GROOVE)
        frame_history.pack(side=tk.RIGHT, fill=tk.Y)
        history_title = tk.Label(frame_history, text="🗂️ Historique (10 derniers)",
                                 font=("Segoe UI", 12, "bold"), bg=self.panel_color, fg=self.fg_color)
        history_title.pack(anchor="w")
        self.history_list = tk.Listbox(frame_history, height=28, width=48, bg="#0b1a2e", fg=self.text_color,
                                       font=("Consolas", 9))
        self.history_list.pack(fill=tk.BOTH, expand=True, pady=(6,0))
        self.refresh_history_listbox()
        # Ajuste colonnes
        for c in range(8):
            frame_personnes.grid_columnconfigure(c, weight=0)
            frame_calcul.grid_columnconfigure(c, weight=0)
        # Style ttk
        try:
            style = ttk.Style()
            try:
                style.theme_use('clam')
            except Exception:
                pass
            style.configure("TCombobox", fieldbackground="#0f2138", background="#0f2138", foreground="#e0f7fa")
        except Exception:
            pass
    def on_percent_change(self, value):
        try:
            v = int(float(value))
        except Exception:
            v = self.percent_equipier.get()
        self.label_percent.config(text=f"{v}%")
    def sync_combo(self):
        self.combo_supprimer["values"] = list(self.personnes.keys())
        if self.combo_supprimer.get() not in self.personnes:
            self.combo_supprimer.set("")
    def update_cout_total(self, event=None):
        """Calcule automatiquement le coût total basé sur les investissements"""
        total = sum(self.personnes.values())
        self.cout_entry.delete(0, tk.END)
        self.cout_entry.insert(0, str(int(total)))
    def ajouter_personne(self):
        nom = self.nom_entry.get().strip()
        try:
            montant = float(self.montant_entry.get().strip())
        except ValueError:
            messagebox.showerror("Erreur", "Le montant doit être un nombre valide.")
            return
        if not nom:
            messagebox.showerror("Erreur", "Le nom ne peut pas être vide.")
            return
        self.personnes[nom] = max(0.0, float(montant))
        self.nom_entry.delete(0, tk.END)
        self.montant_entry.delete(0, tk.END)
        self.update_liste_personnes()
        self.update_cout_total()
        self.sync_combo()
    def supprimer_selection(self):
        nom = self.combo_supprimer.get().strip()
        if not nom:
            messagebox.showinfo("Info", "Sélectionnez une personne à supprimer.")
            return
        if nom in self.personnes:
            del self.personnes[nom]
            self.update_liste_personnes()
            self.update_cout_total()
            self.sync_combo()
            messagebox.showinfo("Supprimé", f"{nom} a été supprimé de l'équipage.")
        else:
            messagebox.showwarning("Attention", "Personne introuvable.")
    def update_liste_personnes(self):
        if not self.personnes:
            self.liste_label.config(text="")
            return
        texte = "═══ ÉQUIPAGE ═══\n"
        for nom, montant in self.personnes.items():
            if montant > 0:
                texte += f"🚀 {nom}: {montant:,.0f} aUEC\n".replace(',', ' ')
            else:
                texte += f"👥 {nom}: Équipier\n"
        self.liste_label.config(text=texte)
    def save_history(self):
        try:
            with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print("Erreur sauvegarde historique:", e)
    def load_history(self):
        if not os.path.exists(HISTORY_FILE):
            return []
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []
    def refresh_history_listbox(self):
        self.history_list.delete(0, tk.END)
        for item in self.history[-10:][::-1]:  # derniers d'abord
            header = f"[{item['date']}] Benef: {item['benefice_total']:,} aUEC | Inv:{item['percent_investisseurs']}% Eq:{item['percent_equipiers']}%".replace(',', ' ')
            self.history_list.insert(tk.END, header)
            self.history_list.insert(tk.END, f"  Coût: {item['cout_total']:,} | Revente: {item['revente_totale']:,}".replace(',', ' '))
            self.history_list.insert(tk.END, "  Acteurs:")
            for nom, part in item['parts'].items():
                self.history_list.insert(tk.END, f"   - {nom}: {part:,} aUEC".replace(',', ' '))
            self.history_list.insert(tk.END, "")
    def calculer_parts(self):
        if not self.personnes:
            messagebox.showwarning("Attention", "Ajoutez au moins une personne.")
            return
        try:
            cout_total = float(self.cout_entry.get().strip())
            revente_totale = float(self.revente_entry.get().strip())
        except ValueError:
            messagebox.showerror("Erreur", "Les montants doivent être des nombres valides.")
            return
        if revente_totale <= cout_total:
            messagebox.showwarning("Attention", "La revente doit être supérieure au coût pour avoir un bénéfice.")
            return
        benefice_total = revente_totale - cout_total
        investisseurs = {nom: m for nom, m in self.personnes.items() if m > 0}
        non_investisseurs = [nom for nom, m in self.personnes.items() if m == 0]
        resultats = {}
        # Pourcentages dynamiques
        p_non = max(5, min(30, self.percent_equipier.get())) / 100.0
        p_inv = 1.0 - p_non
        if investisseurs:
            total_investi = sum(investisseurs.values())
            part_investisseurs = benefice_total * p_inv
            for nom, m in investisseurs.items():
                proportion = (m / total_investi) if total_investi > 0 else 0
                resultats[nom] = part_investisseurs * proportion
        if non_investisseurs:
            part_non = benefice_total * p_non
            par_tete = part_non / len(non_investisseurs)
            for nom in non_investisseurs:
                resultats[nom] = par_tete
        # Output résultats
        self.resultat_text.delete('1.0', tk.END)
        self.resultat_text.insert(tk.END, "════════════════════════════════════════════════════════════════════\n")
        self.resultat_text.insert(tk.END, f"BÉNÉFICE TOTAL: {benefice_total:,.2f} aUEC\n".replace(',', ' '))
        self.resultat_text.insert(tk.END, "════════════════════════════════════════════════════════════════════\n\n")
        if investisseurs:
            self.resultat_text.insert(tk.END, f"🚀 INVESTISSEURS ({int(p_inv*100)}%)\n")
            self.resultat_text.insert(tk.END, "────────────────────────────────────────────────────────────────────\n")
            for nom, m in investisseurs.items():
                part = resultats.get(nom, 0)
                self.resultat_text.insert(tk.END, f"  {nom}:\n")
                self.resultat_text.insert(tk.END, f"    - Investi: {m:,.2f} aUEC\n".replace(',', ' '))
                self.resultat_text.insert(tk.END, f"    - Part du bénéfice: {part:,.2f} aUEC\n".replace(',', ' '))
                self.resultat_text.insert(tk.END, f"    - TOTAL REÇU: {m + part:,.2f} a
