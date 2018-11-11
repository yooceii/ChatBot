var auth;
$(window).load(function(){
    console.log("aaaa");
    login();
});

function initAWSCognito() {
    var authData = {
      ClientId: '78c3fruuhnkbkmeuk8ah0a30mj', // Your client id here
      AppWebDomain: 'chatbot-cs9223.auth.us-east-1.amazoncognito.com',
      TokenScopesArray: ['email', 'openid', 'aws.cognito.signin.user.admin'], // e.g.['phone', 'email', 'profile','openid', 'aws.cognito.signin.user.admin'],
      RedirectUriSignIn: 'https://d4i96u6a4cz9k.cloudfront.net/Chat.html',
      RedirectUriSignOut: 'https://www.google.com',
      IdentityProvider: 'Cognito User Pools', // e.g. 'Facebook',
      // UserPoolId: 'us-east-1_pvmcyMFpG', // Your user pool id here
    };
    auth = new AmazonCognitoIdentity.CognitoAuth(authData);
    // auth.setState({isLoading: true});
    // auth.useCodeGrantFlow();
    auth.userhandler = {
      onSuccess: function (result) {
        alert("Sign in success");
        console.log(result);
        // showSignedIn(result);
        console.log(result.getAccessToken().getJwtToken());
        AWS.config.region = 'us-east-1'; // Region
        AWS.config.credentials = new AWS.CognitoIdentityCredentials({
          IdentityPoolId: 'us-east-1:6b7685cb-c911-4d86-9a54-4070dec6aa9b',
          Logins: {
            'cognito-idp.us-east-1.amazonaws.com/us-east-1_pvmcyMFpG': result.getIdToken().getJwtToken()
          }
        });
        AWS.config.credentials.clearCachedId();
        AWS.config.credentials.get(function () {
  
          // Credentials will be available when this function is called.
          var accessKeyId = config.credentials.accessKeyId;
          var secretAccessKey = config.credentials.secretAccessKey;
          var sessionToken = config.credentials.sessionToken;
  
        });
        // auth.setState({isLoading: false});
      },
      onFailure: function (err) {
        alert("Error!");
      }
    };
  }

  function login() {

    initAWSCognito();
    // window.location.assign('https://' + authData.AppWebDomain + '/login?redirect_uri=' + authData.RedirectUriSignIn + '&response_type=' + 'code' + '&client_id=' + authData.ClientId);
    auth.getSession();
    // auth.setState({isLoading: false});
  }
  