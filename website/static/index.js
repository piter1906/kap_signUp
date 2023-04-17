function delete_item(itemID, path_route, path_refresh) {
  fetch(path_route, {
    method: "POST",
    body: JSON.stringify({ itemID: itemID }),
  }).then((_res) => {
    window.location.href = path_refresh;
  });
}



