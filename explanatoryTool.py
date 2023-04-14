from manim import*
from calculate import*
from decimal import Decimal
import random
import numpy as np
from math import*
# constant

FRAME_WIDTH: float = config.frame_width
FRAME_HEIGHT: float = config.frame_height

# constant for Title-Formula-Animation (TFA) layout type
TFA_TITLE: np.ndarray = np.array((FRAME_WIDTH*0.5, FRAME_HEIGHT*0.09, 0))
TFA_TITLE_WIDTH: float = FRAME_WIDTH*0.8
TFA_TITLE_HEIGHT: float = FRAME_HEIGHT*0.12
TFA_FORMULA: list[np.ndarray] = [np.array((FRAME_WIDTH*0.05, FRAME_HEIGHT*(0.2775+0.085*x), 0)) for x in range(8)]
TFA_FORMULA_WIDTH: float = FRAME_WIDTH*0.4
TFA_FORMULA_HEIGHT: float = FRAME_HEIGHT*0.085
TFA_ANIMATION: np.ndarray = np.array((FRAME_WIDTH*0.55, FRAME_HEIGHT*0.507, 0))
TFA_ANIMATION_WIDTH: float = FRAME_WIDTH*0.4
TFA_ANIMATION_HEIGHT: float = FRAME_HEIGHT*0.544
TFA_ANSWER: np.ndarray = np.array((FRAME_WIDTH*0.55, FRAME_HEIGHT*0.847, 0))
TFA_ANSWER_WIDTH: float = FRAME_WIDTH*0.4
TFA_ANSWER_HEIGHT: float = FRAME_HEIGHT*0.136

# basic fuction

def random_color_set():
    color_set=[
        BLUE_A, BLUE_B, BLUE_C, BLUE_D, BLUE_E, PURE_BLUE, DARK_BLUE,
        TEAL_A, TEAL_B, TEAL_C, TEAL_D, TEAL_E,
        GREEN_A, GREEN_B, GREEN_C, GREEN_D, GREEN_E, PURE_GREEN,
        YELLOW_A, YELLOW_B, YELLOW_C, YELLOW_D, YELLOW_E, 
        RED_A, RED_B, RED_C, RED_D, RED_E, PURE_RED, 
        MAROON_A, MAROON_B, MAROON_C, MAROON_D, MAROON_E,
        PURPLE_A, PURPLE_B, PURPLE_C, PURPLE_D, PURPLE_E,
        PINK, LIGHT_PINK,
        ORANGE,
        LIGHT_BROWN, DARK_BROWN, GRAY_BROWN
    ]
    return random.choice(color_set)

def fill(*args, max_len=0, fil='', rev=False): 
    for i in args:
        if i != []: 
            for j in i:
                for k in range(max_len-len(j)):
                    j.insert(0, fil)
                    if rev:
                        j.reverse()

def adaptiveSize(
    mobject:Mobject, 
    max_width:float=FRAME_WIDTH, 
    max_height:float=FRAME_HEIGHT, 
    min_width:float=0, 
    min_height:float=0
) -> Mobject:
    
    if max_width < min_width:
        raise ValueError('max_width should be bigger than min_width')
    elif min_width < 0:
        raise ValueError('min_width should be 0 or positive')
    else:
        if mobject.width > max_width:
            mobject.width = max_width
        if mobject.width < min_width:
            mobject.width = min_width
    
    if max_height < min_height:
        raise ValueError('max_height should be bigger than min_height')
    elif min_height < 0:
        raise ValueError('min_height should be 0 or positive')
    else:
        if mobject.height > max_height:
            mobject.height = max_height
        if mobject.height < min_height:
            mobject.height = min_height
    
    return mobject

def adaptiveWidth(
    width:float|int, 
    max_width:float=FRAME_WIDTH, 
    min_width:float=0
) -> float|int:
        
    if max_width < min_width:
        raise ValueError('max_width should be bigger than min_width')
    elif min_width < 0:
        raise ValueError('min_width should be 0 or positive')
    else:
        if width > max_width:
            width = max_width
        if width < min_width:
            width = min_width
    
    return width

def adaptiveLocation(
    mobject:Mobject,
    origin:np.ndarray=np.array((-FRAME_WIDTH/2, FRAME_HEIGHT/2, 0.0)),
    position:np.ndarray=ORIGIN,
    aligned_edge:np.ndarray=ORIGIN,
    vertical_mir:bool=False,
    horizontal_mir:bool=False
) -> Mobject:
    
    mirror = ((-1)**horizontal_mir, (-1)**vertical_mir, 0)
    position = np.multiply(position, mirror)
    position = np.add(position, origin)
    mobject.move_to(position, aligned_edge=aligned_edge)
    return mobject

def stringReplace(text:str) -> str:
    replacement_dict = {
        ' ':'',
        '+':' + ',
        'x':' × ',
        'X':' × ',
        '*':' × ',
        '-':' − ',
        '/':' ÷ ',
        '(':' ( ',
        ')':' ) ',
        '=':' = '
    }
    for i in replacement_dict:
        text = text.replace(i, replacement_dict[i])
    
    return text

class explanatoryTools(Scene):

    def column_form(upper=[], middle=[], lower=[], sign='', include_outer_lines=False, include_inner_lines=False, include_vertical_lines=False, include_horizontal_lines=False):

        # Calculate
        max_col = len(str(max(upper+lower)))
        max_row = len(upper+middle+lower)

        upper__str = [list(str(num)) for num in upper]
        middle_str = [list(str(num)) for num in middle]
        lower_str = [list(str(num)) for num in lower]
        fill(upper__str,middle_str,lower_str, max_len=max_col)

        col_labels_ref = []
        for i in ['千兆', '百兆', '十兆', '兆', '千億', '百億', '十億', '億', '千萬', '百萬', '十萬', '萬', '千', '百', '十', '個']:
            col_labels_ref.append(Text(i))
        row_labels = [Text('') for i in range(max_row-2)]+[Text(sign), Text('=')]

        # Table Generating
        table = Table(
            upper__str+middle_str+lower_str,
            row_labels= row_labels,
            col_labels = col_labels_ref[-max_col:],
            )

        # Position and Size Adjustment
        scale_x = (FRAME_WIDTH-2)/table.width
        scale_y = (FRAME_HEIGHT-5)/table.height
        table = table.scale(min(scale_x, scale_y)).to_corner(DOWN, buff=1.6)

        # Style settings
        table_color = random_color_set()
        for i in range(max_col):
                table.add_highlighted_cell((1,2+i), color=table_color)
        table.get_vertical_lines().set_fill(opacity=0).set_stroke(opacity=0)
        table.get_horizontal_lines().set_color(config.background_color)
        table.get_horizontal_lines()[-1].set_color(table_color)
        table.get_entries_without_labels()[-max_col:].set_color(BLACK)

        attention = []
        for i in range(max_col):
            attention.append(table.get_cell((max_row+1, max_col+1-i), color=RED))

        return table, attention, max_col

    def column_form(self, *args, position, width, height, speed=1, clear=False, font="Noto Sans TC Medium", font_color=WHITE, font_size=12, bold=False, slant=False, **kwargs):
        # Calculate
        max_col = len(str(max(args)))
        max_row = len()

        upper__str = [list(str(num)) for num in upper]
        middle_str = [list(str(num)) for num in middle]
        lower_str = [list(str(num)) for num in lower]
        fill(upper__str, middle_str, lower_str, max_len=max_col)

        col_labels_ref = [i for i in ['千兆', '百兆', '十兆', '兆', '千億', '百億', '十億', '億', '千萬', '百萬', '十萬', '萬', '千', '百', '十', '個']]

        row_labels = [Text('') for i in range(max_row-2)]+[Text(sign), Text('=')]

        # Table Generating
        table = Table(
            upper__str+middle_str+lower_str,
            row_labels= row_labels,
            col_labels = col_labels_ref[-max_col:],
            )

        # Position and Size Adjustment
        scale_x = (FRAME_WIDTH-2)/table.width
        scale_y = (FRAME_HEIGHT-5)/table.height
        table = table.scale(min(scale_x, scale_y)).to_corner(DOWN, buff=1.6)

        # Style settings
        table_color = random_color_set()
        for i in range(max_col):
                table.add_highlighted_cell((1,2+i), color=table_color)
        table.get_vertical_lines().set_fill(opacity=0).set_stroke(opacity=0)
        table.get_horizontal_lines().set_color(config.background_color)
        table.get_horizontal_lines()[-1].set_color(table_color)
        table.get_entries_without_labels()[-max_col:].set_color(BLACK)

        attention = []
        for i in range(max_col):
            attention.append(table.get_cell((max_row+1, max_col+1-i), color=RED))

        return table, attention, max_col

    def add_column_form(self, *args, position, width, height, speed=1, clear=False, font="Noto Sans TC Medium", font_color=WHITE, font_size=12, bold=False, slant=False, **kwargs):
        result = sum(args)
        list1, list2 = [list(map(int,str(num))) for num in args]
        list1.reverse()
        list2.reverse()
        carry_str_list=carry_list(list1, list2)
        
        add_table, attention, max_col = self.column_form(upper=list(args), lower=[result], sign='+')

        carry_Text_list = []
        for i in range(max_col):
            carry_Text_list.append(Text(carry_str_list[i], color = YELLOW, stroke_width=0.2).scale(0.4).next_to(add_table.get_cell((1, max_col+1-i)), DL*0.5))

        self.play(Create(add_table))
        self.wait(1)
        
        for i in range(max_col):
            self.play(Create(attention[i]))
            self.wait(1)
            self.play(Write(add_table.get_entries_without_labels()[-(i+1)].set_color(WHITE)))

            if i+1 < max_col:
                self.play(Write(carry_Text_list[i]))
                self.wait(0.5)
            if i > 0:
                self.play(Unwrite(carry_Text_list[i-1]))
                self.wait(1)
            self.play(Uncreate(attention[i]),)
        
    def sub_column_form(self, *args):
        result = args[0]
        for i in args[1:]:
            result = result-i
        result_len = len(str(result))

        list1, list2 = [list(map(int,str(num))) for num in args]
        list1.reverse()
        list2.reverse()
        borrow_str_list=borrow_list(list1, list2)
        
        sub_table, attention, max_col = self.column_form(upper=list(args), lower=[result], sign='-')

        borrow_Text_list = []
        for i in range(len(borrow_str_list)):
            digit_borrow_list = []
            set_color = random_color_set()
            for j in range(len(borrow_str_list[i])):               
                text = Text(borrow_str_list[i][j], color=set_color, stroke_width=0.2).scale(0.4)
                if j == len(borrow_str_list[i])-1:
                    text.next_to(sub_table.get_cell((1,max_col-i-j)), DR*0.5)
                else:
                    text.next_to(sub_table.get_cell((1,max_col+1-i-j)), DR*0.5). shift(LEFT*0.5)
                digit_borrow_list.append(text)
            digit_borrow_list.reverse()
            borrow_Text_list.append(digit_borrow_list)

        #直式減法過程
        self.play(Create(sub_table))

        for i in range(result_len):
            self.play(Create(attention[i]))
            self.wait(1)
            if i < len(borrow_Text_list):
                for j in borrow_Text_list[i]:
                    self.play(Write(j))
                    self.wait(0.5)
            if i < result_len:
                self.play(Write(sub_table.get_entries_without_labels()[-(i+1)].set_color(WHITE)))
                self.wait(1)
            self.play(Uncreate(attention[i]))
        self.wait(1)
    
    def text(self, text, position, max_width=FRAME_WIDTH, max_height=FRAME_HEIGHT, speed=1, aligned_edge=UL, clear=False, font="Noto Sans TC Medium", font_color=WHITE, font_size=24, bold=False, slant=False, type='video', **kwargs):
        text = stringReplace(text)
        text = Text(text=f'{text}', color=font_color, font_size=font_size, font=font, weight=(NORMAL, BOLD)[bold], slant=(NORMAL, ITALIC)[slant])
        text = adaptiveSize(text, max_width, max_height)
        text = adaptiveLocation(text, position=position, aligned_edge=aligned_edge, vertical_mir=True)
        
        match type:
            case 'video':
                self.play(AddTextLetterByLetter(text), run_time=1/speed)
                self.wait(1)
            case 'image':
                self.add(text)

        if clear:
            self.pause()
            self.remove(text)
            self.pause()

    def singleNumberLine(
        self, 
        num, 
        width,
        max_width=FRAME_WIDTH,
        max_height=FRAME_HEIGHT,
        font="Noto Sans TC Medium", 
        font_color=WHITE, 
        font_size=24, 
        bold=False, 
        slant=False, 
        **kwargs
    ) -> VGroup:
        
        weight = {True:BOLD, False:NORMAL}[bold]
        slant = {True:ITALIC, False:NORMAL}[slant]
        
        label = Text(text=f'{num}', color=font_color, font_size=font_size, font=font, weight=weight, slant=slant)
        length = adaptiveWidth(width=width, min_width=label.width*1.5)
        line = NumberLine(x_range=(0, num, num), color=random_color_set(), stroke_width=4, length=length)
        
        line_group = VGroup(label, line).arrange(DOWN, buff=0.2)
        line_group = adaptiveSize(line_group, max_width, max_height)

        return line_group

    def numberLineAdd(
        self, 
        *args:int,
        position:np.ndarray,
        width:float|int,
        max_width:float|int=FRAME_WIDTH,
        max_height:float|int=FRAME_HEIGHT,
        speed:float|int=1,
        display:bool=True,
        aligned_edge:np.ndarray=UL,
        clear:bool=False,
        font:str="Noto Sans TC Medium",
        font_color:str=WHITE,
        font_size:float|int=24,
        bold:bool=False,
        slant:bool=False,
        **kwargs
    ) -> VGroup:

        weight = {True:BOLD, False:NORMAL}[bold]
        slant = {True:ITALIC, False:NORMAL}[slant]

        line_group = VGroup()
        
        for num in args:
            label = Text(text=f'{Decimal(str(num))}', color=font_color, font_size=font_size, font=font, weight=weight, slant=slant)
            length = adaptiveWidth(width*num/sum(args), min_width=label.width)
            line = NumberLine(x_range=(0, num, num), color=random_color_set(), stroke_width=4, length=length)
            line_group.add(VGroup(line, label).arrange(UP, buff=0.2)).arrange(RIGHT, buff=0)

        sum_brace = Brace(line_group, DOWN)
        sum_label = Text(text=f'{sum(args)}', color=font_color, font_size=font_size, font=font, weight=weight, slant=slant)
        sum_group = VGroup(sum_brace, sum_label).arrange(DOWN, buff=0.2)
        
        body = VGroup(line_group, sum_group).arrange(DOWN, buff=0.2, center=False, aligned_edge=LEFT)
        body = adaptiveSize(body, max_width, max_height)
        body = adaptiveLocation(body, position=position, aligned_edge=aligned_edge, vertical_mir=True)
        
        if display:
            self.play(Write(body), run_time=(len(sum_group)+len(line_group))/speed)
            self.wait(1)

            if clear:
                self.remove(body)
                self.wait(1)
        
        return body

    def numberLineSub(
        self, 
        *args:int,
        position:np.ndarray,
        width:float|int,
        max_width:float|int=FRAME_WIDTH,
        max_height:float|int=FRAME_HEIGHT,
        speed:float|int=1,
        display:bool=True,
        aligned_edge:np.ndarray=UL,
        clear:bool=False,
        font:str="Noto Sans TC Medium",
        font_color:str=WHITE,
        font_size:float|int=24,
        bold:bool=False,
        slant:bool=False,
        **kwargs
    ) -> VGroup:

        weight = {True:BOLD, False:NORMAL}[bold]
        slant = {True:ITALIC, False:NORMAL}[slant]
        
        line_group = VGroup()

        for num in args[1:]:
            label = Text(text=f'{Decimal(str(num))}', color=font_color, font_size=font_size, font=font, weight=weight, slant=slant)
            length = adaptiveWidth(width*num/args[0], min_width=label.width)
            line = NumberLine(x_range=(0, num, num), color=random_color_set(), stroke_width=4, length=length)
            line_group.add(VGroup(line, label).arrange(DOWN, buff=0.2)).arrange(RIGHT, buff=0)
        
        diff_label = Text(text=f'{Decimal(str(args[0]))-Decimal(str(sum(args[1:])))}', color=font_color, font_size=font_size, font=font, weight=weight, slant=slant)
        length = adaptiveWidth(width-width*sum(args[1:])/args[0], min_width=label.width)
        diff_line = DashedLine((0, 0, 0), (length, 0, 0), color=WHITE)
        diff_brace = Brace(diff_line, DOWN)
        
        diff_group = VGroup(diff_line, diff_brace).arrange(DOWN, buff=0.2)
        line_group.add(diff_group).arrange(RIGHT, buff=0)

        diff_label.next_to(diff_group, DOWN)
        line_group.add(VGroup(diff_label))

        minuend_line = NumberLine(x_range=(0, args[0], args[0]), color=random_color_set(), stroke_width=4, length=line_group.width)
        minuend_label = Text(text=f'{Decimal(str(args[0]))}', color=font_color, font_size=font_size, font=font, weight=weight, slant=slant)
        minuend_group = VGroup(minuend_line, minuend_label).arrange(UP, buff=0.2)

        body = VGroup(minuend_group, line_group).arrange(DOWN, buff=0.2, center=False, aligned_edge=LEFT)
        body = adaptiveSize(body, max_width, max_height)  
        body = adaptiveLocation(body, position=position, aligned_edge=aligned_edge, vertical_mir=True)
        
        if display:
            self.play(Write(body), run_time=(len(minuend_group)+len(line_group))/speed)
            self.wait(1)

            if clear:
                self.remove(body)
                self.wait(1)
        
        return body

    def numberLineMul(
        self, 
        *args:int,
        position:np.ndarray,
        width:float|int,
        max_width:float|int=FRAME_WIDTH,
        max_height:float|int=FRAME_HEIGHT,
        speed:float|int=1,
        display:bool=True,
        aligned_edge:np.ndarray=UL,
        clear:bool=False,
        font:str="Noto Sans TC Medium",
        font_color:str=WHITE,
        font_size:float|int=24,
        bold:bool=False,
        slant:bool=False,
        **kwargs
    ) -> VGroup:
        
        weight = {True:BOLD, False:NORMAL}[bold]
        slant = {True:ITALIC, False:NORMAL}[slant]
    
        line_groups = VGroup()
        
        nums = list(args).copy()

        for i in range(len(nums)-1):
            nums[i+1] = nums[i]*nums[i+1]
        
        pre_line_width = 0

        for i in range(len(nums)-1):
            num = nums[i]
            color = random_color_set()
            line_group = VGroup()
            
            for j in range(args[i+1]):
                label = Text(text=f'{num}', color=font_color, font_size=font_size, font=font, weight=weight, slant=slant)
                length = adaptiveWidth(width*num/nums[-1], min_width=max(pre_line_width, label.width*1.5))
                line = NumberLine(x_range=(0, num, num), color=color, stroke_width=4, length=length)
                line_group.add(VGroup(line, label).arrange(UP, buff=0.2)).arrange(RIGHT, buff=0)
            
            pre_line_width =  line_group.width

            line_groups.add(line_group).arrange(DOWN, buff=0.2, center=False, aligned_edge=LEFT)

        product_brace = Brace(line_groups, DOWN)
        product_label = Text(text=f'{nums[-1]}', color=font_color, font_size=font_size, font=font, weight=weight, slant=slant)
        product_group = VGroup(product_brace, product_label).arrange(DOWN, buff=0.2)
        
        body = VGroup(line_groups, product_group).arrange(DOWN, buff=0.2, center=False, aligned_edge=LEFT)
        body = adaptiveSize(body, max_width, max_height)
        body = adaptiveLocation(body, position=position, aligned_edge=aligned_edge, vertical_mir=True)

        if display:
            self.play(Write(body), run_time=(len(product_group)+len(line_groups))/speed)
            self.wait(1)
        
            if clear:
                self.remove(body)
                self.wait(1)
            
        return body

    def layout(self, display:bool=True) -> None:

        title_margin = Rectangle(height=FRAME_HEIGHT*0.15, width=FRAME_WIDTH).move_to((0, FRAME_HEIGHT*0.425, 0))
        title_content = Rectangle(height=FRAME_HEIGHT*0.12, width=FRAME_WIDTH*0.8).move_to((0, FRAME_HEIGHT*0.41, 0))
        title = Group(title_margin, title_content)

        formula_margin = Rectangle(height=FRAME_HEIGHT*0.85, width=FRAME_WIDTH*0.5)
        formulaz_content = Rectangle(height=FRAME_HEIGHT*0.68, width=FRAME_WIDTH*0.4, grid_xstep=FRAME_HEIGHT*0.68, grid_ystep=FRAME_HEIGHT*0.085)
        formula = Group(formula_margin, formulaz_content).move_to((-FRAME_WIDTH*0.25, -FRAME_HEIGHT*0.075, 0))
        
        animation_margin = Rectangle(height=FRAME_HEIGHT*0.85, width=FRAME_WIDTH*0.5)
        animation_content = Rectangle(height=FRAME_HEIGHT*0.544, width=FRAME_WIDTH*0.4)
        text_content = Rectangle(height=FRAME_HEIGHT*0.136, width=FRAME_WIDTH*0.4)
        animation_inner = Group(animation_content, text_content).arrange(DOWN, buff=0)
        animation = Group(animation_margin, animation_inner).move_to((FRAME_WIDTH*0.25, -FRAME_HEIGHT*0.075, 0))
        
        body = Group(title_margin, title_content, formula, animation)
        
        uh = FRAME_HEIGHT/2
        uw = FRAME_WIDTH/2
        polist = [(uw,uh,0),
                  (uw,0,0),
                  (uw,-uh,0),
                  (0,-uh,0),
                  (-uw,-uh,0),
                  (-uw,0,0),
                  (-uw,uh,0),
                  (0,uh,0),
                  ORIGIN]
        
        for i in polist:
            body.add(Circle(0.1,PINK).move_to(i))

        if display:
            self.add(body)