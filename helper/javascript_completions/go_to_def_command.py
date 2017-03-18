import sublime, sublime_plugin
import os
from node.main import NodeJS

node = NodeJS()

class go_to_defCommand(sublime_plugin.TextCommand):
  def run(self, edit, **args):
    view = self.view
    if args and "point" in args :
      point = args["point"]
    else :
      point = view.sel()[0].begin()
    self.go_to_def(view, point)

  def go_to_def(self, view, point):
    view = sublime.active_window().active_view()
    view.sel().clear()
    view.sel().add(point)
    sublime.active_window().run_command("goto_definition")
    if view.sel()[0].begin() == point :
      # try flow get-def
      sublime.status_message("")
      deps = flow_parse_cli_dependencies(view)
      result = node.execute_check_output(
        "flow",
        [
          'get-def',
          '--from', 'sublime_text',
          '--root', deps.project_root,
          '--json',
          view.file_name(),
          str(deps.row + 1), str(deps.col + 1)
        ],
        is_from_bin=True,
        use_fp_temp=True, 
        fp_temp_contents=deps.contents, 
        is_output_json=True,
        use_only_filename_view_flow=True
      )
      if result[0] :
        row = result[1]["line"]-1
        col = result[1]["start"]-1
        if result[1]["path"] != "-" and os.path.isfile(result[1]["path"]) :
          view = sublime.active_window().open_file(result[1]["path"])     
        sublime.set_timeout_async(lambda: Util.go_to_centered(view, row, col))

  def is_enabled(self):
    view = self.view
    if not Util.selection_in_js_scope(view, -1, "- string - comment"):
      return False
    return True

  def is_visible(self):
    view = self.view
    if not Util.selection_in_js_scope(view, -1, "- string - comment"):
      return False
    return True