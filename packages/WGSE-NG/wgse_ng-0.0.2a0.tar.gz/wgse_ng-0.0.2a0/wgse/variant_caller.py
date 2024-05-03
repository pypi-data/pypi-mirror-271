from wgse.alignment_map.alignment_map_file import AlignmentMapFile
from wgse.external import External


class VariantCaller:
    def __init__(self, external: External = External()) -> None:
        self._external = external

    def call(self, aligned_file : AlignmentMapFile):
        self._external.bcftool(["mpileup", "-B", "-I", "-C", "50", "{chrM}", "-T", "24", "-f", aligned_file.file_info.reference_genome, "-Ou", aligned_file.path])
        self._external.bcftool(["call", "--ploidy", "{ploidy}" , "-mv", "-P", "0", "--threads", "24", "-Oz", "-o", "{output_file}"])
        self._external.tabix(["{chrM_qFN}"])

# {bcftools} mpileup -B -I -C 50 -r  -f {refgenome_qFN} -Ou {wgse.BAM.file_qFN}
# {bcftools} call --ploidy {ploidy} -mv -P 0 --threads {cpus} -Oz -o {chrM_qFN}
# {tabix} {chrM_qFN}