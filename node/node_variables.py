import platform
import os

PACKAGE_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

PLATFORM_ARCHITECTURE = "64bit" if platform.architecture()[0] == "64bit" else "32bit"

platform_switcher = {"Darwin": "osx", "Linux": "linux", "Windows": "windows"}

NODE_JS_VERSION = "v7.7.2"
NODE_JS_BINARIES_FOLDER_NAME = "node_binaries"
NODE_JS_VERSION_URL_LIST_ONLINE = "https://nodejs.org/dist/index.json"
NODE_JS_BINARIES_FOLDER = os.path.join(PACKAGE_PATH, NODE_JS_BINARIES_FOLDER_NAME)
NODE_JS_BINARIES_FOLDER_PLATFORM = os.path.join(NODE_JS_BINARIES_FOLDER, platform_switcher.get(platform.system()) + "-" + PLATFORM_ARCHITECTURE)
os_switcher = {"osx": "darwin", "linux": "linux", "windows": "win"}
NODE_JS_OS = os_switcher.get(platform_switcher.get(platform.system()))
NODE_JS_ARCHITECTURE = "x64" if PLATFORM_ARCHITECTURE == "64bit" else "x86"
NODE_JS_BINARY_NAME = "node" if NODE_JS_OS != 'win' else "node.exe"
NPM_NAME = "npm"
NODE_JS_PATH_EXECUTABLE = os.path.join(NODE_JS_BINARIES_FOLDER_PLATFORM, "bin", NODE_JS_BINARY_NAME) if NODE_JS_OS != 'win' else os.path.join(NODE_JS_BINARIES_FOLDER_PLATFORM, NODE_JS_BINARY_NAME)
NPM_PATH_EXECUTABLE = os.path.join(NODE_JS_BINARIES_FOLDER_PLATFORM, "bin", NPM_NAME) if NODE_JS_OS != 'win' else os.path.join(NODE_JS_BINARIES_FOLDER_PLATFORM, NPM_NAME)
NODE_MODULES_FOLDER_NAME = "node_modules"
NODE_MODULES_PATH = os.path.join(PACKAGE_PATH, NODE_MODULES_FOLDER_NAME)
NODE_MODULES_BIN_PATH = os.path.join(NODE_MODULES_PATH, ".bin")