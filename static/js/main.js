var $messages = $('.messages-content'),
  d, h, m, key, auth;

var avatar = "https://vignette.wikia.nocookie.net/leonhartimvu/images/d/d7/JARVIS_Logo.png/revision/latest?cb=20131024021443&format=original";

AWS.config;
var accessKeyId;
var secretAccessKey;
var sessionToken;

$(window).load(function () {
  AWS.config.region = 'us-east-1'; // Region
  AWS.config.credentials = new AWS.CognitoIdentityCredentials({
    IdentityPoolId: 'us-east-1:6b7685cb-c911-4d86-9a54-4070dec6aa9b',
    Logins: {
      'cognito-idp.us-east-1.amazonaws.com/us-east-1_pvmcyMFpG': window.location.hash.match(/\#(?:id_token)\=([\S\s]*?)\&/)[1]
    }
  });
  AWS.config.credentials.clearCachedId();
  AWS.config.credentials.get(function (err) {
    console.log(AWS.config.credentials);
    if (err) {
      alert(err);
    }
    // Credentials will be available when this function is called.
    accessKeyId = AWS.config.credentials.accessKeyId;
    secretAccessKey = AWS.config.credentials.secretAccessKey;
    ssessionToken = AWS.config.credentials.sessionToken;

  });
  $messages.mCustomScrollbar();
});

function updateScrollbar() {
  $messages.mCustomScrollbar("update").mCustomScrollbar('scrollTo', 'bottom', {
    scrollInertia: 10,
    timeout: 0
  });
}

function setDate() {
  d = new Date()
  m = d.getMinutes();
  $('<div class="timestamp">' + d.getHours() + ':' + m + '</div>').appendTo($('.message:last'));
}

function insertMessage(text) {
  msg = $('.message-input').val();
  if ($.trim(msg) == '') {
    return false;
  }
  $('<div class="message message-personal">' + msg + '</div>').appendTo($('.mCSB_container')).addClass('new');
  setDate();
  $('.message-input').val(null);
  updateScrollbar();
  setTimeout(function () {
    Message(text);
  }, 100 + (Math.random() * 20) * 100);
}

$('.message-submit').click(function () {
  awsPost();
});

$(window).on('keydown', function (e) {
  if (e.which == 13) {
    awsPost();
    return false;
  }
})


function Message(msg) {
  if ($('.message-input').val() != '') {
    return false;
  }
  $('<div class="message loading new"><figure class="avatar"><img src="' + avatar + '" /></figure><span></span></div>').appendTo($('.mCSB_container'));
  updateScrollbar();

  setTimeout(function () {
    $('.message.loading').remove();
    $('<div class="message new"><figure class="avatar"><img src="' + avatar + '" /></figure>' + msg + '</div>').appendTo($('.mCSB_container')).addClass('new');
    setDate();
    updateScrollbar();
  }, 100 + (Math.random() * 20) * 100);

}

function awsPost() {
  var body = {
    "messages": [{
      "type": "string",
      "unstructured": {
        "id": accessKeyId,
        "text": $('.message-input').val(),
        "timestamp": Date.now()
      }
    }]
  }
  var apigClient = apigClientFactory.newClient({
    accessKey: AWS.config.credentials.accessKeyId,
    secretKey: AWS.config.credentials.secretAccessKey,
    sessionToken: AWS.config.credentials.sessionToken,
  });
  apigClient.chatbotPost({}, body, {
    "headers": {
      "Content-Type": "application/json"
    }
  }).then(function (result) {
    insertMessage(result.data.messages[0].unstructured.text);
  }).catch(function (error) {
    console.log(error);
  });
}