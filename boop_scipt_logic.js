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

    // Wrap the script content in a function that has access to `require` and exposes `main`
    var wrappedScript = `
      (function(require, state) {
        ${scriptContent}
        if (typeof main !== 'function') {
          throw new Error("The script did not define a 'main' function.");
        }
        // Expose main globally
        this.main = main;
      })(require, state);
    `;

    // Execute the wrapped script
    eval(wrappedScript);

    // Check if the main function was defined
    if (typeof main === "function") {
      main(state); // Call the main function with the state object
    } else {
      throw new Error("The script did not define the 'main' function.");
    }

    // Return the formatted text
    return state.text;
  } catch (error) {
    // Return an error message if something goes wrong
    return "Error: " + error.message;
  }
}

// Custom `require` implementation
function createRequire() {
  return function (modulePath) {
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

    var wrappedCode = `
      (function (exports, module) {
        ${scriptContent}
      })(module.exports, module);
    `;

    // Evaluate the wrapped code
    eval(wrappedCode);

    // Return the module's exports
    return module.exports;
  };
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