import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.animation import FuncAnimation
import matplotlib.cm as cm
import numpy as np
from matplotlib.collections import LineCollection
from matplotlib.patches import Rectangle
from matplotlib.patches import Polygon as MPolygon, Circle
from IPython.display import HTML

def visualize_rrt(map_w, map_h, start_x, start_y, goal_x, goal_y, obstacles, all_points, final_path, goal_region: int = None,
                  max_transition: int = 5, goal_bias: float = 0.05, iterations=None, max_iteration=None, path_length=0):
    """
    Функция для визуализации работы алгоритма RRT с постепенным добавлением точек.
    После отрисовки всех точек будет подсвечен путь из final_path.
    """
    cmap = cm.get_cmap('viridis')
    norm = plt.Normalize(vmin=0, vmax=len(all_points))
    sm = cm.ScalarMappable(cmap=cmap, norm=norm)
    
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_axis_off()
    plt.axis('tight')
    ax.set_xlim(0, map_w + 1)
    ax.set_ylim(0, map_h + 1)

    row1 = (
        f"{'Map:'}{int(map_w)}x{int(map_h):<19} "
        f"{'Max Transition:'}{max_transition if max_transition else 'None':<15}  "
        f"{'Goal Bias:'}{goal_bias if goal_bias else 'None'}"
    )
    row2 = (
        f"{'Goal Region:'}{goal_region if goal_region else 'None':<15} "
        f"{'Iterations:'}{iterations if goal_region else 'None'}/"
        f"{max_iteration if goal_region else 'None':<11} "
        f"{'Path length:'}{int(path_length)}"
    )

    fig.text(0.15, 0.93, row1, ha='left', va='center', fontsize=12)
    fig.text(0.15, 0.90, row2, ha='left', va='center', fontsize=12)

    border = Rectangle((0, 0), map_w, map_h, linewidth=2, edgecolor='black', facecolor='#e9fce1')
    ax.add_patch(border)
    
    if goal_region:
        goal_circle = Circle((goal_x, goal_y), goal_region, color='red', alpha=0.3, label=f'Goal Region (r={goal_region})')
        ax.add_patch(goal_circle)

    ax.plot(start_x, start_y, 'go', markersize=15, label='Start')
    ax.plot(goal_x, goal_y, 'ro', markersize=15, label='Goal')

    for obstacle in obstacles:
        polygon = Polygon(obstacle, closed=True, edgecolor='black', facecolor='#f5c19c', alpha=0.7)
        ax.add_patch(polygon)

    scatter = ax.scatter([], [], c=[], cmap=cmap, norm=norm, s=[], label='RRT Points', zorder=2)
    edges = LineCollection([], colors='skyblue', alpha=0.7, linewidths=3, zorder=1)
    ax.add_collection(edges)

    path_edges = LineCollection([], colors='orange', linewidths=4, alpha=0.9)
    ax.add_collection(path_edges)

    def init():
        scatter.set_offsets(np.empty((0, 2)))
        scatter.set_array(np.array([]))
        scatter.set_sizes([])
        edges.set_segments([])
        path_edges.set_segments([])
        return scatter, edges, path_edges

    def update(frame):
        if frame < len(all_points):
            x_data = [p[0].state[0] for p in all_points[:frame + 1]]
            y_data = [p[0].state[1] for p in all_points[:frame + 1]]
            colors = np.arange(0, frame + 1)
            
            sizes = np.linspace(200, 30, num=frame + 1)

            scatter.set_offsets(np.column_stack((x_data, y_data)))
            scatter.set_array(colors)
            scatter.set_sizes(sizes)

            segments = []
            for p in all_points[:frame + 1]:
                if p[0].parent:
                    parent = p[0].parent
                    segments.append([(parent.state[0], parent.state[1]), (p[0].state[0], p[0].state[1])])

            edges.set_segments(segments)
            path_edges.set_segments([])

        elif frame >= len(all_points) + 5:
            path_segments = [(p.state[0], p.state[1]) for p in final_path]
            path_line_segments = [(path_segments[i], path_segments[i + 1]) for i in range(len(path_segments) - 1)]
            path_edges.set_segments(path_line_segments)
        else:
            pass
        

        return scatter, edges, path_edges

    extra_pause_frames = 50 
    anim = FuncAnimation(fig, update, frames=len(all_points) + extra_pause_frames, init_func=init, blit=True, interval=40, repeat=False)
    anim.save('rrt_gradient_edges_with_path.gif', writer='imagemagick') # dpi=700 and say goodbye to your memory :)
    plt.close(fig)
    matplotlib.rcParams['animation.embed_limit'] = 2**128 # Skibidy Hop You PC gonna stop
    return HTML(anim.to_jshtml())
