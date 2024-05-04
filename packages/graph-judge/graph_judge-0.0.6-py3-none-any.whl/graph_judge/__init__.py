import os
from typing import Optional, Any, Callable

from graph_judge.result import Results


class GraphJudge(object):
    def __init__(self, src_set: set[Any]):
        self._src_list: list = list(src_set)
        self._judge_funcs: dict[str, Callable[[str], Any]] = {}
        self._cached_results: dict[str, Any] = {}

    @staticmethod
    def from_directory(directory):
        if not os.path.exists(directory):
            raise ValueError(f"Unable to find directory '{directory}' within current directory '{os.getcwd()}'!")

        files = [os.path.join(directory, f) for f in os.listdir(directory)]
        return GraphJudge(set(files))

    def _hash(self, val) -> str:
        if isinstance(val, list) or isinstance(val, set):
            iterable = val
        elif isinstance(val, dict):
            iterable = list(val.items())
        else:
            return str(hash(val))
        hashes = [self._hash(v) for v in iterable]
        return "L$" + "_".join(hashes)

    def add_judge(self, name: str, judge_func: Callable[[str], Any]):
        if name.startswith("$"):
            raise ValueError("Judge name cannot start with '$'! Char is reserved for internal use")

        self._judge_funcs[name] = judge_func

    def _run_single(self, judge_name: str, use_cached=True) -> list[Any]:
        if judge_name in self._cached_results and use_cached:
            return self._cached_results[judge_name]

        if judge_name not in self._judge_funcs:
            raise ValueError(f"Unknown judge '{judge_name}' Currently registered '{list(self._judge_funcs.keys())}'")

        results = []
        for item in self._src_list:
            results.append(self._judge_funcs[judge_name](item))

        return results

    def _group_resultlist(self, results) -> Results:
        groupings = {}  # hashed_result -> element of _src_list that is this result
        groupings_result_map = {}  # hashed_result -> actual result list
        # For example, a source list of {1,2,3} with two judges j1(x>1), j2(x<2) would give
        # [False, True, True]  [True, False, False]
        # groupings = {_hash([False, True]): [1], _hash([True, False]): [2,3]}
        # groupings_result_map = {_hash([False, True]): [False, True], _hash([True, False]): [True, False]}
        # The actual values are mapped in the groupings_result_map from the hash
        judge_order_list = list(self._judge_funcs.keys())

        for src_idx in range(len(self._src_list)):
            element_results = []
            for judge_idx in range(len(judge_order_list)):
                judge_name = judge_order_list[judge_idx]
                element_results.append(results[judge_name][src_idx])

            hsh = self._hash(element_results)
            self._add_to_listdict(groupings, hsh, self._src_list[src_idx])
            groupings_result_map[hsh] = element_results

        res = Results(judge_order_list, groupings, groupings_result_map)
        return res

    def run_chain_and(self, judge_name_list: list[str], use_cached=True) -> Results:
        # run a chain of functions, and'ing them together for the final result
        for name in judge_name_list:
            if name not in self._judge_funcs:
                raise ValueError(f"Unknown judge '{name}' Currently registered '{list(self._judge_funcs.keys())}'")

        results = {}
        for name in judge_name_list:
            results[name] = self._run_single(name, use_cached=use_cached)

        res = self._group_resultlist(results)
        return res

    def run(self, judge_name, use_cached=True) -> Results:
        reslist = self._run_single(judge_name, use_cached=use_cached)
        res = self._group_resultlist({judge_name: reslist})
        return res

    def _add_to_listdict(self, d, k, el):
        # Add element el to listdict d with key k
        # listdict is a dict of lists, so if k doesn't exist it will need to be created
        if k not in d:
            d[k] = []
        d[k].append(el)
        return d
