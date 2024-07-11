import time


class StudyAgent:
    def __init__(self, work_duration=25, break_duration=5):
        self.work_duration = work_duration
        self.break_duration = break_duration
        self.sessions_completed = 0
        self.total_sessions_completed = 0

    def set_work_duration(self, minutes):
        self.work_duration = minutes

    def set_break_duration(self, minutes):
        self.break_duration = minutes

    def start_pomodoro(self):
        print(f"Starting work session for {self.work_duration} minutes.")
        time.sleep(self.work_duration * 60)
        self.sessions_completed += 1
        print("Work session completed. Time for a break!")

        print(f"Starting break session for {self.break_duration} minutes.")
        time.sleep(self.break_duration * 60)
        print("Break session completed. Back to work!")

        if self.sessions_completed == 4:
            self.break_duration = 15
            print("Long break time! 15 minutes.")
            time.sleep(15 * 60)
            self.total_sessions_completed = self.sessions_completed
            self.sessions_completed = 0
            print("Long break session completed. Back to work!")

    def get_sessions_completed(self):
        return self.total_sessions_completed


# Example usage
if __name__ == "__main__":
    agent = StudyAgent()
    agent.set_work_duration(25)
    agent.set_break_duration(5)
    agent.start_pomodoro()
    print(f"Sessions completed: {agent.get_sessions_completed()}")
