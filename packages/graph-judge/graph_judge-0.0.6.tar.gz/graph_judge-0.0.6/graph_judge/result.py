class Result(object):
    def __init__(self, judge_names, values, members):
        self.judge_resultset = {judge_names[i]: values[i] for i in range(len(judge_names))}
        self.members = members

    def __str__(self):
        desc = ",".join(["=".join(i) for i in self.judge_resultset.items()])
        return f"Result(members:{len(self.members)}, {desc})"


class Results(object):
    def __init__(self, judge_names, groupings, groupings_result_map):
        results = []
        for group_hash, group_members in groupings.items():
            res = Result(judge_names, groupings_result_map[group_hash], group_members)
            results.append(res)

        self._results: list[Result] = results

    def __str__(self):
        if len(self._results) > 0:
            res = list(self._results[0].judge_resultset.keys())
        else:
            res = []
        return "Results(" + ",".join(res) + ")"

    @staticmethod
    def from_resultlist(result_list: list[Result]) -> 'Results':
        if isinstance(result_list, list):
            if len(result_list) > 0:
                if isinstance(result_list[0], Result):
                    r = Results({}, {}, {})
                    r._results = result_list
                    return r
            else:
                return Results({}, {}, {})

        raise ValueError("result_list passed was not a list of Results objects!")

    def get_resultsets(self):
        return [res.judge_resultset for res in self._results]

    def filter(self, judge_name, result_val):
        filtered = []
        for res in self._results:
            if res.judge_resultset.get(judge_name) == result_val:
                filtered.append(res)

        return Results.from_resultlist(filtered)

    def members(self):
        mem = set()
        for res in self._results:
            for el in res.members:
                mem.add(el)
        return list(mem)
