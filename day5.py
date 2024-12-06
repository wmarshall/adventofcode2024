import itertools
import typing

import util


class Rule(typing.NamedTuple):
    before: set[int]
    after: set[int]


def generate_rules_map(rules: list[str]) -> dict[int, Rule]:
    rules_map: dict[int, Rule] = {}
    for before, after in (rule.split("|") for rule in rules):
        after_rule = rules_map.setdefault(int(before), Rule(set(), set()))
        after_rule.after.add(int(after))
        before_rule = rules_map.setdefault(int(after), Rule(set(), set()))
        before_rule.before.add(int(before))
    return rules_map


def is_print_ok(
    rules_map: dict[int, Rule], pages_to_print: typing.Sequence[int]
) -> bool:
    all_pages = set(pages_to_print)
    for i, page in enumerate(pages_to_print):
        try:
            rule = rules_map[page]
            relevant_pages = all_pages - {page}
            before_pages = set(pages_to_print[:i])
            after_pages = set(pages_to_print[i + 1 :])
            required_before = relevant_pages & rule.before
            required_after = relevant_pages & rule.after
            if required_before > before_pages or required_after > after_pages:
                return False
        except KeyError:
            pass
    return True


def find_correct_order(
    rules_map: dict[int, Rule],
    pages_to_print: set[int],
    fixed_prior: None | list[int] = None,
) -> list[int] | None:
    if fixed_prior is None:
        fixed_prior = []
    if len(fixed_prior) == len(pages_to_print):
        return fixed_prior
    prior_set = set(fixed_prior)
    candidates = set()
    for p in pages_to_print - prior_set:
        try:
            rule = rules_map[p]
            relevant_pages = pages_to_print - {p}
            required_before = relevant_pages & rule.before
            required_after = relevant_pages & rule.after
            if required_before > prior_set or required_after > (
                relevant_pages - prior_set
            ):
                continue
            candidates.add(p)
        except KeyError:
            # No rules means it can go anywhere
            candidates.add(p)

    for candidate in candidates:
        if correct := find_correct_order(
            rules_map, pages_to_print, fixed_prior + [candidate]
        ):
            return correct
    return None


def middle_page(pages: list[int]) -> int:
    return pages[len(pages) // 2]


def main():
    puzzle_input = util.load_input(util.REAL, 5).splitlines()
    split_idx = puzzle_input.index("")
    rules = puzzle_input[:split_idx]
    prints = [
        [int(p) for p in pages.split(",")] for pages in puzzle_input[split_idx + 1 :]
    ]
    rules_map = generate_rules_map(rules)

    unprintable = [p for p in prints if not is_print_ok(rules_map, p)]
    s = 0
    for p in unprintable:
        print(p)
        corrected = find_correct_order(rules_map, set(p))
        print(corrected)
        if corrected is None:
            raise Exception("please no")
        s += middle_page(corrected)
    print(s)


if __name__ == "__main__":
    main()
