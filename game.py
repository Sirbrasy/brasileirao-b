from models.team import Team
from models.match import Match
from models.season import Season
from database.teams import SERIE_A, SERIE_B, SERIE_C
import os

class BrazilianFootballManager:
    def __init__(self):
        self.teams = self._load_teams()
        self.current_season = 2024
        self.player_team = None
        self.season = Season(self.current_season, self.teams)
    
    def _load_teams(self):
        """Load teams from database"""
        teams = []
        for team_data in SERIE_A + SERIE_B + SERIE_C:
            teams.append(Team(team_data))
        return teams
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def start_game(self):
        self.clear_screen()
        print("=== Bem-vindo ao Brazilian Football Manager ===")
        print("\nEscolha seu time:")
        
        # Show teams grouped by division
        for division in [1, 2, 3]:
            print(f"\nSérie {division}:")
            division_teams = [t for t in self.teams if t.division == division]
            for i, team in enumerate(division_teams, 1):
                print(f"{len([t for t in self.teams if t.division < division]) + i}. "
                      f"{team.name} ({team.city})")
        
        while True:
            try:
                choice = int(input("\nDigite o número do time: ")) - 1
                if 0 <= choice < len(self.teams):
                    break
                print("Escolha inválida!")
            except ValueError:
                print("Por favor, digite um número válido!")
        
        self.player_team = self.teams[choice]
        print(self.player_team.get_history())
        input("\nPressione Enter para continuar...")
        self.play_season()
    
    def play_season(self):
        while self.season.current_round <= self.season.max_rounds:
            self.clear_screen()
            print(f"\n=== Temporada {self.current_season} - "
                  f"Rodada {self.season.current_round}/{self.season.max_rounds} ===")
            
            round_matches = self.season.get_current_round_matches()
            
            for division, matches in round_matches.items():
                print(f"\nSérie {division} - Rodada {self.season.current_round}")
                for home, away in matches:
                    match = Match(home, away)
                    home_score, away_score = match.simulate()
                    self._update_match_results(home, away, home_score, away_score)
                    
                    if home == self.player_team or away == self.player_team:
                        print(f"\n>>> {home.name} {home_score} - {away_score} {away.name}")
            
            self.show_standings()
            self.season.current_round += 1
            
            if self.player_team:
                print("\nOpções:")
                print("1. Ver informações do time")
                print("2. Continuar para próxima rodada")
                print("3. Ver classificação completa")
                print("4. Ver histórico do time")
                
                choice = input("\nEscolha uma opção: ")
                if choice == "1":
                    self.show_team_info(self.player_team)
                elif choice == "3":
                    self.show_standings(show_all=True)
                    input("\nPressione Enter para continuar...")
                elif choice == "4":
                    print(self.player_team.get_history())
                    input("\nPressione Enter para continuar...")
        
        self.end_season()
    
    def _update_match_results(self, home, away, home_score, away_score):
        """Update team statistics after a match"""
        home.goals_for += home_score
        home.goals_against += away_score
        away.goals_for += away_score
        away.goals_against += home_score
        
        if home_score > away_score:
            home.points += 3
            home.wins += 1
            away.losses += 1
            home.form.append('W')
            away.form.append('L')
        elif away_score > home_score:
            away.points += 3
            away.wins += 1
            home.losses += 1
            home.form.append('L')
            away.form.append('W')
        else:
            home.points += 1
            away.points += 1
            home.draws += 1
            away.draws += 1
            home.form.append('D')
            away.form.append('D')
        
        # Keep only last 5 matches in form
        if len(home.form) > 5:
            home.form.pop(0)
        if len(away.form) > 5:
            away.form.pop(0)
    
    def show_team_info(self, team):
        self.clear_screen()
        print(f"\n=== {team.name} ===")
        print(f"Divisão: Série {team.division}")
        print(f"Força: {team.strength}")
        print(f"Orçamento: ${team.budget:,}")
        print(f"Moral: {team.morale}")
        print(f"\nDesempenho na temporada:")
        print(f"Pontos: {team.points}")
        print(f"V-E-D: {team.wins}-{team.draws}-{team.losses}")
        print(f"Gols: {team.goals_for}-{team.goals_against} "
              f"(saldo: {team.goals_for - team.goals_against})")
        print("\nÚltimos 5 jogos:", " ".join(team.form if team.form else ["-"]))
        input("\nPressione Enter para continuar...")
    
    def show_standings(self, show_all=False):
        for division in [1, 2, 3]:
            if not show_all and self.player_team and self.player_team.division != division:
                continue
            
            print(f"\n=== Série {division} Classificação ===")
            teams_in_division = [t for t in self.teams if t.division == division]
            sorted_teams = sorted(
                teams_in_division,
                key=lambda x: (x.points, x.goals_for - x.goals_against, x.goals_for),
                reverse=True
            )
            
            print("Pos | Time               | P  | J  | V  | E  | D  | GP | GC | SG | Últimos")
            print("-" * 75)
            
            for pos, team in enumerate(sorted_teams, 1):
                games = team.wins + team.draws + team.losses
                goal_diff = team.goals_for - team.goals_against
                form_str = " ".join(team.form if team.form else ["-"])
                team_name = f"{team.name}*" if team == self.player_team else team.name
                print(f"{pos:2}  | {team_name:<18} | {team.points:2} | {games:2} | "
                      f"{team.wins:2} | {team.draws:2} | {team.losses:2} | "
                      f"{team.goals_for:2} | {team.goals_against:2} | {goal_diff:2} | {form_str}")

if __name__ == "__main__":
    game = BrazilianFootballManager()
    game.start_game()