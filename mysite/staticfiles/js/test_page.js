var curr = -1;
var answered = 0;
var not_answered = 0;
var not_visited = 0;
var question = [];
var choices = [];
var answer = [];
var qstatus = [];
var pmark = [];
var nmark = [];
var test_id;
//statuses : 0-not_visited; 1 - answered,2-answered marked for review, 3-marked for review, 4-not answered;


function first(){
    not_visited = parseInt($("#t3t1").html());
    test_id = parseInt($("#test_id").html());
    question.length = not_visited;
    choices.length = not_visited;
    pmark.length = not_visited;
    nmark.length = not_visited;
    qstatus.length = not_visited;
    window.alert("stat len is "+qstatus.length);
    for(i=0;i<question.length;i++){
    question[i] = "-";
    answer[i]="-";
    qstatus[i]=3;
    pmark[i]=0;
    nmark[i]=0;
    }
    for(i=0;i<choices.length;i++){
    choices[i] = ["-","-","-","-"];
    }
    window.alert(qstatus);
    get_and_display(1);
};

function get_and_display(a){
    $("#question").html("Empty question");

    if(question[a-1]=="-"){
        //window.alert("trying to get question "+a+" "+test_id);
        $.ajax({
         async: false,
         type: 'GET',
         url: '/get_question',
         data:{"test_id":test_id,"qno":a},
         success: function(data) {
              //callback
              //window.alert(data);
              //$(".third").html(data);
              question[a-1]=$(data).filter("#question").html();
              choices[a-1][0]=$(data).filter("#c1").html();
              choices[a-1][1]=$(data).filter("#c2").html();
              choices[a-1][2]=$(data).filter("#c3").html();
              choices[a-1][3]=$(data).filter("#c4").html();
              pmark[a-1]=$(data).filter("#pmarks").html();
              nmark[a-1]=$(data).filter("#neg").html();
              /*window.alert(question[a-1]);
              window.alert(choices[a-1]);*/
            }
         });
    }
    $("#question").html(question[a-1]);
    $("#c1").html(choices[a-1][0]);
    $("#c2").html(choices[a-1][1]);
    $("#c3").html(choices[a-1][2]);
    $("#c4").html(choices[a-1][3]);
    $("#pmarks").html(pmark[a-1]);
    $("#nmarks").html(nmark[a-1]);
    curr=a;
    $("input[name='choices_avl']:checked").prop("checked",false);
    if(answer[curr-1]!='-'){
        $("input[name='choices_avl']").filter('[value='+answer[curr-1]+']').prop('checked', true);
    }

    MathJax.typeset();
};

$(document).on('click','.qbut',function(){
    var id = parseInt($(this).attr('id'));
    //window.alert(id);
    if(curr!=id){
    if(qstatus[curr-1]==3){
        update_status(curr,2);
    }

        get_and_display(id);
    }
});

function update_status(a,b){
    ///statuses : 0-not_visited; 1 - answered,2-answered marked for review, 3-marked for review, 4-not answered;
    //statuses 1 - answered, 2- not answered, 3-notvisited, 4 - marked for review, 5 - ansered but marked for review
    window.alert("changing status of "+a+"to "+b);
    qstatus[a-1]=b;
    var a1=a-1;
    window.alert("#"+a);
    var img = [0,0,0,0,0];
    if(b==1){
        $("#"+a).css('background',"url('/static/images/1.png') no-repeat");
        $("#"+a).css('margin-top',"-2px");
        $("#"+a+" p").css("margin-left","0px");
        $("#"+a+" p").css("margin-top","20px");
    }
    else if(b==2){
        $("#"+a).css('background',"url('/static/images/2.png') no-repeat");
        $("#"+a).css('margin-top',"2px");
        $("#"+a+" p").css("margin-left","-5px");
        $("#"+a+" p").css("margin-top","15px");
    }
    else if(b==5){
        $("#"+a).css('background',"url('/static/images/5.png') no-repeat");
        $("#"+a).css('margin-top',"-5px");
        $("#"+a+" p").css("margin-left","-5px");
        $("#"+a+" p").css("margin-top","20px");
    }
    else if(b==4){
        $("#"+a).css('background',"url('/static/images/4.png') no-repeat");
        $("#"+a).css('margin-top',"2px");
        $("#"+a+" p").css("margin-left","-10px");
        $("#"+a+" p").css("margin-top","15px");
    }

    //$("#"+a).css('background',"url('/static/images/5.png') no-repeat");
    //$("#"+a+" p").css("margin-left","-5px");
    //$("#"+a+" p").css("margin-top","20px");
    var t=[0,0,0,0,0,0];
    for(i=0;i<qstatus.length;i++){
        t[qstatus[i]] = t[qstatus[i]]+1;
    }
    $(".t1t1").html(t[1]);//Answered
    $(".t2t1").html(t[2]);//notanswered
    $(".t3t1").html(t[3]);//notvisited
    $(".t4t1").html(t[4]);//marked for review
    $(".t5t1").html(t[5]);//answered marked for review
}

$(document).on('click',".nbutton",function(){
    var go = parseInt($(this).attr('id'));
    window.alert(curr+"stat of curr"+qstatus);
    if(go==1111 && curr>1){
        if(qstatus[curr-1]==3){
            update_status(curr,2);
        }
        get_and_display(curr-1);
    }
    else if(go==2222){
         if(answer[curr-1]!='-'){
            $("input[name='choices_avl']:checked").prop("checked",false);
            answer[curr-1]='-';
            if(qstatus[curr-1]==5){
                update_status(curr,4);
            }
            else{
                update_status(curr,2);
            }
         }
    }
    else if(go==3333){
        if(qstatus[curr-1]==4){
            update_status(curr,2);
        }else if(qstatus[curr-1]==5){
            update_status(curr,1);
        }else if(qstatus[curr-1]==2 || qstatus[curr-1]==3){
            update_status(curr,4);
        }else if(qstatus[curr-1]==1){
            update_status(curr,5);
        }

    }
    else if(go==4444){
        var radioValue = $("input[name='choices_avl']:checked").val();
        window.alert(radioValue);
        if(radioValue){//=='a' || radioValue=="b" || radioValue=="c" ||radioValue=="d"){
            answer[curr-1]=radioValue;
            if(qstatus[curr-1]==4){
                update_status(curr,5);
            }else{
                update_status(curr,1);
            }

        }
    }
    else if(go==5555 && curr<question.length){
        window.alert("current is "+curr);
        if(qstatus[curr-1]==3){
            update_status(curr,2);
        }
        get_and_display(curr+1);
    }
});


$(document).on('click','#submit_but',function(){
    window.alert("submitting testid"+test_id+"with answers "+answer);
    $.ajaxSetup({
     beforeSend: function(xhr, settings) {
         function getCookie(name) {
             var cookieValue = null;
             if (document.cookie && document.cookie != '') {
                 var cookies = document.cookie.split(';');
                 for (var i = 0; i < cookies.length; i++) {
                     var cookie = jQuery.trim(cookies[i]);
                     // Does this cookie string begin with the name we want?
                     if (cookie.substring(0, name.length + 1) == (name + '=')) {
                         cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                         break;
                     }
                 }
             }
             return cookieValue;
         }
         if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
             // Only send the token to relative URLs i.e. locally.
             xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
         }
     }
    });
    $.ajax({
         async: false,
         type: 'POST',
         url: '/store_result',
         data:{"test_id":test_id,"answers[]":answer},
         success: function(data) {
              //callback
              //window.alert(data);
            }
         });
});


$(document).ready(function() {
  //alert('Page is loaded');
  first();
});