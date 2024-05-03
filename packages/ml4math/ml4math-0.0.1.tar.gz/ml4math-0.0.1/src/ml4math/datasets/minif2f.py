"""
The MiniF2F dataset of formal statements math statements aligned to their 
informal counterparts.


Reference:
* https://github.com/facebookresearch/miniF2F/tree/main
* Draft, Sketch, and Prove: Guiding Formal Theorem Provers with Informal Proofs, 
https://arxiv.org/abs/2210.12283
"""
import json
from abc import abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Sequence

import git

from ml4math.datasets.config import DEFAULT_CACHE_DIR


@dataclass
class MiniF2FQuestion:
    formal_statement: str
    informal_statement: str
    informal_proof: str | None = None
    formal_proof: str | None = None
    id: str | int | None = None


class MiniF2F:
    """The MiniF2F dataset with informal statements.

    Currently this only support the Isabelle formal statements.


    Example
    -------
    >>> minif2f = MiniF2F()
    >>> minif2f[0].informal_statement
    # string with the informal math statement for the first question in the dataset.
    >>> minif2f[0].formal_statement
    # string with the formal math statement for the first question in the dataset.
    >>> minif2f[0].question_id
    # string with the question id for the first question in the dataset.
    >>> miniF2F[0].informal_proof
    # string with the informal proof for the first question in the dataset.
    >>> len(miniF2F)
    # number of questions in the dataset.
    """

    git_url = "https://github.com/facebookresearch/miniF2F.git"
    repo_dir = "miniF2F"
    supported_languages = ["isabelle"]

    def __init__(
        self,
        language: Literal["isabelle"] = "isabelle",
        root: str | Path = DEFAULT_CACHE_DIR,
        split: Literal["val", "test", "all"] = "all",
        download: bool = True,
    ):
        """Initialize the MiniF2F dataset.

        Args:
            language: The formal language to be used for formal statement.  Currently only
                "isabelle" is supported.
            root: The root directory to store the dataset. The default is specified by
                DEFAULT_CACHE_DIR = ~/.ml4math/datasets
            split: The data split to use. Either "val", "test", or "all".
            download: Whether to download the dataset from the git repository. If True,
                this will not be downloaded if the directory already exists.
        """
        self.root = Path(root)
        if download:
            self.download()

        self.language = language
        if self._verify_language():
            self.loader = self._get_loader()
            self.formal_dir = self._get_formal_dir()
            self.informal_dir = self._get_informal_dir()
        else:
            raise ValueError(f"Invalid language: {language} must be 'isabelle'")
        self.split: Literal["val", "test", "all"] = split
        self.data = self.load_data()

    def __getitem__(self, idx):
        return self.data[idx]

    def __len__(self):
        return len(self.data)

    def download(self):
        """Downloads the data if it does not exist."""
        if self._check_git_exists():
            return

        git.Repo.clone_from(self.git_url, self.root / self.repo_dir)

    def load_data(self) -> Sequence[MiniF2FQuestion]:
        """Loads the underlying data of formal and informal statements.


        Returns:
            Sequence: The list of MiniF2F questions.
        """
        formal_dir = add_split_to_dir(self.formal_dir, self.split)
        informal_dir = add_split_to_dir(self.informal_dir, self.split)
        return self.loader.load_data(formal_dir, informal_dir)

    def get_question(self, id: str):
        """Get a question by its id."""
        for question in self.data:
            if question.id == id:
                return question
        return None

    def _verify_language(self):
        if self.language in self.supported_languages:
            return True
        return False

    def _check_git_exists(self):
        return (self.root / self.repo_dir).exists()

    def _get_loader(self):
        if self.language == "isabelle":
            return IsabelleLoader()
        else:
            raise ValueError(f"Invalid language: {self.language}")

    def _get_formal_dir(self):
        return self.root / self.repo_dir / self.language

    def _get_informal_dir(self):
        return self.root / self.repo_dir / "informal"


class Loader:
    @abstractmethod
    def load_data(
        self, formal_dir: str, informal_dir: str
    ) -> Sequence[MiniF2FQuestion]:
        pass


class IsabelleLoader(Loader):
    def load_data(
        self, formal_dir: str, informal_dir: str
    ) -> Sequence[MiniF2FQuestion]:
        """Load the MiniF2F questions from the formal and informal directories.

        Args:
            formal_dir (str): The directory with the formal statements.
            informal_dir (str): The directory with the informal statements.

        Returns:
            Sequence[MiniF2FQuestion]: The list of MiniF2F questions.
        """
        questions = []
        for formal_file in Path(formal_dir).rglob("*.thy"):
            formal_path = formal_file.relative_to(formal_dir)
            informal_file = Path(informal_dir) / formal_path.with_suffix(".json")
            if informal_file.exists():
                with open(formal_file, "r") as f:
                    formal_statement = f.read()
                with open(informal_file, "r") as f:
                    informal_data = json.load(f)

                informal_statement = informal_data.pop("informal_statement")
                informal_proof = informal_data.pop("informal_proof")
                id = informal_data["problem_name"]

                questions.append(
                    MiniF2FQuestion(
                        formal_statement=formal_statement,
                        informal_statement=informal_statement,
                        informal_proof=informal_proof,
                        id=id,
                    )
                )

        return questions


def add_split_to_dir(
    path: str | Path, split: Literal["val", "test", "all"] = "all"
) -> str:
    """Add the split to the directory path."""
    path = Path(path)
    if split == "all":
        return str(path)
    if split == "val":
        split_dir = str(path / "val")
    elif split == "test":
        split_dir = str(path / "test")
    else:
        raise ValueError(
            f"Invalid split: {split}, must be one of " "['val', 'test', 'all']"
        )
    return split_dir
