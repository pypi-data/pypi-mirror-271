import enum


class ChromosomeType(enum.Enum):
    Autosome = 0
    X = 1
    Y = 2
    Mitochondrial = 3
    Other = 4
    Unmapped = 5