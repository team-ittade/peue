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

const ENABLE_BY_DEFAULT = true;

document$.subscribe(function () {
  var text = document.getElementsByTagName("article")[0].textContent;
  const result = readingTime(text);
  const node = `<p><small>Estimated reading time: ${result.readingTime} minutes (${result.wordCount} words)</small></p>`;
  title = document.querySelector("h1");
  const defValue = ENABLE_BY_DEFAULT && !title.classList.contains("NO-ERT");
  if (defValue || title.classList.contains("ERT")) {
    title.insertAdjacentHTML("afterend", node);
    console.log("Adding ERT");
  } else {
    console.log("Skipping ERT");
  }
});
