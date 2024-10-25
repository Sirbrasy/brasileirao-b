class Team:
    def __init__(self, data):
        self.name = data["name"]
        self.division = data["division"]
        self.strength = data["strength"]
        self.budget = data["budget"]
        self.stadium = data["stadium"]
        self.capacity = data["capacity"]
        self.city = data["city"]
        self.founded = data["founded"]
        self.titles = data.get("titles", {})
        
        # Performance attributes
        self.points = 0
        self.wins = 0
        self.draws = 0
        self.losses = 0
        self.goals_for = 0
        self.goals_against = 0
        self.form = []
        self.morale = 70
        
    def get_history(self):
        """Returns a formatted string with team's historical data"""
        history = f"\n=== {self.name} ===\n"
        history += f"Fundado em: {self.founded}\n"
        history += f"Cidade: {self.city}\n"
        history += f"Estádio: {self.stadium} ({self.capacity:,} lugares)\n"
        
        if self.titles:
            history += "\nTítulos:\n"
            for title, count in self.titles.items():
                title_name = {
                    "brasileirao": "Brasileirão",
                    "copa_brasil": "Copa do Brasil",
                    "libertadores": "Copa Libertadores",
                    "brasileirao_b": "Brasileirão Série B",
                    "serie_b": "Série B"
                }.get(title, title)
                history += f"- {title_name}: {count}x\n"
        
        return history