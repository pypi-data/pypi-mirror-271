import enum
from pathlib import Path

from wgse.alignment_map.index_stats_calculator import SequenceStatistics
from wgse.data.alignment_stats import AlignmentStats
from wgse.data.chromosome_type import ChromosomeType
from wgse.data.gender import Gender
from wgse.data.sorting import Sorting
from wgse.fasta.reference import Reference


class MTDNANameType(enum.Enum):
    chrM = enum.auto()
    MT = enum.auto()
    chrMT = enum.auto()
    M = enum.auto()
    Accession = enum.auto()


class ChromosomeNameType(enum.Enum):
    Chr = enum.auto()
    Number = enum.auto()
    Accession = enum.auto()


class MitochondrialDNAType(enum.Enum):
    rCRS = enum.auto()
    Yoruba = enum.auto()
    RSRS = enum.auto()
    Unknown = enum.auto()


class AlignmentMapFileType(enum.Enum):
    BAM = enum.auto()
    SAM = enum.auto()
    CRAM = enum.auto()


class AlignmentMapFileInfo:
    def __init__(self) -> None:
        self.path: Path = None
        self.sorted: Sorting = None
        self.indexed: bool = None
        self.file_type: AlignmentMapFileType = None
        self.reference_genome: Reference = None
        self.is_y_only: bool = None
        self.is_mt_only: bool = None
        self.mitochondrial_dna_type: MitochondrialDNAType = None
        self.build: int = None
        self.name_type_chromosomes: ChromosomeNameType = None
        self.name_type_mtdna: MTDNANameType = None
        self.sequence_count: int = None
        self.primary: bool = None
        self.alignment_stats: AlignmentStats = None
        self.index_stats: dict[ChromosomeType, list[SequenceStatistics]] = None
        self.gender: Gender = None
