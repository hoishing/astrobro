import { Streamlit } from "streamlit-component-lib";

async function onRender(event) {
  // Wait 500ms before getting screen width to ensure window is fully loaded
  await new Promise((resolve) => setTimeout(resolve, 300));
  // Get the current screen width
  const screenWidth = window.innerWidth;
  document.getElementById("screen-width").innerText = screenWidth;
  // Send the screen width back to Streamlit
  Streamlit.setComponentValue(screenWidth);
  Streamlit.setFrameHeight(0);
}

// Attach our `onRender` handler to Streamlit's render event.
Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender);

// Tell Streamlit we're ready to start receiving data. We won't get our
// first RENDER_EVENT until we call this function.
Streamlit.setComponentReady();
console.log("component ready");
Streamlit.setFrameHeight(0);
