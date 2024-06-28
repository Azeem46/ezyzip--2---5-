document.addEventListener("DOMContentLoaded", () => {
  const searchInput = document.getElementById("search");
  const suggestionsContainer = document.getElementById("suggestions");

  let data = [];

  fetch("complete.json")
    .then((response) => response.json())
    .then((json) => {
      data = json.map((item) => item.trading_symbol);
    })
    .catch((error) => console.error("Error fetching data:", error));

  searchInput.addEventListener("input", () => {
    const query = searchInput.value.toLowerCase();
    if (query.length > 0) {
      const filteredData = data.filter((symbol) =>
        symbol.toLowerCase().includes(query)
      );
      displaySuggestions(filteredData);
    } else {
      clearSuggestions();
    }
  });

  function displaySuggestions(suggestions) {
    suggestionsContainer.innerHTML = "";
    suggestions.forEach((suggestion) => {
      const suggestionElement = document.createElement("div");
      suggestionElement.classList.add("autocomplete-suggestion");
      suggestionElement.textContent = suggestion;
      suggestionElement.addEventListener("click", () => {
        searchInput.value = suggestion;
        clearSuggestions();
      });
      suggestionsContainer.appendChild(suggestionElement);
    });
  }

  // Clear suggestions
  function clearSuggestions() {
    suggestionsContainer.innerHTML = "";
  }
});
