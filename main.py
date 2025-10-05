import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
from datetime import datetime

HISTORY_FILE = os.path.join(os.path.dirname(__file__), "trade_history.json")

if not os.path.exists(HISTORY_FILE):
    try:
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            f.write("[]")
    except Exception as e:
        print("Erreur de création du fichier d'historique :", e)

class CargoShareApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🚀 Star Citizen - Calculateur de Parts Cargo")
        self.root.geometry("900x980")
        self.bg_color = "#0a1628"
        self.fg_color = "#00d9ff"
        self.button_color = "#1a3a52"
        self.text_color = "#e0f7fa"
        self.panel_color = "#0f2138"
        self.root.configure(bg=self.bg_color)
        self.personnes = {}
        self.percent_collectif = tk.IntVar(value=25)
        self.history = self.load_history()

        frame_personnes = tk.Frame(root, bg=self.panel_color, padx=20, pady=20, bd=1, relief=tk.GROOVE)
        frame_personnes.pack(fill=tk.X, padx=16, pady=(16, 10))
        title_label = tk.Label(frame_personnes, text="👨‍🚀 GESTION DES PERSONNES",
                              font=("Segoe UI", 14, "bold"), bg=self.panel_color, fg=self.fg_color)
        title_label.grid(row=0, column=0, columnspan=8, sticky="w", pady=(0, 10))
        tk.Label(frame_personnes, text="Nom:", bg=self.panel_color, fg=self.text_color, font=("Segoe UI", 10)).grid(row=1, column=0, sticky="w")
        self.nom_entry = tk.Entry(frame_personnes, width=24, font=("Segoe UI", 10))
        self.nom_entry.grid(row=1, column=1, padx=(6, 18), pady=4, sticky="w")
        tk.Label(frame_personnes, text="Montant investi (0 = équipier):", bg=self.panel_color, fg=self.text_color, font=("Segoe UI", 10)).grid(row=1, column=2, sticky="w")
        self.montant_entry = tk.Entry(frame_personnes, width=18, font=("Segoe UI", 10))
        self.montant_entry.grid(row=1, column=3, padx=(6, 18), pady=4, sticky="w")
        btn_ajouter = tk.Button(frame_personnes, text="➕ Ajouter", command=self.ajouter_personne,
                               bg=self.button_color, fg=self.fg_color, font=("Segoe UI", 10, "bold"),
                               cursor="hand2", relief=tk.RAISED)
        btn_ajouter.grid(row=1, column=4, padx=(0, 8))
        tk.Label(frame_personnes, text="Supprimer:", bg=self.panel_color, fg=self.text_color, font=("Segoe UI", 10)).grid(row=2, column=0, sticky="w", pady=(10,0))
        self.combo_supprimer = ttk.Combobox(frame_personnes, state="readonly", width=22, values=[])
        self.combo_supprimer.grid(row=2, column=1, padx=(6, 18), pady=(10,0), sticky="w")
        btn_supprimer = tk.Button(frame_personnes, text="🗑️ Supprimer", command=self.supprimer_selection,
                                 bg="#742a2a", fg="#ffecec", font=("Segoe UI", 10, "bold"), cursor="hand2")
        btn_supprimer.grid(row=2, column=2, pady=(10,0), sticky="w")
        self.liste_label = tk.Label(frame_personnes, text="", bg=self.panel_color, fg=self.text_color,
                                   font=("Consolas", 9), justify=tk.LEFT)
        self.liste_label.grid(row=3, column=0, columnspan=8, sticky="w", pady=(12,0))

        frame_calcul = tk.Frame(root, bg=self.panel_color, padx=20, pady=20, bd=1, relief=tk.GROOVE)
        frame_calcul.pack(fill=tk.X, padx=16, pady=10)
        calc_title = tk.Label(frame_calcul, text="💰 CALCUL DE RÉPARTITION",
                             font=("Segoe UI", 14, "bold"), bg=self.panel_color, fg=self.fg_color)
        calc_title.grid(row=0, column=0, columnspan=8, sticky="w", pady=(0, 10))
        tk.Label(frame_calcul, text="Coût total cargo (aUEC):", bg=self.panel_color, fg=self.text_color, font=("Segoe UI", 10)).grid(row=1, column=0, sticky="w")
        self.cout_entry = tk.Entry(frame_calcul, width=18, font=("Segoe UI", 10))
        self.cout_entry.grid(row=1, column=1, padx=(6, 24), pady=4, sticky="w")
        self.cout_entry.bind('<KeyRelease>', self.update_cout_total)
        tk.Label(frame_calcul, text="Revente totale (aUEC):", bg=self.panel_color, fg=self.text_color, font=("Segoe UI", 10)).grid(row=1, column=2, sticky="w")
        self.revente_entry = tk.Entry(frame_calcul, width=18, font=("Segoe UI", 10))
        self.revente_entry.grid(row=1, column=3, padx=(6, 24), pady=4, sticky="w")
        tk.Label(frame_calcul, text="% Part collective (α):", bg=self.panel_color, fg=self.text_color, font=("Segoe UI", 10, "bold")).grid(row=2, column=0, sticky="w", pady=(10, 0))
        self.scale_collectif = tk.Scale(frame_calcul, from_=10, to=40, orient=tk.HORIZONTAL, variable=self.percent_collectif,
                                       length=240, bg=self.panel_color, fg=self.text_color, troughcolor="#123456",
                                       highlightthickness=0, sliderrelief=tk.RAISED, command=self.on_percent_change)
        self.scale_collectif.grid(row=2, column=1, padx=(6, 24), pady=(10, 0), sticky="w")
        self.label_percent = tk.Label(frame_calcul, text="25%", bg=self.panel_color, fg=self.fg_color, font=("Segoe UI", 10, "bold"))
        self.label_percent.grid(row=2, column=2, sticky="w", pady=(10,0))
        btn_calculer = tk.Button(frame_calcul, text="🧮 Calculer les Parts",
                                 command=self.calculer_parts, bg=self.button_color,
                                 fg=self.fg_color, font=("Segoe UI", 10, "bold"),
                                 cursor="hand2", relief=tk.RAISED)
        btn_calculer.grid(row=3, column=0, columnspan=4, pady=12, sticky="w")

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
        frame_history = tk.Frame(container, bg=self.panel_color, padx=14, pady=12, bd=1, relief=tk.GROOVE)
        frame_history.pack(side=tk.RIGHT, fill=tk.Y)
        history_title = tk.Label(frame_history, text="🗂️ Historique (10 derniers)",
                                 font=("Segoe UI", 12, "bold"), bg=self.panel_color, fg=self.fg_color)
        history_title.pack(anchor="w")
        self.history_list = tk.Listbox(frame_history, height=28, width=48, bg="#0b1a2e", fg=self.text_color,
                                      font=("Consolas", 9))
        self.history_list.pack(fill=tk.BOTH, expand=True, pady=(6,0))
        self.refresh_history_listbox()
        for c in range(8):
            frame_personnes.grid_columnconfigure(c, weight=0)
            frame_calcul.grid_columnconfigure(c, weight=0)
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
            v = self.percent_collectif.get()
        self.label_percent.config(text=f"{v}%")

    def sync_combo(self):
        self.combo_supprimer["values"] = list(self.personnes.keys())
        if self.combo_supprimer.get() not in self.personnes:
            self.combo_supprimer.set("")

    def update_cout_total(self, event=None):
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
        for item in self.history[-10:][::-1]:
            header = f"[{item['date']}] Benef: {item['benefice_total']:,} aUEC | Collectif:{item['percent_collectif']}% Invest:{item['percent_investissement']}%".replace(',', ' ')
            self.history_list.insert(tk.END, header)
            self.history_list.insert(tk.END, f" Coût: {item['cout_total']:,} | Revente: {item['revente_totale']:,}".replace(',', ' '))
            self.history_list.insert(tk.END, " Acteurs:")
            for nom, part in item['parts'].items():
                self.history_list.insert(tk.END, f" - {nom}: {part:,} aUEC".replace(',', ' '))
            self.history_list.insert(tk.END, "")

    def calculer_parts(self):
        """
        Formule mathématique parfaite :
        - Part collective (α%) : (α × T) / n
        - Part investissement ((1-α)%) : ((1-α) × T) × (investissement_individuel / somme_investie)
        - Total = Part collective + Part investissement
        """
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
        # Variables de base
        T = revente_totale - cout_total  # Bénéfice total
        n = len(self.personnes)  # Nombre total de membres
        alpha = max(10, min(40, self.percent_collectif.get())) / 100.0  # α en décimal
        
        investisseurs = {nom: m for nom, m in self.personnes.items() if m > 0}
        non_investisseurs = [nom for nom, m in self.personnes.items() if m == 0]
        somme_investie = sum(investisseurs.values())
        
        resultats = {}
        
        # Calcul part collective : (α × T) / n
        part_collective_par_personne = (alpha * T) / n
        
        # Calcul part investissement : (1-α) × T
        part_investissement_totale = (1 - alpha) * T
        
        # Attribution des parts
        for nom in self.personnes.keys():
            # Tout le monde reçoit la part collective
            resultats[nom] = part_collective_par_personne
            
            # Les investisseurs reçoivent en plus leur part proportionnelle
            if nom in investisseurs and somme_investie > 0:
                proportion = investisseurs[nom] / somme_investie
                resultats[nom] += part_investissement_totale * proportion
        
        # Vérification : somme = bénéfice total (normalisation si nécessaire)
        somme_parts = sum(resultats.values())
        if abs(somme_parts - T) > 1:
            ratio = T / somme_parts
            for k in resultats:
                resultats[k] *= ratio
        
        # Affichage des résultats
        self.resultat_text.delete('1.0', tk.END)
        self.resultat_text.insert(tk.END, "════════════════════════════════════════════════════════════════════\n")
        self.resultat_text.insert(tk.END, f"BÉNÉFICE TOTAL (T): {T:,.2f} aUEC\n".replace(',', ' '))
        self.resultat_text.insert(tk.END, f"MEMBRES (n): {n} | PART COLLECTIVE (α): {int(alpha*100)}%\n")
        self.resultat_text.insert(tk.END, "════════════════════════════════════════════════════════════════════\n\n")
        
        self.resultat_text.insert(tk.END, f"🏆 PART COLLECTIVE ({int(alpha*100)}%)\n")
        self.resultat_text.insert(tk.END, "────────────────────────────────────────────────────────────────────\n")
        self.resultat_text.insert(tk.END, f"Formule : (α × T) / n = ({alpha:.2f} × {T:,.0f}) / {n}\n".replace(',', ' '))
        self.resultat_text.insert(tk.END, f"Part par personne : {part_collective_par_personne:,.2f} aUEC\n\n".replace(',', ' '))
        
        if investisseurs:
            self.resultat_text.insert(tk.END, f"🚀 PART INVESTISSEMENT ({int((1-alpha)*100)}%)\n")
            self.resultat_text.insert(tk.END, "────────────────────────────────────────────────────────────────────\n")
            self.resultat_text.insert(tk.END, f"Formule : (1-α) × T = {1-alpha:.2f} × {T:,.0f} = {part_investissement_totale:,.2f} aUEC\n\n".replace(',', ' '))
            
            for nom, montant in investisseurs.items():
                part_collective = part_collective_par_personne
                part_invest = resultats[nom] - part_collective
                proportion = (montant / somme_investie) * 100 if somme_investie > 0 else 0
                
                self.resultat_text.insert(tk.END, f" {nom} (investissement : {proportion:.1f}%) :\n")
                self.resultat_text.insert(tk.END, f" - Investi : {montant:,.2f} aUEC\n".replace(',', ' '))
                self.resultat_text.insert(tk.END, f" - Part collective : {part_collective:,.2f} aUEC\n".replace(',', ' '))
                self.resultat_text.insert(tk.END, f" - Part investissement : {part_invest:,.2f} aUEC\n".replace(',', ' '))
                self.resultat_text.insert(tk.END, f" - TOTAL REÇU : {resultats[nom]:,.2f} aUEC\n\n".replace(',', ' '))
        
        if non_investisseurs:
            self.resultat_text.insert(tk.END, f"👥 ÉQUIPIERS\n")
            self.resultat_text.insert(tk.END, "────────────────────────────────────────────────────────────────────\n")
            for nom in non_investisseurs:
                part_collective = part_collective_par_personne
                self.resultat_text.insert(tk.END, f" {nom} :\n")
                self.resultat_text.insert(tk.END, f" - Part collective : {part_collective:,.2f} aUEC\n".replace(',', ' '))
                self.resultat_text.insert(tk.END, f" - TOTAL REÇU : {resultats[nom]:,.2f} aUEC\n\n".replace(',', ' '))
        
        # Sauvegarde dans l'historique
        record = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "benefice_total": int(T),
            "cout_total": int(cout_total),
            "revente_totale": int(revente_totale),
            "percent_collectif": int(alpha * 100),
            "percent_investissement": int((1-alpha) * 100),
            "parts": {nom: int(part) for nom, part in resultats.items()}
        }
        self.history.append(record)
        self.save_history()
        self.refresh_history_listbox()

if __name__ == "__main__":
    root = tk.Tk()
    app = CargoShareApp(root)
    root.mainloop()
