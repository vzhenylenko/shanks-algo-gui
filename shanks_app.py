# author: Viacheslav Zhenylenko

from math import sqrt, ceil
from itertools import count, islice
from tkinter import Tk, BOTH, X, LEFT, Button
from tkinter.ttk import Frame, Label, Entry
from typing import Tuple, List


class ShanksApp():
    """Tkinter GUI application with interactive calcualtion of dicrepete logarithm."""

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


    def create_table(self) -> str:
        """Create string with output layout (algorithm steps)."""

        return self.line0 + '\n' + self.line1 + '\n' + self.line2 + '\n' + self.line3 + '\n' + self.line4


    def create_output(self) -> None:
        """Initialization of textual output after correctly specified a, b, p.

        Mainly string operations. Assign values to class instance attributes."""

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


    def exp(self, a: int, b: int, p: int) -> int:
        """Recursive exponentiation a^b modulo p."""

        if b == 0:
            return 1
        res = self.exp(a, int(b/2), p)
        res = (res * res) % p
        if b % 2 == 1:
            res = (res * a) % p
        return res


    def is_prime(self, n: int) -> bool:
        """Checks if n is prime."""
        return n > 1 and all(n % i for i in islice(count(2), int(sqrt(n) - 1)))


    def is_generator(self, a: int, p: int) -> bool:
        """Checks if A generate whole cyclic multiplication group of order P."""

        gen_set = set()
        curr = 1
        gen_set.add(curr)
        for i in range(p - 2):
            curr = (curr * a) % p
            if curr in gen_set:
                return False
            gen_set.add(curr)
        return True


    def validate_input(self) -> None:
        """Validate input values for a, b, p and prompt corresponding errors if some constraints are not satisfiied.

        1. Converts a, b, p to integers, prompt error if not successful
        2. Checks a, b, p to be positive
        3. Checks p to be prime and not exceed p_limit.
        4. Checks if a generates full cyclic group of order p under multiplication
        """

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
            flag = -1  # controls state of error text variable
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


    def run_shanks_algo(self, a: int, b: int, p: int) -> Tuple[int, int, List, List]:
        """Main method for running shanks algorithm.

        Args:
            a: logarithm base
            b: result of power operation on a
            p: order of cyclic group

        Returns:
            self.x1: calculated value of giant step
            self.x2: calculated value of beby step
            giant_list: list with values of giant steps
            baby_list: list with values of baby steps
        """

        m = int(ceil(sqrt(p)))
        giant_dict = {}
        step = self.exp(a, m, p)

        baby_list = []
        giant_list = [1]

        # giant steps calculation
        last_val = 1
        for i in range(m):
            last_val = (last_val * step) % p
            giant_list.append(last_val)
            if last_val not in giant_dict:
                giant_dict[last_val] = i + 1

        # baby steps calculation, terminates when we match value in giant_dict
        last_val = b
        for i in range(m):
            baby_list.append(last_val)
            if last_val in giant_dict:
                self.x1 = giant_dict[last_val]
                self.x2 = i
                break
            last_val = (last_val * a) % p

        return self.x1, self.x2, giant_list, baby_list


    def update_grid_start(self) -> None:
        """Called on start or when Restart button was pressed.

        Destroys old layout elements and create new in the latter case."""

        if not self.is_start:
            self.frame0.destroy()
            self.frame1.destroy()
            self.frame2.destroy()
            self.frame3.destroy()

            try:
                self.frame4.destroy()
                self.frame5.destroy()
                self.frame6.destroy()
            except:
                pass

        self.is_start = False
        self.frame.pack(fill=BOTH, expand=True)

        self.frame0 = Frame(self.frame)
        self.frame0.pack(fill=X)

        self.lbl0 = Label(self.frame0, text="Solving for x: a^x = b mod p. Enter a, b, p:", width=60)
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

        self.lbl3 = Label(self.frame3, text="Prime number p", width=18)
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


    def update_grid_start_algo(self) -> None:
        """Called when "Set button" clicked while all parameters of algorithm specified correctly a, b, p.

        Clears old layout elements, set textual output and new buttons. """

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


    def update_grid_next_step(self) -> None:
        """Called when "Next Step" button pressed during the algorithm run."""

        if self.output_ind == self.max_ind:
            upd_txt = f"Congratulations, we are done! m = {ceil(sqrt(self.p))}, answer: "
            upd_txt += f"x = {ceil(sqrt(self.p))} * {self.x1} - {self.x2} = {ceil(sqrt(self.p)) * self.x1 - self.x2}\n"
            self.lbl0.configure(text=upd_txt + self.output_list[self.max_ind])
        else:
            self.output_ind += 1
            self.lbl0.configure(text=self.output_list[self.output_ind])


    def update_grid_previous_step(self) -> None:
        """Called when "Previous Step" button is pressed. Updates state of layout and layout itself."""

        if self.output_ind != 0:
            self.output_ind -= 1
            self.lbl0.configure(text=self.output_list[self.output_ind])


    def update_grid_exit(self) -> None:
        """Called if "Exit" button is pressed. Closes tkinter's window. """

        self.window.destroy()


    def run_app(self) -> None:
        """Entry point to tkinter app."""

        self.window = Tk()
        self.window.title("Baby-step giant-step algorithm")
        self.window.geometry("500x180")

        self.frame = Frame()
        self.update_grid_start()
        self.frame.mainloop()


if __name__ == "__main__":
    app = ShanksApp()
    app.run_app()