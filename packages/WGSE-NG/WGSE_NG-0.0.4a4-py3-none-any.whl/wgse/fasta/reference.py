from collections import OrderedDict

from wgse.data.reference import Genome, Sequence


class SequenceMatch:
    def __init__(self, name, length, md5, order) -> None:
        self.name = name
        self.length = length
        self.md5 = md5
        self.order = order

    def is_perfect(self):
        if self.md5 is not None:
            return self.name and self.length and self.md5 and self.order
        return self.name and self.length and self.order
        

class Reference:
    def __init__(self, reference_map: OrderedDict[Sequence, list[Sequence]]):
        self.reference_map = reference_map
        self.genome_map = self._index_by_genome()
        self.perfect_match = self._get_genome_percentage_cover(True)
        self.non_perfect_match = self._get_genome_percentage_cover()
        self.percentage_cover = self._get_genome_percentage_cover()
        self.md5_available = self._md5_available()

    def _get_percentage_cover(self):
        at_least_one_match = [len(x)>0 for x in list(self.reference_map.values())].count(True)
        percentage = at_least_one_match/len(self.reference_map)
        return percentage*100

    def _md5_available(self):
        return all([x.md5 is not None for x in self.reference_map.keys()])

    def _index_by_genome(self) -> dict[Genome, dict[Sequence, SequenceMatch]]:
        genome_map = {}
        for index, reference_match in enumerate(self.reference_map.items()):
            sequence, matching = reference_match
            for match in matching:
                if match.parent not in genome_map:
                    genome_map[match.parent] = {
                        x: SequenceMatch(False, False, False, False)
                        for x in self.reference_map.keys()
                    }
                md5_match = True
                if sequence.md5 is not None:
                    md5_match = match.md5 == sequence.md5
                name_match = match.name == sequence.name
                length_match = match.length == sequence.length
                order_match = False
                if len(match.parent.sequences) > index:
                    order_match = match.parent.sequences[index] == match

                genome_map[match.parent][sequence] = SequenceMatch(
                    name_match, length_match, md5_match, order_match
                )
        return genome_map

    def _get_genome_percentage_cover(self, perfect:bool = False):
        genome_percentage = {}
        string = ""
        for genome, matching in self.genome_map.items():
            percentage_matching = 0
            if perfect:
                percentage_matching = [x.is_perfect() for x in matching.values()].count(True) / len(matching)
            else:
                md5_matching = [x.md5 for x in matching.values()]
                md5_matching = [x.length for x in matching.values()]
                
            percentage_matching *= 100
            genome_percentage[genome] = percentage_matching
            string += f"{genome} ({percentage_matching:.1f}%) "
        return genome_percentage
