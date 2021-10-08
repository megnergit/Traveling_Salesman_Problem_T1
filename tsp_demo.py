from tsp.tsp import *
import pandas as pd
import pdb
import sys
import plotly.graph_objs as go
import pretty_errors

# ==================================================
# TSP demo
# ==================================================


def algorithm_demo(algorithm_list) -> None:

    for a in algorithm_list:
        algorithm, n_cities, text, visualize = a

        cities = Cities(n_cities)
        print(f'\033[31m#'+'='*20+'\033[0m')
        print(f'\033[93m{text}\033[0m')
        print(f'\033[92mn_cities\033[0m {len(cities)}')
        t1, t2 = algorithm(cities)
        visualize(t1, t2, text)
        go_next()


# -----------------------------------------------

def reverse_segment_demo(cities):
    tour, segments_list = greedy_tsp(cities)
    tour_initial = tour.copy()
    tour_opt = alter_tour(tour)
    text = 'Reverse Segments (Greedy)'
    visualize_two_tours(tour_opt, tour_initial, text)
    print(f'\033[92mBefore \033[0m{tour_length(tour_initial): 6.0f}')
    print(f'\033[96mAfter  \033[0m{tour_length(tour_opt): 6.0f}')
    go_next()

# -----------------------------------------------


def benchmarks_demo(algorithm_list, maps=Maps) -> None:
    print(f'\033[31m#'+'='*20+'\033[0m')
    print(f'\033[95mBenchmark\033[0m')

    tsp_algorithms = split_algorithm_list(algorithm_list, exact_out=True)
    # do not add 'exact solution', as it takes too long
    df, tours = benchmarks(tsp_algorithms, maps=maps)
    visualize_benchmark(tours, df)
    print(df)
    go_next()


def time_demo(algorithm_list, city_sizes, exact_out) -> None:

    n_rep = 5
    df_list = []

    for n_cities in city_sizes:
        maps = Maps(n_rep, n_cities)
        tsp_algorithms = []

        tsp_algorithms = split_algorithm_list(
            algorithm_list, exact_out=exact_out)

        df, tours = benchmarks(tsp_algorithms, maps=maps)
        df_list.append(df)

    df_time = pd.concat(df_list, axis=0, ignore_index=True)

    # ----------------------
    data = [go.Bar(name=str(name),  x=df_time['algorithm'].unique(),
                   y=df_time[df_time['n_city'] == name]['time'])
            for name in df_time['n_city'].unique()]

    # ----------------------
    layout = go.Layout(hovermode='closest',
                       margin=dict(l=0, r=0, t=64, b=0),
                       title='Execution Time in second',
                       xaxis=dict(tickfont=dict(size=20)),
                       yaxis=dict(type='log', tickfont=dict(size=20)),
                       barmode='group',
                       width=512*2, height=512,
                       legend_title_text='number of cities',
                       showlegend=True)

    fig = go.Figure(data=data, layout=layout)
    fig.show()

# ==================================================


def split_algorithm_list(algorithm_list, exact_out) -> list:

    tsp_algorithms = []

    if exact_out:
        for a, _, _, _ in algorithm_list:
            # do not add 'exact solution', as it takes too long
            if a.__name__ != 'alltours_tsp':
                tsp_algorithms.append(a)

    else:
        for a, _, _, _ in algorithm_list:
            tsp_algorithms.append(a)

    return tsp_algorithms


def go_next() -> None:

    print("Next? [Y]/n")
    char = input()
    if char == 'n':
        exit()
    else:
        pass


# ==================================================
# TSP demo
# ==================================================
if __name__ == '__main__':

    algorithm_list = [
        (alltours_tsp,  6, "Exact Solution", visualize_all_solution),
        (nn_tsp, 40, "Nearest Neighbor", visualize_initial_solution),
        (greedy_tsp, 40, "Greedy", visualize_gd),
        (random_insertion_tsp, 40, "Random Insertion", visualize_initial_solution),
        (nearest_insertion_tsp, 40, "Nearest Insertion", visualize_initial_solution),
        (furthest_insertion_tsp, 40, "Furthest Insertion", visualize_initial_solution),
        (cheapest_insertion_tsp, 40, "Cheapest Insertion", visualize_initial_solution),
        (ortool_tsp, 99, "Ortool", visualize_two_tours)]

    # -------------------------------------
    # show how differdnt  algoithms work
    # -------------------------------------

    algorithm_demo(algorithm_list)

    # -------------------------------------
    # reverse segment for greedy
    # -------------------------------------
    cities = Cities(40, seed=42)
    reverse_segment_demo(cities)

    # -------------------------------------
    # compare performance (length)a
    # -------------------------------------

    maps = Maps(5, 99)
    benchmarks_demo(algorithm_list, maps)

    # -------------------------------------
    # compare how long each algorittm takes
    # -------------------------------------

    city_sizes = [6, 8, 10]
    time_demo(algorithm_list, city_sizes, exact_out=False)

    city_sizes = [16, 64, 256]
    time_demo(algorithm_list, city_sizes, exact_out=True)

# ==================================================
# END
# ==================================================
