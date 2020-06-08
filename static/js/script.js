$(document).ready(function () {

	//Widget Code
	var bot = '<div class="chatCont" id="chatCont">' +
		'<div class="bot_profile">' +
		'<img src="/static/images/logo.png" class="bot_p_img">' +
		'<div class="close">' +
		'<i class="fa fa-times" aria-hidden="true"></i>' +
		'</div>' +
		'</div><!--bot_profile end-->' +
		'<div id="result_div" class="resultDiv"></div>' +
		'<div class="chatForm" id="chat-div">' +
		'<div class="spinner">' +
		'<div class="bounce1"></div>' +
		'<div class="bounce2"></div>' +
		'<div class="bounce3"></div>' +
		'</div>' +
		'<input type="text" id="chat-input" autocomplete="off" placeholder="Start Typing here..."' + 'class="form-control bot-txt"/>' +
		'</div>' +
		'</div><!--chatCont end-->' +

		'<div class="profile_div">' +
		'<div class="row">' +
		'<div class="col-hgt col-sm-offset-2">' +
		'<img src="/static/images/logo.png" class="img-circle img-profile">' +
		'</div><!--col-hgt end-->' +
		'<div class="col-hgt">' +
		'<div class="chat-txt">' +
		'' +
		'</div>' +
		'</div><!--col-hgt end-->' +
		'</div><!--row end-->' +
		'</div><!--profile_div end-->';

	$("mybot").html(bot);

	BotResponse = '<p class="botResult">Hi! <i class="em em-slightly_smiling_face"></i></p><div class="clearfix"></div>';
    $(BotResponse).appendTo('#result_div');

	// ------------------------------------------ Toggle chatbot -----------------------------------------------
	//function to click and open chatbot from icon
	$('.profile_div').click(function () {
		$('.profile_div').toggle();
		$('.chatCont').toggle();
		$('.bot_profile').toggle();
		$('.chatForm').toggle();
		document.getElementById('chat-input').focus();
	});
	
	//function to click and close chatbot to icon
	$('.close').click(function () {
		$('.profile_div').toggle();
		$('.chatCont').toggle();
		$('.bot_profile').toggle();
		$('.chatForm').toggle();
	});



	// on input/text enter--------------------------------------------------------------------------------------
	
	$('#chat-input').on('keyup keypress', function (e) {
		var keyCode = e.keyCode || e.which;
		var text = $("#chat-input").val();
		if (keyCode === 13) {
			if (text == "" || $.trim(text) == '') {
				e.preventDefault();
				return false;
			} else {
				$("#chat-input").blur();
				setUserResponse(text);
				send(text);
				e.preventDefault();
				return false;
			}
		}
	});


	//------------------------------------------- Call the RASA API--------------------------------------
	function send(text) {

        console.log("here")

		$.ajax({
			url: '/get_response/'+text, //  RASA API
			type: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			data: JSON.stringify({
				"sender": "user",
				"message": text
			}),
			success: function (data, textStatus, xhr) {
				console.log(data);

//				if (Object.keys(data).length !== 0) {
//					for (i = 0; i < Object.keys(data[0]).length; i++) {
//						if (Object.keys(data[0])[i] == "buttons") { //check if buttons(suggestions) are present.
//							addSuggestion(data[0]["buttons"])
//						}
//
//					}
//				}

				setBotResponse(data);

			},
			error: function (xhr, textStatus, errorThrown) {
				console.log('Error in Operation');
				setBotResponse('error');
			}
		});

	}

	//------------------------------------ Set bot response in result_div -------------------------------------
	function setBotResponse(val) {
		setTimeout(function () {

			if ($.trim(val) == '' || val == 'error') { //if there is no response from bot or there is some error
				val = 'Sorry I wasn\'t able to understand your Query. Let\' try something else!'
				var BotResponse = '<p class="botResult">' + val + '</p><div class="clearfix"></div>';
				$(BotResponse).appendTo('#result_div');
			} else {
                console.log(val);
				//if we get message from the bot succesfully
				var msg = "";
				for (var i = 0; i < val['data'].length; i++) {
					if (val['data'][i]["image"]) { //check if there are any images
						msg += '<p class="botResult"><img  width="200" height="124" src="' + val['data'][i].image + '/"></p><div class="clearfix"></div>';
					} else {
						msg += '<p class="botResult">' + val['data'][i].text + '</p><div class="clearfix"></div>';
						if (val['data'][i].text == "Didn't found your ticket, could you please create it?"){
						    temp = '<p class="botResult">First Name: <input type="text" id="firstname"><br>Last Name: <input type="text" id="lastname"><br>Email ID: <input type="text" id="emailid"><br>Description: <input type="text" id="desc"><br><br><button style="width: 100px;height:22px" id="my_button" onclick=savedetails()>Submit</button></p><div class="clearfix"></div>'
						    msg += temp

						}
					}

				}
				BotResponse = msg;
				$(BotResponse).appendTo('#result_div');
			}
			scrollToBottomOfResults();
			hideSpinner();
		}, 500);
	}


	//------------------------------------- Set user response in result_div ------------------------------------
	function setUserResponse(val) {
		var UserResponse = '<p class="userEnteredText">' + val + '</p><div class="clearfix"></div>';
		$(UserResponse).appendTo('#result_div');
		$("#chat-input").val('');
		scrollToBottomOfResults();
		showSpinner();
		$('.suggestion').remove();
	}


	//---------------------------------- Scroll to the bottom of the results div -------------------------------
	function scrollToBottomOfResults() {
		var terminalResultsDiv = document.getElementById('result_div');
		terminalResultsDiv.scrollTop = terminalResultsDiv.scrollHeight;
	}


	//---------------------------------------- Spinner ---------------------------------------------------
	function showSpinner() {
		$('.spinner').show();
	}

	function hideSpinner() {
		$('.spinner').hide();
	}




	//------------------------------------------- Buttons(suggestions)--------------------------------------------------
	function addSuggestion(textToAdd) {
		setTimeout(function () {
			var suggestions = textToAdd;
			var suggLength = textToAdd.length;
			$('<p class="suggestion"></p>').appendTo('#result_div');
			// Loop through suggestions
			for (i = 0; i < suggLength; i++) {
				$('<span class="sugg-options">' + suggestions[i].title + '</span>').appendTo('.suggestion');
			}
			scrollToBottomOfResults();
		}, 1000);
	}


	// on click of suggestions get value and send to API.AI
	$(document).on("click", ".suggestion span", function () {
		var text = this.innerText;
		setUserResponse(text);
		send(text);
		$('.suggestion').remove();
	});
	// Suggestions end -----------------------------------------------------------------------------------------



});

function savedetails(){

    firstname = document.getElementById("firstname")['value']
    lastname = document.getElementById("lastname")['value']
    emailid = document.getElementById("emailid")['value']
    desc = document.getElementById("desc")['value']


    console.log(firstname)
    console.log(lastname)

    $.ajax({
			url: '/save_details', //  RASA API
			type: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			data: JSON.stringify({
				"firstName": firstname,
				"lastName": lastname,
				"emailID": emailid,
				"description": desc,
			}),
			success: function (data, textStatus, xhr) {
				console.log(data);
				BotResponse = '<p class="botResult">Thanks for submitting. Your details have been saved successfully.</p><div class="clearfix"></div>';
                $(BotResponse).appendTo('#result_div');
			},
			error: function (xhr, textStatus, errorThrown) {
				BotResponse = '<p class="botResult">Thanks for submitting. Your details were not saved successfully.</p><div class="clearfix"></div>';
                $(BotResponse).appendTo('#result_div');
			}
		});

}
