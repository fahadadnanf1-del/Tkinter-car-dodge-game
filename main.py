import random
import time
from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, Line
from kivy.uix.widget import Widget

class CarGame(Widget):
    def __init__(self, **kwargs):
        super(CarGame, self).__init__(**kwargs)
        self.car_x = 180
        self.car_y = 50
        self.car_width = 40
        self.car_height = 70
        self.obstacles = []
        self.score = 0
        self.game_over = False
        
        # Touch ya click se car move karne ke liye
        self.bind(pos=self.update_canvas, size=self.update_canvas)
        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def on_touch_move(self, touch):
        if not self.game_over:
            self.car_x = touch.x - self.car_width / 2
            # Screen se bahar na jaye
            if self.car_x < 0: self.car_x = 0
            if self.car_x > self.width - self.car_width: 
                self.car_x = self.width - self.car_width

    def update(self, dt):
        if self.game_over:
            return

        self.score += 1

        # Naye obstacles (dusri gaariyan) banana
        if random.randint(1, 40) == 1:
            obs_x = random.randint(0, int(self.width - 40))
            obs_y = self.height
            self.obstacles.append([obs_x, obs_y, 40, 70])

        # Obstacles ko neechay lana
        for obs in self.obstacles[:]:
            obs[1] -= 5  # Speed
            if obs[1] < -70:
                self.obstacles.remove(obs)

            # Collision (Takkar) check karna
            if (self.car_x < obs[0] + obs[2] and 
                self.car_x + self.car_width > obs[0] and 
                self.car_y < obs[1] + obs[3] and 
                self.car_y + self.car_height > obs[1]):
                self.game_over = True

        self.update_canvas()

    def update_canvas(self, *args):
        self.canvas.clear()
        with self.canvas:
            # Background (Road)
            Color(0.2, 0.2, 0.2, 1)
            Rectangle(pos=self.pos, size=self.size)

            if not self.game_over:
                # Player ki Car (Blue color)
                Color(0, 0.5, 1, 1)
                Rectangle(pos=(self.car_x, self.car_y), size=(self.car_width, self.car_height))

                # Enemy Cars (Red color)
                Color(1, 0, 0, 1)
                for obs in self.obstacles:
                    Rectangle(pos=(obs[0], obs[1]), size=(obs[2], obs[3]))
            else:
                # Game Over Text / Screen
                pass

class CarGameApp(App):
    def build(self):
        return CarGame()

if __name__ == '__main__':
    CarGameApp().run()