from tkinter import *
from tkinter import ttk, messagebox
import random, json




class SpeedMathGUI:
    def __init__(self, root):
        root.title('speedmath')
        root.geometry('600x400')
        root.resizable(False, False)

        ###### adding event for when an entry is focused
        root.event_add('<<EntryFocusIn>>', '<FocusIn>')
        root.event_add('<<EntryFocusOut>>', '<FocusOut>')

        self.frame1 = ttk.Frame(root, height=400, width=600)
        self.frame1.place(x=0, y=0)
    


        self.new(root, 'new')



        

        ##### creating a button to check if any answer is wrong
        self.check_button = ttk.Button(root, text='check', command=lambda: self.check_answers())
        self.check_button.place(x= 250, y = 365)

        self.save_button = ttk.Button(root, text='save', command = lambda: self.save())
        self.save_button.place(x = 150, y = 365)

        self.load_button = ttk.Button(root, text='load', command = lambda: self.load())
        self.load_button.place(x = 50, y = 365)

        self.new_button = ttk.Button(root, text='New', command=lambda: self.new(root, 'refresh'))
        self.new_button.place(x= 350, y= 365)


        self.start_stop = ttk.Label(root, text='Start', anchor='center', font= ('Calibri Light', 12, 'bold'))
        self.start_stop.place(x= 450, y = 360)
        self.start_stop.bind('<Button-1>', lambda e: self.time_elapsed())
        self.show_time_elsepsed = ttk.Label(root, text='00:00', anchor='center')
        self.show_time_elsepsed.place(x= 500, y = 360)




        ttk.Label(root, text='JishukhNetwork', font= ('Calibri Light', 12, 'bold', 'italic')).place(x= 480,y= 380)
    def answer_array_fun(self, l1, l2):
         ####### creating an answer arrray so that I can check my answers
        answer_array = []
        for i in self.l1:
            temp = []
            for j in self.l2:
                temp.append(i+j)
            summ = sum(temp) ###### SUMMING UP EVERY ROW
            temp.append(summ)
            answer_array.append(temp)

        temp = [] ###### summing up every column
        for j in range(11):
            count = 0
            for i in range(10):
                count += answer_array[i][j]
            temp.append(count)
        answer_array.append(temp)
        return answer_array

    def new(self, root, *arg):
        self.l1 = [random.randint(11,99) for i in range(10)]
        self.l2 = [random.randint(11,99) for i in range(10)]

        self.answer_array = self.answer_array_fun(self.l1, self.l2)

        if arg[0] == 'refresh':
            for i in range(12):
                for j in range(12):

                    ########## for first row
                    if i == j == 0:
                        continue
                    elif i == 0:
                        if j != 11:
                            self.my_answer_array[i][j].refresh(str(self.l2[j-1]))
                        else:
                            k = TopLabels(root, 'Total', 11*50, 0 )
                    
                    #### for the very first column
                    elif j == 0:
                        if i != 11:
                            self.my_answer_array[i][j].refresh(str(self.l1[i-1]))
                        else:
                            continue
                    
                    # for all those entries and labels which needs to be filled
                    else:
                        self.my_answer_array[i][j].refresh()
        else:
            self.my_answer_array = [[[] for i in range(12)] for j in range(12)] #### created an empty 2d array so that I can strore these labels in that
            for i in range(12):
                for j in range(12):

                    ########## for first row
                    if i == j == 0:
                        k = TopLabels(root, '', j*50, i )
                    elif i == 0:
                        if j != 11:
                            k = TopLabels(root, str(self.l2[j-1]), j*50, i )
                        else:
                            k = TopLabels(root, 'Total', 11*50, 0 )
                    
                    #### for the very first column
                    elif j == 0:
                        if i != 11:
                            k = TopLabels(root, str(self.l1[i-1]), j*50, i*30 )
                        else:
                            k = TopLabels(root, 'Total', j*50, 11*30 )
                    
                    # for all those entries and labels which needs to be filled
                    else:
                        k = Answer(self.frame1, j*50, i*30)
                    self.my_answer_array[i][j] = k

    def save(self):
        really = messagebox.askyesnocancel(title='REALLY Saving??', message='Do you really want to save this progress?'
                                                                '\nOr it is just a wrong click.') 
        if really:
            answers = [[[] for i in range(12)] for j in range(12)]
            for i in range(12):
                for j in range(12):
                    if i > 0 and j > 0:
                        answers[i][j] = self.my_answer_array[i][j].get_label_text()
                    else:
                        answers[i][j] = self.my_answer_array[i][j].get_label_text()
            with open('list_answers.json', 'w') as file:
                json.dump(answers, file)
        else:
            pass

    def load(self):
        with open('list_answers.json', 'r') as file:
            answers = json.load(file)
        
        for i in range(12):
            for j in range(12):

                ########## for first row
                if i == 0:
                    if j != 11:
                        self.my_answer_array[i][j].load_label(f'{answers[i][j] }')
                    continue
                
                #### for the very first column
                elif j == 0:
                    if i != 11:
                        self.my_answer_array[i][j].load_label(f'{answers[i][j] }')
                    continue
                
                # for all those entries and labels which needs to be filled
                else:
                    self.my_answer_array[i][j].load_label(f'{answers[i][j] }')
        self.l2 = list(map(int, answers[0][1:11]))
        for i in range(1, 11):
            self.l1[i-1] = int(answers[i][0])
        
        self.answer_array = self.answer_array_fun(self.l1, self.l2)
        

        
        
    def check_answers(self):
        for i in range(11):
            for j in range(11):
                if  self.my_answer_array[i+1][j+1].label_value() == None:
                    pass
                elif self.answer_array[i][j] != self.my_answer_array[i+1][j+1].label_value():
                    self.my_answer_array[i+1][j+1].change_label_color('y')
                elif str(self.my_answer_array[i+1][j+1].get_label_color()) == 'yellow':
                    if self.answer_array[i][j] == self.my_answer_array[i+1][j+1].label_value():
                        self.my_answer_array[i+1][j+1].change_label_color('g')

    def time_elapsed(self):
        s = self.start_stop.cget('text')
        if s == 'Start':
            self.start_stop.config(text='Stop')
        else:
            self.start_stop.config(text='Start')




class TopLabels:
    def __init__(self, master, text, x, y):
        self.x = x
        self.y = y

        self.label = ttk.Label(master, text=text, font= ('Calibri Light', 12, 'bold'), anchor= 'center')
        self.label.place(x= self.x, y= self.y)
        
    def get_label_text(self):
        return self.label.cget('text')
    
    def load_label(self, text):
        self.label.config(text=text)
    
    def refresh(self, text):
        self.label.config(text=text)


class Answer:

    def __init__(self, master, x, y):
        self.x = x
        self.y = y

        self.label = ttk.Label(master, text='', font= ('Calibri Light', 11), anchor= 'center')
        self.label.place(x= self.x, y= self.y)
        self.label.place_forget()
        self.label.bind('<Button-1>', lambda e: self.show_entry())

        self.entry = Entry(master, width=3, borderwidth= 0, relief= FLAT)#FLAT, SUNKEN(default), RIDGE, GROOVE, RAISED,
        self.entry.place(x= self.x, y= self.y+5)
        self.entry.bind('<Return>', lambda e: self.show_label())
        self.entry.bind('<<EntryFocusIn>>', lambda e: self.entry.config(borderwidth=3))
        self.entry.bind('<<EntryFocusOut>>', lambda e: self.entry.config(borderwidth=0))


        

    def show_label(self):
        a = self.entry.get()
        a = a.strip()
        
        
        if a == "":
            if self.label.cget('text') == '':
                self.entry.tk_focusNext().focus() ####### takes focus to the next entry
            else:
                self.entry.tk_focusNext().focus() ####### takes focus to the next entry
                self.entry.place_forget()
                self.label.place(x= self.x, y= self.y)
        else:
            self.entry.delete(0, END)
            self.label.config(text=a)
            self.entry.tk_focusNext().focus() ####### takes focus to the next entry
            self.entry.place_forget()
            self.label.place(x= self.x, y= self.y)
        

    def show_entry(self):
        self.entry.insert(0, self.label.cget('text'))
        self.label.place_forget()
        self.entry.place(x= self.x, y= self.y)
        self.entry.focus()
    
    def label_value(self):
        '''
            a function to return what is the value label has stored
        '''
        number = self.label.cget('text')
        if number == '':
            return None
        return int(number)
    
    def change_label_color(self, color):
        if color == 'g':
            self.label.config(background="lime")
        if color == 'y':
            self.label.config(background="yellow")

    def get_label_color(self):
        return self.label.cget('background')

    def get_label_text(self):
        return self.label.cget('text')

    def load_label(self, text):
        self.label.config(text = text)
        if text != '':
            self.entry.place_forget()
            self.label.place(x= self.x, y= self.y)

    def refresh(self):
        self.label.config(text = '')
        self.label.place_forget()
        self.entry.place(x= self.x, y= self.y)

        # created this with a frame which costs more memmory and more time
        # self.frame = ttk.Frame(master, height=30, width=50)
        # self.frame.place(x= x, y= y)

        # self.label = ttk.Label(self.frame, text=f'{x},{y}', anchor= 'center')
        # self.label.pack()
        # self.label.pack_forget()
        # self.label.bind('<Button-1>', lambda e: self.show_entry())

        # self.entry = ttk.Entry(self.frame, width=3)
        # self.entry.pack()
        # self.entry.bind('<Return>', lambda e: self.show_label())




def main():
    root = Tk()
    root.option_add('*tearoff', False)
    app = SpeedMathGUI(root)
    root.mainloop()



if __name__ == '__main__':
    main()