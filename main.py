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
        self.root.title("⬢ STAR CITIZEN - CARGO SHARE CALCULATOR ⬢")
        self.root.geometry("1100x1000")

        # Star Citizen Color Palette - Enhanced
        self.bg_color = "#050a12"           # Deep space black
        self.fg_color = "#00e5ff"           # Cyan electric
        self.accent_color = "#ff9500"       # Orange accent
        self.button_color = "#0d1f2d"       # Dark blue-grey
        self.button_hover = "#1a3a52"       # Lighter on hover
        self.text_color = "#e8f4f8"         # Light cyan white
        self.panel_color = "#0a1420"        # Panel dark
        self.panel_border = "#00b8e6"       # Cyan border
        self.input_bg = "#0d1821"           # Input background
        self.input_border = "#1e3a5f"       # Input border
        self.success_color = "#00ff88"      # Success green
        self.error_color = "#ff3366"        # Error red

        self.root.configure(bg=self.bg_color)
        self.personnes = {}
        self.percent_collectif = tk.IntVar(value=25)
        self.history = self.load_history()

        # === HEADER BANNER ===
        header = tk.Frame(root, bg="#0a1928", height=70, bd=2, relief=tk.FLAT)
        header.pack(fill=tk.X, padx=0, pady=0)
        header.pack_propagate(False)

        # Header with glow effect simulation
        header_inner = tk.Frame(header, bg=self.panel_border, padx=2, pady=2)
        header_inner.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        header_content = tk.Frame(header_inner, bg="#0d1f2d")
        header_content.pack(fill=tk.BOTH, expand=True)

        title_main = tk.Label(header_content, text="⬢ CARGO SHARE CALCULATOR ⬢",
                              font=("Arial Black", 20, "bold"),
                              bg="#0d1f2d", fg=self.fg_color)
        title_main.pack(pady=(10, 0))

        subtitle = tk.Label(header_content, text="STAR CITIZEN • PROFIT DISTRIBUTION SYSTEM",
                           font=("Consolas", 9), bg="#0d1f2d", fg=self.accent_color)
        subtitle.pack(pady=(0, 8))

        # === FRAME PERSONNES ===
        frame_personnes_outer = tk.Frame(root, bg=self.panel_border, bd=0)
        frame_personnes_outer.pack(fill=tk.X, padx=16, pady=(16, 10))

        frame_personnes = tk.Frame(frame_personnes_outer, bg=self.panel_color, padx=24, pady=20)
        frame_personnes.pack(fill=tk.X, padx=2, pady=2)

        title_label = tk.Label(frame_personnes, text="⬢ CREW MANAGEMENT",
                              font=("Arial", 13, "bold"), bg=self.panel_color, fg=self.fg_color)
        title_label.grid(row=0, column=0, columnspan=8, sticky="w", pady=(0, 14))

        tk.Label(frame_personnes, text="NAME:", bg=self.panel_color, fg=self.accent_color,
                font=("Consolas", 9, "bold")).grid(row=1, column=0, sticky="w", padx=(0,8))
        self.nom_entry = tk.Entry(frame_personnes, width=22, font=("Consolas", 10),
                                 bg=self.input_bg, fg=self.text_color, insertbackground=self.fg_color,
                                 relief=tk.FLAT, bd=2, highlightthickness=1, highlightbackground=self.input_border,
                                 highlightcolor=self.panel_border)
        self.nom_entry.grid(row=1, column=1, padx=(0, 20), pady=6, sticky="w", ipady=4)

        tk.Label(frame_personnes, text="INVESTMENT (0 = crew):", bg=self.panel_color, fg=self.accent_color,
                font=("Consolas", 9, "bold")).grid(row=1, column=2, sticky="w")
        self.montant_entry = tk.Entry(frame_personnes, width=16, font=("Consolas", 10),
                                      bg=self.input_bg, fg=self.text_color, insertbackground=self.fg_color,
                                      relief=tk.FLAT, bd=2, highlightthickness=1, highlightbackground=self.input_border,
                                      highlightcolor=self.panel_border)
        self.montant_entry.grid(row=1, column=3, padx=(6, 20), pady=6, sticky="w", ipady=4)

        btn_ajouter = tk.Button(frame_personnes, text="▸ ADD MEMBER", command=self.ajouter_personne,
                               bg=self.button_color, fg=self.fg_color, font=("Arial", 9, "bold"),
                               cursor="hand2", relief=tk.FLAT, bd=0, padx=16, pady=8,
                               activebackground=self.button_hover, activeforeground="#ffffff")
        btn_ajouter.grid(row=1, column=4, padx=(0, 8))
        self._add_button_hover(btn_ajouter)

        tk.Label(frame_personnes, text="REMOVE:", bg=self.panel_color, fg=self.accent_color,
                font=("Consolas", 9, "bold")).grid(row=2, column=0, sticky="w", pady=(12,0), padx=(0,8))
        self.combo_supprimer = ttk.Combobox(frame_personnes, state="readonly", width=20, values=[],
                                           font=("Consolas", 9))
        self.combo_supprimer.grid(row=2, column=1, padx=(0, 20), pady=(12,0), sticky="w")

        btn_supprimer = tk.Button(frame_personnes, text="✖ DELETE", command=self.supprimer_selection,
                                 bg="#5a1515", fg="#ffaaaa", font=("Arial", 9, "bold"),
                                 cursor="hand2", relief=tk.FLAT, bd=0, padx=16, pady=6,
                                 activebackground="#8a2a2a", activeforeground="#ffffff")
        btn_supprimer.grid(row=2, column=2, pady=(12,0), sticky="w")
        self._add_button_hover(btn_supprimer, hover_bg="#8a2a2a")
        # Separator line
        sep_line = tk.Frame(frame_personnes, bg=self.panel_border, height=1)
        sep_line.grid(row=3, column=0, columnspan=8, sticky="ew", pady=(16, 12))

        self.liste_label = tk.Label(frame_personnes, text="", bg=self.panel_color, fg=self.text_color,
                                   font=("Consolas", 9), justify=tk.LEFT)
        self.liste_label.grid(row=4, column=0, columnspan=8, sticky="w", pady=(0,0))

        # === FRAME CALCUL ===
        frame_calcul_outer = tk.Frame(root, bg=self.panel_border, bd=0)
        frame_calcul_outer.pack(fill=tk.X, padx=16, pady=10)

        frame_calcul = tk.Frame(frame_calcul_outer, bg=self.panel_color, padx=24, pady=20)
        frame_calcul.pack(fill=tk.X, padx=2, pady=2)

        calc_title = tk.Label(frame_calcul, text="⬢ PROFIT CALCULATION",
                             font=("Arial", 13, "bold"), bg=self.panel_color, fg=self.fg_color)
        calc_title.grid(row=0, column=0, columnspan=8, sticky="w", pady=(0, 14))

        tk.Label(frame_calcul, text="TOTAL COST (aUEC):", bg=self.panel_color, fg=self.accent_color,
                font=("Consolas", 9, "bold")).grid(row=1, column=0, sticky="w", padx=(0,8))
        self.cout_entry = tk.Entry(frame_calcul, width=16, font=("Consolas", 10),
                                  bg=self.input_bg, fg=self.text_color, insertbackground=self.fg_color,
                                  relief=tk.FLAT, bd=2, highlightthickness=1, highlightbackground=self.input_border,
                                  highlightcolor=self.panel_border)
        self.cout_entry.grid(row=1, column=1, padx=(0, 24), pady=6, sticky="w", ipady=4)
        self.cout_entry.bind('<KeyRelease>', self.update_cout_total)

        tk.Label(frame_calcul, text="TOTAL REVENUE (aUEC):", bg=self.panel_color, fg=self.accent_color,
                font=("Consolas", 9, "bold")).grid(row=1, column=2, sticky="w")
        self.revente_entry = tk.Entry(frame_calcul, width=16, font=("Consolas", 10),
                                      bg=self.input_bg, fg=self.text_color, insertbackground=self.fg_color,
                                      relief=tk.FLAT, bd=2, highlightthickness=1, highlightbackground=self.input_border,
                                      highlightcolor=self.panel_border)
        self.revente_entry.grid(row=1, column=3, padx=(6, 24), pady=6, sticky="w", ipady=4)

        tk.Label(frame_calcul, text="COLLECTIVE SHARE % (α):", bg=self.panel_color, fg=self.accent_color,
                font=("Consolas", 9, "bold")).grid(row=2, column=0, sticky="w", pady=(14, 0), padx=(0,8))
        self.scale_collectif = tk.Scale(frame_calcul, from_=10, to=40, orient=tk.HORIZONTAL,
                                       variable=self.percent_collectif, length=220,
                                       bg=self.panel_color, fg=self.fg_color, troughcolor="#0d1821",
                                       highlightthickness=0, sliderrelief=tk.FLAT, command=self.on_percent_change,
                                       activebackground=self.panel_border, width=12)
        self.scale_collectif.grid(row=2, column=1, padx=(0, 24), pady=(14, 0), sticky="w")

        self.label_percent = tk.Label(frame_calcul, text="25%", bg=self.panel_color, fg=self.fg_color,
                                      font=("Arial", 11, "bold"))
        self.label_percent.grid(row=2, column=2, sticky="w", pady=(14,0))

        btn_calculer = tk.Button(frame_calcul, text="▸ CALCULATE SHARES",
                                 command=self.calculer_parts, bg=self.button_color,
                                 fg=self.success_color, font=("Arial", 10, "bold"),
                                 cursor="hand2", relief=tk.FLAT, bd=0, padx=20, pady=10,
                                 activebackground=self.button_hover, activeforeground="#ffffff")
        btn_calculer.grid(row=3, column=0, columnspan=4, pady=(16,0), sticky="w")
        self._add_button_hover(btn_calculer, hover_bg=self.button_hover)

        # === RESULTS AND HISTORY PANELS ===
        container = tk.PanedWindow(root, orient=tk.HORIZONTAL, sashrelief=tk.FLAT,
                                  bg=self.bg_color, sashwidth=8, bd=0)
        container.pack(fill=tk.BOTH, expand=True, padx=16, pady=(10, 16))

        # Results panel with border
        frame_resultats_outer = tk.Frame(container, bg=self.panel_border, bd=0)
        frame_resultats = tk.Frame(frame_resultats_outer, bg=self.panel_color, padx=20, pady=16)
        frame_resultats.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        # History panel with border
        frame_history_outer = tk.Frame(container, bg=self.panel_border, bd=0)
        frame_history = tk.Frame(frame_history_outer, bg=self.panel_color, padx=16, pady=16)
        frame_history.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        container.add(frame_resultats_outer, minsize=400, stretch="always")
        container.add(frame_history_outer, minsize=320, stretch="always")

        result_title = tk.Label(frame_resultats, text="⬢ RESULTS",
                               font=("Arial", 13, "bold"), bg=self.panel_color, fg=self.fg_color)
        result_title.pack(pady=(0,12), anchor="w")

        self.resultat_text = tk.Text(frame_resultats, height=22, width=68,
                                    font=("Consolas", 9), bg="#030810",
                                    fg=self.text_color, relief=tk.FLAT, bd=0,
                                    highlightthickness=1, highlightbackground=self.input_border,
                                    highlightcolor=self.panel_border, padx=12, pady=10,
                                    insertbackground=self.fg_color, selectbackground=self.button_hover)
        self.resultat_text.pack(fill=tk.BOTH, expand=True)

        history_title = tk.Label(frame_history, text="⬢ HISTORY (Last 10)",
                                 font=("Arial", 12, "bold"), bg=self.panel_color, fg=self.fg_color)
        history_title.pack(anchor="w", pady=(0,8))

        self.history_list = tk.Listbox(frame_history, height=28, width=60,
                                      bg="#030810", fg=self.text_color,
                                      font=("Consolas", 8), activestyle='none',
                                      relief=tk.FLAT, bd=0, highlightthickness=1,
                                      highlightbackground=self.input_border,
                                      highlightcolor=self.panel_border,
                                      selectbackground=self.button_color,
                                      selectforeground=self.fg_color)
        self.history_list.pack(fill=tk.BOTH, expand=True, pady=(0,0))
        self.refresh_history_listbox()
        for c in range(8):
            frame_personnes.grid_columnconfigure(c, weight=0)
            frame_calcul.grid_columnconfigure(c, weight=0)
        # Style configuration for ttk widgets
        try:
            style = ttk.Style()
            try:
                style.theme_use('clam')
            except Exception:
                pass
            style.configure("TCombobox",
                          fieldbackground=self.input_bg,
                          background=self.panel_color,
                          foreground=self.text_color,
                          arrowcolor=self.fg_color,
                          bordercolor=self.input_border,
                          lightcolor=self.panel_color,
                          darkcolor=self.panel_color)
            style.map('TCombobox',
                     fieldbackground=[('readonly', self.input_bg)],
                     selectbackground=[('readonly', self.input_bg)],
                     selectforeground=[('readonly', self.text_color)])
        except Exception:
            pass

    def _add_button_hover(self, button, hover_bg=None, normal_bg=None):
        """Add hover effect to a button"""
        if hover_bg is None:
            hover_bg = self.button_hover
        if normal_bg is None:
            normal_bg = button.cget('bg')

        def on_enter(e):
            button['background'] = hover_bg

        def on_leave(e):
            button['background'] = normal_bg

        button.bind('<Enter>', on_enter)
        button.bind('<Leave>', on_leave)

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
        texte = "╔═══ CURRENT CREW ═══╗\n"
        for nom, montant in self.personnes.items():
            if montant > 0:
                texte += f"║ ▸ {nom:<18} │ {montant:>12,.0f} aUEC\n".replace(',', ' ')
            else:
                texte += f"║ ▹ {nom:<18} │ CREW MEMBER\n"
        texte += "╚═══════════════════════════════════════╝"
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
        historique = self.history[-10:][::-1]
        for item in historique:
            self.history_list.insert(tk.END, "╔" + "═" * 58 + "╗")
            self.history_list.insert(tk.END, f"║ ⏱ {item['date']:<54} ║")
            self.history_list.insert(tk.END, "╠" + "═" * 58 + "╣")
            self.history_list.insert(tk.END, f"║ PROFIT  : {item['benefice_total']:>12,} aUEC{' '*27}║".replace(',', ' '))
            self.history_list.insert(tk.END, f"║ COST    : {item['cout_total']:>12,} aUEC{' '*27}║".replace(',', ' '))
            self.history_list.insert(tk.END, f"║ REVENUE : {item['revente_totale']:>12,} aUEC{' '*27}║".replace(',', ' '))
            self.history_list.insert(tk.END, f"║ Collective: {item.get('percent_collectif','')}% | Investment: {item.get('percent_investissement','')}%{' '*24}║")
            self.history_list.insert(tk.END, "╟" + "─" * 58 + "╢")
            for nom, part in item['parts'].items():
                invest = self.personnes.get(nom, 0)
                details = f"║ ▸ {nom:<10} │ +{part:>10,} aUEC".replace(',', ' ')
                if invest > 0:
                    total_net = int(part) + invest
                    details += f" │ Net:{total_net:>10,}".replace(',', ' ') + " ║"
                else:
                    details += " " * 23 + "║"
                self.history_list.insert(tk.END, details)
            self.history_list.insert(tk.END, "╚" + "═" * 58 + "╝")
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

        # Affichage des résultats - Star Citizen Style
        self.resultat_text.delete('1.0', tk.END)
        self.resultat_text.insert(tk.END, "╔" + "═" * 70 + "╗\n")
        self.resultat_text.insert(tk.END, "║" + " " * 18 + "⬢ PROFIT DISTRIBUTION REPORT ⬢" + " " * 22 + "║\n")
        self.resultat_text.insert(tk.END, "╠" + "═" * 70 + "╣\n")
        self.resultat_text.insert(tk.END, f"║ TOTAL PROFIT (T)       : {T:>15,.2f} aUEC" + " " * 21 + "║\n".replace(',', ' '))
        self.resultat_text.insert(tk.END, f"║ CREW MEMBERS (n)       : {n:>15}" + " " * 27 + "║\n")
        self.resultat_text.insert(tk.END, f"║ COLLECTIVE SHARE (α)   : {int(alpha*100):>15}%" + " " * 27 + "║\n")
        self.resultat_text.insert(tk.END, f"║ INVESTMENT SHARE       : {int((1-alpha)*100):>15}%" + " " * 27 + "║\n")
        self.resultat_text.insert(tk.END, "╚" + "═" * 70 + "╝\n\n")

        self.resultat_text.insert(tk.END, "┌─[ COLLECTIVE SHARE CALCULATION ]" + "─" * 37 + "┐\n")
        self.resultat_text.insert(tk.END, f"│ Formula: (α × T) / n = ({alpha:.2f} × {T:,.0f}) / {n}\n".replace(',', ' '))
        self.resultat_text.insert(tk.END, f"│ Per Member: {part_collective_par_personne:,.2f} aUEC\n".replace(',', ' '))
        self.resultat_text.insert(tk.END, "└" + "─" * 71 + "┘\n\n")

        if investisseurs:
            self.resultat_text.insert(tk.END, "┌─[ ⬢ INVESTORS ]" + "─" * 55 + "┐\n")
            self.resultat_text.insert(tk.END, f"│ Investment Pool: (1-α) × T = {part_investissement_totale:,.2f} aUEC\n\n".replace(',', ' '))

            for nom, montant in investisseurs.items():
                part_collective = part_collective_par_personne
                part_invest = resultats[nom] - part_collective
                proportion = (montant / somme_investie) * 100 if somme_investie > 0 else 0

                self.resultat_text.insert(tk.END, f"│ ▸ {nom.upper()} ({proportion:.1f}% stake)\n")
                self.resultat_text.insert(tk.END, f"│   ├─ Investment       : {montant:>14,.2f} aUEC\n".replace(',', ' '))
                self.resultat_text.insert(tk.END, f"│   ├─ Collective Share : {part_collective:>14,.2f} aUEC\n".replace(',', ' '))
                self.resultat_text.insert(tk.END, f"│   ├─ Investment Share : {part_invest:>14,.2f} aUEC\n".replace(',', ' '))
                self.resultat_text.insert(tk.END, f"│   ├─ PROFIT RECEIVED  : {resultats[nom]:>14,.2f} aUEC\n".replace(',', ' '))
                total_net = resultats[nom] + montant
                self.resultat_text.insert(tk.END, f"│   └─ TOTAL NET        : {total_net:>14,.2f} aUEC\n".replace(',', ' '))
                self.resultat_text.insert(tk.END, "│\n")

            self.resultat_text.insert(tk.END, "└" + "─" * 71 + "┘\n\n")

        if non_investisseurs:
            self.resultat_text.insert(tk.END, "┌─[ ⬢ CREW MEMBERS ]" + "─" * 52 + "┐\n")
            for nom in non_investisseurs:
                part_collective = part_collective_par_personne
                self.resultat_text.insert(tk.END, f"│ ▹ {nom.upper()}\n")
                self.resultat_text.insert(tk.END, f"│   └─ Collective Share : {part_collective:>14,.2f} aUEC\n".replace(',', ' '))
                self.resultat_text.insert(tk.END, "│\n")
            self.resultat_text.insert(tk.END, "└" + "─" * 71 + "┘\n")

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
