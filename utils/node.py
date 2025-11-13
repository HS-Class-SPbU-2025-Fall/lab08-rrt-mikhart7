class RRTNode:
    """
    Узел поиска для алгоритма RRT.

    Args
    --------
    state :
        Состояние в пространстве, соответствующее текущему узлу
    parent : RRTNode
        Указатель на родительский узел.
    g : float | int
        Длина пути до текущего узла.
    """
    def __init__(self, 
                 state,
                 parent: "RRTNode" = None,
                 g: float = 0.0):
        self.state = state
        self.parent = parent
        self.g = g

    def __len__(self):
        """
        Вспомогательный метод, необходимый для корректной работы KD-дерева
        """
        return len(self.state)

    def __getitem__(self, i):
        """
        Вспомогательный метод, необходимый для корректной работы KD-дерева
        """
        return self.state[i]

    def __repr__(self):
        return 'Vertex({}, {})'.format(self.state[0], self.state[1])