class Option:
    def __init__(self, name, action, params=None, **kwargs):
        self.name = name
        self.action = action
        self.params = params if params else {}
        self.extra_params = kwargs

    def set_option(self, **kwargs):
        if kwargs is None:
            return

        for k, v in kwargs.items():
            self.__dict__[k] = v

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        for k, v in self.__dict__.items():
            print(f'arg: {k}\n value: {v}\n')


class Menu:
    def __init__(self, name, description='', exit_op=True, input_line=''):
        self.name = name
        self.description = description
        self.options = []
        self.input_line = input_line

        if exit_op:
            self.exit_opt = Option(**{'name': 'exit', 'action': exit})
        else:
            self.exit_opt = None

    def add_option(self, name, action, params=None, **kwargs):
        if params is None:
            params = {}
        self.options.append(Option(name=name, action=action, params=params, **kwargs))

    def set_exit(self, name='exit', action=exit):
        self.exit_opt = Option(**{'name': name, 'action': action})

    def print_options(self):
        for i, opt in enumerate(self.options):
            print(f"{i + 1}: {opt}")

    def __len__(self):
        return len(self.options)

    def print_exit(self):
        if self.exit_opt:
            print(f'{len(self) + 1}: {self.exit_opt}')

    def print_menu(self):
        print(self.name)
        self.print_options()
        self.print_exit()

    def run_menu(self):
        while True:
            print('\n')
            self.print_menu()
            try:
                ans = int(input(f'{self.input_line}'))
            except ValueError:
                print("ERROR: choose valid number option")
                continue
            if 1 <= ans <= len(self.options):
                opt = self.options[ans - 1]
                try:
                    opt.action(**opt.params)
                except Exception as e:
                    print(f"action raise exception: {e}")
                    continue

            elif ans == len(self.options) + 1:
                self.exit_opt.action()
            else:
                print('unknown option')

    def create_sub_menu(self, name, description='', add_to_options=False):
        sub_menu = Menu(name, description)
        sub_menu.set_exit(name='return', action=self.run_menu)
        if add_to_options:
            self.add_option(name=name, action=sub_menu.run_menu)
        return sub_menu
