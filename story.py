import json


class Story():
    def __init__(self, story_file):

        # load story data from json file
        with open(story_file) as file_data:
            self.story = json.load(file_data)

# GLOBALS
        self.current = next(iter(self.story.keys()))
        self.last_answer = ["", ""]

        self.vars = {}
        self.debug = False

# GETTERS

    def get_message(self):
        if self.debug:
            print("\nCurrent story point: \t\t\t" + str(self.current))
        return self.replace_placeholders(self.story[str(self.current)]["message"])

    def get_expected_type(self):
        return self.story[str(self.current)]["expect"]["type"]

    def get_expected_options(self):
        return self.story[str(self.current)]["expect"]["options"]

    def get_expected_var_name(self):
        return self.story[str(self.current)]["expect"]["var_name"]

    def get_response(self):
        if "response" in self.story[str(self.current)]:
            return self.replace_placeholders(self.story[str(self.current)]["response"]["text"][self.calc_last_answer()])
        else:
            return False

    def get_response_options(self):
        return self.replace_placeholders(self.story[str(self.current)]["response"]["options"][self.calc_last_answer()])

    def get_function(self):
        if self.has_function():
            if self.debug:
                print("Function call: \t\t\t\t" + str(self.story[str(self.current)]["func"]["name"]) + "()")
            return self.story[str(self.current)]["func"]["name"]
        else:
            return False

    def has_function(self):
        if "func" in self.story[str(self.current)]:
            return True
        else:
            return False

    def get_last_answer(self):
        #return self.last_answer
        if self.last_answer[1] == "next":
            return self.last_answer[1]
        else:
            return self.last_answer[0]

    def get_current(self):
        return self.current

    def get_var(self, var_name):
        return self.vars[var_name]

    def get_next_index(self):
        if "func" in self.story[str(self.current)]:
            if "next_index" in self.story[str(self.current)]["func"]:
                return self.story[str(self.current)]["func"]["next_index"]

        return False

# SETTERS

    def update_last_answer(self, last_answer):
        #self.last_answer = last_answer
        if last_answer == "next":
            self.last_answer[1] = "next"
        else:
            self.last_answer[0] = last_answer
            if len(self.last_answer) > 1:
                self.last_answer[1] = ""

        if self.debug:
            print("Answers of current story point: \t" + str(self.last_answer))

    def set_next(self):
        self.current = self.story[str(self.current)]["next"][self.calc_last_answer()]

    def set_var(self, var_name, value):
        self.vars[var_name] = value
        if self.debug:
            print("Store variable: \t\t\t$" + str(var_name) + " = " + str(value))

    def set_next_index(self, index):
        self.story[str(self.current)]["func"]["next_index"] = index

    def set_debug_mode(self, mode):
        if mode == True:
            self.debug = True
        elif mode == False:


# FUNCTIONALITY

    def calc_last_answer(self):
        if self.get_next_index():
            return self.get_next_index()
        elif self.last_answer[0] == "no" or self.last_answer[0] == "b":
            return 1
        elif self.last_answer[0] == "c":
            return 2
        else:
            return 0

    def replace_placeholders(self, text):
        if text == "":
            return -1

        words = text.split(' ')
        replaced_char = ""

        for i, word in enumerate(words):
            if(len(word) > 0 and word[0] == '$'):
                name = word.replace('$', '')
                for c in ['.', ',', '?', '!', ':']:
                    if name.replace(c, '') != name:
                        name = name.replace(c, '')
                        replaced_char = replaced_char + c
                words[i] = str(self.vars[name]) + replaced_char

        return ' '.join(words)
