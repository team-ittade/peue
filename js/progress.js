function arrToUl(root, arr) {
  var ul = document.createElement("ul");
  var li;

  root.appendChild(ul); // append the created ul to the root

  arr.forEach(function (item) {
    if (Array.isArray(item)) {
      // if it's an array
      arrToUl(li, item); // call arrToUl with the li as the root
      return;
    }

    li = document.createElement("li"); // create a new list item
    li.innerHTML = item;
    // li.appendChild(document.createTextNode(item)); // append the text to the li
    ul.appendChild(li); // append the list item to the ul
  });
}

rocket =
  '<img alt="🚀" class="twemoji" src="https://twemoji.maxcdn.com/v/latest/svg/1f680.svg" title=":rocket:"></img>';
factory =
  '<img alt="🏭" class="twemoji" src="https://twemoji.maxcdn.com/v/latest/svg/1f3ed.svg" title=":factory:">';

if (window.location.pathname === "/") {
  document$.subscribe(function () {
    console.log("Setting progress");

    fetch("/data/progress.json")
      .then((response) => response.json())
      .then((data) => {
        progress = [];
        totalPages = 0;
        totalDone = 0;
        for (i in data) {
          totalPages += data[i].total;
          totalDone += data[i].done;
          if (data[i].total == data[i].done) {
            prog = `${rocket} terminado`;
          } else {
            prog = `${factory} <code>${Math.round(
              (data[i].done * 100) / data[i].total
            )}%</code> (<code>${data[i].done}</code>/<code>${
              data[i].total
            })</code>`;
          }
          progress.push(`<b>Tema ${i}</b>: ${prog}`);
        }

        div = document.getElementById("progressList");
        arrToUl(div, progress);

        totalDiv = document.getElementById("totalProgress");
        totalDiv.innerHTML = `<b>Progreso total</b>: <code>${Math.round(
          (totalDone * 100) / totalPages
        )}%</code> (<code>${totalDone}</code>/<code>${totalPages})</code>`;
      });
  });
}
