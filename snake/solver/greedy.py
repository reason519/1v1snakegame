from snake.base.pos import Pos
from snake.solver.base import BaseSolver
from snake.solver.path import PathSolver


class GreedySolver(BaseSolver):
    def __init__(self, snake):
        super().__init__(snake)
        self._path_solver = PathSolver(snake)

    def next_direc1(self,snake,s2):
        # Create a virtual snake
        s_copy, m_copy = snake.copy()

        # Step 1

        s2_copy, m2_copy = s2.copy()
        self._path_solver.snake = s2
        path_to_food1 = self._path_solver.shortest_path_to_food()
        if path_to_food1:
            s2_copy.move_path1(path_to_food1)
            s_copy.map.map_merge(s2_copy.map)
            # s_copy.map.map_merge(s2.map)

        self._path_solver.snake = s_copy

        path_to_food = self._path_solver.shortest_path_to_food()

        if path_to_food:
            # Step 2
            s_copy.move_path(path_to_food)
            if m_copy.is_full():
                return path_to_food[0]
            # if len(self.snake.bodies)

            # Step 3

            self._path_solver.snake = s_copy


            # path_to_tail = self._path_solver.longest_path_to_tail()
            path_to_tail = self._path_solver.shortest_path_to_tail()
            if len(path_to_tail) >= 1:
                return path_to_food[0]

        # Step 4
        # self._path_solver.snake = s_copy
        # path_to_tail1 = self._path_solver.longest_path_to_tail()
        # if path_to_tail1:
        self._path_solver.snake = snake
        path_to_tail = self._path_solver.longest_path_to_tail()
        if len(path_to_tail) >=1:
            return path_to_tail[0]
        # Step 5
        head = snake.head()
        direc, max_dist = self.snake.direc, -1
        for adj in head.all_adj():
            if self.map.is_safe(adj):
                dist = Pos.manhattan_dist(adj, self.map.food)
                if dist > max_dist:
                    max_dist = dist
                    direc = head.direc_to(adj)
        return direc

    def next_direc(self,snake):
        # Create a virtual snake
        s_copy, m_copy = snake.copy()

        # Step 1
        self._path_solver.snake = snake
        path_to_food = self._path_solver.shortest_path_to_food()

        if path_to_food:
            # Step 2
            s_copy.move_path(path_to_food)
            if m_copy.is_full():
                return path_to_food[0]
            # if len(self.snake.bodies)

            # Step 3
            self._path_solver.snake = s_copy
            # path_to_tail = self._path_solver.longest_path_to_tail()
            path_to_tail = self._path_solver.shortest_path_to_tail()
            if len(path_to_tail) > 1:
                return path_to_food[0]

        # Step 4
        self._path_solver.snake = snake
        path_to_tail = self._path_solver.longest_path_to_tail()
        if len(path_to_tail) > 1:
            return path_to_tail[0]

        # Step 5
        head = snake.head()
        direc, max_dist = self.snake.direc, -1
        for adj in head.all_adj():
            if self.map.is_safe(adj):
                dist = Pos.manhattan_dist(adj, self.map.food)
                if dist > max_dist:
                    max_dist = dist
                    direc = head.direc_to(adj)
        return direc
