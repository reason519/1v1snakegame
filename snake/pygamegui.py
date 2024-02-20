from snake.base import PointType, Pos
import pygame
import sys,time
from snake.base.direc import Direc

class GameWindow():
    def __init__(self,title, conf, game_map, game=None):
        pygame.init()
        pygame.display.set_caption(title)

        self.screen=pygame.display.set_mode((conf.map_width,conf.map_height))

        self._conf = conf
        self._map = game_map

        if game is not None:
            self._game = game
            self._snake1 = game.snake1
            self._snake2= game.snake2




        self.game_state="running"
        start_time = time.time()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self._conf.interval_draw = 10
                    if event.key == pygame.K_2:
                        self._conf.interval_draw = 20
                    if event.key == pygame.K_3:
                        self._conf.interval_draw = 30
                    if event.key == pygame.K_4:
                        self._conf.interval_draw = 40
                    if event.key == pygame.K_5:
                        self._conf.interval_draw = 50
                    if event.key == pygame.K_d:
                        self._conf.interval_draw = 100
                    if event.key==pygame.K_UP:
                        self._conf.interval_draw=40
                    if event.key==pygame.K_DOWN:
                        self._conf.interval_draw=100

                    if event.key == pygame.K_a:
                        self._snake1._dead=False
                    if event.key == pygame.K_b:
                        self._snake2._dead=False

            if self.game_state == "running":
                # if time.time() - start_time >= self._conf.interval_draw:


                game_over=self._game._game_main_normal()

                self.render()


            if game_over == "game_over":
                temp_time = time.time() - start_time
                self._game.time_count += temp_time
                self._game.game_count += 1

                self.draw_who_win()
                self.game_state = game_over
                length_s=len(self._snake1._bodies) + len(self._snake2._bodies)
                self._game.snake_len+=length_s
                print(f"count:{self._game.game_count},all time: {self._game.time_count},"
                      f"avage time:{self._game.time_count/self._game.game_count},"
                      f"snake length:{length_s},"
                      f"avage snake length{self._game.snake_len/self._game.game_count}")
                pygame.time.wait(8000)
                self._game._reset()
                self.game_state = "running"
                start_time = time.time()



            pygame.time.wait(self._conf.interval_draw)


    def render(self):
        self.screen.fill((255, 255, 255))

        # for i in range(self._conf.map_rows):
        #     pygame.draw.line(self.screen,[255,0,0],[0,i*self._conf.map_cell],[self._conf.map_cols*self._conf.map_cell,i*self._conf.map_cell])
        # for i in range(self._conf.map_cols):
        #     pygame.draw.line(self.screen, [255, 0, 0], [i * self._conf.map_cell,0 ],
        #                      [i * self._conf.map_cell,self._conf.map_rows * self._conf.map_cell])
        # Draw snake
        self.draw_snake1()
        self.draw_snake2()

        #Draw  food
        if self._map.has_food():
            food=self._map._food
            self.draw_rect(food.x, food.y, self._conf.color_food)

        # Draw text
        # self.draw_text()
        # if self.game_state=="game_over":
        #     self.draw_who_win()

        pygame.display.flip()


    def draw_snake1(self):
        head=self._snake1._bodies[0]
        self.draw_circle(head.x,head.y,self._conf.color_head1,self._snake1._direc)
        # self.draw_rect(head.x, head.y, self._conf.color_head1)

        for i in range(1,len(self._snake1._bodies)):
            c, r = self._snake1._bodies[i].x, self._snake1._bodies[i].y
            self.draw_rect(c,r,self._conf.color_body1)

    def draw_snake2(self):
        head=self._snake2._bodies[0]
        self.draw_circle(head.x,head.y,self._conf.color_head2,self._snake2._direc)
        # self.draw_rect(head.x, head.y, self._conf.color_head2)

        for i in range(1,len(self._snake2._bodies)):
            c, r = self._snake2._bodies[i].x, self._snake2._bodies[i].y
            self.draw_rect(c,r,self._conf.color_body2)




    def draw_rect(self,x,y,color):
        x=x-1
        y=y-1
        cell_size = self._conf.map_cell
        head_x = y * cell_size
        head_y = x * cell_size

        rect=pygame.Rect(head_x, head_y, cell_size, cell_size)
        self.screen.fill(color, rect)

        pygame.draw.rect(self.screen, (100, 100, 100),rect, 1)
        rect.inflate_ip(-1, -1)


    def draw_circle(self,x,y,color,direc):
        x=x-1
        y=y-1
        cell_size = self._conf.map_cell
        head_x = y * cell_size
        head_y = x * cell_size
        if direc==Direc.RIGHT:
            pygame.draw.circle(self.screen,color,[head_x,head_y+cell_size/2],cell_size/2)
        elif direc==Direc.LEFT:
            pygame.draw.circle(self.screen,color,[head_x+cell_size,head_y+cell_size/2],cell_size/2)
        elif direc==Direc.UP:
            pygame.draw.circle(self.screen,color,[head_x+cell_size/2,head_y+cell_size],cell_size/2)
        elif direc==Direc.DOWN:
            pygame.draw.circle(self.screen,color,[head_x+cell_size/2,head_y],cell_size/2)
    def draw_text(self):
        font1=pygame.font.SysFont("仿宋gb2312",30)
        text = font1.render("得分:" + str(len(self._snake1._bodies)-1), True, self._conf.color_body1)
        self.screen.blit(text, (10, 10))

        text = font1.render("得分:" + str(len(self._snake2._bodies) -1), True, self._conf.color_body2)
        self.screen.blit(text, (self._conf.map_cols*self._conf.map_cell-130, 10))


    def draw_who_win(self):
        font1 = pygame.font.SysFont("仿宋gb2312", 120)
        if len(self._snake1._bodies) > len(self._snake2._bodies):
            text = font1.render("红胜", True, (0, 0, 0))
            self.screen.blit(text, (0, self._conf.map_rows * self._conf.map_cell / 2- 120))
        elif len(self._snake1._bodies) < len(self._snake2._bodies):
            text = font1.render("蓝胜", True, (0, 0, 0))
            self.screen.blit(text, (0, self._conf.map_rows * self._conf.map_cell / 2- 120 ))
        else:
            text = font1.render("平局", True, (0, 0, 0))
            self.screen.blit(text,
                             (0, self._conf.map_rows * self._conf.map_cell / 2 - 120))
        pygame.display.flip()
        # text = font1.render("不是录播:" + str(int(self._snake.velocity)), True, (64, 64, 64))
        # self.screen.blit(text, (10, 52))

        # text=font1.render("速度:"+str(int(self._snake1.velocity)),True,(64,64,64))
        # self.screen.blit(text,(10,52))


