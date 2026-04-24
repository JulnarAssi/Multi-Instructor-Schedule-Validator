from scheduleparser import ScheduleParser
from scheduleIProcessors import ScheduleProcessors

def main():
    parser = ScheduleParser()
    parser.parse_files()

    for inst_id, instructor in parser.instructors.items():
        instructor.print_info()
        print()

        proc = ScheduleProcessors(instructor, parser.valid_codes)
        proc.process()

        print("\n" + "-" * 60 + "\n")

if __name__ == "__main__":
    main()