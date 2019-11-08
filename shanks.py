from math import sqrt, ceil
from itertools import count, islice
from tkinter import Tk, BOTH, X, LEFT, Button
from tkinter.ttk import Frame, Label, Entry

class ShanksApp:

    is_start = True
    i = 0
    a = 0
    b = 0
    p = 0
    x1 = 0
    x2 = 0
    output_ind = 0
    max_ind = -1
    line0 = 'm ='
    line1 = 'Step number i      '
    line2 = '----------------------------------'
    line3 = 'Big step = a^(i*m)  '
    line4 = 'Small step = b*a^i '

    def create_table(self):
        # create string with output content (algorithm steps)
        return self.line0 + '\n' + self.line1 + '\n' + self.line2 + '\n' + self.line3 + '\n' + self.line4

    def exp(self, a, b, p):
        # optimized, recursive exponentiation a^b modulo p
        if b == 0:
            return 1
        res = self.exp(a, int(b/2), p)
        res = (res * res) % p
        if b % 2 == 1:
            res = (res * a) % p
        return res

    def run_shanks_algo(self, a, b, p):
        # run shanks algorithm and returns info about baby steps and giant steps
        res = -1
        m = ceil(sqrt(p))
        giant_dict = {}
        step = self.exp(a, m, p)

        baby_list = []
        giant_list = [1]

        last_val = 1

        for i in range(m):
            last_val = (last_val * step) % p
            giant_list.append(last_val)
            if last_val not in giant_dict:
                giant_dict[last_val] = i + 1

        last_val = b
        for i in range(m):
            baby_list.append(last_val)
            if last_val in giant_dict:
                self.x1 = giant_dict[last_val]
                self.x2 = i
                break
            last_val = (last_val * a) % p

        return self.x1, self.x2, giant_list, baby_list

    def update_grid_start(self):
        # invoked on start or when Restart button was pressed
        if not self.is_start:
            self.frame0.destroy()
            self.frame1.destroy()
            self.frame2.destroy()
            self.frame3.destroy()

            try:
                self.frame4.destroy()
            except:
                pass

            try:
                self.frame5.destroy()
            except:
                pass

            try:
                self.frame6.destroy()
            except:
                pass

        self.is_start = False
        self.frame.pack(fill=BOTH, expand=True)

        self.frame0 = Frame(self.frame)
        self.frame0.pack(fill=X)

        self.lbl0 = Label(self.frame0, text="a^x = b mod p. Enter a, b, p:", width=60)
        self.lbl0.pack(side=LEFT, padx=20, pady=5)

        self.frame1 = Frame(self.frame)
        self.frame1.pack(fill=X)

        self.lbl1 = Label(self.frame1, text="Logarithm base a", width=18)
        self.lbl1.pack(side=LEFT, padx=20, pady=5)

        self.entry_a = Entry(self.frame1)
        self.entry_a.pack(fill=X, padx=5, expand=True)

        self.frame2 = Frame(self.frame)
        self.frame2.pack(fill=X)

        self.lbl2 = Label(self.frame2, text="Logarithm argument b", width=18)
        self.lbl2.pack(side=LEFT, padx=20, pady=5)

        self.entry_b = Entry(self.frame2)
        self.entry_b.pack(fill=X, padx=5, expand=False)

        self.frame3 = Frame(self.frame)
        self.frame3.pack(fill=X)

        self.lbl3 = Label(self.frame3, text="Group order p", width=18)
        self.lbl3.pack(side=LEFT, padx=20, pady=5)

        self.entry_p = Entry(self.frame3)
        self.entry_p.pack(fill=X, padx=5, expand=True)

        self.frame4 = Frame(self.frame)
        self.frame4.pack(fill=X)

        self.input_button = Button(self.frame4, text="Set", command=lambda: self.validate_input())
        self.input_button.pack(side=LEFT, padx=20, pady=0)

        self.input_button = Button(self.frame4, text="Restart", command=lambda: self.update_grid_start())
        self.input_button.pack(side=LEFT, padx=0, pady=0)

        self.input_button = Button(self.frame4, text="Exit", command=lambda: self.update_grid_exit())
        self.input_button.pack(side=LEFT, padx=0, pady=0)

    def update_grid_start_algo(self):
        # invoked if a, b, p were specified correctly and algorithm started
        self.output_ind = 0

        self.lbl0.configure(text=self.create_table())
        self.frame1.destroy()
        self.frame2.destroy()
        self.frame3.destroy()
        self.frame4.destroy()

        self.frame3 = Frame(self.frame)
        self.frame3.pack(fill=X)

        self.input_button = Button(self.frame3, text="<< Previous step", command=lambda: self.update_grid_previous_step())
        self.input_button.pack(side=LEFT, padx=20, pady=0)

        self.input_button = Button(self.frame3, text="Next step >>", command=lambda: self.update_grid_next_step())
        self.input_button.pack(side=LEFT, padx=0, pady=0)

        self.frame4 = Frame(self.frame)
        self.frame4.pack(fill=X)

        self.input_button = Button(self.frame4, text="Restart", command=lambda: self.update_grid_start())
        self.input_button.pack(side=LEFT, padx=20, pady=0)

        self.input_button = Button(self.frame4, text="Exit", command=lambda: self.update_grid_exit())
        self.input_button.pack(side=LEFT, padx=60, pady=0)

    def update_grid_next_step(self):
        # invoked if Next Step button was pressed
        if self.output_ind == self.max_ind:
            upd_txt = f"Congratulations, we are done! m = {ceil(sqrt(self.p))}, answer: "
            upd_txt += f"x = {ceil(sqrt(self.p))} * {self.x1} - {self.x2} = {ceil(sqrt(self.p)) * self.x1 - self.x2}\n"
            self.lbl0.configure(text=upd_txt + self.output_list[self.max_ind])
        else:
            self.output_ind += 1
            self.lbl0.configure(text=self.output_list[self.output_ind])

    def update_grid_previous_step(self):
        # invoked if Previous Step button was pressed
        if self.output_ind != 0:
            self.output_ind -= 1
            self.lbl0.configure(text=self.output_list[self.output_ind])

    def update_grid_exit(self):
        # invoked if Exit button is pressed
        self.window.destroy()

    def is_prime(self, n):
        # checks if n is prime
        return n > 1 and all(n % i for i in islice(count(2), int(sqrt(n) - 1)))

    def is_generator(self, a, p):
        # checks if a generate whole cyclic multiplication group of order p
        gen_set = set()
        curr = 1
        gen_set.add(curr)
        for i in range(p-2):
            curr = (curr * a) % p
            if curr in gen_set:
                return False
            gen_set.add(curr)
        return True

    def validate_input(self):
        # checks several scenarios of incorrect input and update text window with corresponding errors
        p_limit = 10000000

        try:
            self.p = int(self.entry_p.get())
            self.a = int(self.entry_a.get())
            self.b = int(self.entry_b.get())
        except Exception:
            self.lbl0.config(text=f"Error! Input should be numeric!", foreground="red")
            return

        if self.is_prime(self.p) and self.p < p_limit and 0 < self.a and self.a < self.p and 0 < self.b and \
                        self.b < self.p:
            self.create_output()
            if self.is_generator(self.a, self.p):
                self.lbl0.config(foreground="black")
                self.update_grid_start_algo()
            else:
                self.lbl0.config(text=f"Error! a={self.a} should generate the whole group!", foreground="red")
        else:
            bool_list = [self.is_prime(self.p), self.p < p_limit, 0 < self.a, self.a < self.p, 0 < self.b,
                         self.b < self.p]
            str_list = ['p should be prime', f'p < {p_limit}', '0 < a', 'a < p', '0 < b', 'b < p']
            err = 'Error! Following constraints should be satisfied: '
            flag = -1         # controls state of error text variable
            for bool_val, err_str in zip(bool_list, str_list):
                if not bool_val:
                    # several possibilities of updating err
                    if flag in [0, 2]:
                        err += '; '

                    err += err_str

                    if flag in [-1, 1]:
                        flag += 1

                    if flag == 0 and len(err) > 66:
                        err += '\n'
                        flag = 1

            self.lbl0.configure(text=err, foreground="red")

    def create_output(self):
        # initialization of output after correctly specified a, b, p
        self.x1, self.x2, giant_list, baby_list = self.run_shanks_algo(self.a, self.b, self.p)

        m = ceil(sqrt(self.p))
        self.max_ind = m + len(baby_list)
        self.output_list = []

        self.line0 = f"PROBLEM: {self.a}^x = {self.b} mod {self.p}, find x.\nSOLUTION: Number of big steps is {m}."
        self.line1 = "Step number i               "
        for i in range(m):
            self.line1 += f"| {i}  "
        self.line2 = '-----------------------' + '-' * 4 * m
        self.line3 = f'Big step = {self.a}^(i*{m})         '
        self.line3 = self.line3[:27]
        self.line4 = f'Small step = {self.b}*{self.a}^(-i)    '
        self.line4 = self.line4[:27]

        self.output_list.append(self.create_table())

        for i in range(m):
            temp = f"| {giant_list[i % len(giant_list)]}  "
            self.line3 += temp[:5]
            self.output_list.append(self.create_table())

        for i in range(len(baby_list)):
            temp = f"| {baby_list[i]}  "
            self.line4 += temp[:5]
            self.output_list.append(self.create_table())

        self.line0 = f"PROBLEM: {self.a}^x = {self.b} mod {self.p}, find x.\nSOLUTION: Number of big steps is {m}."
        self.line1 = "Step number i               "
        for i in range(m):
            self.line1 += f"| {i}  "
        self.line2 = '-----------------------' + '-' * 4 * m
        self.line3 = f'Big step = {self.a}^(i*{m})         '
        self.line3 = self.line3[:27]
        self.line4 = f'Small step = {self.b}*{self.a}^(-i)  '
        self.line4 = self.line4[:25]

    def run_app(self):
        self.window = Tk()
        self.window.geometry("500x180")

        self.frame = Frame()
        self.update_grid_start()
        self.frame.mainloop()

if __name__ == "__main__":
    app = ShanksApp()
    app.run_app()