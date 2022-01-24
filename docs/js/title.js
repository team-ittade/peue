document$.subscribe(function () {
  title = document.getElementsByTagName("h1")[0];
  document.title = title.innerText.slice(0, -2);
});
