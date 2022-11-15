"use strict";
const { convert } = require("html-to-text");
// var GMAIL_TAGGER = GMAIL_TAGGER || {};
// loader-code: wait until gmailjs has finished loading, before triggering actual extensiode-code.
const loaderId = setInterval(() => {
  if (!window._gmailjs) {
    return;
  }

  clearInterval(loaderId);
  startExtension(window._gmailjs);
}, 100);

const selectorConstant = {
  mailListTrNew: "zA zE",
  mailListTrHasBeenRead: "zA yO",

  mailerTd: ".yX.xY",

  mailTitleTd: "xY a4W",

  gmailPrimaryTab: 'div[aria-label="Primary"]',
  tabSelectedAttr: "aria-selected",

  mailTitle: "nH V8djrc byY",
  mailHead: "y6",
};

const htmlTpl = {
  handle: '<div class="tag">Text to be replaced</div>',
};

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

function startExtension(gmail) {
  console.log("Hi loading");
  window.gmail = gmail;

  gmail.observe.on("load", () => {
    const userEmail = gmail.get.user_email();
    console.log("Hello, " + userEmail + ". This is your extension talking!");
    init(gmail);
  });

  gmail.observe.on("view_email", (domEmail) => {
    console.log("Looking at email:", domEmail);
    const emailData = gmail.new.get.email_data(domEmail);
    console.log("Email data:", emailData);
    const html = domEmail.body();
    const text = convert(html, {
      wordwrap: 130,
    });
    console.log("Email Subject", emailData["subject"]);
    console.log("Email data:", text);

    var titleTd = selectorConstant.mailTitle;
    var mailTitleTd = document.getElementsByClassName(titleTd);

    console.log("mailtitle", mailTitleTd);
    var htmlNew = htmlTpl.handle
      .replace("Text to be replaced", generateTag(text)[0])
      .replace("tag", "tag" + generateTag(text)[1]);

    console.log(htmlNew);
    mailTitleTd[0].innerHTML += htmlNew;
  });

  // init();
}

function init(gmail) {
  console.log("hi1");
  var emailIDs = [];
  var textData = [];
  const heads = document.getElementsByClassName(selectorConstant.mailHead);
  for (var head of heads) {
    emailIDs.push(
      head.children[0].children[0].getAttribute("data-legacy-thread-id")
    );
  }
  for (var ID of emailIDs) {
    const emailData = gmail.new.get.email_data(ID);
    const html = emailData["content_html"];
    const text = convert(html, {
      wordwrap: 130,
    });
    console.log("Email Subject", emailData["subject"]);
    console.log("Email data:", text);
    textData.push(text);
  }
}
