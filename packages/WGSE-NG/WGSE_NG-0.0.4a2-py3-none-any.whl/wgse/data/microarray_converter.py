from enum import Enum, auto


class MicroarrayConverterExtensions(Enum):
    CSV = ".csv"
    TXT = ".txt"

class MicroarrayConverterTarget(Enum):
    Ancestry_v1 = auto()
    Ancestry_v2 = auto()
    FTDNA_v1 = auto()
    FTDNA_v2 = auto()
    FTDNA_v3 = auto()
    LivingDNA_v1 = auto()
    LivingDNA_v2 = auto()
    MyHeritage_v1 = auto()
    MyHeritage_v2 = auto()
    TwentyThreeAndMe_v3 = auto()
    TwentyThreeAndMe_v35 = auto()
    TwentyThreeAndMe_v4 = auto()
    TwentyThreeAndMe_v5 = auto()
    TwentyThreeAndMe_SNPs_API = auto()