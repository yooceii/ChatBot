var $messages = $('.messages-content'),
  d, h, m ,key;

var avatar = "https://vignette.wikia.nocookie.net/leonhartimvu/images/d/d7/JARVIS_Logo.png/revision/latest?cb=20131024021443&format=original";
apigClientFactory.newClient().chatbotGet({},{},{}).then(function(data){
  key=data.data.key;
});


$(window).load(function () {
  $messages.mCustomScrollbar();
  // setTimeout(function () {
  // }, 100);
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
    "messages": [
      {
        "type": "string",
        "unstructured": {
          "id": 10000*Math.random().toString(),
          "text": $('.message-input').val(),
          "timestamp": Date.now()
        }
      }
    ]
  }
  var apigClient = apigClientFactory.newClient({
    apiKey: key
  });
  apigClient.chatbotPost({}, body, { "headers": { "Content-Type": "application/json" } }).then(function (result) {
    insertMessage(result.data.messages[0].unstructured.text);
  }).catch(function (error) {
    alert(error);
  });
}