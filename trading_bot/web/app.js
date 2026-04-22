const orderForm = document.getElementById("order-form");
const orderType = document.getElementById("orderType");
const priceField = document.getElementById("price-field");
const sideInput = document.getElementById("side");
const statusNode = document.getElementById("form-status");
const submitButton = document.getElementById("submit-btn");
const responseOutput = document.getElementById("response-output");
const sideButtons = document.querySelectorAll(".segmented-btn");

function syncPriceVisibility() {
  const isLimit = orderType.value === "LIMIT";
  priceField.classList.toggle("is-hidden", !isLimit);
  document.getElementById("price").required = isLimit;
}

function setStatus(message, tone = "") {
  statusNode.textContent = message;
  statusNode.className = `form-status ${tone}`.trim();
}

sideButtons.forEach((button) => {
  button.addEventListener("click", () => {
    sideButtons.forEach((item) => item.classList.remove("active"));
    button.classList.add("active");
    sideInput.value = button.dataset.side;
  });
});

orderType.addEventListener("change", syncPriceVisibility);
syncPriceVisibility();

orderForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const formData = new FormData(orderForm);
  const payload = Object.fromEntries(formData.entries());

  submitButton.disabled = true;
  setStatus("Submitting order to the Python backend...");

  try {
    const response = await fetch("/api/order", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || "Order submission failed");
    }

    responseOutput.textContent = JSON.stringify(data, null, 2);
    setStatus("Order submitted successfully.", "success");
  } catch (error) {
    responseOutput.textContent = JSON.stringify(
      { error: error.message },
      null,
      2,
    );
    setStatus(error.message, "error");
  } finally {
    submitButton.disabled = false;
  }
});
