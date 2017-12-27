class enable_menu_build_flowEventListener(enable_menu_project_typeEventListener):
  path = os.path.join(PROJECT_FOLDER, "build_flow", "Main.sublime-menu")
  path_disabled = os.path.join(PROJECT_FOLDER, "build_flow", "Main_disabled.sublime-menu")

class build_flowCommand(manage_cliCommand):

  isNode = True
  isBinPath = True

  def prepare_command(self, **kwargs):

    self.placeholders[":source_folder"] = self.settings["project_settings"]["build_flow"]["source_folder"]
    self.placeholders[":destination_folder"] = self.settings["project_settings"]["build_flow"]["destination_folder"]
    self.command += self.settings["project_settings"]["build_flow"]["options"]
    self.command = self.substitute_placeholders(self.command)
    self._run()

  def _run(self):
    super(build_flowCommand, self)._run()

  def is_enabled(self) :
    settings = get_project_settings()
    if settings and settings["project_settings"]["build_flow"]["source_folder"] and settings["project_settings"]["build_flow"]["destination_folder"] :
      return True
    return False