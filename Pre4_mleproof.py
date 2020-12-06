from manim import *
from scipy.stats import *
import numpy as np


def custom_time(t, partitions, start, end, func):
    duration = end - start
    fragment_time = 1 / partitions
    start_time = start * fragment_time
    end_time = end * fragment_time
    duration_time = duration * fragment_time

    def fix_time(x):
        return (x - start_time) / duration_time

    if t < start_time:
        return func(fix_time(start_time))
    elif start_time <= t and t < end_time:
        return func(fix_time(t))
    else:
        return func(fix_time(end_time))


def Custom(partitions, start, end, func=smooth):
    return lambda t: custom_time(t, partitions, start, end, func)


class equation(GraphScene):
    CONFIG = {
        "x_min": 0,
        "x_max": 8,
        "y_min": 0,
        "y_max": 1,
        "x_tick_frequency": 1,
        "x_labeled_nums": np.arange(0, 8),
        "y_tick_frequency": 0.1,
        "y_labeled_nums": [0, 1],
        'func_color': YELLOW_A,
        # "y_labeled_nums" : np.arange(0,1,0.1),
    }

    def construct(self):
        item = self.extendLH()
        self.logLH(item)

    def extendLH(self):
        pdf = MathTex("f(x) = \\frac{1}{\\sigma\\sqrt{2\\pi}}exp(-\\frac{(x-\\mu)^2}{2\\sigma^2})")
        self.play(FadeInFromEdges(pdf[0]))
        self.wait()
        self.play(pdf.to_edge, UP)
        self.wait()

        transform_tex = MathTex("L(x_1,...,x_n|\\mu,\\sigma) ").scale(0.8).shift(3 * LEFT + 0.5 * UP)
        align_text = MathTex("= \\prod_{i=1}^nf(x_i)").scale(0.8).next_to(transform_tex, RIGHT)
        further = MathTex("= \\prod_{i=1}^n\\frac{1}{\\sigma\\sqrt{2\\pi}}exp(-\\frac{(x-\\mu)^2}{2\\sigma^2})").scale(
            0.8).next_to(align_text, DOWN).align_to(align_text, LEFT)
        constant = MathTex("= \\frac{(2\\pi)^{-\\pi/2}}{\\sigma^n}").scale(0.8).next_to(further, DOWN).align_to(further,
                                                                                                                LEFT)
        ffurther = MathTex("exp\\left[-\\frac{\\sum(x_i-\\mu)^2}{2\\sigma^2}\\right]")
        ffurther.save_state()
        ffurther.scale(0.8).next_to(constant,
                                    RIGHT)
        self.play(Write(VGroup(transform_tex, align_text)))
        self.play(Write(further))
        self.play(Write(VGroup(constant, ffurther)))
        self.play(UnderlineIndication(VGroup(constant, ffurther)))
        self.wait()
        crossout = ZigZag(constant, color=RED, stroke_width=5)
        self.play(
            ShowCreation(crossout),
        )
        self.wait()
        self.play(
            FadeOut(VGroup(pdf, align_text, further, crossout, constant, transform_tex)),
            Restore(ffurther)
        )
        self.wait()
        return ffurther

    def logLH(self, item):
        log = MathTex("\\ln ").next_to(item, LEFT)
        self.play(FadeInFromDown(log))
        self.wait()
        prev = MathTex("\\ln L \\sim").next_to(log, LEFT)
        next = MathTex("= -\\frac{\\sum(x_i-\\mu)^2}{2\\sigma^2}").next_to(item, RIGHT)
        self.play(
            FadeInFrom(prev, LEFT),
            FadeInFrom(next, RIGHT),
        )
        self.wait()
        div = MathTex("\\frac{\\delta(\\ln L)}{\\delta \\mu} \\sim \\sum(x_i-\\mu)")
        rel = MathTex("= 0").next_to(div, RIGHT)
        self.play(
            VGroup(prev, log, item, next).to_edge, UP,
            ShowCreation(div, rate_func=Custom(6, 3, 5)),
            FadeInFrom(rel, RIGHT, rate_functions=Custom(6, 4, 6)),
            run_time=2,
        )
        self.wait()
        muanswer = MathTex("\\hat{\\mu} = \\frac{\\sum x}{n} = \\frac{9+9.5+11}{3} = 9.8333").next_to(div, 1.5*DOWN)
        self.play(Write(muanswer))
        self.wait()
        self.play(
            *[FadeOut(mob) for mob in self.mobjects]
        )
        self.wait()
        sdanswer = MathTex("\\hat{\\sigma} = \\sqrt{\\frac{\\sum(x_i-\\hat{\\mu})^2}{n}} = 0.84984")
        self.play(GrowFromEdge(sdanswer, UP))
        self.wait()


class endit(GraphScene):
    def construct(self):
        sdanswer = MathTex("\\hat{\\sigma} = \\sqrt{\\frac{\\sum(x_i-\\hat{\\mu})^2}{n}} = 0.84984")
        self.add(sdanswer)
        self.play(FadeOut(sdanswer))
        self.wait()

class FadeInFromEdges(LaggedStart):
    def __init__(self, text, **kwargs):
        digest_config(self, kwargs)
        super().__init__(
            *[FadeInFromPoint(obj, point=self.get_vector_from(obj, dist=1.4)) for obj in text],
            **kwargs
        )

    def get_vector_from(self, obj, point=ORIGIN, dist=2):
        vect = obj.get_center() - point
        return vect * dist


class FreehandDraw(VMobject):
    CONFIG = {
        "sign": 1,
        "close": False,
        "dx_random": 7,
        "length": 0.06
    }

    def __init__(self, path, partitions=120, **kwargs):
        VMobject.__init__(self, **kwargs)
        coords = []
        for p in range(int(partitions) + 1):
            coord_i = path.point_from_proportion((p * 0.989 / partitions) % 1)
            coord_f = path.point_from_proportion((p * 0.989 / partitions + 0.001) % 1)
            reference_line = Line(coord_i, coord_f).rotate(self.sign * PI / 2, about_point=coord_i)
            normal_unit_vector = reference_line.get_unit_vector()
            static_vector = normal_unit_vector * self.length
            random_dx = random.randint(0, self.dx_random)
            random_normal_vector = random_dx * normal_unit_vector / 100
            point_coord = coord_i + random_normal_vector + static_vector
            coords.append(point_coord)
        if self.close:
            coords.append(coords[0])
        self.set_points_smoothly(coords)


# FreehandRectangle depends of FreehandDraw
class FreehandRectangle(VMobject):
    CONFIG = {
        "margin": 0.7,
        "partitions": 120,
    }

    def __init__(self, texmob, **kwargs):
        VMobject.__init__(self, **kwargs)
        rect = Rectangle(
            width=texmob.get_width() + self.margin,
            height=texmob.get_height() + self.margin
        )
        rect.move_to(texmob)
        w = rect.get_width()
        h = rect.get_height()
        alpha = w / h
        hp = np.ceil(self.partitions / (2 * (alpha + 1)))
        wp = np.ceil(alpha * hp)
        sides = VGroup(*[
            Line(rect.get_corner(c1), rect.get_corner(c2))
            for c1, c2 in zip([UL, UR, DR, DL], [UR, DR, DL, UL])
        ])
        total_points = []
        for side, p in zip(sides, [wp, hp, wp, hp]):
            path = FreehandDraw(side, p).points
            for point in path:
                total_points.append(point)
        total_points.append(total_points[0])
        self.set_points_smoothly(total_points)


class ZigZag(VMobject):
    CONFIG = {
        "margin": 0.4,
        "sign": 1
    }

    def __init__(self, path, partitions=10, **kwargs):
        VMobject.__init__(self, **kwargs)
        rect = Rectangle(
            width=path.get_width() + self.margin,
            height=path.get_height() + self.margin
        )
        rect.move_to(path)
        w = rect.get_width()
        h = rect.get_height()
        alpha = w / h
        hp = int(np.ceil(partitions / (2 * (alpha + 1))))
        wp = int(np.ceil(alpha * hp))
        sides = VGroup(*[
            Line(rect.get_corner(c1), rect.get_corner(c2))
            for c1, c2 in zip([UL, UR, DR, DL], [UR, DR, DL, UL])
        ])
        total_points = []
        for side, points in zip(sides, [wp, hp, wp, hp]):
            for p in range(points):
                total_points.append(side.point_from_proportion(p / points))
        total_points.append(total_points[0])
        middle = int(np.floor(len(total_points) / 2))
        draw_points = []
        for p in range(2, middle):
            draw_points.append(total_points[-p * self.sign])
            draw_points.append(total_points[p * self.sign])
        self.set_points_smoothly(draw_points)


class UnderlineIndication(AnimationGroup):
    CONFIG = {
        "line_config": {},
        "line_type": Line,
        "reverse": True,
        "run_time": 1.5
    }

    def __init__(self, mobject, margin=0.1, buff=0.2, **kwargs):
        digest_config(self, kwargs)
        line = self.line_type(
            mobject.get_corner(DL) + margin * LEFT,
            mobject.get_corner(DR) + margin * RIGHT,
            **self.line_config
        )
        line.shift(buff * DOWN)
        if self.reverse:
            kwargs["rate_func"] = there_and_back
            kwargs["run_time"] = self.run_time * 2
        if self.line_type == DashedLine:
            kwargs["run_time"] = self.run_time / 2
            kwargs["rate_func"] = smooth
            kwargs["lag_ratio"] = 0.005
        super().__init__(self.return_animation(line, **kwargs))

    def return_animation(self, line, **kwargs):
        if self.line_type == Line:
            return ShowCreationThenDestruction(line, **kwargs)
        elif self.line_type == DashedLine:
            return LaggedStartMap(ShowCreationThenDestruction, line, **kwargs)
