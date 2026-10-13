"""Single source of truth for student, assignment, seeds, and report metadata.

Optimizer seeds are intentionally distinct from benchmark/data construction and
metric-sampling seeds.  Changing the latter changes the problem or measurement,
not merely an independent optimizer trial.
"""
from dataclasses import dataclass


ALGORITHM_NAMES = (
    "Weighted Sum", "Epsilon-Constraint", "Benson reference improvement",
    "Weight Metric", "Value Function", "Goal Programming", "Lexicographic",
    "TOPSIS", "VIKOR", "VEGA", "MOGA", "NSGA", "NPGA", "NSGA-II",
    "NSGA-III", "SPEA2", "PESA-II", "MOEA/D", "MOEA/D-DE", "MOEA/D-ACO",
    "Constrained NSGA-II", "MOPSO", "MOGWO", "MOABC", "MOACO", "MOSA",
    "MODE", "MO-TLBO", "MOBA", "MOMA", "RVEA", "IBEA", "SMS-EMOA",
    "HypE", "R-NSGA-II", "MGDA", "GradNorm",
)


def task_c_algorithm_numbers(roll_suffix: int) -> tuple[int, int, int]:
    """Apply the three assignment formulas to a two-digit roll suffix."""
    if not 0 <= roll_suffix <= 99:
        raise ValueError("roll suffix must be between 00 and 99")
    return (
        ((roll_suffix - 1) % 37) + 1,
        ((roll_suffix + 11) % 37) + 1,
        ((roll_suffix + 23) % 37) + 1,
    )


@dataclass(frozen=True)
class Student:
    name: str
    registration: str
    institution: str
    course: str

    @property
    def roll_suffix(self) -> int:
        if len(self.registration) < 2 or not self.registration.isdigit():
            raise ValueError("registration must be a numeric string")
        return int(self.registration[-2:])


STUDENT = Student(
    name="Sofia Abidi",
    registration="241071072",
    institution="Veermata Jijabai Technological Institute",
    course="B.Tech Computer Engineering",
)

ROLL_SUFFIX = STUDENT.roll_suffix
TASK_C_ALGORITHM_NUMBERS = task_c_algorithm_numbers(ROLL_SUFFIX)
TASK_C_ALGORITHMS = tuple(
    (number, ALGORITHM_NAMES[number - 1]) for number in TASK_C_ALGORITHM_NUMBERS
)

# Independent optimizer trials.  The first value is also the CLI single-run default.
OPTIMIZER_SEEDS = tuple(range(ROLL_SUFFIX * 10, ROLL_SUFFIX * 10 + 10))
DEFAULT_OPTIMIZER_SEED = OPTIMIZER_SEEDS[0]

# Fixed problem/data definitions: do not substitute optimizer seeds here.
P8_INSTANCE_SEED = 7
P9_FOLD_SEED = 63
NETWORK_DATA_SEED = 63
DTLZ_REFERENCE_SEED_OFFSET = 100

# Fixed metric sampling: identical points must be used across algorithms.
HV_MONTE_CARLO_SEED = 991
HV_MONTE_CARLO_SAMPLES = 8192

REPORT_TITLE = "Lab Assignment 7: Multiobjective Optimization"
ASSIGNMENT_ISSUED = "5 October 2026"
ACTIVE_PROVENANCE = f"roll{ROLL_SUFFIX}"

