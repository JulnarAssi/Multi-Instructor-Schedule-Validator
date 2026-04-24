from instructor import Instructor

class ScheduleParser:

    def __init__(self):
        self.valid_codes = []
        self.preferences = {}
        self.instructors = {}

    def parse_files(self):

        #  Valid Codes
        file = open("ValidCodes.txt", "r")
        for l in file:
            l = l.strip()
            if l != "":
                self.valid_codes.append(l)
        file.close()

        # Preferences 
        file = open("Preferences.txt", "r")
        for l in file:
            l = l.strip()
            if l == "":
                continue

            InstID, Codes = l.split(":")
            InstID = InstID.strip()

            codes_list = []
            for c in Codes.split(";"):
                c = c.strip()
                if c != "":
                    codes_list.append(c)

            self.preferences[InstID] = codes_list
        file.close()

        # Schedule 
        file = open("Schedule.txt", "r")
        sched_lines = []
        for l in file:
            l = l.strip()
            if l != "":
                sched_lines.append(l)
        file.close()

        current_id = ""

        for line in sched_lines:
            if "," in line:
                current_id = line.split(",")[0].strip()
                self.instructors[current_id] = Instructor(current_id)
            else:
                day = line.split("|", 1)[0].strip()
                self.instructors[current_id].schedule[day].append(line)

        # Link Preferences 
        for inst_id in self.preferences:
            if inst_id in self.instructors:
                self.instructors[inst_id].preferences = self.preferences[inst_id]
