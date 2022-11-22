const scores = require("./scoreDict");

function generateTag(text) {
  const minThreshold = 100;
  const allwords = text.match(/\b(\w+)\b/g);
  var words = [];
  for (var i in allwords) {
    let val = allwords[i];
    val.replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g, "");
    val = val.toLowerCase();
    if (!words.includes(val)) {
      words.push(val);
    }
  }

  //   const words = [...new Set(allwords)];

  var wordScores = [];
  for (var i in words) {
    let val = words[i];
    // val.replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g, "");
    // val = val.toLowerCase();
    if (val in scores && !wordScores.includes(scores[val])) {
      wordScores.push(scores[val]);
    }
  }
  wordScores.sort(function (a, b) {
    return a - b;
  });
  wordScores.reverse();

  console.log(wordScores);
  const topWordScores = wordScores.slice(0, 2);
  console.log(topWordScores);

  var tags = [];
  for (var i in words) {
    let val = words[i];
    // val.replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g, "");
    // val = val.toLowerCase();
    if (
      val in scores &&
      scores[val] > minThreshold &&
      topWordScores.includes(scores[val])
    ) {
      tags.push(val);
    }
  }
  return tags;
}

module.exports = new export_file();
function export_file() {
  return {
    generateTag: generateTag,
  };
}
