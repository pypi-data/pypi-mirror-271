from pathlib import Path

from wgse.reference_genome.metadata_loader import Genome
from wgse.utility.file_type_checker import FileTypeChecker


class GenomeFileFinder:
    def __init__(self, file_type_checker: FileTypeChecker = FileTypeChecker(), repository = Path("metadata")) -> None:
        self.temporary_dir = repository.joinpath("temp")
        self.genomes_dir = repository.joinpath("genomes")
        self.file_type_checker = file_type_checker
        
    def find(self, genome: Genome):
        if genome.fasta.exists():
            if genome.bgzip_size == genome.fasta.stat().st_size:
                return genome.fasta