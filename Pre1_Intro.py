from manim import *
from scipy.stats import *
import numpy as np


class Pre(GraphScene):
    CONFIG = {
        "x_min": 0,
        "x_max": 8,
        "y_min": 0,
        "y_max": 1,
        "x_tick_frequency": 1,
        "x_labeled_nums": np.arange(0, 8),
        "y_tick_frequency": 0.1,
        "y_labeled_nums": np.arange(0, 1, 0.1),
        'func_color': YELLOW_A,
        "y_label_decimals": 1,
    }

    def construct(self):
        title = Tex("Maximum Likelyhood Estimation $MLE$")
        equation = MathTex("argmax_{\\theta}( P(data | \\theta))")
        coverPage = VGroup(title, equation).arrange(DOWN)
        self.play(
            Write(title),
            FadeInFrom(equation, DOWN),
        )
        self.wait()
        self.play(UnderlineIndication(equation))
        self.wait()

        self.play(FadeOutAndShift(coverPage, LEFT))
        self.setup_axes(animate=True)
        data = np.random.normal(loc=3.0, scale=1.0, size=100)
        dot_collection = VGroup()
        for wgt in data:
            dot = Dot().move_to(self.coords_to_point(wgt, 0))
            # self.add(dot)
            dot_collection.add(dot)
        self.play(
            FadeInFrom(dot_collection, UP),
            # *[Indicate(d) for d in dot_collection]
        )
        self.wait(2)
        hist = self.show_hist(data)
        self.wait(2)
        group = self.try_other_pdf()
        self.play(FadeOut(VGroup(hist, group, dot_collection, self.axes)))

    def show_hist(self, data):
        def freq(x, data):
            return sum((data >= x) & (data <= x + 1)) / data.size

        kwargs = {
            "x_min": 0,
            "x_max": 7,
            "fill_opacity": 0.75,
            "stroke_width": 0.25,
        }
        flat_rectangles = self.get_riemann_rectangles(
            self.get_graph(lambda x: 0),
            dx=0.25,
            start_color=invert_color(PURPLE),
            end_color=invert_color(ORANGE),
            **kwargs
        )
        hist_rectangles = self.get_riemann_rectangles(
            self.get_graph(lambda x: freq(x, data)),
            dx=0.25,
            start_color=invert_color(PURPLE),
            end_color=invert_color(ORANGE),
            **kwargs
        )
        # Show Riemann rectangles
        self.play(ReplacementTransform(flat_rectangles, hist_rectangles))
        return hist_rectangles

    def try_other_pdf(self):
        def par_pdf(x, miu, sd):
            return norm.pdf(x, miu, sd)

        m = ValueTracker(3)
        sd = ValueTracker(1)

        m_decimal = DecimalNumber(m.get_value()).add_updater(lambda v: v.set_value(m.get_value()))
        sd_decimal = DecimalNumber(sd.get_value()).add_updater(lambda v: v.set_value(sd.get_value()))
        m_text = MathTex("\\mu =")
        sd_text = MathTex("\\sigma =")
        m_text.to_corner(UR).shift(LEFT * 1.5)
        m_decimal.next_to(m_text, RIGHT)
        m_decimal.align_to(m_text, DOWN)
        sd_text.next_to(m_text, DOWN)
        sd_decimal.next_to(sd_text, RIGHT)
        sd_decimal.align_to(sd_text, DOWN)
        label_group = VGroup(m_text, sd_text, m_decimal, sd_decimal)
        self.play(
            *[Write(l) for l in label_group]
        )
        self.wait()
        pdf = self.get_graph(lambda x: par_pdf(x, m.get_value(), sd.get_value()), self.func_color)
        self.play(ShowCreation(pdf), run_time=3)
        self.wait()
        group = VGroup(m_text, sd_text, m_decimal, sd_decimal, pdf)

        def update_group(group):
            mt, st, md, sdd, pdf = group
            pdf.become(self.get_graph(lambda x: par_pdf(x, m.get_value(), sd.get_value()), self.func_color))

        group.add_updater(update_group)

        self.add(group)
        self.play(
            m.set_value, 3.2,
            rate_func=there_and_back_with_pause,
            run_time=4
        )
        self.play(
            m.set_value, 2.7,
            rate_func=there_and_back_with_pause,
            run_time=4
        )
        self.wait()
        self.play(
            sd.set_value, 2,
            rate_func=there_and_back_with_pause,
            run_time=4
        )
        self.play(
            sd.set_value, 0.5,
            rate_func=there_and_back_with_pause,
            run_time=4
        )
        self.wait()
        group.clear_updaters()
        return group


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
