// Select display
let display = document.getElementById("display");

// Append number/operator to display
function appendValue(value) {
  display.value += value;
}

// Clear the display
function clearDisplay() {
  display.value = "";
}

// Calculate and show result
function calculateResult() {
  try {
    display.value = eval(display.value);
  } catch {
    display.value = "Error";
  }
}
