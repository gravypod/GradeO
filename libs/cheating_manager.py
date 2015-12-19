import ast
from libs.finished_manager import FinishedLabHandler
from itertools import combinations

__author__ = 'Joshua D. Katz'

"""
Warning: You may think that at some time touching this code will be a good idea.
You are mistaken.

This should be classified as a biohazard.
Do not touch it.
"""


def levenshtein_ast_difference(first, second):
    # Original idea came from SOF
    if type(first) is not type(second):  # Not equal case
        return 1

    if isinstance(first, ast.AST):

        var_pairs = []
        for k, v in vars(first).items():
            if k in ("lineno", "col_offset", "ctx"):
                continue

            try:
                attr = getattr(second, k)
            except:
                attr = None

            var_pairs.append((v, attr))

        test_set = [levenshtein_ast_difference(*pair) + 1 for pair in var_pairs]
        if not test_set:
            return 1
        return max(test_set)

    if isinstance(first, list):
        if not isinstance(second, list):
            return 1

        if not first or not second:
            return 1
        test_set = [levenshtein_ast_difference(*pair) + 1 for pair in zip(first, second)]
        if not test_set:
            return 1
        return max(test_set)

    return 0 if first == second else 1


def module_len(module):
    if isinstance(module, ast.AST):

        total = 0
        for k, v in vars(module).items():
            if k in ("lineno", "col_offset", "ctx"):
                continue

            total += module_len(v)
        return total + 1

    if isinstance(module, list):
        return len(module) + 1
    # print(str(type(module)))
    return sum([module_len(x) for x in module.body])


class CheatingManager(FinishedLabHandler):
    def __init__(self, run):
        self.run = run

    def handle_labs(self, lab_scores):

        if not self.run:
            return

        lab_asts = {}

        for lab in lab_scores:
            path = lab.lab_path
            with open(path) as handle:
                try:
                    compiled = ast.parse(handle.read(), path)
                except:
                    continue
                # print("%s %d" % (lab.ucid, module_len(compiled)))
                lab_asts[lab] = (compiled, module_len(compiled))
        all_combinations = combinations(lab_asts.items(), 2)
        diffthresh = [x[1] for x in lab_asts.values()]

        mind = min(diffthresh)
        maxd = max(diffthresh)

        threash = mind + ((maxd - mind) / 2)

        all_distances = [(c[0][0], c[1][0]) for c in all_combinations if
                         levenshtein_ast_difference(c[0][1][0], c[1][1][0]) >= threash]
        for c, v in all_distances:
            print("Lab from %s and %s might be similar" % (c.ucid, v.ucid))

    def handle_lab(self, lab, broken=False):
        pass
