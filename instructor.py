class Instructor:

    def __init__(self, inst_id):
        self.id = inst_id

      
        self.schedule = {
            "S": [], "M": [], "T": [], "W": [], "Th": []
        }

        self.preferences = []

    def print_info(self):
        print("Instructor ID:", self.id)
        print("Preferences:", self.preferences)
        print("Schedule:")
        for day in self.schedule:
            print(" ", day, "->", self.schedule[day])
