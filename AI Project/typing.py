from tkinter import *
from tkinter import font
from playsound import playsound
import random
import time
from paragraph import get_paragraph_keys, get_paragraph_value

# Creating window
app = Tk()
app.geometry('1300x680+28+20')
app.title('Typing Test')
app.minsize(1300, 680)
app.configure(bg= 'black')

# Creating frame
frame = Frame(app, bg= 'black')
frame.pack()

class Typing:
    list_paragraph = list( get_paragraph_keys() )
    key_pressed: int
    back_space_pressed: int
    flag: int
    start_time: int
    end_time: int
    get_user_text: str
    min: int
    sec: int
    num = IntVar()
    topic = StringVar()
    paragraph: str

    def main(self) -> None:
        self.key_pressed = 0
        self.back_space_pressed = 0
        self.flag = 0
        self.start_time = 0
        self.end_time = 0
        self.min = 0
        self.sec = 0
        self.get_user_text = ""

    def clear_frame(self) -> None:
        # removing  widgest
        for wid in frame.winfo_children():
            wid.destroy()

    def back_to_home(self) -> None:
        playsound('sound.mp3', block= False)
        self.clear_frame()
        self.home()

    def try_again(self) -> None:
        playsound('sound.mp3', block= False)
        self.clear_frame()
        self.main()
        self.start_test()

    def display_format_time(self, time_taken) -> str:
        time_format = ""
        time_format = '{:0>2d}'.format(int(time_taken/60))
        time_format += ':' + '{:0>2d}'.format(int(time_taken%60))
        return time_format

    def check_record_break(self, wpm) -> bool:
        return wpm > self.get_high_score()

    def update_score(self, wpm) -> None:
        with open('high_score.txt', 'w') as score:
            score.write(str(wpm))
        
    def calculate(self) -> int:
        time_taken = int(self.end_time - self.start_time)
        correct_letters = 0
        correct_words = 0
        accuracy = 0
        actual_accuracy = 0
        wpm = 0

        temp = 0
        for p, u in zip(self.paragraph, self.get_user_text):
            if p == ' ':
                correct_words += 1 if temp==0 else 0
                temp = 0
            if p == u:
                correct_letters += 1
            else:
                temp = 1

        correct_words += 1 if temp==0 else 0

        # Calculating accuracy
        accuracy = correct_letters * 100 / len(self.paragraph)
        # Calculating actual accuracy
        actual_accuracy = (correct_letters - self.back_space_pressed) * 100 / len(self.paragraph)
        # Calculating word per minute speed
        wpm = correct_words / (float(time_taken)/60)

        return int(accuracy), int(actual_accuracy) if actual_accuracy>0 else 0, int(wpm) if wpm>0 else 0, self.display_format_time(time_taken)

    def show_chart(self, actual_accuracy) -> None:
        playsound('sound.mp3', block=False)
        import matplotlib.pyplot as plt

        data, title, explode = list(), list(), list()
        color = ['#99ff99', '#ff9999']
        if actual_accuracy == 100:
            data.append(actual_accuracy)
            title.append('Actual Accuracy')
            explode.append(0.05)
        else:    
            data = [actual_accuracy, 100-actual_accuracy]
            title = ['Actual Accuracy', 'Incorrect']
            explode = [0.05, 0.05]

        plt.title('Accuracy Chart', color='Blue', font='Lucida Calligraphy', fontsize=19)
        plt.axis("equal")
        plt.pie(data, labels=title, colors=color, autopct='%1.0f%%', explode = explode)
        plt.show()
        plt.close()
    
    def show_result(self) -> None:
        self.clear_frame()
        accuracy, actual_accuracy, wpm, total_time = self.calculate()

        result = Label(frame,
            text= 'Result',
            bg= 'black', fg= 'light salmon',
            font= 'Lucida\ Calligraphy 26 underline')
        result.grid(row=0, columnspan= 3, pady=40)

        accuracy_h = Label(frame,text= 'Accuracy: ',
            font= 'Lucida\ Fax 22',
            bg= 'black', fg= 'steel blue')
        accuracy_h.grid(row=1, column=0)
        accuracy_l = Label(frame,text= f'{accuracy}%',
            font= 'Lucida\ Fax 22',
            bg= 'black', fg= 'green')
        accuracy_l.grid(row=1, column=1, columnspan=2)

        actual_accuracy_h = Label(frame,text= 'Actual Accuracy: ',
            font= 'Lucida\ Fax 22',
            bg= 'black', fg= 'steel blue')
        actual_accuracy_h.grid(row=2, column=0, pady= (25, 0))
        actual_accuracy_l = Label(frame,text= f'{actual_accuracy}%',
            font= 'Lucida\ Fax 22',
            bg= 'black', fg= 'red')
        actual_accuracy_l.grid(row=2, column=1, columnspan=2, pady= (25, 0))

        wpm_h = Label(frame,text= 'WPM Speed: ',
            font= 'Lucida\ Fax 22',
            bg= 'black', fg= 'steel blue')
        wpm_h.grid(row=3, column=0)
        wpm_l = Label(frame,text= f'{wpm}',
            font= 'Lucida\ Fax 22',
            bg= 'black', fg= 'green')
        wpm_l.grid(row=3, column=1, columnspan=2, pady= 25)

        #Overall Time Taken To Type The Text
        time_taken = Label(frame,text= 'Time: ',
            font= 'Lucida\ Fax 22',
            bg= 'black', fg= 'steel blue')
        time_taken.grid(row=4, column=0)
        time_taken = Label(frame,text= f'{total_time}',
            font= 'Lucida\ Fax 22',
            bg= 'black', fg= 'red')
        time_taken.grid(row=4, column=1, columnspan=2)

        #Check if high score record is broken or not
        if self.check_record_break(wpm):
            self.update_score(wpm)
            new_record = Label(frame,text= 'Congratulation! You just broke the record of high speed...!',
                    font= 'Lucida\ Fax 22',
                    bg= 'black', fg= 'green')
            new_record.grid(row=5, columnspan=3, pady= 10)

        chart = Button(frame,
            text= 'Accuracy Chart',
            font= 'Verdana\ Pro 18',
            borderwidth= 5,
            bg= 'black', fg= 'salmon',
            command= lambda: self.show_chart(actual_accuracy))
        chart.grid(row=6, columnspan=3, pady= 25)

        retry = Button(frame,
            text= 'Try Again',
            font= 'Verdana\ Pro 18',
            borderwidth= 5,
            bg= 'black', fg= 'salmon',
            command= self.try_again)
        retry.grid(row=7, column=0, padx= 150)

        new_test = Button(frame,
            text= 'New Test',
            font= 'Verdana\ Pro 18',
            borderwidth= 5,
            bg= 'black', fg= 'salmon',
            command= self.choose_option)
        new_test.grid(row=7, column=1, padx=30)

        home = Button(frame,
            text= 'Home',
            font= 'Verdana\ Pro 18',
            borderwidth= 5,
            bg= 'black', fg= 'salmon',
            command= self.back_to_home)
        home.grid(row=7, column=2, padx= 150)

    def show_timer(self, s_time) -> None:

        current = time.time()
        if int(current - s_time) > 0:
            self.sec += 1
        if(self.sec == 60):
            self.sec = 0
            self.min += 1

        min_p = '{:0>2d}'.format(int(self.min))
        sec_p = '{:0>2d}'.format(int(self.sec))

        time_elapsed.config(text= f'{min_p}:{sec_p}')
        time_elapsed.after(1000, lambda: self.show_timer(s_time))

    def key_release(self, event) -> None:
        if self.flag == 0:
            self.flag = 1
            self.start_time = time.time()
            self.show_timer(self.start_time)

        #change input color
        self.get_user_text = user_input.get('1.0', 'end - 1c')
        if self.paragraph.startswith(self.get_user_text):
            user_input.config(fg= 'green')
        else:
            user_input.config(fg= 'red')

        # calculate backspace
        if event.keysym == 'BackSpace':
            self.back_space_pressed += 1

        #Generate and test
        self.key_pressed = len(self.get_user_text)
        if self.key_pressed >= len(self.paragraph):
            self.end_time = time.time()
            self.show_result()

    def start_test(self) -> None:
        playsound('sound.mp3', block= False)
        self.clear_frame()

        title = Label(frame,
            fg= 'magenta', bg= 'black',
            text= self.topic.get(),
            font='Ludica\ Fax 24 underline')
        title.grid(row= 0, column= 0, columnspan= 1, pady= 50)

        global time_elapsed
        time_elapsed = Label(frame,
                fg= 'red', bg= 'black',
                text= '00:00',
                font= 'Lucida\ Console 22 underline')
        time_elapsed.grid(row= 0, column= 2, pady= 50)

        content = Message(frame,
            text= self.paragraph,
            bg= 'black', fg= 'white',
            width= 1000,
            justify= 'center',
            font= 'Verdana\ Pro 18')
        content.grid(row= 1, pady= 40)

        global user_input
        user_input = Text(frame, width= 70, height= 10,
            bg= 'black', fg= 'white',
            relief= RAISED, borderwidth= 5,
            insertbackground= 'white',
            padx=5, pady=5,
            font= 'Verdana\ Pro 16')
        user_input.grid(row=2)
        user_input.bind('<KeyRelease>', self.key_release)
        user_input.focus()
        user_input.bind('<Control-x>', lambda e: 'break') #disable cut
        user_input.bind('<Control-c>', lambda e: 'break') #disable copy
        user_input.bind('<Control-v>', lambda e: 'break') #disable paste
        user_input.bind('<Button-3>', lambda e: 'break')  #disable right-click
    
    def random_paragraph(self) -> None:
        self.topic.set(random.choice(self.list_paragraph))
        self.paragraph = get_paragraph_value(self.topic.get())
        self.start_test()

    def go_backward(self, backward, forward, title, status, content) -> None:
        playsound('sound.mp3', block= False)
        if self.num.get() == 2:
            backward.config(state= DISABLED)
        else:
            backward.config(state= NORMAL)
        forward.config(state= NORMAL)
        self.num.set(self.num.get()-1)
        self.topic.set(self.list_paragraph[self.num.get()-1])
        title.config(text= self.topic.get())
        self.paragraph = get_paragraph_value(self.list_paragraph[self.num.get()-1])
        content.config(text= self.paragraph)
        status.config(text= f'Paragraph {self.num.get()} of {len(self.list_paragraph)}')

    def go_forward(self, backward, forward, title, status, content) -> None:
        playsound('sound.mp3', block= False)
        if self.num.get() == len(self.list_paragraph)-1:
            forward.config(state= DISABLED)
        else:
            forward.config(state= NORMAL)
        backward.config(state= NORMAL)
        self.num.set(self.num.get()+1)
        self.topic.set(self.list_paragraph[self.num.get()-1])
        title.config(text= self.topic.get())
        self.paragraph = get_paragraph_value(self.list_paragraph[self.num.get()-1])
        content.config(text= self.paragraph)
        status.config(text= f'Paragraph {self.num.get()} of {len(self.list_paragraph)}')

    def choose_option(self) -> None:
        playsound('sound.mp3', block= False)
        self.clear_frame()
        self.num.set(1)
        self.topic.set(self.list_paragraph[0])
        self.main()

        # page header
        header = Label(frame,
                text= 'Choose Paragraph To Start Typing', 
                font= 'Lucida\ Console 26 underline',
                bg= 'black', fg= 'green')
        header.grid(row= 0, column= 1, pady= (40, 20))

        backward = Button(frame,
            text= '<<',
            fg= 'red', bg= 'black',
            font='Helvetica 20',
            state= DISABLED,
            command= lambda: self.go_backward(backward, forward, title, status, content))
        title = Label(frame,
            fg= 'crimson', bg= 'black',
            text= self.topic.get(),
            font='Helvetica 22')
        forward = Button(frame,
            fg= 'red', bg= 'black',
            text= '>>',
            font='Helvetica 20',
            command= lambda: self.go_forward(backward, forward, title, status, content))

        backward.grid(row= 1, column= 0, pady=35)
        title.grid(row= 1, column= 1, pady= 35)
        forward.grid(row= 1, column= 2, pady=(35, 0))

        global status
        status = Label(frame,
            text= f'Paragraph {self.num.get()} of {len(self.list_paragraph)}',
            bg= 'black', fg= 'light blue',
            font= 'Monospace 10 italic',
            relief= FLAT)
        status.grid(row= 2, column= 2, pady= (0, 10))

        self.paragraph = get_paragraph_value(self.topic.get())
        content = Message(frame,
            text= self.paragraph,
            fg= 'dark gray', bg= 'black',
            width= 1000,
            justify= 'center',
            font= 'Verdana\ Pro 18')
        content.grid(row= 3, column= 0, columnspan= 3)
    
        start = Button(frame,
            text= 'Start',
            font= 'Verdana\ Pro 18',
            borderwidth= 5,
            bg= 'black', fg= 'dark green',
            command= self.start_test)
        start.grid(row= 4, column= 1, pady= 25)

        randomly = Button(frame,
            text= 'Random Paragraph',
            font= 'Verdana\ Pro 18',
            borderwidth= 5,
            bg= 'black', fg= 'dark green',
            command= self.random_paragraph)
        randomly.grid(row= 5, column= 1, pady= (0, 25))

        back = Button(frame,
            text= 'Back',
            font= 'Verdana\ Pro 18',
            borderwidth= 5,
            bg= 'black', fg= 'dark green',
            command= self.back_to_home)
        back.grid(row= 6, column= 1)

    def get_high_score(self) -> int:
        with open('high_score.txt', 'r') as score:
            result = score.readline()
        return int(result)

    def reset_score(self) -> None:
        self.update_score(0)
        self.show_high_score()

    def show_high_score(self) -> None:
        playsound('sound.mp3', block= False)
        self.clear_frame()

        heading = Label(frame,
            text= 'Top Score',
            font= 'Monospace 26 underline',
            bg= 'black', fg= 'magenta')
        heading.pack(pady= 50)
    
        speed = Message(frame,
            text=f"Top WPM speed: {self.get_high_score()}",
            font= 'Verdana\ Pro 20',
            justify= 'center',
            width= 500,
            bg= 'black', fg= 'magenta')
        speed.pack(pady= 50)

        reset = Button(frame,
            text= 'Reset',
            font= 'Verdana\ Pro 18',
            borderwidth= 5,
            bg= 'black', fg= 'magenta',
            command= self.reset_score)
        reset.pack(pady= 40)

        back = Button(frame,
            text= 'Back',
            font= 'Verdana\ Pro 18',
            borderwidth= 5,
            bg= 'black', fg= 'magenta',
            command= self.back_to_home)
        back.pack()

    def get_exit(self) -> None:
        app.quit()

    def home(self) -> None:
        # Creating label
        header = Label(frame,
            text= 'Typing Speed & Accuracy Test', 
            font= 'rockwell 30 bold underline',
            bg= 'black', fg= 'cyan')
        header.pack(pady= 80)

        # Creating Buttons
        start = Button(frame,
            text= 'Start',
            font= 'Verdana\ Pro 20',
            borderwidth= 5,
            bg= 'black', fg= 'dark cyan',
            command= self.choose_option)
        start.pack(pady= 25)

        high_score = Button(frame,
            text= 'High Score',
            font= 'Verdana\ Pro 20',
            borderwidth= 5,
            bg= 'black', fg= 'dark cyan',
            command= self.show_high_score)
        high_score.pack(pady= 25)

        exit = Button(frame,
            text= 'Exit',
            font= 'Verdana\ Pro 20',
            borderwidth= 5,
            bg= 'black', fg= 'dark cyan',
            command= self.get_exit)
        exit.pack(pady= 25)

if __name__ == '__main__':
    typing = Typing()
    typing.main()
    typing.home()
    app.mainloop()