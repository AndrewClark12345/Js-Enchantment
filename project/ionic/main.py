import sublime, sublime_plugin
import os, webbrowser, shlex, json

def create_ionic_project_process(line, process, panel, project_data, sublime_project_file_name, open_project) :
  print(line)
  if line != None and panel:
    panel.run_command("print_panel_cli", {"line": line, "hide_panel_on_success": True})

  if line == "OUTPUT-SUCCESS":
    Util.move_content_to_parent_folder(os.path.join(project_data["ionic_settings"]["working_directory"], "temp"))

    if open_project :
      open_project_folder(sublime_project_file_name)

def create_ionic_project(json_data):
  project_data = json_data["project_data"]
  project_details = project_data["project_details"]
  project_folder = project_data["ionic_settings"]["working_directory"]
  create_options = []

  if "create_options" in project_data and project_data["create_options"]:
    create_options = project_data["create_options"]

  panel = Util.create_and_show_panel("ionic_panel_installer_project")

  node = NodeJS()

  if "ionic_settings" in project_data and "package_json" in project_data["ionic_settings"] and "use_local_cli" in project_data["ionic_settings"] and project_data["ionic_settings"]["use_local_cli"] :
    node.execute('ionic', ["start", "temp"] + create_options, is_from_bin=True, bin_path=os.path.join(project_folder, ".jc-project-settings", "node_modules", ".bin"), chdir=project_folder, wait_terminate=False, func_stdout=create_ionic_project_process, args_func_stdout=[panel, project_data, (project_data['project_file_name'] if "sublime_project_file_name" not in json_data else json_data["sublime_project_file_name"]), (False if "sublime_project_file_name" not in json_data else True) ])
  else :  
    node.execute('ionic', ["start", "temp"] + create_options, is_from_bin=True, chdir=project_folder, wait_terminate=False, func_stdout=create_ionic_project_process, args_func_stdout=[panel, project_data, (project_data['project_file_name'] if "sublime_project_file_name" not in json_data else json_data["sublime_project_file_name"]), (False if "sublime_project_file_name" not in json_data else True) ])

  return json_data

Hook.add("ionic_create_new_project", create_ionic_project)

Hook.add("ionic_add_new_project_type", create_ionic_project)

class enable_menu_ionicEventListener(enable_menu_project_typeEventListener):
  project_type = "ionic"
  path = os.path.join(PROJECT_FOLDER, "ionic", "Main.sublime-menu")
  path_disabled = os.path.join(PROJECT_FOLDER, "ionic", "Main_disabled.sublime-menu")

class ionic_baseCommand(cordova_baseCommand):
  cli = "ionic"
  name_cli = "Ionic"
  bin_path = ""

  def append_args_execute(self) :
    custom_args = []
    command = self.command_with_options[0]

    if command == "serve" :
      custom_args = custom_args + ["--port"] + [self.settings["cordova_settings"]["serve_port"]]

    elif command == "platform" or command == "build" or command == "run" or command == "emulate" :
      custom_args = custom_args + self.settings["ionic_settings"]["cli_"+command+"_options"]
      if command == "emulate":
        mode = self.command_with_options[2][2:]
        platform = self.placeholders[":platform"]
        custom_args_platform = ""
        custom_args_platform = Util.getDictItemIfExists(self.settings["ionic_settings"]["platform_"+command+"_options"][mode], platform)
        if custom_args_platform :
          custom_args = custom_args + ["--"] + shlex.split(custom_args_platform)

    elif "cli_"+command+"_options" in self.settings["ionic_settings"] :
      custom_args = custom_args + self.settings["ionic_settings"]["cli_"+command+"_options"]

    return super(ionic_baseCommand, self).append_args_execute() + custom_args

  def before_execute(self):

    if self.settings["ionic_settings"]["cli_custom_path"] :
      self.bin_path = self.settings["ionic_settings"]["cli_custom_path"]
    elif self.settings["ionic_settings"]["use_local_cli"] :
      self.bin_path = os.path.join(self.settings["settings_dir_name"], "node_modules", ".bin")

    command = self.command_with_options[0]
    if command == "serve" :
      del self.command_with_options[1]

  def is_enabled(self):
    return is_type_javascript_project("ionic") and is_type_javascript_project("cordova")

  def is_visible(self):
    return is_type_javascript_project("ionic") and is_type_javascript_project("cordova")

class manage_ionicCommand(ionic_baseCommand, manage_cordovaCommand):

  def run(self, **kwargs):
    super(manage_ionicCommand, self).run(**kwargs)

class manage_serve_ionicCommand(ionic_baseCommand, manage_serve_cordovaCommand):
  
  def run(self, **kwargs):
    super(manage_serve_ionicCommand, self).run(**kwargs)

class manage_plugin_ionicCommand(manage_ionicCommand, manage_plugin_cordovaCommand):

  def run(self, **kwargs):
    super(manage_plugin_ionicCommand, self).run(**kwargs)

class manage_add_platform_ionicCommand(manage_ionicCommand, manage_add_platform_cordovaCommand):

  def run(self, **kwargs):
    super(manage_add_platform_ionicCommand, self).run(**kwargs)

class manage_remove_platform_ionicCommand(manage_ionicCommand, manage_remove_platform_cordovaCommand):

  def run(self, **kwargs):
    super(manage_remove_platform_ionicCommand, self).run(**kwargs)

  def on_success(self):
    Util.delItemIfExists(self.settings["ionic_settings"]["platform_emulate_options"]["debug"], self.placeholders[":platform"])
    Util.delItemIfExists(self.settings["ionic_settings"]["platform_emulate_options"]["release"], self.placeholders[":platform"])
    super(manage_remove_platform_ionicCommand, self).on_success()

class sync_ionic_projectCommand(ionic_baseCommand, sync_cordova_projectCommand):

  platform_list = []
  plugin_list = []

  def run(self, **kwargs):
    super(sync_ionic_projectCommand, self).run(**kwargs)
