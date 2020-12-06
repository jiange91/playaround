from manim import *
from scipy.stats import *
import numpy as np


class Detail(GraphScene):
    CONFIG = {
        "x_min": 0,
        "x_max": 18,
        "y_min": 0,
        "y_max": 1.0,
        "x_tick_frequency": 1.5,
        "x_labeled_nums": np.arange(3, 16, 3),
        "y_tick_frequency": 0.1,
        "y_labeled_nums": np.arange(0, 1, 0.1),
        'func_color': YELLOW_A,
        "y_label_decimals": 1,
    }

    def construct(self):
        self.showExemple()

    def showExemple(self):
        data_text = Tex("data = $[9, 9.5, 11]$")
        self.play(FadeIn(data_text))
        self.wait()
        conditional = MathTex("L(x_1, x_2, x_3| \\mu, \\sigma)")
        self.play(
            data_text.shift, UP,
            Write(conditional),
        )
        self.wait()
        self.play(
            data_text.to_edge, UP,
            FadeOutAndShift(conditional, UP),
        )
        self.setup_axes(animate=True)

        def par_pdf(x, miu, sd):
            return norm.pdf(x, miu, sd)

        m = ValueTracker(9)
        sd = ValueTracker(1)

        m_decimal = DecimalNumber(m.get_value())
        sd_decimal = DecimalNumber(sd.get_value())
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
        pdf = self.get_graph(lambda x: par_pdf(x, m.get_value(), sd.get_value()), self.func_color)
        self.play(ShowCreation(pdf), run_time=2)
        ugroup = VGroup(m_decimal, sd_decimal, pdf)

        def update_group(group):
            md, sdd, pdf = group
            md.set_value(m.get_value())
            sdd.set_value(sd.get_value())
            pdf.become(self.get_graph(lambda x: par_pdf(x, m.get_value(), sd.get_value()), self.func_color))

        ugroup.add_updater(update_group)
        self.add(ugroup)
        self.wait()
        data = [9, 9.5, 11]
        data_collection = VGroup()
        line_collection = VGroup()
        for wgt in data:
            dot = Dot().move_to(self.coords_to_point(wgt, 0))
            line = self.get_vertical_line_to_graph(wgt, pdf, color=TEAL_A)
            data_collection.add(dot)
            line_collection.add(line)
        self.play(
            FadeInFrom(data_collection, UP),
            *[Flash(point, color=GRAY, flash_radius=0.5) for point in data_collection]
        )
        self.wait()
        self.play(
            *[ShowCreation(line) for line in line_collection]
        )

        def update_lines(group):
            for x, point in zip(data, group):
                pdf = self.get_graph(lambda x: par_pdf(x, m.get_value(), sd.get_value()), self.func_color)
                new_line = self.get_vertical_line_to_graph(x, pdf, color=TEAL_A)
                point.become(new_line)

        line_collection.add_updater(update_lines)
        self.add(line_collection)

        def getp():
            p1 = par_pdf(9, m.get_value(), sd.get_value())
            p2 = par_pdf(9.5, m.get_value(), sd.get_value())
            p3 = par_pdf(11, m.get_value(), sd.get_value())
            jp = p1 * p2 * p3
            return p1, p2, p3, jp

        p1, p2, p3, jp = getp()
        p1_decimal = DecimalNumber(p1, num_decimal_places=3)
        p2_decimal = DecimalNumber(p2, num_decimal_places=3)
        p3_decimal = DecimalNumber(p3, num_decimal_places=3)
        jp_decimal = DecimalNumber(jp, num_decimal_places=3)
        p1_text = MathTex("p1 =")
        p2_text = MathTex("p2 =")
        p3_text = MathTex("p3 =")
        jp_text = MathTex("LH = ")
        p1_text.align_to(sd_text, LEFT).next_to(sd_text, DOWN * 1.6)
        p2_text.next_to(p1_text, DOWN)
        p3_text.next_to(p2_text, DOWN)
        jp_text.next_to(p3_text, DOWN).align_to(p1_text, LEFT)
        p1_decimal.next_to(p1_text, RIGHT).align_to(p1_text, DOWN)
        p2_decimal.next_to(p2_text, RIGHT).align_to(p2_text, DOWN)
        p3_decimal.next_to(p3_text, RIGHT).align_to(p3_text, DOWN)
        jp_decimal.next_to(jp_text, RIGHT).align_to(jp_text, DOWN)
        plabels = VGroup(p1_decimal, p1_text, p2_decimal, p2_text, p3_decimal, p3_text)

        self.play(
            FadeInFrom(VGroup(p1_text, p2_text, p3_text, p1_decimal, p2_decimal, p3_decimal))
        )
        self.wait()
        self.play(Write(VGroup(jp_text,jp_decimal)))
        self.wait()
        pgroup = VGroup(p1_decimal, p2_decimal, p3_decimal, jp_decimal)

        def update_pgroup(group):
            p1d, p2d, p3d, jpd = group
            cp1, cp2, cp3, cjp = getp()
            p1d.set_value(cp1)
            p2d.set_value(cp2)
            p3d.set_value(cp3)
            jpd.set_value(cjp)

        pgroup.add_updater(update_pgroup)
        self.add(pgroup)

        self.play(
            m.set_value, 10,
            rate_func=there_and_back_with_pause,
            run_time=3
        )
        self.wait()
        self.play(
            sd.set_value, 2,
            rate_func=there_and_back_with_pause,
            run_time=3
        )
        self.wait()
        ugroup.clear_updaters()
        line_collection.clear_updaters()
        pgroup.clear_updaters()
        self.play(
            FadeOut(VGroup(self.axes, ugroup, line_collection, plabels,jp_text,jp_decimal, m_text, sd_text, data_text, data_collection))
        )
