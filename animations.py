from PySide6.QtWidgets import QWidget, QGraphicsOpacityEffect
from PySide6.QtCore import (
    QPropertyAnimation,
    QPoint,
    QEasingCurve,
    QParallelAnimationGroup,
    QSequentialAnimationGroup,
    QVariantAnimation,
    Qt,
)
from PySide6.QtGui import QPainter, QColor
import random


class ConfettiParticle(QWidget):
    def __init__(self, color, size=5, parent=None):
        super().__init__(parent)
        self.color = color
        self.setFixedSize(size, size)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(self.color)
        painter.setPen(Qt.NoPen)
        painter.drawRect(self.rect())


def run_confetti_animation(parent, config):
    """
    Runs the confetti animation effect on the given parent widget.
    """
    num_particles = config.confetti_amount
    confetti_group = QParallelAnimationGroup(parent)

    for _ in range(num_particles):
        # Generate a random color and particle size.
        color = QColor(
            random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
        )
        size = random.randint(4, 15)
        particle = ConfettiParticle(color, size, parent=parent)

        # Set a random starting position (e.g. within the top half of the window).
        start_x = random.randint(0, parent.width())
        start_y = random.randint(0, parent.height() // 2)
        particle.move(start_x, start_y)
        particle.show()

        # Determine the end position with some random horizontal shift.
        end_x = start_x + random.randint(-50, 50)
        end_y = start_y + random.randint(100, 200)
        pos_anim = QPropertyAnimation(particle, b"pos")
        pos_anim.setDuration(config.effect_duration)
        pos_anim.setStartValue(particle.pos())
        pos_anim.setEndValue(QPoint(end_x, end_y))
        pos_anim.setEasingCurve(QEasingCurve.OutQuad)

        # Animate opacity from full to transparent.
        opacity_effect = QGraphicsOpacityEffect(particle)
        particle.setGraphicsEffect(opacity_effect)
        opacity_anim = QPropertyAnimation(opacity_effect, b"opacity")
        opacity_anim.setDuration(config.effect_duration // 2)
        opacity_anim.setStartValue(1.0)
        opacity_anim.setEndValue(0.0)

        # Group the animations for this particle.
        particle_group = QParallelAnimationGroup(parent)
        particle_group.addAnimation(pos_anim)
        particle_group.addAnimation(opacity_anim)
        particle_group.finished.connect(particle.deleteLater)

        confetti_group.addAnimation(particle_group)

    confetti_group.start()


def run_glow_animation(label, config):
    """
    Runs a glow animation on the provided label by transitioning its text color.
    """
    half_duration = config.effect_duration // 2

    original_color = QColor(config.fg_color[0], config.fg_color[1], config.fg_color[2])
    glow_color = QColor(
        config.glow_color[0], config.glow_color[1], config.glow_color[2]
    )

    glow_animation_group = QSequentialAnimationGroup(label)

    # Phase 1: Animate from original color to glow color.
    anim_to_glow = QVariantAnimation(label)
    anim_to_glow.setDuration(half_duration)
    anim_to_glow.setStartValue(original_color)
    anim_to_glow.setEndValue(glow_color)
    anim_to_glow.valueChanged.connect(
        lambda value: label.setStyleSheet(
            f"color: rgb({value.red()}, {value.green()}, {value.blue()});"
        )
    )

    # Phase 2: Animate back from glow color to original color.
    anim_to_original = QVariantAnimation(label)
    anim_to_original.setDuration(half_duration)
    anim_to_original.setStartValue(glow_color)
    anim_to_original.setEndValue(original_color)
    anim_to_original.valueChanged.connect(
        lambda value: label.setStyleSheet(
            f"color: rgb({value.red()}, {value.green()}, {value.blue()});"
        )
    )

    glow_animation_group.addAnimation(anim_to_glow)
    glow_animation_group.addAnimation(anim_to_original)
    glow_animation_group.start()
