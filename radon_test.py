from pprint import pprint
from radon.complexity import cc_rank, SCORE
from radon.cli.harvest import CCHarvester
from radon.cli import Config


def calc_avg_cc(results):
    total_cc = 0
    for filename in results.values():
        file_cc = 0
        for block in filename:
            file_cc += block['complexity']

        total_cc += file_cc

    return total_cc / len(results)


def main():
    path = ['./tmp']
    config = Config(
        exclude='',
        ignore='venv',
        order=SCORE,
        no_assert=True,
        show_closures=False,
        min='A',
        max='F',
    )

    h = CCHarvester(path, config)
    print(calc_avg_cc(h._to_dicts()))


if __name__ == '__main__':
    main()
