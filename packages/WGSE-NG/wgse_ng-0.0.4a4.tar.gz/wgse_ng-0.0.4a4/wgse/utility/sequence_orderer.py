import typing


class SequenceOrderer:
    def __init__(self, sequences=typing.List[str]) -> None:
        # Map a canonic name with its index in the original sequences.
        self._sequences : dict[str, int] = {
            SequenceOrderer.canonicalize(x[1]): x[0] for x in enumerate(sequences)
        }
        self._ordered = self._get_ordered()

    def __iter__(self):
        for sequence in self._ordered:
            yield self._sequences[sequence], sequence

    def _get_ordered(self):
        autosome = self._get_autosome()
        sexual = self._get_sexual()
        mitochondrial = self._get_mitochondrial()
        others = self._get_others(autosome, sexual, mitochondrial)
        merged = [*autosome, *sexual, *mitochondrial, *others]
        return merged

    def _get_autosome(self):
        autosome = [x for x in self._sequences if x.isnumeric()]
        autosome.sort(key=lambda x: int(x))
        return autosome

    def _get_mitochondrial(self):
        return [x for x in self._sequences if x == "m"]

    def _get_sexual(self):
        sexual = []
        if "x" in self._sequences:
            sexual.append("x")
        if "y" in self._sequences:
            sexual.append("y")
        return sexual

    def _get_others(self, autosome, sexual, mitochondrial):
        others = []
        for sequence in self._sequences.keys():
            is_autosome = sequence in autosome
            is_sexual = sequence in sexual
            is_mitochondrial = sequence in mitochondrial
            if not is_autosome and not is_sexual and not is_mitochondrial:
                others.append(sequence)
        others.sort()
        return others

    def canonicalize(sequence_name: str) -> str:
        normalized = sequence_name.upper()
        if normalized.startswith("CHR"):
            normalized = normalized.replace("CHR", "", 1)
        if normalized.startswith("MT"):
            normalized = normalized.replace("MT", "M", 1)
        return normalized
