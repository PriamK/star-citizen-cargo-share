import tkinter as tk
from tkinter import ttk, messagebox

class CargoShareApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Star Citizen - Calculateur de Parts Cargo")
        self.root.geometry("800x600")
        
        # Données
        self.personnes = {}  # {nom: montant_investi}
        
        # Interface
        self.create_widgets()
    
    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Section 1: Ajouter des personnes
        ttk.Label(main_frame, text="Gestion des Personnes", font=('Arial', 12, 'bold')).grid(row=0, column=0, columnspan=3, pady=5)
        
        ttk.Label(main_frame, text="Nom:").grid(row=1, column=0, sticky=tk.W, padx=5)
        self.nom_entry = ttk.Entry(main_frame, width=20)
        self.nom_entry.grid(row=1, column=1, padx=5)
        
        ttk.Label(main_frame, text="Montant investi:").grid(row=2, column=0, sticky=tk.W, padx=5)
        self.montant_entry = ttk.Entry(main_frame, width=20)
        self.montant_entry.grid(row=2, column=1, padx=5)
        
        ttk.Button(main_frame, text="Ajouter Personne", command=self.ajouter_personne).grid(row=3, column=0, columnspan=2, pady=5)
        
        # Liste des personnes
        ttk.Label(main_frame, text="Liste des Participants:", font=('Arial', 10, 'bold')).grid(row=4, column=0, columnspan=3, pady=5)
        
        self.liste_frame = ttk.Frame(main_frame)
        self.liste_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.liste_text = tk.Text(self.liste_frame, height=8, width=50)
        self.liste_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(self.liste_frame, command=self.liste_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.liste_text.config(yscrollcommand=scrollbar.set)
        
        ttk.Button(main_frame, text="Supprimer Personne", command=self.supprimer_personne).grid(row=6, column=0, columnspan=3, pady=5)
        
        # Section 2: Calcul du cargo
        ttk.Separator(main_frame, orient='horizontal').grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Label(main_frame, text="Calcul de Répartition", font=('Arial', 12, 'bold')).grid(row=8, column=0, columnspan=3, pady=5)
        
        ttk.Label(main_frame, text="Coût total du cargo:").grid(row=9, column=0, sticky=tk.W, padx=5)
        self.cout_entry = ttk.Entry(main_frame, width=20)
        self.cout_entry.grid(row=9, column=1, padx=5)
        
        ttk.Label(main_frame, text="Revente totale:").grid(row=10, column=0, sticky=tk.W, padx=5)
        self.revente_entry = ttk.Entry(main_frame, width=20)
        self.revente_entry.grid(row=10, column=1, padx=5)
        
        ttk.Button(main_frame, text="Calculer les Parts", command=self.calculer_parts).grid(row=11, column=0, columnspan=2, pady=10)
        
        # Section 3: Résultats
        ttk.Label(main_frame, text="Résultats", font=('Arial', 12, 'bold')).grid(row=12, column=0, columnspan=3, pady=5)
        
        self.resultat_text = tk.Text(main_frame, height=10, width=70)
        self.resultat_text.grid(row=13, column=0, columnspan=3, pady=5)
        
        resultat_scrollbar = ttk.Scrollbar(main_frame, command=self.resultat_text.yview)
        self.resultat_text.config(yscrollcommand=resultat_scrollbar.set)
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(5, weight=1)
    
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
        
        if revente_totale <= cout_total:
            messagebox.showwarning("Attention", "La revente doit être supérieure au coût pour avoir un bénéfice.")
        
        # Calcul du bénéfice total
        benefice_total = revente_totale - cout_total
        
        # Séparation investisseurs/non-investisseurs
        investisseurs = {nom: montant for nom, montant in self.personnes.items() if montant > 0}
        non_investisseurs = {nom: montant for nom, montant in self.personnes.items() if montant == 0}
        
        # Calcul des parts
        resultats = {}
        
        # 85% pour les investisseurs (proportionnel à leur investissement)
        if investisseurs:
            total_investi = sum(investisseurs.values())
            part_investisseurs = benefice_total * 0.85
            
            for nom, montant in investisseurs.items():
                proportion = montant / total_investi if total_investi > 0 else 0
                part = part_investisseurs * proportion
                resultats[nom] = part
        
        # 15% pour les non-investisseurs (équitablement)
        if non_investisseurs:
            part_non_investisseurs = benefice_total * 0.15
            nb_non_investisseurs = len(non_investisseurs)
            part_par_personne = part_non_investisseurs / nb_non_investisseurs
            
            for nom in non_investisseurs:
                resultats[nom] = part_par_personne
        
        # Affichage des résultats
        self.resultat_text.delete('1.0', tk.END)
        self.resultat_text.insert(tk.END, "=" * 70 + "\n")
        self.resultat_text.insert(tk.END, f"BÉNÉFICE TOTAL: {benefice_total:.2f} aUEC\n")
        self.resultat_text.insert(tk.END, "=" * 70 + "\n\n")
        
        if investisseurs:
            self.resultat_text.insert(tk.END, "INVESTISSEURS (85% du bénéfice):\n")
            self.resultat_text.insert(tk.END, "-" * 70 + "\n")
            for nom, montant in investisseurs.items():
                part = resultats.get(nom, 0)
                self.resultat_text.insert(tk.END, f"  {nom}:\n")
                self.resultat_text.insert(tk.END, f"    - Investi: {montant:.2f} aUEC\n")
                self.resultat_text.insert(tk.END, f"    - Part du bénéfice: {part:.2f} aUEC\n")
                self.resultat_text.insert(tk.END, f"    - TOTAL REÇU: {montant + part:.2f} aUEC\n\n")
        
        if non_investisseurs:
            self.resultat_text.insert(tk.END, "NON-INVESTISSEURS (15% du bénéfice):\n")
            self.resultat_text.insert(tk.END, "-" * 70 + "\n")
            for nom in non_investisseurs:
                part = resultats.get(nom, 0)
                self.resultat_text.insert(tk.END, f"  {nom}: {part:.2f} aUEC\n")
        
        self.resultat_text.insert(tk.END, "\n" + "=" * 70 + "\n")
        total_distribue = sum(resultats.values())
        self.resultat_text.insert(tk.END, f"Total distribué: {total_distribue:.2f} aUEC\n")
        self.resultat_text.insert(tk.END, f"Vérification: {abs(total_distribue - benefice_total):.2f} aUEC de différence\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = CargoShareApp(root)
    root.mainloop()
