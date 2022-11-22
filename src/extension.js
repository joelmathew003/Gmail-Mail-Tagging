"use strict";
const { convert } = require("html-to-text");
const gen1 = require("./generateTag1");
const gen2 = require("./generateTag2");
const { front } = require("./scoreDict");

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

function startExtension(gmail) {
  console.log("Hi loading");
  window.gmail = gmail;

  gmail.observe.on("load", () => {
    const userEmail = gmail.get.user_email();
    console.log("Hello, " + userEmail + ". This is your extension talking!");
  });

  gmail.observe.on("view_email", (domEmail) => {
    // console.log(scores);

    // console.log("Looking at email:", domEmail);
    const emailData = gmail.new.get.email_data(domEmail);
    // console.log("Email data:", emailData);
    const html = domEmail.body();
    const text = convert(html, {
      wordwrap: 130,
    });
    console.log("Email Subject", emailData["subject"]);
    // console.log("Email data:", text);

    var titleTd = selectorConstant.mailTitle;
    var mailTitleTd = document.getElementsByClassName(titleTd);

    console.log("mailtitle", mailTitleTd);
    // var htmlNew = htmlTpl.handle
    //   .replace("Text to be replaced", gen1.generateTag(text)[0])
    //   .replace("tag", "tag" + gen1.generateTag(text)[1]);
    var tags = gen2.generateTag(text);
    console.log(tags);
    for (var i in tags) {
      var tag = tags[i];
      var k = parseInt(i, 10) + 1;
      var htmlNew = htmlTpl.handle
        .replace("Text to be replaced", tag)
        .replace("tag", "tag" + k);

      console.log(htmlNew);
      mailTitleTd[0].innerHTML += htmlNew;
    }
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
