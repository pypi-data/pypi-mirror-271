import configparser
import logging
import multiprocessing
from pathlib import Path

import wgse


class WGSEDefaults:
    """Specify some directory where to find configuration files."""

    WGSE_FOLDER = Path(wgse.__file__).parents[1]
    PROGRAM_CONFIG = Path(WGSE_FOLDER, "configuration", "main.ini")
    RELEASE_CONFIG = Path(Path.home(), ".wgse", "main.ini")


class GeneralConfig:
    def __init__(self) -> None:
        self.last_path: Path = Path.home()


class ExternalConfig:
    def __init__(self) -> None:
        self.root: Path = Path(WGSEDefaults.WGSE_FOLDER, "3rd_party")
        self.threads: int = multiprocessing.cpu_count()


class RepositoryConfig:
    def __init__(self) -> None:
        self.repository: Path = Path(WGSEDefaults.WGSE_FOLDER, "repository")
        self.metadata: Path = Path(self.repository, "metadata")
        self.temporary: Path = Path(self.repository, "temp")


class AlignmentStatsConfig:
    def __init__(self) -> None:
        self.skip: int = 40000
        self.samples: int = 20000


EXTERNAL_CFG: ExternalConfig = None
REPOSITORY_CFG: RepositoryConfig = None
GENERAL_CFG: GeneralConfig = None
ALIGNMENT_STATS_CFG: AlignmentStatsConfig = None


class ConfigurationManager:
    def __init__(self) -> None:
        self._section_map = {
            "general": ("GENERAL_CFG", GeneralConfig),
            "external": ("EXTERNAL_CFG", ExternalConfig),
            "repository": ("REPOSITORY_CFG", RepositoryConfig),
            "alignment_stats": ("ALIGNMENT_STATS_CFG", AlignmentStatsConfig),
        }
        self.load()

    def load(self) -> None:
        self._parser = configparser.ConfigParser()
        self._parser.read(WGSEDefaults.PROGRAM_CONFIG)
        self._parser.read(WGSEDefaults.RELEASE_CONFIG)

        for section, value in self._section_map.items():
            (var, class_name) = value
            globals()[var] = class_name()
            if section not in self._parser:
                continue
            for key, value in self._parser[section].items():
                if key not in globals()[var].__dict__:
                    logging.warning(f"Configuration {section}.{key} not known")
                    continue
                if value is None:
                    continue
                var_type = type(globals()[var].__dict__[key])
                globals()[var].__dict__[key] = var_type(value)

    def save(self):
        for section, value in self._section_map.items():
            (var, _) = value
            for key, value in globals()[var].__dict__.items():
                if section not in self._parser:
                    self._parser.add_section(section)
                self._parser[section][key] = str(value)
        for config in [WGSEDefaults.RELEASE_CONFIG, WGSEDefaults.PROGRAM_CONFIG]:
            if not config.exists():
                continue
            with config.open("wt") as f:
                self._parser.write(f)


MANAGER_CFG = None
if MANAGER_CFG is None:
    MANAGER_CFG = ConfigurationManager()
