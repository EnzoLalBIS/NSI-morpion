"""
Morpion - Exercice NSI Terminal
================================
Objectif : Compléter la classe Bot pour qu'elle puisse jouer au morpion

Instructions pour les élèves :
- Complétez la méthode jouer() dans la classe Bot
- Utilisez les méthodes de la classe Grille pour analyser le jeu
- Essayez différentes stratégies (aléatoire, puis plus intelligente)
"""

import random


class Grille:
    """Représente la grille de morpion 3x3"""
    
    def __init__(self):
        # Grille vide représentée par une liste de listes
        # ' ' = case vide, 'X' = joueur 1, 'O' = joueur 2
        self.cases = [[' ' for _ in range(3)] for _ in range(3)]
        self.joueur_actuel = 'X'
    
    def afficher(self):
        """Affiche la grille dans la console"""
        print("\n  0   1   2")
        for i, ligne in enumerate(self.cases):
            print(f"{i} {ligne[0]} | {ligne[1]} | {ligne[2]}")
            if i < 2:
                print(" -----------")
        print()
    
    def est_case_vide(self, ligne, colonne):
        """Vérifie si une case est vide"""
        return self.cases[ligne][colonne] == ' '
    
    def jouer_coup(self, ligne, colonne):
        """
        Place le symbole du joueur actuel à la position donnée
        Retourne True si le coup est valide, False sinon
        """
        if 0 <= ligne < 3 and 0 <= colonne < 3 and self.est_case_vide(ligne, colonne):
            self.cases[ligne][colonne] = self.joueur_actuel
            return True
        return False
    
    def changer_joueur(self):
        """Alterne entre les joueurs X et O"""
        self.joueur_actuel = 'O' if self.joueur_actuel == 'X' else 'X'
    
    def obtenir_cases_vides(self):
        """
        Retourne la liste des cases vides sous forme de tuples (ligne, colonne)
        Exemple : [(0, 0), (0, 2), (1, 1)]
        """
        vides = []
        for i in range(3):
            for j in range(3):
                if self.cases[i][j] == ' ':
                    vides.append((i, j))
        return vides
    
    def obtenir_case(self, ligne, colonne):
        """Retourne le contenu d'une case (' ', 'X' ou 'O')"""
        return self.cases[ligne][colonne]
    
    def compter_symbole_ligne(self, ligne, symbole):
        """Compte le nombre d'occurrences d'un symbole dans une ligne"""
        return self.cases[ligne].count(symbole)
    
    def compter_symbole_colonne(self, colonne, symbole):
        """Compte le nombre d'occurrences d'un symbole dans une colonne"""
        return sum(1 for i in range(3) if self.cases[i][colonne] == symbole)
    
    def compter_symbole_diagonale_principale(self, symbole):
        """Compte les occurrences d'un symbole sur la diagonale \ """
        return sum(1 for i in range(3) if self.cases[i][i] == symbole)
    
    def compter_symbole_diagonale_secondaire(self, symbole):
        """Compte les occurrences d'un symbole sur la diagonale / """
        return sum(1 for i in range(3) if self.cases[i][2-i] == symbole)
    
    def verifier_victoire(self):
        """
        Vérifie si un joueur a gagné
        Retourne 'X', 'O' ou None
        """
        # Vérifier les lignes
        for ligne in self.cases:
            if ligne[0] == ligne[1] == ligne[2] != ' ':
                return ligne[0]
        
        # Vérifier les colonnes
        for col in range(3):
            if self.cases[0][col] == self.cases[1][col] == self.cases[2][col] != ' ':
                return self.cases[0][col]
        
        # Vérifier les diagonales
        if self.cases[0][0] == self.cases[1][1] == self.cases[2][2] != ' ':
            return self.cases[1][1]
        if self.cases[0][2] == self.cases[1][1] == self.cases[2][0] != ' ':
            return self.cases[1][1]
        
        return None
    
    def est_pleine(self):
        """Vérifie si la grille est pleine (match nul)"""
        return all(self.cases[i][j] != ' ' for i in range(3) for j in range(3))


class BotDefensif:
    """
    Bot Niveau 2 - Stratégie Défensive
    Bloque l'adversaire s'il a 2 symboles alignés, sinon joue aléatoirement
    """
    
    def __init__(self, nom="BotDefensif", symbole='O'):
        self.nom = nom
        self.symbole = symbole
        self.symbole_adversaire = 'X' if symbole == 'O' else 'O'
        self.niveau = 2
    
    def jouer(self, grille):
        """
        Stratégie défensive :
        1. Bloquer l'adversaire s'il peut gagner au prochain coup
        2. Sinon jouer aléatoirement
        """
        # D'abord, vérifier si on peut bloquer l'adversaire
        coup_bloquant = self._trouver_coup_critique(grille, self.symbole_adversaire)
        if coup_bloquant:
            return coup_bloquant
        
        # Sinon jouer aléatoirement
        cases_vides = grille.obtenir_cases_vides()
        if cases_vides:
            return random.choice(cases_vides)
        return None
    
    def _trouver_coup_critique(self, grille, symbole):
        """
        Trouve un coup critique : une case qui complète 2 symboles alignés
        Utilisé pour gagner (notre symbole) ou bloquer (symbole adversaire)
        """
        # Vérifier les lignes
        for i in range(3):
            if grille.compter_symbole_ligne(i, symbole) == 2 and grille.compter_symbole_ligne(i, ' ') == 1:
                for j in range(3):
                    if grille.est_case_vide(i, j):
                        return (i, j)
        
        # Vérifier les colonnes
        for j in range(3):
            if grille.compter_symbole_colonne(j, symbole) == 2 and grille.compter_symbole_colonne(j, ' ') == 1:
                for i in range(3):
                    if grille.est_case_vide(i, j):
                        return (i, j)
        
        # Vérifier diagonale principale
        if grille.compter_symbole_diagonale_principale(symbole) == 2 and grille.compter_symbole_diagonale_principale(' ') == 1:
            for i in range(3):
                if grille.est_case_vide(i, i):
                    return (i, i)
        
        # Vérifier diagonale secondaire
        if grille.compter_symbole_diagonale_secondaire(symbole) == 2 and grille.compter_symbole_diagonale_secondaire(' ') == 1:
            for i in range(3):
                if grille.est_case_vide(i, 2-i):
                    return (i, 2-i)
        
        return None


class BotMinimax:
    """
    Bot Niveau 5 - Algorithme Minimax
    Stratégie optimale : explore tous les coups possibles et choisit le meilleur
    Ce bot ne peut pas perdre au morpion !
    """
    
    def __init__(self, nom="BotMinimax", symbole='X'):
        self.nom = nom
        self.symbole = symbole
        self.symbole_adversaire = 'X' if symbole == 'O' else 'O'
        self.niveau = 5
    
    def jouer(self, grille):
        """
        Utilise l'algorithme Minimax pour trouver le coup optimal
        """
        meilleur_score = float('-inf')
        meilleur_coup = None
        
        for coup in grille.obtenir_cases_vides():
            # Simuler le coup
            ligne, colonne = coup
            grille.cases[ligne][colonne] = self.symbole
            
            # Évaluer avec minimax
            score = self._minimax(grille, 0, False)
            
            # Annuler le coup
            grille.cases[ligne][colonne] = ' '
            
            if score > meilleur_score:
                meilleur_score = score
                meilleur_coup = coup
        
        return meilleur_coup
    
    def _minimax(self, grille, profondeur, est_maximisant):
        """
        Algorithme Minimax récursif
        
        Principe :
        - Explore récursivement tous les coups possibles
        - Le joueur maximisant (notre bot) cherche à maximiser le score
        - Le joueur minimisant (adversaire) cherche à minimiser le score
        - Retourne le meilleur score pour la position actuelle
        
        Scores :
        - +10 : Victoire (bonus si victoire rapide)
        - -10 : Défaite (moins mauvais si défaite tardive)
        - 0 : Match nul
        """
        # Vérifier les conditions de fin
        gagnant = grille.verifier_victoire()
        if gagnant == self.symbole:
            return 10 - profondeur  # Victoire (préférer victoire rapide)
        elif gagnant == self.symbole_adversaire:
            return profondeur - 10  # Défaite (retarder la défaite)
        elif grille.est_pleine():
            return 0  # Match nul
        
        if est_maximisant:
            # Tour du bot (maximiser le score)
            meilleur_score = float('-inf')
            for coup in grille.obtenir_cases_vides():
                ligne, colonne = coup
                grille.cases[ligne][colonne] = self.symbole
                score = self._minimax(grille, profondeur + 1, False)
                grille.cases[ligne][colonne] = ' '
                meilleur_score = max(score, meilleur_score)
            return meilleur_score
        else:
            # Tour de l'adversaire (minimiser le score)
            meilleur_score = float('inf')
            for coup in grille.obtenir_cases_vides():
                ligne, colonne = coup
                grille.cases[ligne][colonne] = self.symbole_adversaire
                score = self._minimax(grille, profondeur + 1, True)
                grille.cases[ligne][colonne] = ' '
                meilleur_score = min(score, meilleur_score)
            return meilleur_score


class Jeu:
    """Gère le déroulement d'une partie"""
    
    def __init__(self, bot1=None, bot2=None):
        self.grille = Grille()
        self.bot1 = bot1  # Joue avec 'X'
        self.bot2 = bot2  # Joue avec 'O'
        self.mode = self._determiner_mode()
    
    def _determiner_mode(self):
        """Détermine le mode de jeu selon les bots fournis"""
        if self.bot1 is None and self.bot2 is None:
            return "humain_vs_humain"
        elif self.bot1 is None:
            return "humain_vs_bot"
        elif self.bot2 is None:
            return "bot_vs_humain"
        else:
            return "bot_vs_bot"
    
    def jouer_humain(self, symbole):
        """Demande au joueur humain de jouer"""
        while True:
            try:
                print(f"Votre tour (vous êtes {symbole})")
                ligne = int(input("Ligne (0-2) : "))
                colonne = int(input("Colonne (0-2) : "))
                
                if self.grille.jouer_coup(ligne, colonne):
                    break
                else:
                    print("Case invalide ou déjà occupée !")
            except (ValueError, IndexError):
                print("Entrée invalide ! Utilisez des nombres entre 0 et 2.")
    
    def jouer_bot(self, bot):
        """Fait jouer un bot"""
        print(f"\nTour de {bot.nom} (niveau {bot.niveau}, {bot.symbole})...")
        coup = bot.jouer(self.grille)
        if coup:
            ligne, colonne = coup
            self.grille.jouer_coup(ligne, colonne)
            print(f"{bot.nom} joue en ({ligne}, {colonne})")
    
    def lancer(self):
        """Lance une partie complète"""
        print("=== MORPION ===")
        if self.mode == "bot_vs_bot":
            print(f"{self.bot1.nom} (X, niveau {self.bot1.niveau}) VS {self.bot2.nom} (O, niveau {self.bot2.niveau})")
            print("Appuyez sur Entrée pour voir chaque coup...")
        elif self.mode == "humain_vs_bot":
            print(f"Vous jouez avec X contre {self.bot2.nom} (O, niveau {self.bot2.niveau})")
        elif self.mode == "bot_vs_humain":
            print(f"{self.bot1.nom} (X, niveau {self.bot1.niveau}) contre vous (O)")
        else:
            print("Deux joueurs humains")
        
        while True:
            self.grille.afficher()
            
            # Gérer le tour selon le joueur actuel
            if self.grille.joueur_actuel == 'X':
                if self.bot1:
                    self.jouer_bot(self.bot1)
                    if self.mode == "bot_vs_bot":
                        input()  # Pause pour voir le coup
                else:
                    self.jouer_humain('X')
            else:
                if self.bot2:
                    self.jouer_bot(self.bot2)
                    if self.mode == "bot_vs_bot":
                        input()  # Pause pour voir le coup
                else:
                    self.jouer_humain('O')
            
            # Vérifier la victoire
            gagnant = self.grille.verifier_victoire()
            if gagnant:
                self.grille.afficher()
                if self.mode == "bot_vs_bot":
                    if gagnant == 'X':
                        print(f"🏆 {self.bot1.nom} a gagné !")
                    else:
                        print(f"🏆 {self.bot2.nom} a gagné !")
                else:
                    if (gagnant == 'X' and not self.bot1) or (gagnant == 'O' and not self.bot2):
                        print("🎉 Vous avez gagné !")
                    else:
                        nom_bot = self.bot1.nom if gagnant == 'X' else self.bot2.nom
                        print(f"😔 {nom_bot} a gagné !")
                break
            
            # Vérifier le match nul
            if self.grille.est_pleine():
                self.grille.afficher()
                print("🤝 Match nul !")
                break
            
            # Changer de joueur
            self.grille.changer_joueur()


# Programme principal
if __name__ == "__main__":
    print("=== AFFRONTEMENT BOT MINIMAX (Niveau 5) VS BOT DÉFENSIF (Niveau 2) ===\n")
    
    # Créer les deux bots avec des classes différentes
    bot_minimax = BotMinimax("MiniMax", symbole='X')
    bot_defensif = BotDefensif("Défensif", symbole='O')
    
    # Lancer plusieurs parties pour voir les statistiques
    nb_parties = 5
    scores = {'X': 0, 'O': 0, 'Nul': 0}
    
    print(f"Lancement de {nb_parties} parties...\n")
    
    for i in range(nb_parties):
        print(f"\n{'='*50}")
        print(f"PARTIE {i+1}/{nb_parties}")
        print(f"{'='*50}")
        
        jeu = Jeu(bot_minimax, bot_defensif)
        
        # Jouer la partie
        while True:
            jeu.grille.afficher()
            
            if jeu.grille.joueur_actuel == 'X':
                jeu.jouer_bot(bot_minimax)
            else:
                jeu.jouer_bot(bot_defensif)
            
            # Pause pour voir
            input("  [Appuyez sur Entrée]")
            
            # Vérifier victoire
            gagnant = jeu.grille.verifier_victoire()
            if gagnant:
                jeu.grille.afficher()
                print(f"\n🏆 {bot_minimax.nom if gagnant == 'X' else bot_defensif.nom} gagne !")
                scores[gagnant] += 1
                break
            
            if jeu.grille.est_pleine():
                jeu.grille.afficher()
                print("\n🤝 Match nul !")
                scores['Nul'] += 1
                break
            
            jeu.grille.changer_joueur()
    
    # Afficher les statistiques finales
    print(f"\n{'='*50}")
    print("STATISTIQUES FINALES")
    print(f"{'='*50}")
    print(f"{bot_minimax.nom} (niveau 5) : {scores['X']} victoires")
    print(f"{bot_defensif.nom} (niveau 2) : {scores['O']} victoires")
    print(f"Matchs nuls : {scores['Nul']}")
    print(f"\nTaux de victoire de {bot_minimax.nom} : {scores['X']/nb_parties*100:.1f}%")