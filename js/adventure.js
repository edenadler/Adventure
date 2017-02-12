var Adventures = {};
//currentAdventure is used for the adventure we're currently on (id). This should be determined at the beginning of the program
Adventures.currentAdventure = 1; //todo keep track from db
//>>>>>>> eca66f829150c3676dd09324e4781f88db57d05b
//currentStep is used for the step we're currently on (id). This should be determined at every crossroad, depending on what the user chose
Adventures.currentStep = 0;//todo keep track from db
Adventures.currentUser = "";//todo keep track from db
Adventures.currentScore = 90;
Adventures.adv1 = [1,2,3,4,5,6,7]
Adventures.adv2 = [8,9,10,11,12,13,14]


//TODO: remove for production
Adventures.debugMode = true;
Adventures.DEFAULT_IMG = "./images/decision.jpg";


//Handle Ajax Error, animation error and speech support
Adventures.bindErrorHandlers = function () {
    //Handle ajax error, if the server is not found or experienced an error
    $(document).ajaxError(function (event, jqxhr, settings, thrownError) {
        Adventures.handleServerError(thrownError);
    });

    //Making sure that we don't receive an animation that does not exist
    $("#situation-image").error(function () {
        Adventures.debugPrint("Failed to load img: " + $("#situation-image").attr("src"));
        Adventures.setImage(Adventures.DEFAULT_IMG);
    });
};

Adventures.updateScore = function(){
    if (Adventures.currentScore > 0){
    $("#progress-bar").attr("aria-valuenow",Adventures.currentScore);
    $("#progress-values").text(Adventures.currentScore + "% Complete (danger)");
    $("#progress-bar").text(Adventures.currentScore +"%");
    $("#progress-bar").css("width",Adventures.currentScore +"%");
    }
}

Adventures.determineNextStep = function(){
    if(Adventures.currentAdventure == 1){
        nextStep = Adventures.adv1.pop(random.randrange(len(x)))
        return nextStep
    }
    else if(Adventures.currentAdventure == 2){
        nextStep = Adventures.adv2.pop(random.randrange(len(x)))
        return nextStep
     }

    else{
        x = [15,16,17,18,19,20,21]
        nextStep = x.pop(random.randrange(len(x)))
        return nextStep
     }
};

//The core function of the app, sends the user's choice and then parses the results to the server and handling the response
Adventures.chooseOption = function(){
    Adventures.currentScore += parseInt($(this).val());
    Adventures.updateScore();
    Adventures.currentStep +=1;
    $.ajax("/story",{
        type: "POST",
        data: {"user": Adventures.currentUser,
            "adventure": Adventures.currentAdventure,
            "currentScore": Adventures.currentScore,
            "nextStep": Adventures.currentStep
            },
        dataType: "json",
        contentType: "application/json",
        success: function (data) {
            Adventures.write(data);
            Adventures.checkScore(Adventures.currentScore)
            Adventures.currentStep = data["current"];
            console.log(data);
            console.log(Adventures.currentScore);
            $(".greeting-text").hide();
        }
    });
};

Adventures.write = function (message) {
    //Writing new choices and image to screen
    $(".situation-text").text(message["text"]).show();
    for(var i=0;i<message['options'].length;i++){
        var opt = $("#option_" + (i+1));
        opt.text(message['options'][i]['question_options']);
        opt.val(message['options'][i]['score']);
    }
    Adventures.setImage(message["image"]);
};


Adventures.start = function(){
    $(document).ready(function () {
        $(".game-option").click(Adventures.chooseOption);
        $("#nameField").keyup(Adventures.checkName);
        $(".adventure-button").click(Adventures.initAdventure);
        $(".adventure").hide();
        $(".welcome-screen").show();
        $(".lives").hide();
    });
};

//Setting the relevant image according to the server response
Adventures.setImage = function (img_name) {
    $("#situation-image").attr("src", "./images/" + img_name+".jpg");
};

Adventures.checkName = function(){
    if($(this).val() !== undefined && $(this).val() !== null && $(this).val() !== ""){
        $(".adventure-button").prop("disabled", false);
    }
    else{
        $(".adventure-button").prop("disabled", true);
    }
};


Adventures.initAdventure = function(){

    $.ajax("/start",{
        type: "POST",
        data: {"name":
            $("#nameField").val(),
            "adventure_id": $(this).val()
        },
        dataType: "json",
        contentType: "application/json",
        success: function (data) {
            console.log(data);
            Adventures.currentUser = data["user"];
            Adventures.currentAdventure = data["adventure"];
            Adventures.currentStep = data["current"];
            Adventures.currentScore = data["score"];
            Adventures.updateScore();
            $(".greeting-text").hide();
            Adventures.write(data);
            $(".adventure").show();
            $(".welcome-screen").hide();
            $(".lives").show();
        }
    });
};

Adventures.handleServerError = function (errorThrown) {
    Adventures.debugPrint("Server Error: " + errorThrown);
    var actualError = "";
    if (Adventures.debugMode) {
        actualError = " ( " + errorThrown + " ) ";
    }
    Adventures.write("Sorry, there seems to be an error on the server. Let's talk later. " + actualError);

};

Adventures.debugPrint = function (msg) {
    if (Adventures.debugMode) {
        console.log("Adventures DEBUG: " + msg)
    }
};


Adventures.showPopup = function(popupId){
    $(".popup-lightbox .popup-page").hide();
    $(".popup-lightbox .popup-page#" + popupId).show();
    $(".popup-lightbox").fadeIn();
};


Adventures.checkScore = function(score){
    if(score>=100){
        Adventures.showPopup("Win");
        $("#ok1").bind("click",function(){
            Adventures.currentStep = 0;
            location.reload();
            Adventures.closepo
        })
    }
    if(score<=0){
        Adventures.showPopup("Lose");
          $("#ok2").bind("click",function(){
            Adventures.currentStep = 0;
            location.reload();
        })
    }

};

Adventures.start();

