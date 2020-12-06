from manim import *
from scipy.stats import *
import numpy as np


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
        self.show_how()
        self.show_intuition()
        self.show_independent()

    def show_how(self):
        begin = Tex("How ?").scale(2)
        self.play(FadeInFromEdges(begin))
        self.wait()
        origin_q = MathTex("P(model| data)")
        wwg = MathTex("P(data| model)").shift(4*RIGHT)
        fing = SVGMobject("finger").scale(0.6)
        finalwwg = MathTex("argmax_{model} P(data| model)").next_to(wwg, DOWN*2)
        self.play(
            begin.to_edge, UP,
            LaggedStart(
                Write(origin_q),
            ),
            # Write(origin_q),
        )
        self.wait()
        self.play(
            origin_q.shift, 4*LEFT,
            FadeInFrom(wwg, RIGHT),
        )
        self.wait()
        self.play(Write(fing))
        self.wait()
        self.play(TransformFromCopy(wwg, finalwwg))
        self.wait()
        self.play(
            *[FadeOut(mob) for mob in self.mobjects]
        )
        self.wait()

    def show_intuition(self):
        data_text = Tex("data = $[9, 9.5, 11]$")
        self.play(FadeIn(data_text))
        self.wait()
        joint_prob = MathTex("P(x_1, x_2, x_3)").shift(UP)
        conditional = MathTex("L(x_1, x_2, x_3| \\mu, \\sigma)")
        group = VGroup(joint_prob, conditional).arrange(DOWN)
        self.play(
            data_text.shift, 2 * UP,
            FadeInFromDown(joint_prob),
        )
        self.wait()
        self.play(ReplacementTransform(joint_prob, conditional))
        self.wait()
        self.play(FadeOutAndShift(VGroup(group, data_text), UP))
        self.wait()

    def show_independent(self):
        ea = MathTex("Event: A").to_corner(LEFT + UP).shift(RIGHT + DOWN)
        eb = MathTex("B").next_to(ea, RIGHT)
        joinab = MathTex("P(A,B) = P(A|B) * P(B)")
        self.play(
            Write(VGroup(ea, eb)),
            FadeInFromEdges(joinab)
        )
        self.wait()
        ec = MathTex("C").next_to(eb, RIGHT)
        joinabc = MathTex("P(A,B,C) = P(A|B,C) * P(B|C) * P(C)")
        self.play(
            FadeInFromEdges(ec),
            ReplacementTransform(joinab, joinabc)
        )
        self.wait()
        ed = MathTex("D").next_to(ec, RIGHT)
        joinabcd = MathTex("P(A,B,C,D) = P(A|B,C,D) * P(B|C,D) * P(C|D) * P(D)")
        self.play(
            FadeInFromEdges(ed),
            ReplacementTransform(joinabc, joinabcd)
        )
        self.wait()
        detailGroup = VGroup(ea, eb, ec, ed, joinabcd)
        egeneral = Tex("Chain rule for conditional probability: ").to_corner(LEFT + UP).shift(RIGHT + DOWN)
        joingeneral = MathTex("P(A_1,A_2,...,A_n)", "=",
                              "P(A_1)P(A_2|A_1)P(A_3|A_2,A_1)...P(A_n|A_{n-1}A_{n-2}...A_1)").scale(0.8)
        self.play(
            FadeOutAndShift(detailGroup, LEFT),
            Write(VGroup(egeneral, joingeneral)),
        )
        self.wait()
        ind_text = Tex("Assumption: independent data points").to_edge(DOWN).scale(1.3).shift(UP)
        ind_fh = FreehandRectangle(ind_text, margin=0.2, color=RED, fill_opacity=1, fill_color=PURPLE, partitions=20)
        self.play(
            ShowCreation(ind_fh),
            Write(ind_text)
        )
        self.wait()
        draw = ZigZag(joingeneral, color=RED, stroke_width=10)
        self.play(
            ShowCreation(draw, run_time=1, rate_func=linear)
        )
        self.wait()
        ind_join = MathTex(
            "P(A_1,A_2,...,A_n)", "=",
            "P(A_1)P(A_2)P(A_3)...P(A_n)")
        self.play(
            VGroup(joingeneral, draw).shift, UP * 1.5,
            DrawBorderThenFill(ind_join)
        )
        self.wait()
        self.play(
            FadeOut(VGroup(egeneral,draw,joingeneral,ind_join,ind_text,ind_fh))
        )


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


class compliment(GraphScene):
    def construct(self):
        pdf = MathTex("p(x; \\mu,\\sigma) = \\frac{1}{\\sigma\\sqrt{2\\pi}}exp(-\\frac{(x-\\mu)^2}{2\\sigma^2})")
        self.play(FadeInFromEdges(pdf[0]))
        self.wait()
        self.play(FadeOutAndShift(pdf, DOWN))
        self.wait()