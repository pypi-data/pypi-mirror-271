import enum
import pathlib
import subprocess
import sys
import os
import shutil

if "win" in sys.platform:
    """On windows we expect to find all the 
    executables under .\\3rd_party (if not specified 
    differently). On other OSs the executables need 
    to be under path.
    """
    third_party = str(pathlib.Path(".", "3rd_party"))
    if third_party not in os.environ["PATH"]:
        os.environ["PATH"] += ";" + third_party
    if ".JAR" not in os.environ["PATHEXT"]:
        os.environ["PATHEXT"] += ";.JAR"


class BgzipAction(enum.Enum):
    Compress = 0
    Decompress = 1
    Reindex = 2


def run(f, interpreter=[]):
    """This decorator will return a function that will try to launch
    an executable from disk that has the same name of the function
    it's decorating, passing the arguments that were received when
    the function was invoked.

    Args:
        f (Callable): function to decorate.
    """

    def execute_binary(self, args=[], stdout=None, stdin=None, stderr=None, wait=False):
        args = [*interpreter, f.__name__, *[str(x) for x in args]]

        if wait:
            # Force stdout/stderr to be PIPE as we
            # need to collect the output
            stdout = subprocess.PIPE
            stderr = subprocess.PIPE

        output = subprocess.Popen(args, stdout=stdout, stdin=stdin, stderr=stderr)
        if wait == True:
            out, err = output.communicate()
            if output.returncode != 0:
                raise RuntimeError(f"Call to {f.__name__} failed: {err.decode()}")
            return out
        return output

    return execute_binary


def jar(f):
    """Same thing as run but this deals with .jar files 
    automatically, invoking java from PATH and specifying 
    the right arguments, including the full path of the .jar
    file.

    Args:
        f (callable): function to decorate

    Returns:
        callable: Decorated function
    """
    full_path = shutil.which(f.__name__)
    if full_path is None:
        return f
    full_path = pathlib.Path(".", full_path)
    full_path = full_path.with_suffix(".jar")
    f.__name__ = str(full_path)
    return run(f, ["java", "-jar"])


class External:
    """Wrapper around 3rd party executables"""

    def __init__(self, installation_directory: pathlib.Path = None, threads = None) -> None:
        if installation_directory is not None:
            if not installation_directory.exists():
                raise FileNotFoundError(
                    f"Unable to find root directory for External: {str(installation_directory)}"
                )
            if str(installation_directory) not in os.environ["PATH"]:
                os.environ["PATH"] += ";" + str(installation_directory)
        if threads is None:
            threads = 32

        self.threads = threads
        self._htsfile = "htsfile"
        self._samtools = "samtools"
        self._bgzip = "bgzip"
        self._gzip = "gzip"

    def get_file_type(self, path: pathlib.Path):
        process = subprocess.run([self._htsfile, path], capture_output=True, check=True)
        return process.stdout.decode("utf-8")

    def fasta_index(self, path: pathlib.Path, output: pathlib.Path = None):
        if output is None:
            output = pathlib.Path(str(path) + ".fai")

        arguments = [self._samtools, "faidx", path, "-o", output]
        process = subprocess.run(arguments, check=True, capture_output=True)
        return process.stdout.decode("utf-8")

    def view(self, file: pathlib.Path, output: pathlib.Path, *args):
        arguments = [self._samtools, "view", "-H", "--no-PG", *args, file]
        process = subprocess.run(arguments, check=True, capture_output=True)
        return process.stdout.decode("utf-8")

    def make_dictionary(self, path: pathlib.Path, output: pathlib.Path = None):
        if output is None:
            output = pathlib.Path(path.parent, path.name + ".dict")
        arguments = [self._samtools, "dict", str(path), "-o", str(output)]
        process = subprocess.run(arguments, check=True, capture_output=True)
        return process.stdout.decode("utf-8")
    
    def index(self, path: pathlib.Path):
        return self.samtools(["index", "-@", self.threads, "-b", str(path)], wait=True)

    def _gzip_filename(self, input: pathlib.Path, action: BgzipAction):
        if action == BgzipAction.Compress:
            return pathlib.Path(str(input) + ".gz")
        elif action == BgzipAction.Decompress:
            if len(input.suffixes) == 0:
                raise RuntimeError(
                    f"Unable to determine decompressed filename, invalid filename {str(input)} (no extensions)."
                )
            return input.with_suffix("")
        elif action == BgzipAction.Reindex:
            return pathlib.Path(str(input) + ".gzi")
        else:
            raise RuntimeError(f"Action {action.name} not supported.")

    def gzip(
        self,
        input: pathlib.Path,
        output: pathlib.Path,
        action: BgzipAction = BgzipAction.Decompress,
    ) -> pathlib.Path:
        if output.exists():
            raise RuntimeError(
                f"Trying to decompress {str(input)} but the destination file {str(output)} exists."
            )
        inferred_filename = self._gzip_filename(input, action)

        action_flags = {BgzipAction.Compress: "", BgzipAction.Decompress: "-d"}

        arguments = [self._gzip, action_flags[action], str(input)]
        process = subprocess.run(arguments, capture_output=True)

        if process.returncode != 0:
            # RAFZ format is libz compatible but will make gzip sometime exit
            # with a != 0 code, complaining about "trailing garbage data".
            # This is not a real error, as the file is decompressed anyway.
            # The issue is potentially fixable by truncating the file, but
            # there's no practical advantage in doing so. If we fall in this
            # situation, ignore the error.
            if "trailing garbage" not in process.stderr.decode():
                raise RuntimeError(
                    f"gzip exited with return code {process.returncode}: {process.stderr.decode()}"
                )

        if inferred_filename != output:
            inferred_filename.rename(output)

    def bgzip_wrapper(
        self,
        input: pathlib.Path,
        output: pathlib.Path,
        action: BgzipAction = BgzipAction.Compress,
    ) -> pathlib.Path:
        if output.exists():
            output.unlink()

        action_flags = {
            BgzipAction.Compress: "-if",
            BgzipAction.Decompress: "-d",
            BgzipAction.Reindex: "-r",
        }
        inferred_filename = self._gzip_filename(input, action)

        out = self.bgzip([action_flags[action], str(input), "-@", "32"], wait=True)
        if inferred_filename != output:
            inferred_filename.rename(output)
            if action == BgzipAction.Compress:
                inferred_gzi_filename = pathlib.Path(str(inferred_filename) + ".gzi")
                inferred_gzi_filename.rename(str(output) + ".gzi")

    def idxstats(self, input: pathlib.Path):
        """Generate BAM index statistics"""
        arguments = [self._samtools, "idxstat", input]
        process = subprocess.run(arguments)
        return process.stdout.decode("utf-8")

    def haplogrep_classify(self, vcf_file, output_file):
        output = self.haplogrep(
            ["classify", "--in", vcf_file, "--format", "vcf", "--out", output_file],
            wait=True,
        )
        output.decode("utf-8")
        return output
    
    # Starting from here all the functions are
    # just calling executables with the same name.
    # See the implementation of run and jar decorator
    # for more details.
    
    @run
    def bgzip(self, args=[], stdout=None, stdin=None, wait=False):
        pass

    @run
    def samtools(self, args=[], stdout=None, stdin=None, wait=False):
        pass

    @run
    def bwa(self, args=[], stdout=None, stdin=None, wait=False):
        pass

    @run
    def bwamem2(self, args=[], stdout=None, stdin=None, wait=False):
        pass

    @run
    def minimap2(self, args=[], stdout=None, stdin=None, wait=False):
        pass

    @run
    def fastp(self, args=[], stdout=None, stdin=None, wait=False):
        pass

    @run
    def bcftool(self, args=[], stdout=None, stdin=None, wait=False):
        pass

    @run
    def tabix(self, args=[], stdout=None, stdin=None, wait=False):
        pass

    @jar
    def haplogrep(self, args=[], stdout=None, stdin=None, wait=False):
        pass
    
    @jar
    def FastQC(self, args=[], stdout=None, stdin=None, wait=False):
        pass
    
    @jar
    def picard(self, args=[], stdout=None, stdin=None, wait=False):
        pass
    
    @jar
    def DISCVRSeq(self, args=[], stdout=None, stdin=None, wait=False):
        pass