class manage_cliCommand(sublime_plugin.WindowCommand):
  cli = ""
  name_cli = ""
  bin_path = ""
  panel = None
  output_panel_name = "output_panel_cli"
  panel_command = "print_panel_cli"
  status_message_before = ""
  status_message_after_on_success = ""
  status_message_after_on_error = ""
  settings = {}
  command_with_options = []
  show_panel = True
  placeholders = {}
  hide_panel_on_success = True
  process = None

  def run(self, **kwargs):

    self.settings = get_project_settings()
    if self.settings:

      self.callback_after_get_settings(**kwargs)

      self.cli = kwargs.get("cli") if "cli" in kwargs else self.cli
      if not self.cli:
        raise Exception("'cli' field of the manage_cliCommand not defined.")

      self.command_with_options = self.substitute_placeholders( kwargs.get("command_with_options" if "command_with_options" in kwargs else self.command_with_options) )
      if not self.command_with_options or len(self.command_with_options) <= 0:
        raise Exception("'command_with_options' field of the manage_cliCommand not defined.")

      self.show_panel = kwargs.get("show_panel") if "show_panel" in kwargs != None else self.show_panel
      self.output_panel_name = self.substitute_placeholders( str(kwargs.get("output_panel_name") if "output_panel_name" in kwargs else self.output_panel_name) )
      self.status_message_before = self.substitute_placeholders( str(kwargs.get("status_message_before")) if "status_message_before" in kwargs else self.status_message_before )
      self.status_message_after_on_success = self.substitute_placeholders( str(kwargs.get("status_message_after_on_success")) if "status_message_after_on_success" in kwargs else self.status_message_after_on_success )
      self.status_message_after_on_error = self.substitute_placeholders( str(kwargs.get("status_message_after_on_error")) if "status_message_after_on_error" in kwargs else self.status_message_after_on_error )
      self.hide_panel_on_success = kwargs.get("hide_panel_on_success") if "hide_panel_on_success" in kwargs else self.hide_panel_on_success
      
      if self.settings["project_dir_name"]+"_"+self.output_panel_name in manage_cli_window_command_processes : 

        sublime.error_message("This command is already running! If you want execute it, you must stop it first.")
        return

      sublime.set_timeout_async(lambda: self.manage())

    else :

      sublime.error_message("Error: can't get project settings")

  def manage(self) :
    global manage_cli_window_command_processes

    if self.status_message_before :
      self.window.status_message(self.name_cli+": "+self.status_message_before)

    if self.show_panel :
      self.panel = Util.create_and_show_panel(self.output_panel_name, window=self.window)

    self.command_with_options = self.command_with_options + self.append_args_execute()

    self.before_execute()

    if ( self.can_execute() ) :

      node = NodeJS(check_local = True)

      if self.bin_path :
        node.execute(self.cli, self.command_with_options, is_from_bin=True, bin_path=self.bin_path, chdir=self.settings["project_dir_name"], wait_terminate=False, func_stdout=self.print_panel)
      else :
        node.execute(self.cli, self.command_with_options, is_from_bin=True, chdir=self.settings["project_dir_name"], wait_terminate=False, func_stdout=self.print_panel)

  def print_panel(self, line, process):
    global manage_cli_window_command_processes

    if not self.process :
      self.process = process

    self.process_communicate(line)

    if not self.settings["project_dir_name"]+"_"+self.output_panel_name in manage_cli_window_command_processes :
      manage_cli_window_command_processes[self.settings["project_dir_name"]+"_"+self.output_panel_name] = {
        "process": self.process
      }

    if line != None and self.show_panel:
      self.panel.run_command(self.panel_command, {"line": line, "hide_panel_on_success": self.hide_panel_on_success})
  
    if line == "OUTPUT-SUCCESS" :
      if self.status_message_after_on_success :
        self.window.status_message(self.name_cli+": "+self.status_message_after_on_success)

      self.on_success()

    if line == "OUTPUT-ERROR" :
      if self.status_message_after_on_error :
        self.window.status_message(self.name_cli+": "+self.status_message_after_on_error)

      self.on_error()

    if line == "OUTPUT-DONE":
      self.process = None

      if self.settings["project_dir_name"]+"_"+self.output_panel_name in manage_cli_window_command_processes :
        del manage_cli_window_command_processes[self.settings["project_dir_name"]+"_"+self.output_panel_name]

      self.on_done()

  def substitute_placeholders(self, variable):
    
    if isinstance(variable, list) :

      for index in range(len(variable)):
        for key, placeholder in self.placeholders.items():
          variable[index] = variable[index].replace(key, placeholder)

      return variable

    elif isinstance(variable, str) :

      for key, placeholder in self.placeholders.items():
        variable = variable.replace(key, placeholder)
        
      return variable

  def can_execute(self) :
    return True

  def before_execute(self) :
    return 

  def append_args_execute(self):
    return []

  def process_communicate(self, line):
    return
    
  def callback_after_get_settings(self, **kwargs):
    return

  def on_success(self):
    return

  def on_error(self):
    return

  def on_done(self):
    return