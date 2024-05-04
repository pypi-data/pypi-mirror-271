import typing

from wgse.data.reference import Genome, Sequence
from wgse.reference_genome.metadata_loader import MetadataLoader
from wgse.reference_genome.repository_manager import RepositoryManager


class Finder:
    def __init__(
        self,
        metadata: MetadataLoader = MetadataLoader(),
        repository: RepositoryManager = RepositoryManager()
    ) -> None:
        if metadata is None:
            raise RuntimeError("Metadata cannot be None")

        self._metadata = metadata
        self._repository = repository

    def find_genome_1(self, sequences: typing.List[Sequence]):
        [x.md5 for x in sequences]

    def find_genome(self, sequences: typing.List[Sequence]):
        # Given a list of name/length/MD5, find a sequence that
        # matches.
        genomes = self._metadata.load()

        # Attempt 1: Exact sequence
        for genome in genomes:
            if genome.sequences is None:
                continue
            if genome.sequences == sequences:
                return genome

        # Attempt 2: ignore the name, ignore the order. Restrict the search to a specific genome.
        for genome in genomes:
            if genome.sequences is None:
                continue
            matches = {x: False for x in sequences}
            for sequence_1 in sequences:
                for sequence_2 in genome.sequences:
                    if sequence_1.md5 == sequence_2.md5:
                        matches[sequence_1] = sequence_2
            if all(matches.values()):
                return genome

        # Attempt 3: ignore the name, ignore the order. Search in every known reference genomes.
        matches = {x: False for x in sequences}
        for genome in genomes:
            if genome.sequences is not None:
                for sequence_1 in sequences:
                    for sequence_2 in genome.sequences:
                        if sequence_1.md5 == sequence_2.md5:
                            matches[sequence_1] = sequence_2

        if all([True for x in matches.values() if x if not False]):
            return matches
