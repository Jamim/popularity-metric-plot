import argparse

import bezier
import matplotlib.pyplot as plt
import numpy as np


def make_curve(x, y):
    nodes = np.asfortranarray([x, y])
    return bezier.Curve.from_nodes(nodes)


def evaluate_curve(x, y, linspace):
    curve = make_curve(x, y)
    return curve.evaluate_multi(np.linspace(*linspace))


def get_data():
    first_month_data = evaluate_curve(
        (0.0, 0.4, 0.6, 1.0),
        (0.0, 0.0, 8.0, 10.0),
        (0.0, 1.0, 101),
    )
    remaining_data = evaluate_curve(
        (1.0, 1.4, 6.0),
        (10.0, 12.0, 12.0),
        (0.01, 1.0, 500),
    )
    timeline, ratio = np.concatenate(
        (first_month_data, remaining_data), axis=1
    )
    popularity = np.divide(
        # timeline[0] is 0, so it should be skipped
        ratio,
        timeline,
        out=np.zeros_like(ratio),
        where=timeline > 0,
    )

    return timeline, ratio, popularity


def prepare_plot(font_size, dpi, line_width, width, height, **kwargs):
    plt.figure(figsize=(width / dpi, height / dpi), dpi=dpi, layout='tight')
    plt.rcParams['font.size'] = font_size
    plt.rcParams['savefig.dpi'] = dpi
    plt.xlabel('Elapsed time (months)', color='gray')
    plt.ylabel('Metric value', color='gray')
    plt.grid(True)


def draw_metrics(line_width):
    timeline, ratio, popularity = get_data()
    plt.plot(timeline, ratio, timeline, popularity, linewidth=line_width)
    plt.legend(['Ratio', 'Popularity'])


def parse_args():
    parser = argparse.ArgumentParser(
        description='Draws a metric correlation plot', add_help=False
    )
    parser.add_argument(
        '--save', '-s', dest='path', help='save the plot as a file'
    )
    parser.add_argument('--font-size', type=int, default=16, help='font size')
    parser.add_argument('--dpi', type=int, default=150, help='image DPI')
    parser.add_argument(
        '--line-width', '-l', type=int, default=2, help='plot line width'
    )
    parser.add_argument(
        '--width', '-w', type=int, default=3840, help='image width'
    )
    parser.add_argument(
        '--height', '-h', type=int, default=2160, help='image height'
    )
    parser.add_argument(
        '--help',
        action='help',
        default=argparse.SUPPRESS,
        help='show this help message and exit',
    )
    return parser.parse_args()


def main(args):
    prepare_plot(**vars(args))
    draw_metrics(args.line_width)

    if args.path:
        plt.savefig(args.path)
    else:
        plt.show()


if __name__ == '__main__':
    main(parse_args())
