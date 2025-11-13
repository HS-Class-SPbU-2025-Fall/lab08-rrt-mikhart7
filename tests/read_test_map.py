def read_test_map(path_to_map_file):
    with open(path_to_map_file, 'r') as f:
        width = float(f.readline().strip())
        height = float(f.readline().strip())
        f.readline()
        start = tuple(map(float, f.readline().strip().split(';')))

        goal = tuple(map(float, f.readline().strip().split(';')))
        f.readline()
        obstacles = []
        cur_obstacle = []
        
        for line in f:
            line = line.strip()
            if line:
                cur_obstacle.append(tuple(map(float, line.split(';'))))
            else:
                obstacles.append(cur_obstacle)
                cur_obstacle = []
        if cur_obstacle:
            obstacles.append(cur_obstacle)
        
    return width, height, start, goal, obstacles