import sublime, sublime_plugin
import os, webbrowser, shlex, json, collections

def angularv1_ask_custom_path(project_path, type):
    sublime.active_window().show_input_panel("Yeoman CLI custom path", "yo", lambda angularv1_custom_path: angularv1_prepare_project(project_path, angularv1_custom_path) if type == "create_new_project" or type == "add_project_type" else add_angularv1_settings(project_path, angularv1_custom_path), None, None)

def add_angularv1_settings(working_directory, angularv1_custom_path):
  project_path = working_directory
  settings = get_project_settings()
  if settings :
    project_path = settings["project_dir_name"]
    
  # flowconfig_file_path = os.path.join(project_path, ".flowconfig")
  # with open(flowconfig_file_path, 'r+', encoding="utf-8") as file:
  #   content = file.read()
  #   content = content.replace("[ignore]", """[ignore]""")
  #   file.seek(0)
  #   file.truncate()
  #   file.write(content)

  PROJECT_SETTINGS_FOLDER_PATH = os.path.join(project_path, PROJECT_SETTINGS_FOLDER_NAME)

  default_config = json.loads(open(os.path.join(PROJECT_FOLDER, "angularv1", "default_config.json")).read(), object_pairs_hook=collections.OrderedDict)
  default_config["working_directory"] = working_directory
  default_config["cli_custom_path"] = angularv1_custom_path

  angularv1_settings = os.path.join(PROJECT_SETTINGS_FOLDER_PATH, "angularv1_settings.json")

  with open(angularv1_settings, 'w+', encoding="utf-8") as file:
    file.write(json.dumps(default_config, indent=2))

def angularv1_prepare_project(project_path, angularv1_custom_path):
  
  terminal = Terminal(cwd=project_path)
  
  if sublime.platform() != "windows": 
    open_project = ["&&", shlex.quote(sublime_executable_path()), shlex.quote(get_project_settings(project_path)["project_file_name"])] if not is_project_open(get_project_settings(project_path)["project_file_name"]) else []
    terminal.run([shlex.quote(angularv1_custom_path), "angular"] + open_project)
  else:
    open_project = [sublime_executable_path(), get_project_settings(project_path)["project_file_name"], "&&", "exit"] if not is_project_open(get_project_settings(project_path)["project_file_name"]) else []
    terminal.run([angularv1_custom_path, "angular"])
    if open_project:
      terminal.run(open_project)

  add_angularv1_settings(project_path, angularv1_custom_path)

Hook.add("angularv1_after_create_new_project", angularv1_ask_custom_path)
Hook.add("angularv1_add_javascript_project_configuration", angularv1_ask_custom_path)
Hook.add("angularv1_add_javascript_project_type", angularv1_ask_custom_path)

class enable_menu_angularv1EventListener(enable_menu_project_typeEventListener):
  project_type = "angularv1"
  path = os.path.join(PROJECT_FOLDER, "angularv1", "Main.sublime-menu")
  path_disabled = os.path.join(PROJECT_FOLDER, "angularv1", "Main_disabled.sublime-menu")

class angularv1_cliCommand(manage_cliCommand):

  cli = "yo"
  custom_name = "angularv1"
  settings_name = "angularv1_settings"

  def prepare_command(self, **kwargs):

    if ":name" in self.command:
      sublime.active_window().show_input_panel( (self.command[0].replace("angular:", ""))+" name:", "", self.name_on_done, None, None )
    else :
      self._run()

  def name_on_done(self, name):
    self.placeholders[":name"] = shlex.quote(name.strip())
    self.command = self.substitute_placeholders(self.command)
    self._run()

  def _run(self):
    # try:
    #   self.command = {
    #     'serve': lambda : self.command + self.settings["angularv1_settings"]
    #   }[self.command[0]]()
    # except KeyError as err:
    #   pass
    # except Exception as err:
    #   print(traceback.format_exc())
    #   pass

    super(angularv1_cliCommand, self)._run()

