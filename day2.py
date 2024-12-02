import util


def parse_reports(reports: str) -> list[list[int]]:
    output = []
    for reportline in reports.splitlines():
        if len(reportline) == 0:
            continue
        output.append([int(i) for i in reportline.split()])

    return output


def is_safe(report: list[int], dampen=False) -> bool:
    lastval = report[0]
    increasing = report[0] < report[1]
    safe = True
    for v in report[1:]:
        diff = v - lastval
        if abs(diff) < 1 or abs(diff) > 3:
            safe = False
            break
        step_increasing = diff > 0
        if step_increasing != increasing:
            safe = False
            break
        lastval = v
    if not safe and dampen:
        for i in range(len(report)):
            sliced = report[:i] + report[i+1:]
            if is_safe(sliced):
                return True
    return safe


def main():
    reports = parse_reports(util.load_input(util.REAL, 2))
    print(sum(is_safe(report, dampen=True) for report in reports))


if __name__ == "__main__":
    main()
