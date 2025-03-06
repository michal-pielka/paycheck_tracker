import time
from config import Config


class PaycheckTrackerLogic:
    def __init__(self, config: Config):
        self.config = config
        self.next_milestone = self.config.milestone_multiple
        self.running = True
        self.start_time = time.time()
        self.accumulated_time = 0

    def calculate_earnings(self):
        """Calculate earnings based on elapsed time."""
        if self.running:
            current_time = time.time()
            elapsed = self.accumulated_time + (current_time - self.start_time)
            return (
                self.config.hourly_rate / 3600
            ) * elapsed
        return self.get_paused_earnings()

    def get_paused_earnings(self):
        """Return earnings when paused."""
        return (self.config.hourly_rate / 3600) * self.accumulated_time

    def update_next_milestone(self):
        self.next_milestone += self.config.milestone_multiple

    def get_next_milestione(self):
        return self.next_milestone

    def toggle_pause(self):
        """Pause or resume tracking."""
        if self.running:
            self.accumulated_time += time.time() - self.start_time
            self.running = False
        else:
            self.start_time = time.time()
            self.running = True
