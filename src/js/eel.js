export const eel = window["eel"];

eel.expose(hello_from_js);
function hello_from_js() {
  console.log(eel.hello_from_py());
}
