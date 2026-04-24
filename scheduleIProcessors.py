class ScheduleProcessors:
    def __init__(self, instructor, valid_codes):
        self.instructor = instructor
        self.valid_codes = set(valid_codes)     # convert the list to a set for faster looking up
        # computing the total lecture time and office hour time
        self.lecture_minutes = 0
        self.oh_minutes = 0

        # these slots holds all activity per a day with information of each
        self.slots = {"S": [], "M": [], "T": [], "W": [], "Th": []}
        self.course_slots = {"S": [], "M": [], "T": [], "W": [], "Th": []}

        self.schedule_courses = []      #convert munits to hours

        def minutes_to_time(self, m):
            h = m // 60
            mi = m % 60
            return f"{h}:{mi:02d}"

    def parse_schedule(self):
        """
        read instructor schedule lines and covert them into:
        => LIST OF TIME INTERVALS
        => INTERVALS FOR COURSES
        => LECTURE MINUTES , OH MINUTES
        => COURSE, LAB CODE VALIDATION
        """
        for day in self.instructor.schedule:
            for line in self.instructor.schedule[day]:
                rest = line.split("|", 1)[1]
                activities = [a.strip() for a in rest.split(";") if a.strip()]

                for act in activities:
                    timepart = act.split(']')[0].split('[')[1]
                    timepart = timepart.replace("–", "-")  # to be sure that the - is the original one
                    start_time = timepart.split('-')[0].strip()
                    end_time = timepart.split('-')[1].strip()

                    # START
                    if ":" in start_time:
                        sh, sm = start_time.split(":")
                        sh = int(sh); sm = int(sm)
                    else:
                        sh = int(start_time); sm = 0

                    # END
                    if ":" in end_time:
                        eh, em = end_time.split(":")
                        eh = int(eh); em = int(em)
                    else:
                        eh = int(end_time); em = 0

                    # convert to minutes
                    start_min = sh * 60 + sm
                    end_min = eh * 60 + em
                    if end_min <= start_min:    # for 24 to 12 converting according to the scdule format
                        end_min += 12 * 60

                    duration = end_min - start_min
                    self.slots[day].append((start_min, end_min))

                    typ = act.split("]")[1].strip()
                    if typ == "OH":
                        self.oh_minutes += duration
                    else:
                        self.lecture_minutes += duration
                        self.course_slots[day].append((start_min, end_min))

                        self.schedule_courses.append(typ)   # we store the course code to use it for  validation
    def check_load(self):
        """
        Validate teaching load:
        => lecture hours must be between 12 - 18
        => office hours must be at least 50% of lecture hours
        """
        lec_hours = self.lecture_minutes / 60
        oh_hours = self.oh_minutes / 60


        print(f"Instructor {self.instructor.id}")
        print("Total Lectures Time:", round(lec_hours, 2))
        print("Total Office Hour Time:", round(oh_hours, 2))

        # Teaching load rule
        valid_load = (12 <= lec_hours <= 18)
        if valid_load:
            print("Teaching Load Valid")
        elif lec_hours < 12:
            print("Invalid Teaching Load: Teaching load is less than 12 hours")
        else:
            print("Invalid Teaching Load: Teaching load is more than 18 hours")

        # OH >= 50% of lectures
        valid_oh = (oh_hours * 2 >= lec_hours)
        if valid_oh:
            print("Office Hours Ratio Valid")

        else:
            print("Invalid Office Hours: Office hours are less than 50% of teaching load")

        return valid_load and valid_oh

    def check_teaching_days(self):
        """
        Ensure the instructor teaches on at least 4 different days (lec, oh)
        """
        days = 0
        for d in self.slots:
            if self.slots[d]:
                days += 1

        if days >= 4:
            print("Teaching Days Distribution Valid")
            return True
        else:
            print("Invalid Schedule: Less than four teaching days")
            return False

    def check_conflicts(self):
        """
        Detect time conflict between lectures or oh..
        """
        
        valid = True

        for day in self.slots:
            slots = list(set(self.slots[day]))

            # compare
            for i in range(len(slots)):
                for j in range(i + 1, len(slots)):
                    s1, e1 = slots[i]
                    s2, e2 = slots[j]

                    # overlab condition
                    if s1 < e2 and s2 < e1:
                        h1s, m1s = divmod(s1, 60)
                        h1e, m1e = divmod(e1, 60)
                        h2s, m2s = divmod(s2, 60)
                        h2e, m2e = divmod(e2, 60)

                        print(
                            f"Conflict on {day} between "
                            f"[{h1s}:{m1s:02d}-{h1e}:{m1e:02d}] and "
                            f"[{h2s}:{m2s:02d}-{h2e}:{m2e:02d}]"
                        )

                        valid = False
        if valid:
            print("No Time Conflicts Detected")
        if not valid:
            print("Invalid Schedule: Time Conflicts Found")

        return valid

    def check_consecutive(self):
        """
        ensure that No more than two consecutive courses in a row.
        """
        invalid = False

        for day in self.course_slots:
            slots = sorted(self.course_slots[day])
            prev_end = None
            count = 1

            for start, end in slots:
                if prev_end is not None and start == prev_end:
                    count += 1
                else:
                    count = 1

                if count > 2:
                    print(f"Day {day} violates consecutive teaching rule")
                    invalid = True
                    break

                prev_end = end

        if invalid:
            print("Invalid Schedule: More than two consecutive courses found")
            return False
        else:
            print("Consecutive Teaching Rule Valid")
            return True


    # this function Ensure all scheduled courses/labs exist in the valid codes file
    def isValidCode(self):
        invalid = []
        for  code in self.schedule_courses:
            if code not in self.valid_codes:
                invalid.append(code)

        if invalid:
            print("Invalid Code: Invalid < Course | Lab > codes: ", sorted(set(invalid)))
            return False
        else:
            print("Valid < Course | Lab > code.")
            return True


    # this function put validation on assigned courses/labs and see if its match the instructor’s preference list.
    def isValidPreferences(self):
        not_allowed = []
        preferences_set = set(self.instructor.preferences)      # converting preferences list into a set

        for code in self.schedule_courses:
            if code not in preferences_set:
                not_allowed.append(code)

        if not_allowed:
            print("Invalid Prefernces: < Course | Lab > not in instructor preferences: ", sorted(set(not_allowed)))
            return False
        else:
            print("Valid Instructor Preference.")
            return True
    def isAllowedDays(self):
        """
        if the activity is a lab → check lab repetition
        if it is a lecture → ensure it is only in one group (SMW or T/Th)
          """
        course_groups = {}
        labs_found = set()

        for day in self.instructor.schedule:
           for line in self.instructor.schedule[day]:
               rest = line.split("|", 1)[1]
               activities = [a.strip() for a in rest.split(";") if a.strip()]

               for act in activities:
                  typ = act.split("]")[1].strip()

                  if typ == "OH":
                    continue

               
                  if self.isLab(typ):
                     labs_found.add(typ)
                     continue   

               
                  group = "SMW" if day in ("S", "M", "W") else "TTH"

                  if typ not in course_groups:
                    course_groups[typ] = set()
                  course_groups[typ].add(group)

  
        invalid_courses = [
           c for c, g in course_groups.items()
            if "SMW" in g and "TTH" in g
        ]

        valid = True

        if invalid_courses:
           print(
            "Invalid Teaching Group Day: these courses appear in BOTH groups (SMW and T/Th):",
            sorted(invalid_courses)
            )
           valid = False
        else:
            print("Valid Course Day Grouping.")

    
        if labs_found:
           if not self.isLabsRepeated():
            valid = False

        return valid


    def isLab(self, code):
        """
        Decide if the course code represents a lsb or lecture.
        => by extarcting all digits from the code if its less than  digits then its not even a cours
        => then by checking the second digit if its 1 then its a lab otherwise  its a lecture.
         """
        digits = ""
        for ch in code:
            if ch.isdigit():
                digits += ch

        if len(digits) < 2:
            return False

        return digits[1] == "1"


    def isLabsRepeated(self):
        lab_counts = {}

        for day in self.instructor.schedule:
            for line in self.instructor.schedule[day]:
              rest = line.split("|", 1)[1]
              activities = [a.strip() for a in rest.split(";") if a.strip()]

              for act in activities:
                code = act.split("]")[1].strip()

                if self.isLab(code):
                    lab_counts[code] = lab_counts.get(code, 0) + 1

        repeated = [c for c, cnt in lab_counts.items() if cnt > 1]

        if repeated:
            print("Invalid Lab Rule: Lab course repeated in the week:", repeated)
            return False
        else:
          print("Lab Rule Valid: No Repetition")
        return True


    def process(self):
        """
        Main driver that runs all validations and prints final results.
        """
        self.parse_schedule()
        v1 = self.check_load()
        v2 = self.isValidCode()
        v3 = self.isValidPreferences()
        v4 = self.check_teaching_days()
        v5= self.isAllowedDays()
        v6 = self.check_conflicts()
        v7 = self.check_consecutive()
        

        # for make final decision if the schedule is valid or not
        valid = v1 and v2 and v3 and v4 and v5 and v6 and v7  
        if valid:
            print("OVERALL SCHEDULE STATUS: VALID")
        else:
            print("OVERALL SCHEDULE STATUS: INVALID")