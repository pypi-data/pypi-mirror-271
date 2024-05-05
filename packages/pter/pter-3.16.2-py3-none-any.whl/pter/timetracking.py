"""Integration with external time trackers"""
import shutil
import subprocess

from cursedspace import ShellContext


class Tracker:
    def __init__(self, app, configuration):
        self.app = app
        self.program = ''
        self.parameters = []

        self.parse_configuration(configuration)

    def start(self, task):
        parameters = self.expand_parameters(task)

        with ShellContext(self.app.screen, False):
            result = subprocess.run([self.program] + parameters,
                                    stdout=subprocess.DEVNULL,
                                    stderr=subprocess.PIPE,
                                    check=False)
        return result

    def parse_configuration(self, text):
        parts = parse_tracker_configuration(text)

        self.program = shutil.which(parts[0])
        self.parameters = parts[1:]

    def expand_parameters(self, task):
        expanded = []
        contexts = [c for c in task.contexts if len(c) > 0]
        context = ''
        if len(contexts) > 0:
            context = contexts[0]
        projects = [p for p in task.projects if len(p) > 0]
        project = ''
        if len(projects) > 0:
            project = projects[0]
        taskid = ''
        if len(task.attributes.get('id', [])) > 0:
            taskid = task.attributes['id'][0]

        mapping = [('{description}', task.bare_description()),
                   ('{full}', task.description),
                   ('{raw}', str(task)),
                   ('{context}', context),
                   ('{project}', project),
                   ('{id}', taskid)]

        for part in self.parameters:
            if isinstance(part, str):
                expanded.append(part)
                continue

            selector = part[-1]
            prefix = part[:-1]

            if '{contexts}' in selector or '{projects}' in selector:
                collection = contexts
                placeholder = '{contexts}'
                if '{projects}' in selector:
                    collection = projects
                    placeholder = '{projects}'

                for value in collection:
                    expanded += prefix \
                                + [selector.replace(placeholder, value)]
            elif '{*contexts}' in selector or '{*projects}' in selector:
                collection = contexts
                placeholder = '{*contexts}'
                if '{*projects}' in selector:
                    collection = projects
                    placeholder = '{*projects}'
                if len(collection) == 0:
                    continue
                expanded += prefix
                if selector != placeholder:
                    expanded += [selector.replace(placeholder, value)
                                 for value in collection]
                else:
                    expanded += list(collection)
            else:
                some_replacement = False
                for pattern, replacement in mapping:
                    if pattern not in selector:
                        continue
                    if len(replacement) == 0:
                        continue
                    selector = selector.replace(pattern, replacement)
                    some_replacement = True
                    break

                if len(selector) == 0 or not some_replacement:
                    continue

                expanded += prefix
                expanded += [selector]
        return expanded


def parse_tracker_configuration(text):
    tokens = []
    token = ''
    group = []

    in_brace = 0
    quoted = ''
    escaped = False

    for letter in text:
        if escaped:
            token += letter
            escaped = False
        elif letter == quoted:
            quoted = ''
        elif letter == '\\':
            escaped = True
        elif len(quoted) > 0:
            token += letter
        elif in_brace > 0 and letter == '}':
            in_brace -= 1
            if in_brace == 0:
                if len(token) > 0:
                    group.append(token)
                tokens.append(group)
                group = []
                token = ''
            else:
                token += letter
        elif letter == '{':
            if in_brace > 0:
                token += letter
            else:
                group = []
            in_brace += 1
        elif letter in '"\'':
            quoted = letter
        elif letter == ' ':
            if len(token) > 0:
                if in_brace:
                    group.append(token)
                else:
                    tokens.append(token)
            token = ''
        else:
            token += letter

    return tokens
