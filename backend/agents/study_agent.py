import time


class StudyAgent:
    def __init__(self):
        self.study_time = None
        self.break_time = None

    def start_study_session(self, task):
        print(f"Starting study session for: {task}")
        try:
            self.countdown(self.study_time, "Study")
        except Exception as e:
            print(f"An error occurred during the study session: {str(e)}")

    def start_break(self):
        print("Break time! Relax and recharge.")
        try:
            self.countdown(self.break_time, "Break")
        except Exception as e:
            print(f"An error occurred during the break: {str(e)}")

    def countdown(self, duration, session_type):
        try:
            total_seconds = duration * 60
            while total_seconds > 0:
                minutes, seconds = divmod(total_seconds, 60)
                time_format = f"{minutes:02d}:{seconds:02d}"
                print(f"{session_type} Time Remaining: {time_format}", end="\r")
                time.sleep(1)
                total_seconds -= 1
            print(f"\n{session_type} session has ended.")
        except Exception as e:
            print(f"An error occurred during the countdown: {str(e)}")

    def run(self, study_schedule, study_time, break_time):
        self.study_time = study_time
        self.break_time = break_time
        for session in study_schedule:
            task = session["topic"]
            duration = session["duration"]
            self.study_time = duration
            self.start_study_session(task)
            self.start_break()
