import Vue from "vue";


const keyEvent = new Vue();

window.addEventListener("keydown", event => {
  if (event.isTrusted) {
    if (event.key.match(/[0-9]/))
      keyEvent.$emit("digit", event.key * 1);
    else if (event.code === "Space")
      keyEvent.$emit("space");
  }
});

export { keyEvent };
