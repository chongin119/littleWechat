$(document).ready(function (){
    if(window.location.pathname === '/register'){
        registercheck();
    }
});

function registercheck(){
    $('#regname').on("keyup",function (){
        let username = $(this).val();
        let pattern = /(^[A-Za-z0-9_@]+$)/;
        let validuser = $('#validuser')
        if(pattern.test(username) === true){
            $.ajax({
               url:'/valid',
               method:"post",
               data:{'username':username},
               success:function(resp){
                   console.log(resp)
                   if(resp === "true"){
                       validuser.removeClass();
                       validuser.addClass('correct');
                       validuser.html('可以使用此帐号');
                       if($('#validpwd').html() === "密码匹配"){

                           $('#submit').removeAttr('disabled');
                       }
                   }else{
                       validuser.removeClass();
                       validuser.addClass('wrong');
                       validuser.html('不可以使用此帐号');
                       $('#submit').attr('disabled','disabled');
                   }
               }
           });
       }else{
           validuser.removeClass();
           validuser.addClass('wrong');
           validuser.html('非法帐号');
           $('#submit').attr('disabled','disabled');
       }
    });

    $('#regpassword').on("keyup",function (){
        let password = $(this).val();
        let repassword = $('#reregpassword').val();
        let validpwd = $('#validpwd');

        if(password === repassword && password !== ""){
            validpwd.removeClass();
            validpwd.addClass('correct');
            validpwd.html('密码匹配');
            if($('#validuser').html() === "可以使用此帐号"){
                   $('#submit').removeAttr('disabled');
               }
        }else{
            validpwd.removeClass();
            validpwd.addClass('wrong');
            validpwd.html('密码不匹配');
            $('#submit').attr('disabled','disabled');

        }
    });

    $('#reregpassword').on("keyup",function (){
        let repassword = $(this).val();
        let password = $('#regpassword').val();
        let validpwd = $('#validpwd');

        if(password === repassword && repassword !== ""){
            validpwd.removeClass();
            validpwd.addClass('correct');
            validpwd.html('密码匹配');
            if($('#validuser').html() === "可以使用此帐号"){
                   $('#submit').removeAttr('disabled');
               }
        }else{
            validpwd.removeClass();
            validpwd.addClass('wrong');
            validpwd.html('密码不匹配');
            $('#submit').attr('disabled','disabled');
        }
    });

    $('#personalpic').on("change",function(){
        let acceptType = $(this).attr('accept');
        let selectedFile = $(this).val();

        let fileType = selectedFile.substring(selectedFile.indexOf('.')+1,selectedFile.length)
        let location = acceptType.indexOf(fileType);
        if(location > -1){
            return true;
        }else{
            $(this).val('');
        }
    });
}
