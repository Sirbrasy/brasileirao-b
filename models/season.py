class Season:
    def __init__(self, year, teams):
        self.year = year
        self.teams = teams
        self.current_round = 1
        self.max_rounds = self._calculate_max_rounds()
        self.fixtures = self._generate_fixtures()
    
    def _calculate_max_rounds(self):
        """Calculate number of rounds based on teams per division"""
        teams_per_division = {}
        for team in self.teams:
            teams_per_division[team.division] = teams_per_division.get(team.division, 0) + 1
        return max(count - 1 for count in teams_per_division.values())
    
    def _generate_fixtures(self):
        """Generate season fixtures for each division"""
        fixtures = {}
        teams_by_division = self._group_teams_by_division()
        
        for division, teams in teams_by_division.items():
            division_fixtures = []
            for round_num in range(self.max_rounds):
                round_matches = []
                available_teams = teams.copy()
                while len(available_teams) >= 2:
                    home = available_teams.pop(0)
                    away = available_teams.pop(0)
                    round_matches.append((home, away))
                division_fixtures.append(round_matches)
            fixtures[division] = division_fixtures
        
        return fixtures
    
    def _group_teams_by_division(self):
        teams_by_division = {}
        for team in self.teams:
            if team.division not in teams_by_division:
                teams_by_division[team.division] = []
            teams_by_division[team.division].append(team)
        return teams_by_division
    
    def get_current_round_matches(self):
        """Get matches for current round across all divisions"""
        round_matches = {}
        for division, fixtures in self.fixtures.items():
            if self.current_round <= len(fixtures):
                round_matches[division] = fixtures[self.current_round - 1]
        return round_matches