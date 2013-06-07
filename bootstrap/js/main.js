$(function(){
   
    $(".upvote").click(function(){
      
     // alert("help me");
        $.ajax({
            type: "POST",
            url: "/ajax",
            async: true,
            data: {"act": "upvote", "uid": $(this).val()},
            dataType: "json"
        }).done(function(msg){ alert(msg.resp);});
    });

 $(".downvote").click(function(){
      
     // alert("help me");
        $.ajax({
            type: "POST",
            url: "/ajax",
            async: true,
            data: {"act": "downvote", "uid": $(this).val()},
            dataType: "json"
        }).done(function(msg){ alert(msg.resp);});
    });



});
