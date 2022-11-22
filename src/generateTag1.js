function generateTag(text) {
  // text = text.translate(str.maketrans("", "", string.punctuation));
  const CDCrelated = [
    "internship",
    "cdc",
    "job profile",
    "recruitment",
    "placement",
    "offer",
    "apply",
    "application",
    "applications",
  ];
  const Fellowship = [
    "fellowship",
    "fellowships",
    "scholarship",
    "scholarships",
    "higher studies",
    "higher education",
    "sponsor",
    "registration",
    "application",
    "applications",
  ];
  const Talks = [
    "talk",
    "invite",
    "invited",
    "venue",
    "location",
    "research",
    "abstract",
    "speaker",
    "link",
  ];

  var topicArray = [0, 0, 0];
  const minThreshold = 2;
  const words = text.match(/\b(\w+)\b/g);

  for (var i in words) {
    let val = words[i];
    val.replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g, "");
    val = val.toLowerCase();
    // console.log(val);
    if (CDCrelated.includes(val)) {
      topicArray[0]++;
    }
    if (Fellowship.includes(val)) {
      topicArray[1]++;
    }
    if (Talks.includes(val)) {
      topicArray[2]++;
    }
  }
  const mx = Math.max(...topicArray);
  console.log(topicArray);
  if (mx < minThreshold) {
    return ["General Category", 1];
  } else if (mx === topicArray[0]) {
    return ["CDC Stuff", 2];
  } else if (mx === topicArray[1]) {
    return ["Fellowship", 3];
  } else {
    return ["Informative Talks", 4];
  }
}

module.exports = new export_file();
function export_file() {
  return {
    generateTag: generateTag,
  };
}
