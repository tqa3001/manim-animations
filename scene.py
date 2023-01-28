from manim import *

class Anim1(Scene): 
    def construct(self): 
        vn = TexTemplate(preamble=r"\usepackage[english, vietnamese]{babel}")
        s = Text("ABAACABABABAABC").to_corner(LEFT + UP) # Cannot use len() for Tex()?
        str_len = 15
        
        array_len, array_height, array_width = str_len, 0.6, 0.6
        mid_index = str_len // 2 
        array = [Rectangle(color=ORANGE, height=array_height, width=array_width) for i in range(array_len)]
        array[mid_index].move_to(ORIGIN) 
        for i in range(mid_index - 1, -1, -1): 
            array[i].next_to(array[i + 1], LEFT / 3)
        for i in range(mid_index + 1, array_len): 
            array[i].next_to(array[i - 1], RIGHT / 3)
        indices = [Integer(i).move_to(array[i].get_center() + DOWN / 1.6).scale(0.7) for i in range(array_len)]

        self.play(FadeIn(s))
        self.play(s.animate.scale(0.5))

        for i in range(array_len): 
            self.play(Create(array[i]), Create(indices[i]), run_time=0.04)
        for i in range(str_len): 
            self.play(s[i].animate.move_to(array[i].get_center()), run_time=0.04) 

        desc_group = VGroup(Tex("Chúng ta cần tìm $\pi[9]$.", tex_template=vn), Tex("$\pi[0], \pi[1], \dots, \pi[8]$ đã được tính", tex_template=vn)) 
        desc_group.to_corner(UP)
        desc_group.arrange(DOWN, buff=0.5, center=False)
        self.play(Write(desc_group[0]), run_time=0.5)
        
        index_tracker = ValueTracker(0)
        cur_index = lambda: int(index_tracker.get_value())

        arrow_length = 1.3
        arrow = Arrow()  # indices[mid_index].get_center()
        arrow.add_updater(
            lambda x: x.become(Arrow(
                start=indices[cur_index()].get_bottom() + arrow_length * DOWN, 
                end=indices[cur_index()].get_bottom(), 
                stroke_width=6, color=RED)
            )
        )

        self.play(Create(arrow))
        self.play(index_tracker.animate.set_value(9))
        self.play(Write(desc_group[1]), run_time=0.5)
        
        temp_line = Line(indices[0].get_bottom(), indices[cur_index() - 1].get_bottom()) 
        brace = Brace(temp_line)
        self.play(Create(brace)) 

        pi_label = Tex('$\pi$:  ').to_corner(LEFT + DOWN).shift([1, 1, 0])
        self.play(Write(pi_label), run_time=0.3) 

        prefix_funct = [0, 0, 1, 1, 0, 1, 2, 3, 2, '?']
        pi_mobj = []
        previous_rec = pi_label
        for i, ref in enumerate(array[0:cur_index() + 1]): 
            cur = ref.copy() # A different copy function for Mobject
            cur.color = YELLOW_D if i < cur_index() else RED_B
            self.play(cur.animate.next_to(previous_rec, RIGHT/3), run_time=0.25)
            if i == cur_index():
                self.wait()
            cur_pi_text = Text(str(prefix_funct[i]), font_size=20).move_to(cur.get_center())
            self.play(Write(cur_pi_text), 
                run_time=0.05 if i < cur_index() else 1)
            previous_rec = cur 
            pi_mobj.append(cur)

        self.play(FadeOut(brace), FadeOut(desc_group), FadeOut(cur_pi_text), run_time=0.6)
        self.play(Write(desc_group[0].become(Tex('$\pi[8] = 2$ (``AB")'), match_center=True)), run_time=0.5)

        # Rectangle boxes
        box_1 = SurroundingRectangle(VGroup(*array[0: prefix_funct[cur_index() - 1]]), buff=0.05)
        box_2 = SurroundingRectangle(VGroup(*array[cur_index() - prefix_funct[cur_index() - 1]: cur_index()]), buff=0.05)
            
        self.play(Create(box_1), Create(box_2), run_time=0.5) 
        
        desc_group[1].become(Tex('So sánh s[i] và s[$\pi[i - 1]$]', tex_template=vn), match_center=True) 
        self.play(Write(desc_group[1]), run_time=1.5)
        self.play(
            desc_group[1].animate.become(
                Tex(f'So sánh s[{cur_index()}] và s[{prefix_funct[cur_index() - 1]}]', tex_template=vn), 
                match_center=True
            ), 
            run_time=1.5
        )
        # non-generalizing
        temp_text = Tex('Ta có ', f's[{cur_index()}] = s[{prefix_funct[cur_index() - 1]}] (== ``A")', tex_template=vn)
        temp_text[1].set_color(GREEN)
        self.play(
            desc_group[1].animate.become(
                temp_text.copy(), 
                match_center=True    
            ), 
            run_time = 2
        )
        self.play(
            array[prefix_funct[cur_index() - 1]].animate.set_fill(GREEN_E, opacity=0.6), 
            array[cur_index()].animate.set_fill(GREEN_E, opacity=0.6)
        )
        
        self.play(FadeOut(desc_group), run_time=0.5)
        desc_group[0].become(Tex(f'Suy ra $\pi[{cur_index()}]$ = ', f'{prefix_funct[cur_index() - 1] + 1}', color=RED, tex_template=vn), match_center=True)
        temp_text.become(desc_group[0][1].copy().set(font_size=20)) 
        self.play(Write(desc_group[0]), run_time=2)
        
        self.play(
            box_1.animate.become(SurroundingRectangle(VGroup(*array[0: prefix_funct[cur_index() - 1] + 1]), buff=0.05)), 
            box_2.animate.become(
                SurroundingRectangle(VGroup(*array[cur_index() - prefix_funct[cur_index() - 1]: cur_index() + 1]), buff=0.05)
            ), 
            temp_text.animate.move_to(cur_pi_text)
        )   
        prefix_funct[cur_index()] = prefix_funct[cur_index() - 1] + 1 
        self.wait()

        self.play(
            FadeOut(VGroup(
                box_1, box_2, desc_group[0], 
            )), 
            array[prefix_funct[cur_index() - 1]].animate.set_fill(GREEN_E, opacity=0), 
            array[cur_index()].animate.set_fill(GREEN_E, opacity=0), 
            temp_text.animate.set_color(WHITE), 
            cur.animate.set_color(YELLOW_D)
        )

        cur = (cur.copy()).next_to(cur, RIGHT/3)
        pi_mobj.append(cur)
        self.play(
            Write(desc_group[0].become(Tex('Tính $\pi[10]$', tex_template=vn), match_center=True)), 
            index_tracker.animate.set_value(10)
        )
        self.play(Create(cur))
        
        self.play(Write(desc_group[1].become(Tex('Ta thử mở rộng tiền tố có độ dài $\pi[9]$ = 3', tex_template=vn), match_center=True)))
        
        self.play(FadeOut(desc_group))  
         
        self.play(
            Create(box_1.become(SurroundingRectangle(VGroup(*array[0: prefix_funct[cur_index() - 1]]), buff=0.05))), 
            Create(box_2.become(
                SurroundingRectangle(VGroup(*array[cur_index() - prefix_funct[cur_index() - 1]: cur_index()]), buff=0.05)
            )), 
        ) 

        self.play(
            Write(desc_group[0].become(Tex(f'$s[{prefix_funct[cur_index() - 1]}] \\neq s[{cur_index()}]$'), match_center=True)), 
            array[prefix_funct[cur_index() - 1]].animate.set_fill(RED_E, opacity=0.6), 
            array[cur_index()].animate.set_fill(RED_E, opacity=0.6)
        )

        self.play(
            Write(desc_group[1].become(Tex(f'Do đó ta thử một tiền tố ngắn hơn cũng là hậu tố của $s[0 \dots {cur_index() - 1}]$', tex_template=vn), match_center=True))
        )

        self.play(
            FadeOut(VGroup(desc_group, box_1, box_2)),  
            array[prefix_funct[cur_index() - 1]].animate.set_fill(RED_E, opacity=0), 
            array[cur_index()].animate.set_fill(RED_E, opacity=0)
        )

        self.play(Write(desc_group[0].become(Tex(f'Thử tiền tố có độ dài $\pi[\pi[{cur_index() - 1}] - 1]$', tex_template=vn), match_center=True)))
        
        brace = Brace(Line(array[0].get_center() + UP/3, array[2].get_center() + UP/3), direction=UP)
        temp_text = Tex(f'$\pi[{cur_index() - 1}] = 3$').next_to(brace, UP/3)
        self.play(
            Create(box_1.become(SurroundingRectangle(VGroup(*array[0: prefix_funct[cur_index() - 1]]), buff=0.05))), 
            Create(brace),  
            Write(temp_text)
        ) 
        self.play(temp_text.animate.become(Tex(f'$\pi[{cur_index() - 1}] - 1 = 2$'), match_center=True))
        self.play(FadeOut(brace), temp_text.animate.next_to(pi_mobj[2].get_top(), UP))
        self.play(
            pi_mobj[2].animate.set_fill(BLUE_E, opacity=0.6), 
            desc_group[0].animate.become(
                Tex('Thử tiền tố có độ dài 1', tex_template=vn), match_center=True)
        )
        # return 

        # Code is non-generalizing starting from here. 
        self.play(  
            array[0].animate.set_fill(GREEN_E, opacity=0.6), 
            array[2].animate.set_fill(GREEN_E, opacity=0.6)
        )

        self.play(
            Create(box_2.become(
                SurroundingRectangle(VGroup(*array[cur_index() - prefix_funct[cur_index() - 1]: cur_index()]), buff=0.05)
            )), 
        )
    
        self.play(  
            array[cur_index() - prefix_funct[cur_index() - 1]].animate.set_fill(GREEN_E, opacity=0.6),
            array[cur_index() - 1].animate.set_fill(GREEN_E, opacity=0.6)
        )
        
        self.play(
            FadeOut(temp_text),  # among us moment
            pi_mobj[2].animate.set_fill(BLUE_E, opacity=0), 
            array[2].animate.set_fill(GREEN_E, opacity=0), 
            array[cur_index() - prefix_funct[cur_index() - 1]].animate.set_fill(GREEN_E, opacity=0),
            box_1.animate.become(SurroundingRectangle(array[0], buff=0.05)), 
            box_2.animate.become(SurroundingRectangle(array[cur_index() - 1], buff=0.05))
        ) 

        self.play(Write(desc_group[1].become(Tex(f'So sánh s[1] và s[{cur_index()}]', tex_template=vn), match_center=True)))
        self.play(
            desc_group[1].animate.become(Tex('s[1] = s[10]'), match_center=True), 
            array[1].animate.set_fill(GREEN_E, opacity=0.6), 
            array[cur_index()].animate.set_fill(GREEN_E, opacity=0.6)
        )
        self.play(FadeOut(desc_group))
        self.play(
            Write(desc_group[0].become(Tex('Suy ra $\pi[10]$ = ', '2', tex_template=vn), match_center=True)),  
            box_1.animate.become(SurroundingRectangle(VGroup(array[0], array[1]), buff=0.05)), 
            box_2.animate.become(SurroundingRectangle(VGroup(array[cur_index() - 1], array[cur_index()]), buff=0.05))
        )

        temp_text = desc_group[0][1].copy().set_color(GREEN_E).scale(0.7)
        print(cur) 
        self.play(temp_text.animate.move_to(cur.get_center()))
        self.wait(2)

class Anim2(Scene): 
    def construct(self): 
        vn = TexTemplate(preamble=r"\usepackage[english, vietnamese]{babel}")
        # This part is bad repetitive code. It does the job but you should improve it later. 
        s = Text("ABAMVABADEABAMVABAB").to_corner(LEFT + UP) # Cannot use len() for Tex()?
        str_len = 19
        
        array_len, array_height, array_width = str_len, 0.6, 0.6
        mid_index = str_len // 2 
        array = [Rectangle(color=ORANGE, height=array_height, width=array_width) for i in range(array_len)]
        array[mid_index].move_to(ORIGIN) 
        for i in range(mid_index - 1, -1, -1): 
            array[i].next_to(array[i + 1], LEFT / 3)
        for i in range(mid_index + 1, array_len): 
            array[i].next_to(array[i - 1], RIGHT / 3)
        indices = [Integer(i).move_to(array[i].get_center() + DOWN / 1.6).scale(0.7) for i in range(array_len)]

        self.play(FadeIn(s))
        self.play(s.animate.scale(0.5))

        for i in range(array_len): 
            self.play(Create(array[i]), Create(indices[i]), run_time=0.04)
        for i in range(str_len): 
            self.play(s[i].animate.move_to(array[i].get_center()), run_time=0.04) 
        
        desc = Tex('Liên tiếp cập nhật $j = \pi[j-1]$ đồng nghĩa với duyệt qua mọi tiền tố cũng là hậu tố của $s[0 \dots i-1]$', font_size=35, tex_template=vn).to_corner(LEFT + UP)
        self.play(Write(desc)) 

        box, brace, text = VMobject(), VMobject(), VMobject()
        values_j = [8, 3, 1]
            
        prev_j = 17  
        for cnt, j in enumerate(values_j): 
            temp_arr = []
            for rectangle in array: 
                temp_arr.append(rectangle.copy())
            for i in range(array_len - 1): 
                temp_arr[i].set_fill(GREEN_E, opacity=0.6)
            temp_line = Line(array[0].get_center(), array[j - 1].get_center())
            temp_label = [r"$\pi[17]$", r"$\pi[\pi[17] - 1]]$", r"$\pi[\pi[\pi[17] - 1]] - 1]$"]
            self.play(
                box.animate.become(
                    SurroundingRectangle(VGroup(*array[0:j]), buff=0.05)
                ), 
                brace.animate.become(
                    Brace(temp_line, direction=UP, buff=0.5)
                ), 
                text.animate.become(
                    Text(f'j = {j}', font_size=30).next_to(temp_line.get_center(), UP * 3)
                ),
                FadeIn(
                    VGroup(*temp_arr[0: j], *temp_arr[prev_j - j + 1: prev_j + 1], *temp_arr[array_len - j - 1: array_len - 1])
                    if cnt > 0
                    else VGroup(*temp_arr[0: j], *temp_arr[array_len - j - 1: array_len - 1])
                ), 
            )
            if (cnt < 2):
                temp_text = Tex(f"$s[{j}] \\neq s[{array_len - 1}]$", font_size=35).next_to(desc, DOWN)
            else:  # \eq does not exists smh my head
                temp_text = Tex(f"$s[{j}] = s[{array_len - 1}]$", font_size=30).next_to(desc, DOWN)
            self.play(
                array[j].animate.set_fill(RED_E if cnt < 2 else GREEN_E, opacity=0.6), 
                temp_arr[array_len - 1].animate.set_fill(RED_E if cnt < 2 else GREEN_E, opacity=0.6),
                Write(temp_text)
            )
            self.play(
                FadeOut(
                    VGroup(*temp_arr[0: j], *temp_arr[prev_j - j + 1: prev_j + 1])
                    if cnt > 0
                    else VGroup(*temp_arr[0: j])
                ),
                VGroup(*temp_arr[array_len - j - 1: array_len]).animate.shift((DOWN / 1.5) * (cnt + 3)), 
                array[j].animate.set_fill(RED if cnt < 2 else GREEN_E, opacity=0)
            )
            sub_text = Tex(temp_label[cnt] + f" = {j}", font_size=35, color=(RED if cnt < 2 else GREEN)).next_to(
                VGroup(*temp_arr[array_len - j - 1: array_len - 1]), LEFT)
            self.play(
                Write(sub_text)
            ) 
            self.play(FadeOut(temp_text))
            prev_j = j 

        self.play(
            Write(Tex(f'Suy ra $\pi[{array_len - 1}]$ = 2', color=GREEN, tex_template=vn).to_corner(LEFT + DOWN)), 
            FadeOut(box), 
            FadeOut(text)
        )
        self.wait(5)

