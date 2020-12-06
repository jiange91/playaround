from manim import *
from scipy.stats import *
import numpy as np


class pdf(GraphScene):
    CONFIG = {
        "x_min": 0,
        "x_max": 18,
        "y_min": 0,
        "y_max": 0.8,
        "x_tick_frequency": 1.5,
        "x_labeled_nums": np.arange(3, 16, 3),
        # "y_tick_frequency": 0.2,
        # "y_labeled_nums": np.arange(0, 0.8, 0.2),
        'func_color': YELLOW_A,
        # "y_label_decimals": 1,
        "x_axis_width": 8,
        "y_axis_height": 2.5,
    }

    def construct(self):
        data = self.showData()
        self.add_pdf_and_line(data)

    def showData(self):
        data_text = Tex("data = $[9, 9.5, 11]$")
        self.play(
            FadeIn(data_text),
            data_text.to_edge, UP,
        )
        self.graph_origin = 0.5 * UP + 6 * LEFT
        self.setup_axes(animate=True)
        data = [9, 9.5, 11]
        data_colloction = VGroup()
        for wgt in data:
            dot = Dot().move_to(self.coords_to_point(wgt, 0))
            data_colloction.add(dot)
        self.play(
            FadeInFrom(data_colloction, UP),
            # *[Indicate(d) for d in data_colloction]
        )
        self.wait()
        return data

    def add_pdf_and_line(self, data):
        def par_pdf(x, miu, sd):
            return norm.pdf(x, miu, sd)

        m = ValueTracker(59 / 6)
        sd = ValueTracker(0.84984)

        m_decimal = DecimalNumber(m.get_value(), num_decimal_places=4)
        sd_decimal = DecimalNumber(sd.get_value(), num_decimal_places=4)
        m_text = MathTex("\\mu =")
        sd_text = MathTex("\\sigma =")
        m_text.to_corner(UR).shift(LEFT * 1.5 + DOWN * 1.5)
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
        self.play(ShowCreation(pdf), run_time=3)
        generalGroup = VGroup(m_decimal, sd_decimal, pdf)

        def update_ggroup(group, dt):
            md, sdd, pdf = group
            md.set_value(m.get_value())
            sdd.set_value(sd.get_value())
            pdf.become(self.get_graph(lambda x: par_pdf(x, m.get_value(), sd.get_value()), self.func_color))

        generalGroup.add_updater(update_ggroup)
        self.add(generalGroup)
        self.wait()
        line_collection = VGroup()
        for wgt in data:
            line = self.get_vertical_line_to_graph(wgt, pdf, color=TEAL_A)
            line_collection.add(line)

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
        p1_text.align_to(sd_text, LEFT).next_to(sd_text, DOWN * 7)
        p2_text.next_to(p1_text, DOWN)
        p3_text.next_to(p2_text, DOWN)
        jp_text.next_to(p3_text, DOWN).align_to(p1_text, LEFT)
        p1_decimal.next_to(p1_text, RIGHT).align_to(p1_text, DOWN)
        p2_decimal.next_to(p2_text, RIGHT).align_to(p2_text, DOWN)
        p3_decimal.next_to(p3_text, RIGHT).align_to(p3_text, DOWN)
        jp_decimal.next_to(jp_text, RIGHT).align_to(jp_text, DOWN)
        plabels = VGroup(p1_decimal, p1_text, p2_decimal, p2_text, p3_decimal, p3_text, jp_decimal, jp_text)

        self.play(
            *[ShowCreation(line) for line in line_collection],
            FadeInFrom(VGroup(p1_text, p2_text, p3_text, jp_text, p1_decimal, p2_decimal, p3_decimal, jp_decimal))
        )
        pgroup = VGroup(p1_decimal, p2_decimal, p3_decimal, jp_decimal)
        self.wait()
        def update_lines(group, dt):
            for x, point in zip(data, group):
                pdf = self.get_graph(lambda x: par_pdf(x, m.get_value(), sd.get_value()), self.func_color)
                new_line = self.get_vertical_line_to_graph(x, pdf, color=TEAL_A)
                point.become(new_line)

        line_collection.add_updater(update_lines)
        self.add(line_collection)

        def update_pgroup(group, dt):
            p1d, p2d, p3d, jpd = group
            cp1, cp2, cp3, cjp = getp()
            p1d.set_value(cp1)
            p2d.set_value(cp2)
            p3d.set_value(cp3)
            jpd.set_value(cjp)

        pgroup.add_updater(update_pgroup)
        self.add(pgroup)

        self.play(
            m.set_value, 15,
            rate_func=there_and_back_with_pause,
            run_time=3,
        )
        self.wait()
        self.play(
            m.set_value, 3,
            rate_func=there_and_back_with_pause,
            run_time=3,
        )
        self.wait(3)
        self.play(
            sd.set_value, 0.5,
            rate_functions=linear,
            run_time=3,
        )
        self.wait(2)
        self.play(
            sd.set_value, 2,
            rate_functions=linear,
            run_time=4,
        )
        self.wait(2)
        self.play(
            sd.set_value, 0.84984,
            rate_functions=linear,
            run_time=3,
        )
        self.wait()


class jp(GraphScene):
    CONFIG = {
        "x_min": 0,
        "x_max": 18,
        "y_min": 0,
        "y_max": 0.05,
        "x_tick_frequency": 1.5,
        "x_labeled_nums": np.arange(3, 16, 3),
        # "y_tick_frequency": 0.2,
        # "y_labeled_nums": np.arange(0, 0.8, 0.2),
        'func_color': YELLOW_A,
        # "y_label_decimals": 1,
        "x_axis_width": 8,
        "y_axis_height": 2.5,
    }

    def construct(self):
        self.wait(7)
        self.graph_origin = 3.5 * DOWN + 6 * LEFT
        self.setup_axes(animate=True)
        data = [9, 9.5, 11]
        m = ValueTracker(59 / 6)
        sd = ValueTracker(0.84984)

        def par_pdf(x, miu, sd):
            return norm.pdf(x, miu, sd)

        def getp():
            p1 = par_pdf(9, m.get_value(), sd.get_value())
            p2 = par_pdf(9.5, m.get_value(), sd.get_value())
            p3 = par_pdf(11, m.get_value(), sd.get_value())
            jp = p1 * p2 * p3
            return jp

        def getp_mu(mu):
            p1 = par_pdf(9, mu, sd.get_value())
            p2 = par_pdf(9.5, mu, sd.get_value())
            p3 = par_pdf(11, mu, sd.get_value())
            jp = p1 * p2 * p3
            return jp

        def lh_dot():
            jp = getp()
            d = Dot().move_to(self.coords_to_point(m.get_value(), jp))
            return d

        dd = always_redraw(lh_dot)
        self.add(dd)
        self.wait()
        jp_max_x = 15
        jp_min_x = 3

        jp_miu = self.get_graph(
            lambda mu: getp_mu(mu),
            x_max=jp_max_x,
            x_min=jp_min_x,
            color=BLUE_B,
        )

        def update_sd_to_jp(func, dt):
            new_func = self.get_graph(
                lambda mu: getp_mu(mu),
                x_max=jp_max_x,
                x_min=jp_min_x,
                color=RED_A,
            )
            func.become(new_func)
            return func
        jp_miu.add_updater(update_sd_to_jp)
        self.wait(2)
        self.play(
            m.set_value, jp_max_x,
            rate_func=there_and_back_with_pause,
            run_time=3,
        )
        self.wait()
        self.play(
            m.set_value, jp_min_x,
            rate_func=there_and_back_with_pause,
            run_time=3,
        )
        self.wait()
        self.play(ShowCreation(jp_miu), run_time=2)
        # self.add(jp_miu_copy)
        self.play(
            sd.set_value, 0.5,
            rate_functions=linear,
            run_time=3,
        )
        jp_miu_sd1 = self.get_graph(
            lambda mu: getp_mu(mu),
            x_max=jp_max_x,
            x_min=jp_min_x,
            color=GREEN_A,
        )
        self.play(ShowCreation(jp_miu_sd1), run_time=1)
        self.wait()
        self.play(
            sd.set_value, 2,
            rate_functions=linear,
            run_time=4,
        )
        print(m.get_value(), sd.get_value())
        jp_miu_sd2 = self.get_graph(
            lambda mu: getp_mu(mu),
            x_max=jp_max_x,
            x_min=jp_min_x,
            color=BLUE_A,
        )
        self.play(ShowCreation(jp_miu_sd2), run_time=1)
        self.wait()
        self.play(
            sd.set_value, 0.84984,
            rate_functions=linear,
            run_time=3,
        )
        self.wait()
