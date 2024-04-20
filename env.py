
from fischer.pygenv import PygEnv


def bezier_curve(num_points: int, *points: tuple[tuple[int, int]]) -> list[tuple[int, int]]:
    def bezier(t, *points):
        if len(points) == 1:
            return points[0]
        return PygEnv.lerp_vector(*bezier(t, *points[:-1]), *bezier(t, *points[1:]), t)
    return [bezier(t/num_points, *points) for t in range(num_points+1)]


class VehicleSlopeEnv(PygEnv):
    def __init__(self):
        super().__init__(screen_size=(610, 377))
        self.set_bg_color((255, 255, 255))
        self.set_gravity(0, -400)
        self.set_pannable(False)
        self.set_target_follow_speed(1.75)
        self.wheel0 = self.spawn_circle((0, 0, 0), (0, 0),
            radius=10,
            density=1,
            elasticity=0,
            friction=1,
            drag=0,
            angular_drag=0,
            draw_line=True,
        )
        self.wheel1 = self.spawn_circle((0, 0, 0), (30, 0),
            radius=10,
            density=1,
            elasticity=0,
            friction=1,
            drag=0,
            angular_drag=0,
            draw_line=True,
        )
        self.pymunk_space.add(self.pym.constraints.PinJoint(self.wheel0.body, self.wheel1.body, (0, 0), (0, 0)))
        self.road_lines = []
        self.x = -50
        self.y = -50
        self.segments_per_road = 6
        for _ in range(200):
            # self.add_road(self.random(90, 180), self.random(-50, 50), self.random(0.3, 0.7))
            self.add_road(self.random(90, 300), self.random(-200, 200), self.random(0.3, 0.7))
    def add_bezier_curve(self, points: list[tuple[int, int]]) -> list:
        bp = bezier_curve(self.segments_per_road, *points)
        lines = []
        for p0, p1 in zip(bp[:-1], bp[1:]):
            lines.append(self.add_static_line((0, 0, 0), p0, p1,
                elasticity=0,
                friction=1,
                radius=3,
            ))
        self.road_lines.append(lines)
        return lines
    def add_road(self, length: float, y: float, steepness: float):
        p0 = self.x, self.y
        p1 = self.x + length * steepness, self.y
        p2 = self.x + length * (1 - steepness), self.y + y
        p3 = self.x + length, self.y + y
        self.add_bezier_curve([p0, p1, p2, p3])
        self.x += length
        self.y += y
    def update(self):
        # delta = self.wheel1.body.position - self.wheel0.body.position
        # delta = self.normalized_vector(*delta, length=30)
        # new_pos = self.wheel0.body.position + delta
        # delta = self.normalized_vector(*(new_pos - self.wheel1.body.position), length=100000, default=(0, 0))
        # self.wheel1.body.apply_force_at_world_point(delta, self.wheel1.body.position)

        if self.key_is_held(self.KEYCODES.K_d):
            t = 40000
            for w in self.wheel0, self.wheel1:
                w.body.apply_force_at_world_point((t, 0), (self.wheel0.body.position[0], self.wheel0.body.position[1] + 10))
                w.body.apply_force_at_world_point((-t, 0), (self.wheel0.body.position[0], self.wheel0.body.position[1] - 10))
                t *= .75
        elif self.key_is_held(self.KEYCODES.K_a):
            t = 40000
            for w in self.wheel0, self.wheel1:
                w.body.apply_force_at_world_point((-t, 0), (self.wheel0.body.position[0], self.wheel0.body.position[1] + 10))
                w.body.apply_force_at_world_point((t, 0), (self.wheel0.body.position[0], self.wheel0.body.position[1] - 10))
                t *= .75
        elif self.key_is_held(self.KEYCODES.K_s):
            self.wheel0.body.angular_velocity = 0
            self.wheel1.body.angular_velocity = 0
        self.set_camera_target_pos(*self.wheel1.body.position)



env = VehicleSlopeEnv()
env.run_loop()



