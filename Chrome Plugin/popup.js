window.onload = function() {
  var link = document.querySelector("a");
  link.onclick = function() {
    chrome.tabs.create({ url: "https://email-generator-neevan.streamlit.app/" });
  };
};
