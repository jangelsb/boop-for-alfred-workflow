// Requried variables
// `input`
// `input_script_path`

ObjC.import('stdlib')

// JXA eval() only sees file-level variables, not locals inside run()
var boopRequire
var boopState

function run (argv) {
  var query = $.getenv('input')

  boopState = {
    text: query,
    fullText: query,
    selection: query,
    postError: function (message) {
      throw new Error(message)
    },
    postInfo: function (message) {
      this.text += '\n' + message
    }
  }

  try {
    boopRequire = createRequire()

    var scriptPath = $.getenv('input_script_path')
    var scriptContent = readFile(scriptPath)

    if (!scriptContent) {
      throw new Error('Script content is empty or undefined.')
    }

    var wrappedScript = `
      (function(require, state) {
        ${scriptContent}
        if (typeof main !== 'function') {
          throw new Error("The script did not define a 'main' function.");
        }
        this.main = main;
      })(boopRequire, boopState);
    `

    eval(wrappedScript)

    if (typeof main === 'function') {
      main(boopState)
    } else {
      throw new Error("The script did not define the 'main' function.")
    }

    return boopState.fullText !== query ? boopState.fullText : boopState.text
  } catch (error) {
    return 'Error: ' + error.message
  }
}

function createRequire () {
  return function (modulePath) {
    if (modulePath.startsWith('@boop/')) {
      modulePath = './scripts/lib/' + modulePath.substring(6) + '.js'
    } else if (!modulePath.endsWith('.js')) {
      modulePath += '.js'
    }

    var scriptContent = readFile(modulePath)

    if (!scriptContent) {
      throw new Error('Module not found: ' + modulePath)
    }

    var module = { exports: {} }

    var wrappedCode = `
      (function (exports, module, require) {
        ${scriptContent}
      })(module.exports, module, boopRequire);
    `

    eval(wrappedCode)

    return module.exports
  }
}

function readFile (filePath) {
  var app = Application.currentApplication()
  app.includeStandardAdditions = true

  try {
    return app.doShellScript('cat ' + filePath)
  } catch (error) {
    throw new Error('Unable to read file at: ' + filePath)
  }
}
