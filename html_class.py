from datetime import datetime
import os


class TestRun:
    def __init__(self, name, dataset, function):
        self.name = name
        self.dataset = dataset
        self.function_list = function

    def run(self):
        now = datetime.now()
        path = f'runs/{now.strftime("%d-%m-%Y")}/{now.timestamp()}'
        os.makedirs(path)
        with open(f'{path}/main.html', 'w') as file:
            file.write((f'<!DOCTYPE html>\n<html>\n<head>\n'
                        f'<link rel="stylesheet" href="mystyle.css">\n</head>\n<body>\n'))
            for key in self.function_list:  # chose data category from dictionary
                for column_name in key:  # chose column from specific data category
                    file.write(f'<div class="column">\n\t<h1>{column_name.title()}</h1>')
                    for func in self.function_list[key]:  # apply all function from specific category to column
                        self._function_implement(file, func, column_name, path)
            file.write(f'</body>\n</html>')

    def _function_implement(self, file_name, func, column_name, path):
        file_name.write(f'\n\t<div class="func">')
        print(func)
        for key, value in func.items():
            result = key(self.dataset, column_name, path, **value)
        title = result.get('title')
        text = result.get('text')
        image = result.get('image')
        if title:
            file_name.write(f'\n\t\t<div class="title">\n\t\t\t<h2>{title}</h2>\n\t\t</div>')
        if text:
            file_name.write(f'\n\t\t<div class="text">\n\t\t\t<p>{text}<p>\n\t\t</div>')
        if image:
            file_name.write(f'\n\t\t<div class="image">\n\t\t\t<image src="{image}", alt = "Error">\n\t\t</div>')
        file_name.write(f'\n\t</div>\n')
