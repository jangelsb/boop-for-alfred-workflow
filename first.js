function run(argv) {
  var query = argv[0]; // Get the JSON string from the arguments

  // State object to pass to the `main` function
  var state = {
    text: query,
    fullText: query,
    selection: query,
    postError: function(message) {
      throw new Error(message); // Throw errors if invalid JSON
    }
  };

  try {
    // Load the external script
    // var scriptPath = "./scripts/FormatJSON.js";
    var scriptPath = "./scripts/FormatXML.js";
    var scriptContent = readFile(scriptPath);

    // Debug: Check the script content
    if (scriptContent) {
      console.log("Script content loaded successfully.");
    } else {
      console.log("Script content is empty or undefined.");
    }
    
    // Define and execute the `main` function from the cleaned script
    eval(scriptContent); // This will define `main` in the current scope

    // Now call the main function with the state object
    if (typeof main === 'function') {
      main(state); // Call the main function with the state object
    } else {
      throw new Error("The script did not define the 'main' function.");
    }

    // Return the formatted JSON
    return state.text;
  } catch (error) {
    // Return an error message if something goes wrong
    return "Error: " + error.message;
  }
}

function readFile(filePath) {
  var app = Application.currentApplication();
  app.includeStandardAdditions = true;
  
  // Run a shell command to read the file content
  try {
    var result = app.doShellScript("cat " + filePath);
    return result; // Return the content of the file
  } catch (error) {
    throw new Error("Unable to read file at: " + filePath);
  }
}