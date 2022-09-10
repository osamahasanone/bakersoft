from django.db import models
from django.db.models import TextChoices
from django_fsm import FSMField, transition


class State(TextChoices):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    BLOCKED = "BLOCKED"
    COMPLETED = "COMPLETED"


class FiniteStateMachine(models.Model):
    state = FSMField(choices=State.choices, default=State.OPEN)

    @transition(
        field=state,
        source=State.BLOCKED,
        target=State.OPEN,
    )
    def transition_to_open(self) -> None:
        pass

    @transition(
        field=state,
        source=[State.OPEN, State.BLOCKED],
        target=State.IN_PROGRESS,
    )
    def transition_to_in_progress(self) -> None:
        pass

    @transition(
        field=state,
        source=[State.OPEN, State.IN_PROGRESS],
        target=State.BLOCKED,
    )
    def transition_to_blocked(self) -> None:
        pass

    @transition(field=state, source=State.IN_PROGRESS, target=State.COMPLETED)
    def transition_to_completed(self) -> None:
        pass

    class Meta:
        abstract = True
