from manim import *
import math

class OpeningManim(Scene):
    def construct(self):
        title = Tex("This is some \\LaTeX")
        basel = MathTex("\\sum_{n=1}^\\infty " "\\frac{1}{n^2} = \\frac{\\pi^2}{6}")
        VGroup(title, basel).arrange(DOWN)
        self.play(
            Write(title),
            FadeInFrom(basel, UP),
        )
        self.wait()

        transform_title = Tex("That was a transform")
        transform_title.to_corner(UP + LEFT)
        self.play(
            Transform(title, transform_title),
            LaggedStart(*map(lambda obj: FadeOutAndShift(obj, direction=DOWN), basel)),
        )
        self.wait()

        grid = NumberPlane()
        grid_title = Tex("This is a grid")
        grid_title.scale(1.5)
        grid_title.move_to(transform_title)

        self.add(grid, grid_title)  # Make sure title is on top of grid
        self.play(
            FadeOut(title),
            FadeInFrom(grid_title, direction=DOWN),
            ShowCreation(grid, run_time=3, lag_ratio=0.1),
        )
        self.wait()

        grid_transform_title = Tex(
            "That was a non-linear function \\\\" "applied to the grid"
        )
        grid_transform_title.move_to(grid_title, UL)
        grid.prepare_for_nonlinear_transform()
        self.play(
            grid.apply_function,
            lambda p: p
                      + np.array(
                [
                    np.sin(p[1]),
                    np.sin(p[0]),
                    0,
                ]
            ),
            run_time=3,
        )
        self.wait()
        self.play(Transform(grid_title, grid_transform_title))
        self.wait()

class SineCurveUnitCircle(Scene):
    # contributed by heejin_park, https://infograph.tistory.com/230
    def construct(self):
        self.show_axis()
        self.show_circle()
        self.move_dot_and_draw_curve()
        self.wait()

    def show_axis(self):
        x_start = np.array([-6,0,0])
        x_end = np.array([6,0,0])

        y_start = np.array([-4,-2,0])
        y_end = np.array([-4,2,0])

        x_axis = Line(x_start, x_end)
        y_axis = Line(y_start, y_end)

        self.add(x_axis, y_axis)
        self.add_x_labels()

        self.orgin_point = np.array([-4,0,0])
        self.curve_start = np.array([-3,0,0])

    def add_x_labels(self):
        x_labels = [
            MathTex("\pi"), MathTex("2 \pi"),
            MathTex("3 \pi"), MathTex("4 \pi"),
        ]

        for i in range(len(x_labels)):
            x_labels[i].next_to(np.array([-1 + 2*i, 0, 0]), DOWN)
            self.add(x_labels[i])

    def show_circle(self):
        circle = Circle(radius=1)
        circle.move_to(self.orgin_point)

        self.add(circle)
        self.circle = circle

    def move_dot_and_draw_curve(self):
        orbit = self.circle
        orgin_point = self.orgin_point

        dot = Dot(radius=0.08, color=YELLOW)
        dot.move_to(orbit.point_from_proportion(0))
        self.t_offset = 0
        rate = 0.25

        def go_around_circle(mob, dt):
            self.t_offset += (dt * rate)
            # print(self.t_offset)
            mob.move_to(orbit.point_from_proportion(self.t_offset % 1))

        def get_line_to_circle():
            return Line(orgin_point, dot.get_center(), color=BLUE)

        def get_line_to_curve():
            x = self.curve_start[0] + self.t_offset * 4
            y = dot.get_center()[1]
            return Line(dot.get_center(), np.array([x,y,0]), color=YELLOW_A, stroke_width=2 )


        self.curve = VGroup()
        self.curve.add(Line(self.curve_start,self.curve_start))
        def get_curve():
            last_line = self.curve[-1]
            x = self.curve_start[0] + self.t_offset * 4
            y = dot.get_center()[1]
            new_line = Line(last_line.get_end(),np.array([x,y,0]), color=YELLOW_D)
            self.curve.add(new_line)

            return self.curve

        dot.add_updater(go_around_circle)

        origin_to_circle_line = always_redraw(get_line_to_circle)
        dot_to_curve_line = always_redraw(get_line_to_curve)
        sine_curve_line = always_redraw(get_curve)

        self.add(dot)
        self.add(orbit, origin_to_circle_line, dot_to_curve_line, sine_curve_line)
        self.wait(8.5)

        dot.remove_updater(go_around_circle)

class Pcurve(GraphScene):
    def construct(self):
        self.setup_axes()

        def graph_to_be_drawn(x):
            return (1 / 2) * x ** 2 - 3

        vt = ValueTracker(0)

        graph_1 = self.get_graph(graph_to_be_drawn, x_min=-2)

        def moving_dot():
            x = vt.get_value()
            d = Dot().move_to(self.coords_to_point(x, graph_to_be_drawn(x)))
            return d

        dd = always_redraw(moving_dot)

        self.add(dd, graph_1)
        self.play(vt.set_value, 5, rate_func=there_and_back, run_time=5)
        self.wait()


class ParabolaCreation(GraphScene):
    CONFIG = {
        "x_min": -6,
        "x_max": 6,
        "x_axis_width": 12,
        "y_axis_height": 7,
        "graph_origin": 3.5 * DOWN,
        "y_min": 0,
        "y_max": 7,
    }

    def construct(self):
        self.setup_axes()
        self.x_axis.remove(self.x_axis[1])
        self.y_axis.remove(self.y_axis[1])
        self.play(Write(self.axes))

        h = 0;
        k = 1;
        p = 1
        parabola_function = lambda x: ((x - h) ** 2) / (4 * p) + k

        parabola_right = self.get_graph(
            parabola_function,
            x_min=0,
            x_max=5,
            color=BLUE
        )

        parabola_left = self.get_graph(
            parabola_function,
            x_min=0,
            x_max=-5,
            color=BLUE
        )
        anim_kwargs = {"run_time": 5, "rate_func": linear}
        self.move_dot_path(parabola_right, anim_kwargs)
        self.move_dot_path(parabola_left, anim_kwargs)

    def move_dot_path(self, parabola, anim_kwargs):
        h = 0;
        k = 1;
        p = 1
        parabola_copy = parabola.copy()
        focus = Dot(self.coords_to_point(0, 2))
        dot_guide = Dot(self.coords_to_point(h, p))
        dot_d = Dot(self.coords_to_point(0, 0))
        circle = Circle(radius=1).move_to(self.coords_to_point(h, p))
        line_f_d = DashedLine(focus.get_center(), dot_guide.get_center())
        line_d_d = DashedLine(dot_guide.get_center(), dot_d.get_center())

        group = VGroup(circle, line_f_d, line_d_d, dot_d)

        def update_group(group):
            c, f_d, d_d, d = group
            d.move_to(self.coords_to_point(dot_guide.get_center()[0], 0))
            radius = get_norm(focus.get_center() - dot_guide.get_center())
            new_c = Circle(radius=radius)
            new_c.move_to(dot_guide)
            c.become(new_c)
            f_d.become(DashedLine(focus.get_center(), dot_guide.get_center()))
            d_d.become(DashedLine(dot_guide.get_center(), dot_d.get_center()))

        group.add_updater(update_group)

        self.play(
            FadeInFromLarge(circle, scale_factor=2),
            *[GrowFromCenter(mob) for mob in [line_f_d, line_d_d, dot_guide, dot_d, focus]],
        )
        self.add(
            group,
            focus,
            dot_guide,
        )
        self.wait()
        self.add(parabola)
        self.bring_to_back(parabola)
        self.bring_to_back(self.axes)
        self.play(
            MoveAlongPath(dot_guide, parabola_copy),
            ShowCreation(parabola),
            **anim_kwargs
        )
        group.clear_updaters()
        self.wait(1.2)
        self.play(FadeOut(VGroup(group, dot_guide, focus)))