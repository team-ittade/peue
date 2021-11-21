function readingTime(post) {
  const WORDS_PER_MINUTE = 200;
  let result = {};
  //Matches words
  //See
  //https://regex101.com/r/q2Kqjg/6
  const regex = /\w+/g;
  result.wordCount = (post || "").match(regex).length;

  result.readingTime = Math.ceil(result.wordCount / WORDS_PER_MINUTE);
  return result;
}

document$.subscribe(function () {
  var text = document.body.textContent;
  const result = readingTime(text);
  const node = `<p><small>Estimated reading time: ${result.readingTime} minutes (${result.wordCount} words)</small></p>`;
  title = document.querySelector("h1");
  if (title.classList.contains("ERT")) {
    title.insertAdjacentHTML("afterend", node);
    console.log("Adding ERT");
  } else {
    console.log("Skipping ERT");
  }
});
