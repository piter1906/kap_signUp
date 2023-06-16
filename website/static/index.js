function delete_item(itemID, path_route, path_refresh) {
  fetch(path_route, {
    method: "POST",
    body: JSON.stringify({ itemID: itemID }),
  }).then((_res) => {
    window.location.href = path_refresh;
  });
}

function get_event(event_name, path_route) {
  fetch(path_route, {
    let number = document.getElementById("number").value; 
    method: "POST",
    body: JSON.stringify({ event_name: event_name,
                            number: number }),
  }).then((_res) => {
    window.location.href = '/form';
  });
}


