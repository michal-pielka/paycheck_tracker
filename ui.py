from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QFont
from config import Config
from tracker import PaycheckTrackerLogic
from animations import run_confetti_animation, run_glow_animation


class PaycheckTracker(QWidget):
    def __init__(self, config_path):
        super().__init__()

        self.config = Config(config_path)
        self.tracker = PaycheckTrackerLogic(self.config)

        self.setup_window()
        self.setup_layout()
        self.setup_timer()

        self.original_geometry = None

    def setup_window(self):
        self.setWindowTitle("Paycheck Tracker")
        self.resize(self.config.width, self.config.height)

        if self.config.hide_menu_bar:
            self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
            self.setAttribute(Qt.WA_TranslucentBackground)

        self.setStyleSheet(
            f"""
            QWidget {{
                background-color: rgb({self.config.bg_color[0]}, {self.config.bg_color[1]}, {self.config.bg_color[2]});
                border-radius: 9px;
            }}
            """
        )

    def setup_layout(self):
        layout = QVBoxLayout(self)
        self.label = QLabel("0.00 zł")
        self.label.setAlignment(Qt.AlignCenter)
        self.original_style = f"color: rgb({self.config.fg_color[0]}, {self.config.fg_color[1]}, {self.config.fg_color[2]});"
        self.label.setStyleSheet(self.original_style)
        self.label.setFont(QFont(self.config.font, self.config.font_size))
        layout.addWidget(self.label)

    def setup_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_earnings)
        self.timer.start(self.config.refresh_rate)

    def showEvent(self, event):
        self.original_geometry = self.label.geometry()
        super().showEvent(event)

    def update_earnings(self):
        show_effects = self.config.show_effects
        earnings = self.tracker.calculate_earnings()
        next_milestone = self.tracker.get_next_milestione()
        self.label.setText(f"{earnings:0.{self.config.decimal_digits}f} zł")

        if show_effects and earnings >= next_milestone:
            self.trigger_effects()
            self.tracker.update_next_milestone()

    def trigger_effects(self):
        if "confetti" in self.config.effects:
            run_confetti_animation(self, self.config)
        if "glow" in self.config.effects:
            run_glow_animation(self.label, self.config)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_start_pos = event.globalPos()
            self._drag_offset = event.globalPos() - self.frameGeometry().topLeft()
            self._dragging = False
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            if (event.globalPos() - self._drag_start_pos).manhattanLength() > 5:
                self._dragging = True
                self.move(event.globalPos() - self._drag_offset)
                event.accept()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if not self._dragging:
            self.tracker.toggle_pause()
        super().mouseReleaseEvent(event)
