import sublime
import sublime_plugin
import re
import sys
from collections import defaultdict


class SortTodoCommand(sublime_plugin.TextCommand):


    def run(self, edit):

        for region in [sublime.Region(0, self.view.size())]:

            # Determine the current line ending setting, so we can rejoin the
            # sorted lines using the correct line ending character.
            lend = '\n'  # Default.
            line_endings = self.view.line_endings()
            if line_endings == 'CR':
                lend = '\r'
            elif line_endings == 'Windows':
                lend = '\r\n'

            projects = defaultdict(list)
            unassigned = []
            done = []
            lines = [self.view.substr(r) for r in self.view.lines(region)]
            for line in lines:
                project = re.findall('\+(\w+)', line)
                if line.startswith('x'):
                    done.append(line)
                elif len(project) == 1:
                    projects[project[0]].append(line)
                elif len(line) > 1:
                    unassigned.append(line)

            output = ''
            # unassigned
            for item in sorted(unassigned):
                output += '%s%s' % (item, lend)
            output += lend * 2

            # projects
            for p_name in sorted(projects):
                for item in sorted(projects[p_name]):
                    output +=  '%s%s' % (item, lend)
                output +=  lend * 2

            # done
            for item in done:
                output +=  '%s%s' % (item, lend)
            output +=  lend

            self.view.replace(edit, region, output)
