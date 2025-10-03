import tkinter as tk
from tkinter import ttk, messagebox

DARK_BG = "#0B1220"      # very dark blue
PANEL_BG = "#0F1A2E"     # dark navy panel
ACCENT = "#00B3FF"       # cyan accent
TEXT = "#D7E3F8"         # light text
SUBTEXT = "#9BB5D1"
ERROR = "#FF5C5C"

class CargoShareApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Star Citizen - Calculateur de Parts Cargo")
        self.root.geometry("900x650")
        self.root.minsize(860, 560)

        # Data
        self.personnes = {}  # {nom: montant_investi}

        # Theming (ttk style + base backgrounds)
        self._setup_theme()

        # UI
        self.create_widgets()

    def _setup_theme(self):
        self.root.configure(bg=DARK_BG)
        style = ttk.Style()
        # Use default theme as base, then override
        try:
            style.theme_use('clam')
        except Exception:
            pass

        style.configure('TFrame', background=DARK_BG)
        style.configure('Panel.TFrame', background=PANEL_BG, relief='flat')
        style.configure('Title.TLabel', background=DARK_BG, foreground=TEXT, font=('Segoe UI', 14, 'bold'))
        style.configure('Sub.TLabel', background=DARK_BG, foreground=SUBTEXT, font=('Segoe UI', 10))
        style.configure('PanelTitle.TLabel', background=PANEL_BG, foreground=TEXT, font=('Segoe UI', 12, 'bold'))
        style.configure('TLabel', background=DARK_BG, foreground=TEXT, font=('Segoe UI', 10))
        style.configure('Accent.TButton', foreground=DARK_BG, background=ACCENT, font=('Segoe UI Semibold', 10))
        style.map('Accent.TButton',
                  background=[('active', '#23C7FF'), ('pressed', '#0AA6E6')],
                  relief=[('pressed', 'sunken')])
        style.configure('TButton', foreground=TEXT, background='#14233D', font=('Segoe UI', 10), padding=6)
        style.map('TButton', background=[('active', '#193055')])
        style.configure('TEntry', fieldbackground='#0E1A2F', foreground=TEXT, insertcolor=TEXT)
        style.map('TEntry', fieldbackground=[('focus', '#112342')])
        style.configure('Separator', background='#203450')

    def _panel(self, master):
        panel = ttk.Frame(master, style='Panel.TFrame', padding=(14, 12))
        return panel

    def create_widgets(self):
        main = ttk.Frame(self.root, padding=16)
        main.grid(row=0, column=0, sticky='nsew')
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        for i in range(3):
            main.columnconfigure(i, weight=1)
        main.rowconfigure(2, weight=1)

        # Header
        header = ttk.Frame(main)
        header.grid(row=0, column=0, columnspan=3, sticky='ew', pady=(0, 10))
        ttk.Label(header, text="🚀 Star Citizen - Calculateur de Parts Cargo", style='Title.TLabel').pack(side='left')
        ttk.Label(header, text="Répartition 85% investisseurs / 15% équipiers", style='Sub.TLabel').pack(side='right')

        # Panels
        left = self._panel(main)
        left.grid(row=1, column=0, sticky='nsew', padx=(0, 8), pady=(0, 10))

        mid = self._panel(main)
        mid.grid(row=1, column=1, sticky='nsew', padx=8, pady=(0, 10))

        right = self._panel(main)
        right.grid(row=1, column=2, rowspan=2, sticky='nsew', padx=(8, 0), pady=(0, 10))

        # Left: Participants
        ttk.Label(left, text="👨‍🚀 Gestion des Personnes", style='PanelTitle.TLabel').grid(row=0, column=0, columnspan=3, sticky='w')
        ttk.Label(left, text="Nom:").grid(row=1, column=0, sticky='w', pady=(8, 2))
        self.nom_entry = ttk.Entry(left, width=20)
        self.nom_entry.grid(row=1, column=1, sticky='ew', padx=6, pady=(8, 2))
        ttk.Label(left, text="Montant investi (aUEC):").grid(row=2, column=0, sticky='w')
        self.montant_entry = ttk.Entry(left, width=20)
        self.montant_entry.grid(row=2, column=1, sticky='ew', padx=6)
        add_btn = ttk.Button(left, text="Ajouter", style='Accent.TButton', command=self.ajouter_personne)
        add_btn.grid(row=1, column=2, rowspan=2, sticky='nsew', padx=(6, 0))

        ttk.Separator(left).grid(row=3, column=0, columnspan=3, sticky='ew', pady=10)
        ttk.Label(left, text="Participants (nom: investissement)", foreground=SUBTEXT).grid(row=4, column=0, columnspan=3, sticky='w')

        list_frame = ttk.Frame(left, style='Panel.TFrame')
        list_frame.grid(row=5, column=0, columnspan=3, sticky='nsew')
        self.liste_text = tk.Text(list_frame, height=10, width=40, bg='#0E1A2F', fg=TEXT, insertbackground=TEXT, relief='flat', bd=0)
        self.liste_text.pack(side='left', fill='both', expand=True)
        sb = ttk.Scrollbar(list_frame, command=self.liste_text.yview)
        sb.pack(side='right', fill='y')
        self.liste_text.configure(yscrollcommand=sb.set)

        del_btn = ttk.Button(left, text="Supprimer (nom dans le champ)", command=self.supprimer_personne)
        del_btn.grid(row=6, column=0, columnspan=3, sticky='ew', pady=(10, 0))

        for c in range(3):
            left.columnconfigure(c, weight=1)
        left.rowconfigure(5, weight=1)

        # Middle: Calcul
        ttk.Label(mid, text="💰 Calcul de Répartition", style='PanelTitle.TLabel').grid(row=0, column=0, columnspan=2, sticky='w')
        ttk.Label(mid, text="Coût total du cargo (aUEC):").grid(row=1, column=0, sticky='w', pady=(8, 2))
        self.cout_entry = ttk.Entry(mid)
        self.cout_entry.grid(row=1, column=1, sticky='ew', pady=(8, 2))
        ttk.Label(mid, text="Revente totale (aUEC):").grid(row=2, column=0, sticky='w')
        self.revente_entry = ttk.Entry(mid)
        self.revente_entry.grid(row=2, column=1, sticky='ew')
        calc_btn = ttk.Button(mid, text="Calculer les Parts", style='Accent.TButton', command=self.calculer_parts)
        calc_btn.grid(row=3, column=0, columnspan=2, sticky='ew', pady=(10, 0))

        tip = ttk.Label(mid, text="Rappel: 85% aux investisseurs proportionnellement, 15% aux non-investisseurs à parts égales.", foreground=SUBTEXT)
        tip.grid(row=4, column=0, columnspan=2, sticky='w', pady=(6, 0))

        mid.columnconfigure(1, weight=1)

        # Right: Résultats
        ttk.Label(right, text="📊 Résultats", style='PanelTitle.TLabel').grid(row=0, column=0, sticky='w')
        self.resultat_text = tk.Text(right, height=22, bg='#0E1A2F', fg=TEXT, insertbackground=TEXT, relief='flat', bd=0)
        self.resultat_text.grid(row=1, column=0, sticky='nsew', pady=(8, 0))
        rsb = ttk.Scrollbar(right, command=self.resultat_text.yview)
        rsb.grid(row=1, column=1, sticky='ns')
        self.resultat_text.configure(yscrollcommand=rsb.set)

        export_btn = ttk.Button(right, text="Copier le Résumé", command=self._copier_resume)
        export_btn.grid(row=2, column=0, columnspan=2, sticky='ew', pady=(10, 0))

        right.columnconfigure(0, weight=1)
        right.rowconfigure(1, weight=1)

    def _copier_resume(self):
        contenu = self.resultat_text.get('1.0', 'end').strip()
        if not contenu:
            messagebox.showinfo("Info", "Aucun résultat à copier.")
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(contenu)
        messagebox.showinfo("Copié", "Résumé copié dans le presse-papiers.")

    def ajouter_personne(self):
        nom = self.nom_entry.get().strip()
        montant_str = self.montant_entry.get().strip()
        if not nom:
            messagebox.showwarning("Attention", "Veuillez entrer un nom.")
            return
        try:
            montant = float(montant_str) if montant_str else 0.0
            if montant < 0:
                raise ValueError("Montant négatif")
        except ValueError:
            messagebox.showerror("Erreur", "Montant invalide. Utilisez un nombre positif.")
            return
        self.personnes[nom] = montant
        self.nom_entry.delete(0, tk.END)
        self.montant_entry.delete(0, tk.END)
        self.actualiser_liste()

    def supprimer_personne(self):
        nom = self.nom_entry.get().strip()
        if nom in self.personnes:
            del self.personnes[nom]
            self.nom_entry.delete(0, tk.END)
            self.actualiser_liste()
        else:
            messagebox.showwarning("Attention", "Personne non trouvée.")

    def actualiser_liste(self):
        self.liste_text.delete('1.0', tk.END)
        if not self.personnes:
            self.liste_text.insert(tk.END, "Aucun participant pour l'instant.\n")
        for nom, montant in self.personnes.items():
            self.liste_text.insert(tk.END, f"{nom}: {montant:.2f} aUEC\n")

    def calculer_parts(self):
        if not self.personnes:
            messagebox.showwarning("Attention", "Ajoutez au moins une personne.")
            return
        try:
            cout_total = float(self.cout_entry.get())
            revente_totale = float(self.revente_entry.get())
        except ValueError:
            messagebox.showerror("Erreur", "Entrez des valeurs valides pour le coût et la revente.")
            return
        if revente_totale < cout_total:
            messagebox.showwarning("Attention", "La revente doit être supérieure au coût pour avoir un bénéfice.")
        benefice_total = revente_totale - cout_total

        investisseurs = {nom: m for nom, m in self.personnes.items() if m > 0}
        non_investisseurs = [nom for nom, m in self.personnes.items() if m == 0]

        resultats = {}
        if investisseurs:
            total_investi = sum(investisseurs.values())
            part_investisseurs = benefice_total * 0.85
            for nom, m in investisseurs.items():
                proportion = (m / total_investi) if total_investi > 0 else 0
                resultats[nom] = part_investisseurs * proportion
        if non_investisseurs:
            part_non = benefice_total * 0.15
            par_tete = part_non / len(non_investisseurs)
            for nom in non_investisseurs:
                resultats[nom] = par_tete

        # Output
        self.resultat_text.delete('1.0', tk.END)
        self.resultat_text.insert(tk.END, "════════════════════════════════════════════════════════════════════\n")
        self.resultat_text.insert(tk.END, f"BÉNÉFICE TOTAL: {benefice_total:,.2f} aUEC\n".replace(',', ' '))
        self.resultat_text.insert(tk.END, "════════════════════════════════════════════════════════════════════\n\n")

        if investisseurs:
            self.resultat_text.insert(tk.END, "🚀 INVESTISSEURS (85%)\n")
            self.resultat_text.insert(tk.END, "────────────────────────────────────────────────────────────────────\n")
            for nom, m in investisseurs.items():
                part = resultats.get(nom, 0)
                self.resultat_text.insert(tk.END, f"  {nom}:\n")
                self.resultat_text.insert(tk.END, f"    - Investi: {m:,.2f} aUEC\n".replace(',', ' '))
                self.resultat_text.insert(tk.END, f"    - Part du bénéfice: {part:,.2f} aUEC\n".replace(',', ' '))
                self.resultat_text.insert(tk.END, f"    - TOTAL REÇU: {m + part:,.2f} aUEC\n\n".replace(',', ' '))
        if non_investisseurs:
            self.resultat_text.insert(tk.END, "👥 ÉQUIPIERS (15%)\n")
            self.resultat_text.insert(tk.END, "────────────────────────────────────────────────────────────────────\n")
            for nom in non_investisseurs:
                part = resultats.get(nom, 0)
                self.resultat_text.insert(tk.END, f"  {nom}: {part:,.2f} aUEC\n".replace(',', ' '))

        total_distribue = sum(resultats.values())
        self.resultat_text.insert(tk.END, "\n════════════════════════════════════════════════════════════════════\n")
        self.resultat_text.insert(tk.END, f"Total distribué: {total_distribue:,.2f} aUEC\n".replace(',', ' '))
        self.resultat_text.insert(tk.END, f"Vérification: {abs(total_distribue - benefice_total):,.2f} aUEC de différence\n".replace(',', ' '))


if __name__ == "__main__":
    root = tk.Tk()
    app = CargoShareApp(root)
    root.mainloop()
