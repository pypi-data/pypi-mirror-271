from pathlib import Path

from wgse.external import External
from wgse.reference_genome.metadata_loader import Genome


class BGZIPCompressor:
    def __init__(self, external: External = External()) -> None:
        self._external = external

    def perform(self, genome: Genome, file: Path) -> Path:
            return self._external.bgzip_wrapper(file, genome.fasta)