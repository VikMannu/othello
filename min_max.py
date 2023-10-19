class MinMax:
    def __init__(self, cutting_level, max_cutting_time, is_alpha_beta):
        self.cutting_level = cutting_level
        self.max_cutting_time = max_cutting_time
        self.is_alpha_beta = is_alpha_beta
        self.position_weight = [
            [100, -20, 10, 5, 5, 10, -20, 100],
            [-20, -50, -2, -2, -2, -2, -50, -20],
            [10, -2, 2, 1, 1, 2, -2, 10],
            [5, -2, 1, 1, 1, 1, -2, 5],
            [5, -2, 1, 1, 1, 1, -2, 5],
            [10, -2, 2, 1, 1, 2, -2, 10],
            [-20, -50, -2, -2, -2, -2, -50, -20],
            [100, -20, 10, 5, 5, 10, -20, 100]
        ]

    