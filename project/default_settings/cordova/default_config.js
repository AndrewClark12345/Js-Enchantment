module.exports = {
  "project_details": {
    "type": ["cordova"]
  },
  "flow_settings": {
    "ignore": [
      "<PROJECT_ROOT>/platforms/.*",
      "<PROJECT_ROOT>/hooks/.*",
      "<PROJECT_ROOT>/plugins/.*",
      "<PROJECT_ROOT>/node_modules/.*"
    ],
    "include": [
    
    ],
    "libs":[
      ":PACKAGE_PATH/flow/libs/cordova/cordova.js"
    ]
  },
  "cordova_settings": {
    "cli_global_options": [],
    "platform_versions": {}
  }
}