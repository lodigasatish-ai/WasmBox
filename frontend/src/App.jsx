import Editor from "@monaco-editor/react";

function App() {
  return (
    <div>
      <h1>WasmBox</h1>

      <Editor
        height="500px"
        defaultLanguage="python"
        defaultValue={`print("Hello from WasmBox!")`}
        theme="vs-dark"
      />
    </div>
  );
}

export default App;