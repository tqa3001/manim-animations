from manim import *

class Test(Scene): 
    def construct(self): 
        # myTemplate = TexTemplate(tex_compiler="xelatex", output_format=".pdf", preamble=r"\usepackage[banglamainfont=Kalpurush, banglattfont=Kalpurush]{latexbangla}")
        # tex = Tex(r"আইনস্টাইনের সমীকরণ, $E^2=(mc^2)^2+(pc)^2$", tex_template=myTemplate)
        # self.play(Write(tex))
        # return 
        vn = TexTemplate(preamble=r"\usepackage[english, vietnamese]{babel}")  # \usepackage[utf8]{inputenc} 
        text = Tex(r"kẻ hủy diệt C3", tex_template=vn) 
        self.play(Write(text))
