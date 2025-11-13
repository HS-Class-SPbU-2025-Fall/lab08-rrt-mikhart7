import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MPolygon, Circle

def show_map_vectorized(width, height, obstacles, start=None, goal=None, goal_region=None, show_obstacles_index=False, show_vertexes=False, show_cords=False, label="Field with Obstacles"):
    fig, ax = plt.subplots(figsize=(5, 5))  

    for idx, obstacle in enumerate(obstacles):
        polygon = MPolygon(obstacle, closed=True, edgecolor='red', facecolor='red', alpha=0.5)
        ax.add_patch(polygon)
        if show_cords:
            for (x, y) in obstacle:
                ax.text(x, y, f'({x:.2f},{y:.2f})', color='blue', fontsize=10, ha='right', va='bottom')

        if show_obstacles_index:
            centroid_x = sum(x for x, y in obstacle) / len(obstacle)
            centroid_y = sum(y for x, y in obstacle) / len(obstacle)
            ax.text(centroid_x, centroid_y, f'{idx}', color='green', fontsize=12, ha='center', va='center')

        if show_vertexes:
            x_vals, y_vals = zip(*obstacle)
            ax.scatter(x_vals, y_vals, color='black', s=5)
    if start:
        ax.scatter(*start, color='green', s=100, label='Start')
    if goal:
        ax.scatter(*goal, color='red', s=100, label='Goal')

    if goal_region:
        goal_circle = Circle(goal, goal_region, color='red', alpha=0.3, label=f'Goal Region (r={goal_region})')
        ax.add_patch(goal_circle)

    ax.set_xlim(0, width)
    ax.set_ylim(0, height)
    ax.set_aspect('equal')
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title(label)
    plt.grid(True)
    if start or goal or goal_region:
        plt.legend()
    plt.show()
