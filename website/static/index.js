function delete_event(itemID) {
  fetch("/delete-event", {
    method: "POST",
    body: JSON.stringify({ itemID: itemID }),
  }).then((_res) => {
    window.location.href = "/test";
  });
}

function delete_bl(itemID) {
  fetch("/delete-bl", {
    method: "POST",
    body: JSON.stringify({ itemID: itemID }),
  }).then((_res) => {
    window.location.href = "/test";
  });
}

function delete_year(itemID) {
  fetch("/delete-year", {
    method: "POST",
    body: JSON.stringify({ itemID: itemID }),
  }).then((_res) => {
    window.location.href = "/test";
  });
}
