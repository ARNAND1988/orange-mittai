import { reactive } from "vue"

export const toast = reactive({
  show: false,
  message: "",
  type: "success",
})

export const showGlobalToast = (message, type = "success") => {
  window.dispatchEvent(
    new CustomEvent("global-toast", {
      detail: { message, type },
    })
  );
};