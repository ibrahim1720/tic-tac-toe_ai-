import matplotlib.pyplot as plt
from Ai_Algorithms import AiAlgorithms
import time
from UI import UI


# Example function to run multiple tests and plot the results
def plot_performance():
    moves = []

    times = []
    alg_name = ['Minimax', 'Alpha-Beta', 'AB Sy', 'Minimax HR']
    algorithms = [
        ('Minimax', AiAlgorithms().minimax),
        # ('Minimax Depth', AiAlgorithms().minimax_depth),
        ('Alpha-Beta', AiAlgorithms().alpha_beta),
        # ('Alpha-Beta Depth', AiAlgorithms().alpha_beta_depth),
        ('Alpha-Beta Symmetry', AiAlgorithms().alpha_beta_symmetry),
        ('Minimax Heuristic Reduction', AiAlgorithms().minimax_heuristic_reduction)
    ]

    # Simulate multiple games with different algorithms
    for algorithm_name, algorithm in algorithms:
        board = [[None, None, None], [None, 'x', None], [None, None, None]]  # Reset board
        metrics = {'moves': 0}

        start_time = time.time()
        # Choose the algorithm to use
        if algorithm_name == 'Minimax':
            algorithm(board, True, 'o', metrics=metrics)
        elif algorithm_name == 'Alpha-Beta':
            algorithm(board, -20, 20, True, 'o', metrics=metrics)
        elif algorithm_name == 'Alpha-Beta Symmetry':
            algorithm(board, 0, -20, 20, True, 'o', metrics=metrics)
        elif algorithm_name == 'Minimax Heuristic Reduction':
            algorithm(board, 0, True, 'o', metrics=metrics)

        elapsed_time = time.time() - start_time

        moves.append(metrics['moves'])
        times.append(elapsed_time)

        print(
            f"{algorithm_name}: Moves: {metrics['moves']}, Time: {elapsed_time:.4f} seconds")

    # Plotting the comparison of all algorithms
    plt.figure(figsize=(25, 6))

    # Moves plot
    plt.subplot(1, 3, 1)
    plt.bar(alg_name, moves, color='blue')
    plt.title('Moves Evaluated')
    plt.xlabel('Algorithm')
    plt.ylabel('Moves')

    # Time plot
    plt.subplot(1, 3, 2)
    plt.bar(alg_name, times, color='red')
    plt.title('Execution Time')
    plt.xlabel('Algorithm')
    plt.ylabel('Time (seconds)')

    plt.tight_layout()
    plt.show()


# Call plot function
if __name__ == "__main__":
    UI()
    plot_performance()
