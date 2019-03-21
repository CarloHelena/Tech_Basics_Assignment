# import modules
from tkinter import *
import random

# import files
from story import *


class Application(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        master.minsize(width=485, height=235)

        self.frame1 = Frame(master, pady=5, padx=5)
        self.frame1.grid(row=0, column=0, sticky="news")
        self.frame2 = Frame(master, height=20, pady=5, padx=5)
        self.frame2.grid(row=1, column=0, sticky="ew")

        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)
        self.frame1.grid_columnconfigure(0, weight=1)
        self.frame1.grid_rowconfigure(0, weight=1)
        self.frame2.grid_columnconfigure(0, weight=1)
        self.frame2.grid_columnconfigure(1, weight=1)
        self.frame2.grid_columnconfigure(2, weight=1)
        self.frame2.grid_rowconfigure(0, weight=1)

        self.grid()
        self.create_widgets()

        self.story = Story("story.json")
        self.story.set_debug_mode(True) #-> to be shown in the console or not?!

        self.show_message()

    # populate the window frame with widgets
    def create_widgets(self):

        # create widgets
        self.txt_out    = Text(self.frame1, wrap=WORD)
        self.txt_in     = Entry(self.frame2)
        self.btn_ok     = Button(self.frame2, width=20, command= lambda: self.pressed_btn("ok"))
        self.btn_next   = Button(self.frame2, width=20, command= lambda: self.pressed_btn("next"))
        self.btn_enter  = Button(self.frame2, width=20, command= lambda: self.pressed_btn("enter"))
        self.btn_a      = Button(self.frame2, width=20, command= lambda: self.pressed_btn("a"))
        self.btn_b      = Button(self.frame2, width=20, command= lambda: self.pressed_btn("b"))
        self.btn_c      = Button(self.frame2, width=20, command= lambda: self.pressed_btn("c"))
        self.btn_yes    = Button(self.frame2, width=20, command= lambda: self.pressed_btn("yes"))
        self.btn_no     = Button(self.frame2, width=20, command= lambda: self.pressed_btn("no"))

        # layout widgets
        self.txt_out.grid(row=0, column=0, sticky="news")
        self.txt_in.grid(row=0, column=0, columnspan=2, sticky="news")
        self.btn_ok.grid(row=0, column=1)
        self.btn_next.grid(row=0, column=1)
        self.btn_enter.grid(row=0, column=2)
        self.btn_a.grid(row=0, column=0, sticky="e")
        self.btn_b.grid(row=0, column=1)
        self.btn_c.grid(row=0, column=2, sticky="w")
        self.btn_yes.grid(row=0, column=0, sticky="e")
        self.btn_no.grid(row=0, column=2, sticky="w")

        # hide all widgets
        self.hide_all_widgets();


    # Widget layout (hide/show)
    def hide_widget(self, widget):
        widget.grid_remove()

    def show_widget(self, widget, text=None):
        if not text == None:
            widget.config(text=text)
        widget.grid()

    def hide_all_widgets(self):
        self.hide_widget(self.btn_enter)
        self.hide_widget(self.txt_in)
        self.txt_in.delete(0, END)
        self.txt_in.focus()
        self.hide_widget(self.btn_ok)
        self.hide_widget(self.btn_next)
        self.hide_widget(self.btn_a)
        self.hide_widget(self.btn_b)
        self.hide_widget(self.btn_c)
        self.hide_widget(self.btn_yes)
        self.hide_widget(self.btn_no)


    # FUNCTIONALITY #
    def display_text(self, text):
        if not isinstance(text, str):
            return False
        self.txt_out.delete(0.0, END)
        self.txt_out.insert(0.0, text)

    def show_message(self):
        self.display_text(self.story.get_message())
        self.hide_all_widgets()
        # check which buttons need to be shown
        if self.story.get_expected_type() == "ok":
            self.show_widget(self.btn_ok, text = self.story.get_expected_options()[0])
        elif self.story.get_expected_type() == "yesno":
            self.show_widget(self.btn_yes, text = self.story.get_expected_options()[0])
            self.show_widget(self.btn_no, text = self.story.get_expected_options()[1])
        elif self.story.get_expected_type() == "abc":
            self.show_widget(self.btn_a, text = self.story.get_expected_options()[0])
            self.show_widget(self.btn_b, text = self.story.get_expected_options()[1])
            self.show_widget(self.btn_c, text = self.story.get_expected_options()[2])
        elif self.story.get_expected_type() == "input":
            self.show_widget(self.txt_in)
            self.show_widget(self.btn_enter, text = self.story.get_expected_options()[0])

    def show_response(self):
        self.display_text(self.story.get_response())
        self.hide_all_widgets()
        self.show_widget(self.btn_next, text = self.story.get_response_options())

    def pressed_btn(self, btn_name):
        self.story.update_last_answer(btn_name)

        if self.story.get_last_answer() == "next":
            self.story.set_next()
            self.show_message()
        else:
            # check for user input
            if self.story.get_expected_type() == "input":
                self.story.set_var(self.story.get_expected_var_name(), self.txt_in.get())

            # check for function call
            if self.story.has_function():
                eval("self." + self.story.get_function() + "()")

            # check if response object exist
            if self.story.get_response():
                self.show_response()
            else:
                self.pressed_btn("next")


# BEGIN custom story functions
# DONT FORGET!! set variables to self.story.vars["key"] = value !!!!

    def fight(self):
        seen = random.randint(1, 2)

        if seen == 1:
            self.story.set_next_index(1)    # seen
        else:
            self.story.set_next_index(0)    # unseen


    def fight_1(self):
        humans = int(random.randint(3, 10))
        zombies = int(random.randint(1, 5))

        self.story.set_var("humans", humans)
        self.story.set_var("zombies", zombies)

        if humans >= zombies:
            self.story.set_next_index(0)    # Humans have won
        else:
            self.story.set_next_index(1)    # Zombies have won

    def search_home(self):
        seen = random.randint(1, 2)
        if seen == 1:
            self.story.set_next_index(1)    # girl's there
        else:
            self.story.set_next_index(0)    # girl's not there


    def end(self):
        exit()

# END custom story functions


# main function
def main():
    root = Tk()
    root.title("text based game")
    app = Application(root)
    root.mainloop()


main()
