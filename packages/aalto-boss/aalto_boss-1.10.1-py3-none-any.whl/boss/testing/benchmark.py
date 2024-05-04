import datetime
import itertools
import logging
import pickle
import socket
from pathlib import Path
from typing import *

from boss import __version__
from boss.bo.bo_main import BOMain
from boss.bo.results import BOResults
from boss.utils.os import execute_in


class KeywordMixer:
    def __init__(
        self, variable_keywords: dict, mixing: Union[str, dict] = "product"
    ) -> None:
        """Helper class for combining variable keywords.

        This class is used by the Benchmarker class to form, and iterate over, zipped lists and
        carteisan products (here called mixes) of any variable keywords used by the Benchmarker.
        How the variable keywords are mixed together is determined by the mixing argument.

        Parameters
        ----------
        variable_keywords : dict
            A mapping from keywords to lists of their allowed values.
        mixing : Union[str, dict]
            Determines how the variable keywords should be mixed together.
            If mixing = 'zip' or 'proudct', all variable keywords will either be
            zipped together or their carteisan proudct will be used. It is also possible
            to pass a dict that maps 'zip' to a list of keywords that should be zipped
            and 'product' to a list of keywords over which a subsequent carteisan product
            will be taken (including any previous zipped values). In other words, mixing
            = {'zip': ['foo', 'bar'], 'proudct': ['baz']} will zip the values of foo and
            bar and the take the product with the values of baz.
        """
        self.variable_keywords = variable_keywords
        self.mixing_plan = {"zip": [], "product": []}
        if isinstance(mixing, str):
            self.mixing_plan[mixing] = list(variable_keywords.keys())
        else:
            for k in variable_keywords:
                if k in mixing.get("zip", []):
                    self.mixing_plan["zip"].append(k)
                else:
                    self.mixing_plan["product"].append(k)
        self.keys_mix, self.vals_mix, self.inds_mix = self._mix()
        self.iter_vals_mix = iter(self.vals_mix)
        self.iter_inds_mix = iter(self.inds_mix)

    def _mix(self) -> Tuple[list, list, list]:
        """Mixes keywords together according to the given mixing plan."""
        var_kws = self.variable_keywords
        vals_mix = []
        inds_mix = []

        # First we handle zipping
        keys_zip = self.mixing_plan["zip"]
        kws_zip = {k: var_kws[k] for k in keys_zip}
        if len(keys_zip) >= 2:
            vals_zip = list(zip(*kws_zip.values()))
            vals_mix.append(vals_zip)
            inds_zip = list(zip(*[range(len(vals)) for vals in kws_zip.values()]))
            inds_mix.append(inds_zip)

        # After zipping we handle products (that may involve zipped keywords)
        keys_prod = self.mixing_plan["product"]
        kws_prod = {k: var_kws[k] for k in keys_prod}
        vals_mix.extend(list(kws_prod.values()))
        vals_mix = list(itertools.product(*vals_mix))
        inds_prod = [list(range(len(vals))) for vals in kws_prod.values()]
        inds_mix.extend(inds_prod)
        inds_mix = list(itertools.product(*inds_mix))

        # Flatten all zipped keywords
        if len(keys_zip) >= 2:
            vals_mix = [v[0] + (v[1],) for v in vals_mix]
            inds_mix = [i[0] + (i[1],) for i in inds_mix]

        keys_mix = keys_zip + keys_prod
        return keys_mix, vals_mix, inds_mix

    def __iter__(self) -> "KeywordMixer":
        return self

    def __next__(self) -> Tuple[Tuple[int], Dict[str, Any]]:
        """Makes the mixer iterable, returning indicies and mixed keywords. 
        
        Returns
        -------
        inds : Tuple[int]
            The indices are a tuple (i1, i2, ..., ik, ...) where ik is the index of
            the k-th keyword value as it appears in the variable_keywords dict,
            i.e. (3, 4) means the 3rd value of the first keyword and the 4th value
            of the 2nd keyword.

        keywords : Dict[str, Any]
            The mixed keywords and their values.
        """
        inds = next(self.iter_inds_mix)
        keywords = {k: v for k, v in zip(self.keys_mix, next(self.iter_vals_mix))}
        return inds, keywords


def _store_results_default(bo_results: BOResults) -> Dict[str, Any]:
    """Default function for storing BO results in the benchmarker.

    Parameters
    ----------
    bo_results : BOResults
        The benchmarker will automatically pass any new BOResults objects
        to this function so results and be selected for storage.
    """
    store = {
        "mu_glmin": float(bo_results.select("mu_glmin", -1)),
        "x_glmin": list(bo_results.select("x_glmin", -1)),
        "userfn_evals": len(bo_results["Y"]),
        "iterpts": bo_results.num_iters - 1,
    }
    return store


def _name_subdir_default(
    keywords: Dict[str, Any], inds_kw_vals: Tuple[int], rep: int
) -> Path:
    """Default function for naming the run folders created by the benchmarker.

    The default name format for the subdirectories is kw{ind_kw}-{ind_val}/run-{rep} where
    ind_kw is the index of a variable keyword as it appears in the variable_keywords property
    of the Benchmarker, ind_val is the index of the current value of that keyword,
    and rep is the current repetition for the current keyword-value combinations.

    Parameters
    ----------
    keywords : Dict[str, Any]
        Keywords used to name the subdir, ignored in the default naming function but can
        be used in custom implementations.
    inds_kw_vals : Tuple[int]
        Indices for the current combination of keyword values.
    rep : int
        The current run repetition.
    """
    p = Path("_".join([f"kw{ind_kw}-{ind_val}" for ind_kw, ind_val in enumerate(inds_kw_vals)]))
    p = p / f"run-{rep}"
    return p


def _name_rep_subdir_default(keywords: Dict[str, Any], inds_kw_vals: Tuple[int], rep: int) -> Path:
    """Default function for naming the repetition run folders created by the benchmarker.

    The default name format for the repetition subdirectories is run-{rep} where
    rep is the current repetition for the current keyword-value combinations.

    Parameters
    ----------
    keywords : Dict[str, Any]
        Keywords used to name the subdir, ignored in the default naming function but can
        be used in custom implementations.
    inds_kw_vals : Tuple[int]
        Indices for the current combination of keyword values, ignored by default.
    rep : int
        The current run repetition.
    """
    return Path(f"run-{rep}")


def _timestamp() -> datetime.datetime:
    """Returns the current date and time in isoformat"""
    return datetime.datetime.now().replace(microsecond=0).isoformat()


class Benchmarker:
    def __init__(
        self,
        fixed_keywords: Optional[dict] = None,
        variable_keywords: Optional[dict] = None,
        rundir: str = "benchmark",
        keyword_mixing: str = "product",
        store_results: Optional[Callable] = None,
        subdir_namer: Optional[Callable] = None,
        loglevel: int = logging.DEBUG,
    ) -> None:
        """Tool for running repeated BOSS runs with different keyword combinations.

        Parameters
        ----------
        fixed_keywords : Optional[dict]
            BOSS keywords that will remain fixed for all runs.
        variable_keywords : Optional[dict]
            BOSS keywords that will change (be looped over) during the runs.
        rundir : str
            The name of a new or existing directory in which the runs will take place.
        keyword_mixing : str
            Mixing scheme for the variable keywords.
        store_results : Optional[Callable]
            A callback function that given a BOResults obejct stores selected results
            and returns them in a dictionary. These results can later be accessed using
            KeywordMixer.results['data'] where they are indexed using the compound index
            for the current run. See the _store_results_default function for a list of the default
            results that are stored.
        subdir_namer : Optional[Callable]
            A callback function that given keyword names, a compound index and repetition
            number, returns a folder name in which to perform the corresponding run.
        loglevel : int
            Logging level of the logger. The logging.DEBUG corresponds to the maximum verbosity.
        """
        if fixed_keywords:
            self.fixed_keywords = fixed_keywords
        else:
            self.fixed_keywords = {}

        if variable_keywords:
            self.variable_keywords = variable_keywords
        else:
            self.variable_keywords = {}

        self.num_repeat = None
        self.keyword_mixing = keyword_mixing
        self.results = {
            "variable_keywords": variable_keywords,
            "fixed_keywords": fixed_keywords,
            "data": {},
        }
        self.rundir = Path(rundir)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(loglevel)
        self.subdir_namer = subdir_namer
        if not store_results:
            store_results = _store_results_default
        self.store_results = store_results

    def add_variable_keyword(self, keyword: str, vals) -> None:
        """Adds a new variable keyword to the benchmarker.

        Parameters
        ----------
        keyword : str
            The name of the keyword to be added.
        vals : List[Any]
            Corresponding values for the specified keyword.
        """
        self.variable_keywords.update({keyword: vals})

    def _init_log(self) -> None:
        """Writes initial info to the logfile."""
        logger = self.logger
        fh = logging.FileHandler(self.rundir / "benchmark.log", mode="a")
        formatter = logging.Formatter("%(message)s")
        fh.setFormatter(formatter)
        logger.addHandler(fh)

        logger.info("=========================")
        logger.info(f"    BOSS BENCHMARKER    ")
        logger.info("=========================")
        logger.info(f"timestamp: {_timestamp()}")
        logger.info(f"BOSS version: {__version__}")
        logger.info(f"host: {socket.gethostname()}")
        logger.info(f"directory: {self.rundir}")

        logger.info("\nfixed keywords:")
        for key, val in self.fixed_keywords.items():
            logger.info(f"{'':>2}{key}: {val}")

        logger.info("\nvariable keyword spans:")
        for key, val in self.variable_keywords.items():
            logger.info(f"{'':>2}{key}: {val}")

        logger.info(f"\nvariable keyword mixing: {self.keyword_mixing}")
        logger.info(f"repetitions per keyword combination: {self.num_repeat}")

    def run(self, num_repeat: int = 50) -> None:
        """Runs the benchmarker for the current (mix of variable) keywords.

        Parameters
        ----------
        num_repeat : int
            The number of repeated runs to do for each combination of keyword values.
        """
        self.num_repeat = num_repeat

        self.rundir.mkdir(exist_ok=True)
        if not self.subdir_namer:
            if len(self.variable_keywords) > 0:
                self.subdir_namer = _name_subdir_default
            else:
                self.subdir_namer = _name_rep_subdir_default

        logger = self.logger
        self._init_log()
        logger.debug("\nCOMMENCING BECHMARK")
        logger.debug("===================\n")

        if len(self.variable_keywords) == 0:
            self._run_repeat()
        else:
            kw_mixer = KeywordMixer(self.variable_keywords, self.keyword_mixing)
            for inds_kw_vals, kws in kw_mixer:
                logger.debug("variable keywords:")
                logger.debug(
                    f"{'':>2}" + " | ".join([f"{k}: {v}" for k, v in kws.items()])
                )
                self._run_repeat(extra_kws=kws, inds=inds_kw_vals)
                logger.debug("\n------------------\n")

    def _run_repeat(
        self, extra_kws: Optional[dict] = None, inds: Optional[Tuple[int]] = None
    ) -> None:
        """Non-user-facing for carrying out the actual repeated BOSS runs.

        Parameters
        ----------
        extra_kws : Optional[dict]
            Extra keywords that are given to BOSS in addition to the fixed keywords,
            usually a combination of variable keywords.
        inds : Optional[Tuple[int]]
            A tuple of indices that indicates where in the data dict the results
            should be stored. Typically these are the indices of the current variable keyword
            values.
        """
        logger = self.logger
        logger.debug(f"repetitions:")
        for rep in range(self.num_repeat):
            dir = self.rundir / self.subdir_namer(extra_kws, inds, rep)
            dir.mkdir(parents=True)
            logger.debug(
                f"{'':>2}{rep}: started {_timestamp()} in {dir.relative_to(dir.parent.parent)}"
            )
            with execute_in(dir):
                bo = BOMain(**self.fixed_keywords, **extra_kws)
                bo_res = bo.run()

                if len(self.variable_keywords) == 0:
                    if len(self.results["data"]) == 0:
                        self.results["data"] = {k: [] for k in res_to_store}
                    for key, val in res_to_store.items():
                        self.results["data"][key].append(val)
                else:
                    res_to_store = self.store_results(bo_res)
                    if not self.results["data"].get(inds):
                        self.results["data"][inds] = {k: [] for k in res_to_store}
                    for key, val in res_to_store.items():
                        self.results["data"][inds][key].append(val)

        with open(self.rundir / "results.pkl", "wb") as fp:
            pickle.dump(self.results, fp)
