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
    try:
        # Try to use a more futuristic font if available
        root.option_add('*Font', 'Segoe UI 10')
    except Exception:
        pass
    app = CargoShareApp(root)
    root.mainloop()
