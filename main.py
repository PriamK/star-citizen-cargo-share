import tkinter as tk
from tkinter import messagebox

class CargoShareApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🚀 Star Citizen - Calculateur de Parts Cargo")
        self.root.geometry("700x800")
        
        # Couleurs thème Star Citizen
        self.bg_color = "#0a1628"
        self.fg_color = "#00d9ff"
        self.button_color = "#1a3a52"
        self.text_color = "#e0f7fa"
        
        self.root.configure(bg=self.bg_color)
        
        self.personnes = {}
        
        # Frame pour les personnes
        frame_personnes = tk.Frame(root, bg=self.bg_color, padx=20, pady=20)
        frame_personnes.pack(fill=tk.X)
        
        title_label = tk.Label(frame_personnes, text="👨‍🚀 GESTION DES PERSONNES", 
                              font=("Arial", 14, "bold"), bg=self.bg_color, fg=self.fg_color)
        title_label.pack(pady=(0,10))
        
        tk.Label(frame_personnes, text="Nom:", bg=self.bg_color, fg=self.text_color, font=("Arial", 10)).pack()
        self.nom_entry = tk.Entry(frame_personnes, width=30, font=("Arial", 10))
        self.nom_entry.pack(pady=5)
        
        tk.Label(frame_personnes, text="Montant investi (0 pour non-investisseur):", 
                bg=self.bg_color, fg=self.text_color, font=("Arial", 10)).pack()
        self.montant_entry = tk.Entry(frame_personnes, width=30, font=("Arial", 10))
        self.montant_entry.pack(pady=5)
        
        btn_ajouter = tk.Button(frame_personnes, text="➕ Ajouter Personne", 
                               command=self.ajouter_personne, bg=self.button_color, 
                               fg=self.fg_color, font=("Arial", 10, "bold"), 
                               cursor="hand2", relief=tk.RAISED)
        btn_ajouter.pack(pady=10)
        
        # Frame pour liste des personnes
        self.liste_label = tk.Label(root, text="", bg=self.bg_color, fg=self.text_color, 
                                   font=("Arial", 9), justify=tk.LEFT)
        self.liste_label.pack(pady=5)
        
        # Frame pour calcul
        frame_calcul = tk.Frame(root, bg=self.bg_color, padx=20, pady=20)
        frame_calcul.pack(fill=tk.X)
        
        calc_title = tk.Label(frame_calcul, text="💰 CALCUL DE RÉPARTITION", 
                             font=("Arial", 14, "bold"), bg=self.bg_color, fg=self.fg_color)
        calc_title.pack(pady=(0,10))
        
        tk.Label(frame_calcul, text="Coût total cargo (aUEC):", 
                bg=self.bg_color, fg=self.text_color, font=("Arial", 10)).pack()
        self.cout_entry = tk.Entry(frame_calcul, width=30, font=("Arial", 10))
        self.cout_entry.pack(pady=5)
        self.cout_entry.bind('<KeyRelease>', self.update_cout_total)
        
        tk.Label(frame_calcul, text="Revente totale (aUEC):", 
                bg=self.bg_color, fg=self.text_color, font=("Arial", 10)).pack()
        self.revente_entry = tk.Entry(frame_calcul, width=30, font=("Arial", 10))
        self.revente_entry.pack(pady=5)
        
        btn_calculer = tk.Button(frame_calcul, text="🧮 Calculer les Parts", 
                                command=self.calculer_parts, bg=self.button_color, 
                                fg=self.fg_color, font=("Arial", 10, "bold"), 
                                cursor="hand2", relief=tk.RAISED)
        btn_calculer.pack(pady=10)
        
        # Frame pour résultats
        frame_resultats = tk.Frame(root, bg=self.bg_color, padx=20, pady=10)
        frame_resultats.pack(fill=tk.BOTH, expand=True)
        
        result_title = tk.Label(frame_resultats, text="📊 RÉSULTATS", 
                               font=("Arial", 14, "bold"), bg=self.bg_color, fg=self.fg_color)
        result_title.pack(pady=(0,10))
        
        self.resultat_text = tk.Text(frame_resultats, height=15, width=60, 
                                     font=("Courier New", 9), bg="#051020", 
                                     fg=self.text_color, relief=tk.SUNKEN, bd=2)
        self.resultat_text.pack(fill=tk.BOTH, expand=True)
        
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
        
        self.personnes[nom] = montant
        self.nom_entry.delete(0, tk.END)
        self.montant_entry.delete(0, tk.END)
        self.update_liste_personnes()
        self.update_cout_total()
        
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
    try:
        root = tk.Tk()
        try:
            # Try to use a more futuristic font if available
            root.option_add('*Font', ('Segoe UI', 10))
        except Exception:
            # Fallback to default font
            pass
        app = CargoShareApp(root)
        root.mainloop()
    except Exception as e:
        # Global error handler to show error message box instead of crashing
        import traceback
        error_msg = f"ERREUR CRITIQUE:\n\n{str(e)}\n\nDétails techniques:\n{traceback.format_exc()}"
        try:
            root_err = tk.Tk()
            root_err.withdraw()
            messagebox.showerror("Erreur - Star Citizen Cargo Share", error_msg)
            root_err.destroy()
        except:
            print(error_msg)
