from matplotlib import pyplot as pp


def plot_results():
    with open('results.txt', 'r') as results_file:
        lines = results_file.readlines()
    points = dict()
    for i in range(0, len(lines), 2):
        x = int(lines[i].split(' ')[1].strip())
        y = float(lines[i + 1].split(' ')[1].strip())

        if x in points.keys():
            points[x].append(y)

        else:
            points[x] = [y]

    # Average out times
    for key in points:
        points[key] = sum(points[key]) / len(points[key])

    x, y = zip(*sorted(points.items()))
    pp.figure()
    pp.subplot(111)
    pp.title('Workers vs Time')
    pp.xlabel('Workers')
    pp.ylabel('Time')
    pp.plot(x, y)
    pp.show()


if __name__ == '__main__':
    plot_results()
