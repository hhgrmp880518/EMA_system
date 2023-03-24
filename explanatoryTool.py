from manim import*
from calculate import*
from decimal import Decimal
import random

def random_color_set():
    color_set=[
        BLUE_A,
        BLUE_B,
        BLUE_C,
        BLUE_D,
        BLUE_E,
        PURE_BLUE,
        DARK_BLUE,
        TEAL_A,
        TEAL_B,
        TEAL_C,
        TEAL_D,
        TEAL_E,
        GREEN_A,
        GREEN_B,
        GREEN_C,
        GREEN_D,
        GREEN_E,
        PURE_GREEN,
        YELLOW_A,
        YELLOW_B,
        YELLOW_C,
        YELLOW_D,
        YELLOW_E,
        RED_A,
        RED_B,
        RED_C,
        RED_D,
        RED_E,
        PURE_RED,
        MAROON_A,
        MAROON_B,
        MAROON_C,
        MAROON_D,
        MAROON_E,
        PURPLE_A,
        PURPLE_B,
        PURPLE_C,
        PURPLE_D,
        PURPLE_E,
        PINK,
        LIGHT_PINK,
        ORANGE,
        LIGHT_BROWN,
        DARK_BROWN,
        GRAY_BROWN
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
        scale_x = (config.frame_width-2)/table.width
        scale_y = (config.frame_height-5)/table.height
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

    def column_form(self, *args, position, width, height, speed=1, clear=False, font="Noto Sans CJK TC Medium", font_color=WHITE, font_size=12, bold=False, slant=False, **kwargs):
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
        scale_x = (config.frame_width-2)/table.width
        scale_y = (config.frame_height-5)/table.height
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

    def add_column_form(self, *args, position, width, height, speed=1, clear=False, font="Noto Sans CJK TC Medium", font_color=WHITE, font_size=12, bold=False, slant=False, **kwargs):
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
    
    def title(self, text, font="Noto Sans CJK TC Medium", font_color=WHITE, font_size=24, bold=False, slant=False, **kwargs):
        title_text = Text(text=f'{text}', color=font_color, font_size=font_size, font=font, weight=(NORMAL, BOLD)[bold], slant=(NORMAL, ITALIC)[slant])
        title_text.center()
        self.add(title_text)
        

    def ask(self, text, position, speed=1, clear=False, font="Noto Sans CJK TC Medium", font_color=WHITE, font_size=24, bold=False, slant=False, **kwargs):
        question_text = Text(text=f'{text}', color=font_color, font_size=font_size, font=font, weight=(NORMAL, BOLD)[bold], slant=(NORMAL, ITALIC)[slant])
        question_text.move_to((position[0]-config.frame_width/2, config.frame_height/2-position[1], 0), aligned_edge=UL)
        self.play(AddTextLetterByLetter(question_text, lag_ratio=speed))
    
    def ans(self, text, position, speed=1, clear=False, font="Noto Sans CJK TC Medium", font_color=WHITE, font_size=24, bold=False, slant=False, **kwargs):
        ans_text = Text(text=f'答案是：{text}', color=font_color, font_size=font_size, font=font, weight=(NORMAL, BOLD)[bold], slant=(NORMAL, ITALIC)[slant])
        ans_text.move_to((position[0]-config.frame_width/2, config.frame_height/2-position[1], 0), aligned_edge=UL)
        self.play(AddTextLetterByLetter(ans_text, lag_ratio=speed))

    def numberLineAdd(self, *args, position, length, speed=1, clear=False, font="Noto Sans CJK TC Medium", font_color=WHITE, font_size=24, bold=False, slant=False, **kwargs):

        line_group = [NumberLine(x_range=[0, num, num], color=random_color_set(), stroke_width=4, length=length*num/sum(args)) for num in args]
        label_group = [Text(text=f'{Decimal(str(num))}', color=font_color, font_size=font_size, font=font, weight=(NORMAL, BOLD)[bold], slant=(NORMAL, ITALIC)[slant]) for num in args]

        for i in range(len(args)):
            if i == 0:
                line_group[i].move_to((position[0]-config.frame_width/2, config.frame_height/2-position[1], 0), aligned_edge=UL)
                label_group[i].next_to(line_group[i], UP)
                self.play(Create(line_group[i]), Write(label_group[i]), run_time=1/speed)
                
            else:
                line_group[i].move_to(line_group[i-1].get_right(), aligned_edge=LEFT)
                label_group[i].next_to(line_group[i], UP)
                self.play(Create(line_group[i]), Write(label_group[i]), run_time=1/speed)
        
        args = [Decimal(str(num)) for num in args]

        sum_line = NumberLine(length=length).move_to((line_group[0].get_left()), aligned_edge=LEFT)
        sum_brace = Brace(sum_line, DOWN)
        sum_label = Text(text=f'{sum(args)}', color=font_color, font_size=font_size, font=font, weight=(NORMAL, BOLD)[bold], slant=(NORMAL, ITALIC)[slant]).next_to(sum_brace, DOWN)
        self.play(Write(sum_brace), Write(sum_label), run_time=1/speed)

        if clear:
            self.pause()
            for i in range(len(args)):
                self.remove(line_group[i], label_group[i])
            self.remove(sum_brace, sum_label)
            self.pause()
    
    def numberLineSub(self, *args, position, length, speed=1, clear=False, font="Noto Sans CJK TC Medium", font_color=WHITE, font_size=24, bold=False, slant=False, **kwargs):
        
        line_group = [NumberLine(x_range=[0, num, num], color=random_color_set(), stroke_width=4, length=length*num/args[0]) for num in args]
        label_group = [Text(text=f'{Decimal(str(num))}', color=font_color, font_size=font_size, font=font, weight=(NORMAL, BOLD)[bold], slant=(NORMAL, ITALIC)[slant]) for num in args]

        for i in range(len(line_group)):
            if i == 0:
                line_group[i].move_to((position[0]-config.frame_width/2, config.frame_height/2-position[1], 0), aligned_edge=UL)
                label_group[i].next_to(line_group[i], UP)
                self.play(Create(line_group[i]), Write(label_group[i]), run_time=1/speed)
            elif i == 1:
                line_group[i].move_to(line_group[0].get_corner(DL), aligned_edge=UL)
                label_group[i].next_to(line_group[i], DOWN)
                self.play(Create(line_group[i]), Write(label_group[i]), run_time=1/speed)
            else:
                line_group[i].move_to(line_group[i-1].get_right(), aligned_edge=LEFT)
                label_group[i].next_to(line_group[i], DOWN)
                self.play(Create(line_group[i]), Write(label_group[i]), run_time=1/speed)

        diff_line = DashedLine([0, 0, 0], [length-length*sum(args[1:])/args[0], 0, 0], color=WHITE).move_to((line_group[-1].get_right()), aligned_edge=LEFT)
        diff_brace = Brace(diff_line, DOWN)
        diff_label = Text(text=f'{Decimal(str(args[0]))-sum([Decimal(str(num)) for num in args[1:]])}', color=font_color, font_size=font_size, font=font, weight=(NORMAL, BOLD)[bold], slant=(NORMAL, ITALIC)[slant]).next_to(diff_brace, DOWN)
        self.play(Create(diff_line), run_time=1/speed)
        self.play(Write(diff_brace), Write(diff_label), run_time=1/speed)

        if clear:
            self.pause()
            for i in range(len(args)):
                self.remove(line_group[i], label_group[i])
            self.remove(diff_line, diff_brace, diff_label)
            self.pause()

    def numberLineMul(self, *args, position, length, speed=1, clear=False, font="Noto Sans CJK TC Medium", font_color=WHITE, font_size=24, bold=False, slant=False, **kwargs):
        nums = list(args).copy()
        line_groups = []
        label_groups = []

        for i in range(len(nums)-1):
            nums[i+1] = nums[i]*nums[i+1]

        for i in range(len(nums)-1):
            num = nums[i]
            color=random_color_set()
            line_groups.append([])
            label_groups.append([])
            
            for j in range(args[i+1]):
                line_groups[i].append(NumberLine(x_range=[0, num, num], color=color, stroke_width=4, length=length*num/nums[-1]))
                label_groups[i].append(Text(text=f'{num}', color=font_color, font_size=font_size, font=font, weight=(NORMAL, BOLD)[bold], slant=(NORMAL, ITALIC)[slant]))

        for i in range(len(line_groups)):
            for j in range(len(line_groups[i])):
                if j == 0:
                    line_groups[i][j].move_to((position[0]-config.frame_width/2, config.frame_height/2-position[1]-0.6*i, 0), aligned_edge=UL)
                    label_groups[i][j].next_to(line_groups[i][j], UP*0.2)
                    self.play(Create(line_groups[i][j]), Write(label_groups[i][j]), run_time=1/speed)
                else:
                    line_groups[i][j].move_to(line_groups[i][j-1].get_right(), aligned_edge=LEFT)
                    label_groups[i][j].next_to(line_groups[i][j], UP*0.2)
                    self.play(Create(line_groups[i][j]), Write(label_groups[i][j]), run_time=1/speed)
        
        sum_line = NumberLine(length=length).move_to((line_groups[i][0].get_left()), aligned_edge=LEFT)
        sum_brace = Brace(sum_line, DOWN)
        sum_label = Text(text=str(nums[-1]), color=font_color, font_size=font_size, font=font, weight=(NORMAL, BOLD)[bold], slant=(NORMAL, ITALIC)[slant]).next_to(sum_brace, DOWN)
        self.play(Write(sum_brace), Write(sum_label), run_time=1/speed)

        if clear:
            self.pause(1)
            for i in range(len(line_groups)):
                for j in range(len(line_groups[i])):
                    self.remove(line_groups[i][j], label_groups[i][j])
            self.remove(sum_brace, sum_label)