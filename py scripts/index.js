const fs = require('fs').promises;
const path = require('path');
const process = require('process');
const { authenticate } = require('@google-cloud/local-auth');
const { google } = require('googleapis');

// If modifying these scopes, delete token.json.
const SCOPES = ['https://www.googleapis.com/auth/gmail.modify'];
// The file token.json stores the user's access and refresh tokens, and is
// created automatically when the authorization flow completes for the first
// time.
const TOKEN_PATH = path.join(process.cwd(), 'token.json');
const CREDENTIALS_PATH = path.join(process.cwd(), 'credentials.json');

/**
 * Reads previously authorized credentials from the save file.
 *
 * @return {Promise<OAuth2Client|null>}
 */
async function loadSavedCredentialsIfExist() {
  try {
    const content = await fs.readFile(TOKEN_PATH);
    const credentials = JSON.parse(content);
    return google.auth.fromJSON(credentials);
  } catch (err) {
    return null;
  }
}

/**
 * Serializes credentials to a file comptible with GoogleAUth.fromJSON.
 *
 * @param {OAuth2Client} client
 * @return {Promise<void>}
 */
async function saveCredentials(client) {
  const content = await fs.readFile(CREDENTIALS_PATH);
  const keys = JSON.parse(content);
  const key = keys.installed || keys.web;
  const payload = JSON.stringify({
    type: 'authorized_user',
    client_id: key.client_id,
    client_secret: key.client_secret,
    refresh_token: client.credentials.refresh_token,
  });
  //const OAuth2Client = new google.auth.OAuth2(client_id, client_secret, redirect_uris[0]);
  await fs.writeFile(TOKEN_PATH, payload);
}

/**
 * Load or request or authorization to call APIs.
 *
 */
async function authorize() {
  let client = await loadSavedCredentialsIfExist();

  if (client) {
    return client;
  }
  client = await authenticate({
    scopes: SCOPES,
    keyfilePath: CREDENTIALS_PATH,
  });
  if (client.credentials) {
    await saveCredentials(client);
  }
  return client;
}

/**
 * Lists the labels in the user's account.
 *
 * @param {google.auth.OAuth2} auth An authorized OAuth2 client.
 */
// async function listLabels(auth) {
//   const gmail = google.gmail({ version: 'v1', auth });
//   const res = await gmail.users.labels.list({
//     userId: 'me',
//   });
//   const labels = res.data.labels;
//   if (!labels || labels.length === 0) {
//     console.log('No labels found.');
//     return;
//   }
//   console.log('Labels:');
//   labels.forEach((label) => {
//     console.log(`- ${label.name} : ${label.id}`);
//   });
// }
async function listLabels(auth) {
  const gmail = google.gmail({ version: 'v1', auth });
  const ids = await gmail.users.messages.list({
    userId: 'me'
  });
  const labels = ids.data.messages;
  if (!labels || labels.length === 0) {
    console.log('No labels found.');
    return;
  }
  const idls = []
  var count = 0;
  console.log('Labels:');
  const fs1 = require('fs');
  fs1.appendFile('data.txt', "", (err) => {
    // In case of a error throw err.
    if (err) throw err;
  })
  const forEachLoop = _ => {
    labels.forEach(async label => {
      console.log(label);
      idls.push(label.id)
      const res = await gmail.users.messages.get({
        userId: 'me',
        id: label.id
      });
      var data = res.data.payload;
      while (data.parts != undefined) {
        data = data.parts[0];
      };
      const plaintext = Buffer.from(data.body.data, 'base64').toString() + "\n***************************************************************\n";
      console.log(plaintext);
      //const separator = "\n***************************************************************\n";
      //console.log(seperator); 
      fs1.appendFile('data.txt', plaintext, (err) => {
        // In case of a error throw err.
        if (err) throw err;
      })
      //fs1.appendFile('data.txt', "\n***************************************************************\n");
    });
  };
  forEachLoop();
  // const forEachLoop = _ => {
  //   idls.forEach(async idl => {
  //     const res = await gmail.users.messages.get({
  //       userId: 'me',
  //       id: idl
  //     });
  //     console.log(Buffer.from(res.data.payload.parts[0].body.data, 'base64').toString());
  //   });
  // };
  // forEachLoop;

}
// const res = await gmail.users.messages.get({
//   userId: 'me',
//   id: idls[0],
//   // {
//   //   userId: 'me',
//   //   q: 'label:inbox subject:reminder',
//   // }, (err, res) => {
//   //   if (err) {
//   //     reject(err);
//   //     return;
//   //   }
//   //   if (!res.data.messages) {
//   //     resolve([]);
//   //     return;
//   //   } resolve(res.data.messages);
//   // }
// });
// console.log(Buffer.from(res.data.payload.parts[0].body.data, 'base64').toString());

// async function listMessages(auth) {
//   return new Promise((resolve, reject) => {
//     const gmail = google.gmail({ version: 'v1', auth });
//     gmail.users.messages.list({
//       userId: 'me'
//       // {
//       //   userId: 'me',
//       //   q: 'label:inbox subject:reminder',
//       // }, (err, res) => {
//       //   if (err) {
//       //     reject(err);
//       //     return;
//       //   }
//       //   if (!res.data.messages) {
//       //     resolve([]);
//       //     return;
//       //   } resolve(res.data.messages);
//       // }
//     });
//   })
//     ;
// }
//authorize().then(listLabels).catch(console.error);

authorize().then(listLabels).catch(console.error);
// const messages = listMessages(oAuth2Client, );
// const fst = require('fs')

// // Write data in 'Output.txt' .
// fst.writeFile('Output.txt', messages, (err) => {

//   // In case of a error throw err.
//   if (err) throw err;
// })
// const fs = require('fs').promises;
// const path = require('path');
// const process = require('process');
// const { authenticate } = require('@google-cloud/local-auth');
// const { google } = require('googleapis');

// // If modifying these scopes, delete token.json.
// const SCOPES = ['https://www.googleapis.com/auth/gmail.readonly'];
// // The file token.json stores the user's access and refresh tokens, and is
// // created automatically when the authorization flow completes for the first
// // time.
// const TOKEN_PATH = path.join(process.cwd(), 'token.json');
// const CREDENTIALS_PATH = path.join(process.cwd(), 'credentials.json');

// /**
//  * Reads previously authorized credentials from the save file.
//  *
//  * @return {Promise<OAuth2Client|null>}
//  */
// async function loadSavedCredentialsIfExist() {
//   try {
//     const content = await fs.readFile(TOKEN_PATH);
//     const credentials = JSON.parse(content);
//     return google.auth.fromJSON(credentials);
//   } catch (err) {
//     return null;
//   }
// }

// /**
//  * Serializes credentials to a file comptible with GoogleAUth.fromJSON.
//  *
//  * @param {OAuth2Client} client
//  * @return {Promise<void>}
//  */
// async function saveCredentials(client) {
//   const content = await fs.readFile(CREDENTIALS_PATH);
//   const keys = JSON.parse(content);
//   const key = keys.installed || keys.web;
//   const payload = JSON.stringify({
//     type: 'authorized_user',
//     client_id: key.client_id,
//     client_secret: key.client_secret,
//     refresh_token: client.credentials.refresh_token,
//   });
//   await fs.writeFile(TOKEN_PATH, payload);
// }

// /**
//  * Load or request or authorization to call APIs.
//  *
//  */
// async function authorize() {
//   let client = await loadSavedCredentialsIfExist();
//   if (client) {
//     return client;
//   }
//   client = await authenticate({
//     scopes: SCOPES,
//     keyfilePath: CREDENTIALS_PATH,
//   });
//   if (client.credentials) {
//     await saveCredentials(client);
//   }
//   return client;
// }

// /**
//  * Lists the labels in the user's account.
//  *
//  * @param {google.auth.OAuth2} auth An authorized OAuth2 client.
//  */
// async function listLabels(auth) {
//   const gmail = google.gmail({ version: 'v1', auth });
//   const res = await gmail.users.labels.list({
//     userId: 'me',
//   });
//   const labels = res.data.labels;
//   if (!labels || labels.length === 0) {
//     console.log('No labels found.');
//     return;
//   }
//   console.log('Labels:');
//   labels.forEach((label) => {
//     console.log(`- ${label.name}`);
//   });
// }

// authorize().then(listLabels).catch(console.error);