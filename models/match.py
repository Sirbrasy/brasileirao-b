import random

class Match:
    def __init__(self, home_team, away_team):
        self.home_team = home_team
        self.away_team = away_team
        
    def simulate(self):
        """Simulates a match between two teams considering various factors"""
        # Base factors
        strength_diff = (self.home_team.strength - self.away_team.strength) * 0.6
        morale_diff = (self.home_team.morale - self.away_team.morale) * 0.2
        home_advantage = 5  # Home team advantage
        
        # Form factor
        home_form = self._calculate_form_factor(self.home_team)
        away_form = self._calculate_form_factor(self.away_team)
        form_impact = (home_form - away_form) * 10
        
        # Final base chance calculation
        base_chance = 50 + strength_diff + morale_diff + home_advantage + form_impact
        
        # Simulate goals
        home_score = self._simulate_team_goals(base_chance)
        away_score = self._simulate_team_goals(100 - base_chance)
        
        return home_score, away_score
    
    def _calculate_form_factor(self, team):
        if not team.form:
            return 0.5
        
        return sum(1 if result == 'W' else 0.5 if result == 'D' else 0 
                  for result in team.form[-3:]) / len(team.form[-3:])
    
    def _simulate_team_goals(self, chance):
        goals = 0
        for _ in range(90):  # Simulate minute by minute
            if random.random() * 100 < chance / 30:
                goals += 1
        return goals