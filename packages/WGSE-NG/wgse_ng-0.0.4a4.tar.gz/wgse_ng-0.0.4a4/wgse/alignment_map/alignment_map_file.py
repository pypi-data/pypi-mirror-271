import logging
import subprocess
from pathlib import Path

from wgse.alignment_map.alignment_map_header import AlignmentMapHeader
from wgse.alignment_map.alignment_stats_calculator import \
    AlignmentStatsCalculator
from wgse.alignment_map.index_stats_calculator import (IndexStatsCalculator,
                                                       SequenceStatistics)
from wgse.data.alignment_map_file_info import (AlignmentMapFileInfo,
                                               AlignmentMapFileType,
                                               MitochondrialDNAType)
from wgse.data.chromosome_type import ChromosomeType
from wgse.data.gender import Gender
from wgse.data.sorting import Sorting
from wgse.external import External
from wgse.reference_genome.repository_manager import RepositoryManager
from wgse.utility.sequence_orderer import SequenceOrderer

logger = logging.getLogger(__name__)


class AlignmentMapFile:
    SUPPORTED_FILES = {
        ".bam": AlignmentMapFileType.BAM,
        ".sam": AlignmentMapFileType.SAM,
        ".cram": AlignmentMapFileType.CRAM,
    }

    LENGTH_TO_MITOCHONDRIAL_TYPE = {
        16569: MitochondrialDNAType.rCRS,
        16571: MitochondrialDNAType.Yoruba,
    }

    def __init__(
        self,
        path: Path,
        external: External = External(),
        repository: RepositoryManager = RepositoryManager(),
    ) -> None:
        if isinstance(path, str):
            path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Unable to find file {path.name}")
        if path.suffix.lower() not in AlignmentMapFile.SUPPORTED_FILES:
            raise RuntimeError(f"Unrecognized file extension: {path.name}")

        self.path = path
        self._repo = repository
        self._external = external
        self.header = self._load_header()
        self.file_info = self._initialize_file_info()

    def _load_header(self) -> AlignmentMapHeader:
        lines = self._external.samtools(
            ["view", "-H", "--no-PG", self.path], stdout=subprocess.PIPE, wait=True
        )
        lines = lines.decode().split("\n")
        return AlignmentMapHeader(lines)

    def _initialize_file_info(self):
        file_info = AlignmentMapFileInfo()
        file_info.path = self.path
        file_info.file_type = AlignmentMapFile.SUPPORTED_FILES[self.path.suffix.lower()]
        file_info.sorted = self.header.metadata.sorted
        file_info.name_type_mtdna = self.header.mtdna_name_type()
        file_info.name_type_chromosomes = self.header.chromosome_name_type()
        file_info.sequence_count = self.header.sequence_count()
        file_info.indexed = self._indexed(file_info.file_type)
        file_info.gender = Gender.Unknown
        file_info.reference_genome = self._repo.find(list(self.header.sequences.values()))
        file_info.mitochondrial_dna_type = self.get_mitochondrial_dna_type(file_info)
        
        if file_info.indexed:
            indexed_stats = IndexStatsCalculator(self.path)
            file_info.index_stats = indexed_stats.get_stats()
            file_info.gender = self.get_gender(file_info.index_stats)
        if file_info.sorted == Sorting.Coordinate:
            calculator = AlignmentStatsCalculator(file_info)
            file_info.alignment_stats = calculator.get_stats()
        return file_info

    def get_mitochondrial_dna_type(self, file_info):
        if self.header.sequences is not None:
            sequences = {
                SequenceOrderer.canonicalize(x.name): x
                for x in self.header.sequences.values()
            }
            if "M" not in sequences:
                return MitochondrialDNAType.Unknown
            elif sequences["M"].length in AlignmentMapFile.LENGTH_TO_MITOCHONDRIAL_TYPE:
                return AlignmentMapFile.LENGTH_TO_MITOCHONDRIAL_TYPE[
                    sequences["M"].length
                ]
        return MitochondrialDNAType.Unknown

    def _indexed(self, type=None):
        if type == None:
            type = self.file_info.file_type

        file = str(self.path)
        if type == AlignmentMapFileType.BAM:
            return Path(file + ".bai").exists()
        elif type == AlignmentMapFileType.CRAM:
            return Path(file + ".crai").exists()
        return False
    
    def get_gender(self, stats :list[SequenceStatistics]):
        x_stats = [x for x in stats if x.type == ChromosomeType.X]
        y_stats = [x for x in stats if x.type == ChromosomeType.Y]
        x_length = 0
        y_length = 0
        
        if len(x_stats) != 0 and len(x_stats) != 1:
            return Gender.Unknown
        
        if len(y_stats) != 0 and len(y_stats) != 1:
            return Gender.Unknown
        
        if len(x_stats) == 1:
            x_length = x_stats[0].mapped + x_stats[0].unmapped
        if len(y_stats) == 1:
            y_length = y_stats[0].mapped + y_stats[0].unmapped
        
        if x_length == 0 and y_length == 0:
            return Gender.Unknown
        elif y_length == 0 or (x_length / y_length) > 20:
            return Gender.Female
        else:
            return Gender.Male