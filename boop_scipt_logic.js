// Requried variables
// `input`
// `input_script_path`

// Outputs the content of the script

ObjC.import("stdlib")

function run(argv) {
  var query = $.getenv("input")

  // State object to pass to the `main` function
  var state = {
      text: query,
      fullText: query,
      selection: query,
      postError: function (message) {
        throw new Error(message); // Throw errors if invalid JSON
      },
      postInfo: function (message) {
        this.text += '\n' + message; // Append message to text with a newline
      },
  };

  try {
    // Inject the custom `require` function
    var require = createRequire();

    // Load the external script
    var scriptPath = $.getenv("input_script_path")
    var scriptContent = readFile(scriptPath);

    // Debug: Check the script content
    if (scriptContent) {
      console.log("Script content loaded successfully.");
    } else {
      console.log("Script content is empty or undefined.");
    }

    // Compile the script with `new Function` instead of eval so `require` and
    // `state` are passed in explicitly (macOS Tahoe's JXA runs eval'd code in
    // global scope, where function locals like `require` are not visible)
    var makeMain = new Function("require", "state", scriptContent +
      '\nif (typeof main !== "function") { throw new Error("The script did not define a \'main\' function."); }' +
      '\nreturn main;');

    // Get the script's main function and call it with the state object
    var main = makeMain(require, state);
    main(state);

    // Return the formatted text
    return state.text;
  } catch (error) {
    // Return an error message if something goes wrong
    return "Error: " + error.message;
  }
}

// Custom `require` implementation
function createRequire() {
  var requireFn = function (modulePath) {
    // Replace `@boop/` with the `scripts/lib` path
    if (modulePath.startsWith("@boop/")) {
      modulePath = "./scripts/lib/" + modulePath.substring(6) + ".js";
    } else if (!modulePath.endsWith(".js")) {
      modulePath += ".js";
    }

    // Read the module file
    var scriptContent = readFile(modulePath);

    if (!scriptContent) {
      throw new Error("Module not found: " + modulePath);
    }

    // Wrap the code in CommonJS-like structure
    var module = { exports: {} };

    // Compile with `new Function` (see note in run()); passing `require` also
    // lets modules require other modules
    var factory = new Function("exports", "module", "require", scriptContent);
    factory(module.exports, module, requireFn);

    // Return the module's exports
    return module.exports;
  };
  return requireFn;
}

// Function to read file content
function readFile(filePath) {
  var app = Application.currentApplication();
  app.includeStandardAdditions = true;

  try {
    // Use a shell command to read the file content
    var result = app.doShellScript("cat " + filePath);
    return result; // Return the content of the file
  } catch (error) {
    throw new Error("Unable to read file at: " + filePath);
  }
}