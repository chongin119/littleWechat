let getnewsclockid = "";
let newfriendreqclockid = "";
let newmessageclockid = "";
let newmessagereqclockid = "";
let _relationship_id = "";
let _maxmessage_id = "";
let totalchatfriend = "";

let selector = "";

let lstupdateMessageCount = "";
let path = "/static/img/";
let usericonpath = "/static/usericon/"
let filepath = "/static/filemessage/"
let checktime = 1000;

$(document).ready(function (){
    //getnewsclockid = setInterval(getnews,checktime);
    getnews();

    lstupdateMessageCount = -1;
    funcbar();
    scrollbarAct();
    addfriendbutton();
    coverpage();
    showchatfriend();
    sendmessage();
    Upload();
});

function funcbar(){
    $('#chatIcon').on('click',function(){

        lstupdateMessageCount = -1;
        let content = "";
        show($('#contentWindow'),content);


        clearFocus();
        changetoFirst();

        $(this).attr('src',`${path}chatIconFocus.png`);
        $('#addfriend').attr('src',`${path}plus.png`);

        $('.contentWindow').addClass('chatboxpage');
        $('.mainother').removeClass('friendpagecontent');

        showchatfriend();

    });

    $('#friendsIcon').on('click',function(){
        clearInterval(newmessageclockid);
        let content = "";
        show($('#contentWindow'),content);

        $('#inputWindow').empty();

        clearFocus();
        changetoSecond();

        $(this).attr('src',`${path}friendsIconFocus.png`);
        $('#addfriend').attr('src',`${path}friendplus.png`);

        $('.contentWindow').removeClass('chatboxpage');
        $('.mainother').addClass('friendpagecontent');


        $('#newfriend').addClass('chosen');
        checkaddfriend();
        scrollbarAct();
    });

    $('#logoutIcon').on('click',function(){
       $.ajax({
         method:"post",
         url:"/logout",
         success:function () {
             window.location = window.location.origin
         }
       });
    });
}

function addfriendbutton(){
    $('#addfriend').on('click',function () {
       if($(this).attr('src').indexOf('friendplus') !== -1){
           $('#addfriendFromSQL').val('');
           $('#cantfounduser').addClass('hidden');
           $('#showsearchuser').addClass('hidden');

           $('#confirm').css('background','#E0E0E0');
           $('#confirm').attr('disabled','disabled');

           $('.coverpage').fadeIn(300);
       }else{


           //console.log($(this).attr('src'));

           createGroup();
           $('#createConfirm').addClass('disa');
           $('.createGroupCoverPage').fadeIn(300);
       }
    });
}

function clearFocus(){
    $('#chatIcon').attr('src',`${path}chatIcon.png`);
    $('#friendsIcon').attr('src',`${path}friendsIcon.png`);
}

function changetoFirst(){
    clearInterval(newfriendreqclockid);
    $('#mainheadertopic').html('');
    //上傳圖片跟檔案功能
    let content = `<div>
                   <form method="post" action="">
                        <input style="position: absolute;display: none" id="uploadfilebutton" type="file" name="" value="">
                    </form>
                    <label for="uploadfilebutton">
                        <img id="uploadfile" style="margin-left:1vmin;width: 2vmin;cursor: pointer" src="${path}file-open.png"/>
                    </label>
                </div>
                <div class="inputWindowText"><textarea value=""></textarea></div>
                <div class="inputWindowButton"><div>传送 (S)</div></div>`;
    $('#inputWindow').empty();
    $('#inputWindow').append(content);

    Upload();
    sendmessage();
}

function Upload(){
    $('#uploadfilebutton').on("change",function (){
        let selectedFile = $(this).val();
        let relationship_id = $('.friendslist').children('.chosen').children('input:eq(1)').val();
        console.log(selectedFile,relationship_id);

        let files = $('#uploadfilebutton')[0].files;
        if(files.length <=0){
            return alert('haha');
        }

        let fd = new FormData();
        fd.append('avator',files[0]);

        $.ajax({
           method:"post",
            url:"/savefile",
            data:fd,
            processData:false,
            contentType:false,
            success:function (res) {
                $.ajax({
                   method:"post",
                   url:"/sendfile",
                    data:{"locate":res,"relationship_id":relationship_id},
                    success:function(resp){
                        selector = $('#friendslist').children('.chosen');
                        showmessage();
                        clickToRead();
                    }
                });
            }
        });


    })

}

function changetoSecond(){

    $('#showMore').remove();
    showfriendlist();

    clearInterval(newfriendreqclockid);
    //newfriendreqclockid = setInterval(checkaddfriend,checktime);
    checkaddfriend();

    $('#newfriend').on('click',function(){

        clearInterval(newfriendreqclockid);
        //newfriendreqclockid = setInterval(checkaddfriend,checktime);
        checkaddfriend();

        $(this).parents("div:eq(0)").children(".box").removeClass('chosen');
        $('#newfriend').addClass('chosen');
        $('#mainheadertopic').html('新的朋友');

        //checkaddfriend();
        scrollbarAct();
    });


}

function scrollbarAct(){
    $('#friendslist').hover(function(){
        $(this).removeClass('hiddenscrollbar');
    },function (){
        $(this).addClass('hiddenscrollbar');
    });

    $('.friendpagecontent').hover(function(){
        $(this).removeClass('hiddenscrollbar');
    },function (){
        $(this).addClass('hiddenscrollbar');
    });

    $('.chatboxpage').hover(function(){
        $(this).removeClass('hiddenscrollbar');
    },function (){
        $(this).addClass('hiddenscrollbar');
    });

    $('#createLSTLeft').hover(function(){
        $(this).removeClass('hiddenscrollbar');
    },function (){
        $(this).addClass('hiddenscrollbar');
    });

    $('#createLSTRight').hover(function(){
        $(this).removeClass('hiddenscrollbar');
    },function (){
        $(this).addClass('hiddenscrollbar');
    });

}

function coverpage(){
    $('#back').on("click",function(){
        $('.coverpage').fadeOut(300);
    });

    $('#addfriendFromSQL').on('keyup',function(){
        //console.log($(this).val());
       $.ajax({
           method:'post',
           url:'/addfriendvalid',
           data:{"username" : $(this).val()},
           success:function(resp){
               //console.log(resp)
               if(resp.status === "true"){
                   $('#showsearchuser').removeClass('hidden');
                   $('#cantfounduser').addClass('hidden');
                   $('#addfriendname').html(`${resp.info[1]}`);
                   $('#addfriendicon').attr('src',`${usericonpath}${resp.info[2]}`);
                   $('#confirm').css('background','');
                   $('#confirm').removeAttr('disabled');
               }else{
                   if(resp.status === "own") {
                       $('#cantfounduser').html('不能搜索自己！！');

                   }else{
                       if(resp.status === "hvRepeat"){
                           $('#cantfounduser').html('曾经发送好友邀请了！！');
                       }else{
                           if(resp.status === "isFd"){
                               $('#cantfounduser').html('已经是朋友了！！');
                           }else{
                               $('#cantfounduser').html('用户不存在！！');
                           }
                       }
                   }

                    $('#confirm').css('background','#E0E0E0');
                    $('#confirm').attr('disabled','disabled');
                    $('#cantfounduser').removeClass('hidden');
                    $('#showsearchuser').addClass('hidden');
               }
           }
       });
    });

    $('#confirm').on('click',function (){
        let comment = "";
        comment = $('#addfriendFromSQLcomment').val()
        $.ajax({
           method: "post",
           url:"/addfriendsendreq",
           data:{"receiver_id":$('#addfriendFromSQL').val(),"comment":comment},
           success:function(resp){
                $('.coverpage').fadeOut(300);
           }
        });
    });
}

function createGroup(){
    $('#createLSTLeft').empty();
    $('#createLSTRight').empty();

    $('#createExit').on('click',function () {
        $('#createLSTLeft').empty();
        $('#createLSTRight').empty();
        $('.createGroupCoverPage').fadeOut(300);
    });

    $('#createGroupName').on('keyup',function(){

       if($(this).val().length === 0){
           $('#createConfirm').addClass('disa');
       }else{
           $('#createConfirm').removeClass('disa');
       }
    });

    $('#createConfirm').on('click',function(){
        let username = new Array();
         $('#createLSTRight').children().each(function(i,n){
             let child = $(n);
             username.push(child.children('div').children('input').val());
         });

         if(username.length >= 2){
             username.push({"GroupName":$('#createGroupName').val()})
             $.ajax({
                 method:"post",
                 url:"/createGroup",
                 data:JSON.stringify(username),
                 contentType: "application/json",
                 success:function (resp) {
                    $('#createLSTLeft').empty();
                    $('#createLSTRight').empty();
                    $('.createGroupCoverPage').fadeOut(300);
                 }
             });
         }

    });

    $.ajax({
       method:"post",
       url:"/getfriendlist",
       data:"",
       success:function (resp){
            let friendlist = "";
            let count = 1;
            for(let i of resp) {
                friendlist += `
                <div class="friendreqbox createGroupbox" id="createfriend${count}">
                    <img  class="boxicon" src=${usericonpath}${i.icon}>
                    <div>
                        <span style="cursor: default">${i.name}</span>
                        <input type="hidden" id="createusername${count}" value="${i.username}"/>
                    </div>
                    <input id="createfriendcheckbox${count++}" class="friendreqboxbutton" type="checkbox" value="">
                </div>
                `;
            }
            $('#createLSTLeft').append(friendlist);

            for(let i = 1;i<=count;i++){
                $(`#createfriendcheckbox${i}`).on('click',function () {
                    if(!$(this).prop('checked')){
                        $(`#createfriendRight${i}`).remove();
                    }else{
                        let _parent = $(this).parent();
                        let src = _parent.children('img').attr('src');
                        let name = _parent.children('div').children('span').html();
                        let username = _parent.children('div').children('input').val();

                        let friendlist = "";
                        friendlist+=`
                        <div class="friendreqbox createGroupbox" id="createfriendRight${i}">
                            <img  class="boxicon" src=${src}>
                            <div>
                                <span style="cursor: default">${name}</span>
                                <input type="hidden" id="createusernameRight${i}" value="${username}"/>
                            </div>
                        </div>
                        `;
                        $('#createLSTRight').append(friendlist);
                    }

                    let username = new Array();
                    $('#createLSTRight').children().each(function(i,n){
                         let child = $(n);
                         username.push(child.children('div').children('input').val());
                     });
                    if(username.length >= 2 && $('#createGroupName').val() !== ""){
                        $('#createConfirm').removeClass('disa');
                    }else{
                        $('#createConfirm').addClass('disa');
                    }
                });
            }
       }
    });
}

function getnews(){
    $.ajax({
        method: "post",
        url: "/getnews",
        data:{"message":"needCounter"},
        success:function(resp){
            if(resp.counter !== 0){
                $('#secondred').removeClass('hidden');
                $('#secondred>span').html(`${resp.counter}`);
            }else{
                $('#secondred').addClass('hidden');
                $('#secondred>span').html(`${resp.counter}`);
            }
        }
    });

    $.ajax({
       method:"post",
       url:"/getUnreadMessage",
       data:"",
       success:function(resp){
           if(resp.counter !== 0){
               $('#firstred').removeClass('hidden');
               $('#firstred>span').html(`${resp.counter}`);

           }else{
               $('#firstred').addClass('hidden');
               $('#firstred>span').html('');
           }
       }
    });
}


function checkaddfriend(){
    $.ajax({
        method: "post",
        url: "/getnews",
        data:{"message":""},
        success:function(resp){
            if(resp.counter !== ""){
                let content = "";
                let count = 1;
                for(let i of resp.info){
                    if(i.status === "0"){
                        content += `<div class="friendreqbox" id="friendreqbox${count}">
                                    <img  class="boxicon" src=${usericonpath}${i.icon}>
                                    <div>
                                        <span style="cursor: default">${i.name}</span>
                                        <input type="hidden" id="username${count++}" value="${i.username}"/>
                                        <span class="commentspan">${i.comment}</span>
                                    </div>
                                    <div class="friendreqboxbutton">新增</div>
                                </div>`;
                    }else{
                        content += `<div class="friendreqbox">
                                    <img  class="boxicon" src=${usericonpath}${i.icon}>
                                    <div>
                                        <span style="cursor: default">${i.name}</span>
                                        <span class="commentspan">${i.comment}</span>
                                    </div>
                                    <div style="background: #E0E0E0;cursor: default" class="friendreqboxbutton">已新增</div>
                                </div>`;
                    }

                }
                show($('#contentWindow'),content);

                for(let i = 1;i<count;i++){
                    $(`#friendreqbox${i}>.friendreqboxbutton`).on('click',function(){
                        $.ajax({
                            method:"post",
                            url:"/confirmFriendReq",
                            data:{"username":$(`#username${i}`).val()},
                            success:function(resp){
                                getnews();
                                checkaddfriend();
                                showfriendlist();
                            }
                        });
                    });
                }

            }
        }
    });
}



function show(selector,content){
    selector.empty();
    selector.append(content);
}

function showfriendlist(){
    $('#friendslist').empty();
    $('#mainheadertopic').html('新的朋友');
    $('#friendslist').append(`
    <div class="labelbox">新的朋友</div>
    <div class="box" id="newfriend">
        <img  class="boxicon" src=${path}friendpluswhite.png>
        <span>新的朋友</span>
    </div>
    <div class="labelbox">朋友</div>
    `);

    $.ajax({
        method:"post",
        url:"/getfriendlist",
        success:function(resp){

            let friendlist = "";
            let count = 1;
            for(let i of resp) {
                friendlist += `
                <div class="box" id="friend${count++}">
                    <img  class="boxicon" src=${usericonpath}${i.icon}>
                    <input type="hidden" value="${i.username}">
                    <span>${i.name}</span>
                </div>
                `;
            }
            $('#friendslist').append(friendlist);

            for(let i = 1;i<=count;i++){
                $(`#friend${i}`).on('click',function () {
                    clearInterval(newfriendreqclockid);
                    $(this).parents("div:eq(0)").children(".box").removeClass('chosen');
                    $(this).addClass('chosen');
                    $('#mainheadertopic').html(`用户${$(this).children("span").html()}资讯`);
                    let content = "";
                    content = `
                    <div style="text-align: center;margin-top: 5vmin">
                        <img style="width: 25vw" src="${$(this).children('img').attr('src')}"/>
                        <h2>名字：${$(this).children('span').html()}</h2>
                        <h2>用户号：${$(this).children('input').val()}</h2>
                    </div>
                    `;
                    show($('#contentWindow'),content);
                });
            }
        }
    });

}

function showchatfriend(){
    $('#friendslist').empty();
    $.ajax({
       method:"post",
       url:"/getchatfriends",
       data:"",
       success:function(resp){
           //console.log(resp)
           let chatfriendlist = "";
           let count = 1;
           for(let i of resp){
               let message = i.message;
               if(message.length > 10){
                   message = message.substr(0,6)+"...";
               }
               chatfriendlist += `
               <div class="box" id="chatfriend${count++}">
                    <input type="hidden" value="${i.username}">
                    <input type="hidden" value="${i.relationship_id}">
                    <input type="hidden" value="${i.type}">
                    <div class="redcommentmessage hidden">
                        <img src="${path}redcircle.png"/>
                    </div>
                    <img  class="boxicon" src=${usericonpath}${i.icon}>
                    <div style="cursor: default;flex: 0.9;margin: auto 0">
                        <span style="display: block">${i.name}</span>
                        <span class="commentspan">${message}</span>
                    </div>
                </div>
               `;
           }
           $('#friendslist').append(chatfriendlist);
           $('#chatfriend1').addClass('chosen');
           totalchatfriend = count;

           clearInterval(newmessageclockid);
           //newmessageclockid = setInterval(getEachUnRead,checktime);
           //getEachUnRead();

           //console.log(lstupdateMessageCount);

           //第一次請求網頁
           if(lstupdateMessageCount === -1){
               //console.log("aaaa");
               selector = $('#chatfriend1');
               clickToRead();
               getnews();
               getEachUnRead();
               showmessage();
               lstupdateMessageCount = $('#firstred>span').html();
           }

           for(let i = 1;i<=count;i++){
               $(`#chatfriend${i}`).on('click',function(){
                    $(this).parents("div:eq(0)").children(".box").removeClass('chosen');
                    $(this).addClass('chosen');
                    selector = $(this);
                    clickToRead();
                    getnews();
                    getEachUnRead();
                    showmessage();
               });
           }
       }
    });

}

function showmessage(){
    clearInterval(newmessagereqclockid);
    let topic = selector.children("div").children("span").html();
    if(topic === undefined)topic = "";

    $('#mainheadertopic').html(`${topic}`);
    $('#showMore').remove();
    $('#contentWindow').empty();


    let uurl = "";
    let ddata = "";
    if(selector.children('input:eq(2)').val() === "friend"){
        uurl = "/getmessage";
        ddata = {"username":selector.children('input:eq(0)').val()};
        $('#showMore').remove();
    }else{
        uurl = "/getGroupmessage";
        ddata = {"relationship_id":selector.children('input:eq(1)').val()}
        showMoreButton();
    }

    //console.log(uurl);
    $.ajax({
        method:"post",
        url:uurl,
        data:ddata,
        success:function(resp){
            //console.log(resp);
            let messages = "";
            let maxmessage_id = -1;
            for(let i of resp){
                if(parseInt(i.message_id) > maxmessage_id){
                    maxmessage_id = parseInt(i.message_id)
                }
                console.log(uurl,i.type);
                if(i.type === "text"){
                    if(i.isOwn === "true"){
                        messages += `
                        <div class="chatbox chatboxright">
                            <div style="padding-left:5vmin;"><p class="chatboxpright">${i.content}</p></div>
                            <img class="chatboxicon" src="${usericonpath}${i.sender_icon}">                    
                        </div>
                        `;
                    }else{
                        messages += `
                        <div class="chatbox chatboxleft">
                            <img class="chatboxicon" src="${usericonpath}${i.sender_icon}">
                            <div style="padding-right:5vmin;"><p class="chatboxpleft">${i.content}</p></div>                  
                        </div>
                        `;
                    }
                }else{
                    if(i.isOwn === "true"){
                        messages += `
                        <div class="chatbox chatboxright">
                            <div style="padding-left:5vmin;text-align: right;"><img src="${filepath}${i.content}" alt="暂不支持此类型档案" style="width: 5vw;right: 1vmin" class="chatboxpright"></div>
                            <img class="chatboxicon" src="${usericonpath}${i.sender_icon}">                    
                        </div>
                        `;
                    }else{
                        messages += `
                        <div class="chatbox chatboxleft">
                            <img class="chatboxicon" src="${usericonpath}${i.sender_icon}">
                            <div style="padding-right:5vmin;text-align: left;"><img src="${filepath}${i.content}" alt="暂不支持此类型档案" style="width: 5vw;right: 1vmin" class="chatboxpleft"></div>                  
                        </div>
                        `;
                    }
                }
            }
            $('#contentWindow').append(messages);
            scrollbarTobottom();
            _relationship_id = $('#friendslist').children('.chosen').children('input:eq(1)').val();
            _maxmessage_id = maxmessage_id;


            //newmessagereqclockid = setInterval(checknewmessage,checktime);
            checknewmessage();
        }
    });
}

function showMoreButton(){
    $('.mainheader').append(`
    <div class="showMore" id="showMore">
        <img style="width: 3vmin;" src=${path}options.png>
    </div>
    `);

    $('#showMoreBack').on('click',function(){
        $('.showMoreContent').empty();
        $('.showMoreCoverPage').fadeOut(300)
    });

    $('#showMore').on('click',function () {
        $('.showMoreContent').empty();
        $('.showMoreCoverPage').fadeIn(300)
        $.ajax({
           method:"post",
           url:"/getGroupMember",
           data:{"relationship_id":$('.friendslist').children('.chosen').children('input:eq(1)').val()},
           success:function (resp) {
               let content = "";
               content += `
                    <div class="friendreqbox" style="grid-template-columns: 1fr 1fr">
                        <img  style="margin-left: 7vw" class="boxicon" src=${usericonpath}${resp.leader.icon}>
                        <div>
                            <span style="cursor: default">${resp.leader.name}</span>
                            <span class="commentspan" style="color: #3300FF">群主</span>
                        </div>
                    </div>`;
               for(let i of resp.member){
                   content += `
                    <div class="friendreqbox" style="grid-template-columns: 1fr 1fr">
                        <img  style="margin-left: 7vw" class="boxicon" src=${usericonpath}${i.icon}>
                        <div>
                            <span style="cursor: default">${i.name}</span>
                            <span class="commentspan">群成员</span>
                        </div>
                    </div>`;
               }

               $('.showMoreContent').append(content);
           }
        });

    })
}

function checknewmessage(){
    $.ajax({
       method:"post",
       url:"/checknewmessage",
       data:{"relationship_id":_relationship_id,"maxmessage_id":_maxmessage_id},
       success:function(resp){
           let messages = "";
           let maxmessage_id = _maxmessage_id;
            for(let i of resp){
                if(parseInt(i.message_id) > maxmessage_id){
                    maxmessage_id = parseInt(i.message_id)
                }
                if(i.type === "text"){
                    if(i.isOwn === "true"){
                        messages += `
                        <div class="chatbox chatboxright">
                            <div style="padding-left:5vmin;"><p class="chatboxpright">${i.content}</p></div>
                            <img class="chatboxicon" src="${usericonpath}${i.sender_icon}">                    
                        </div>
                        `;
                    }else{
                        messages += `
                        <div class="chatbox chatboxleft">
                            <img class="chatboxicon" src="${usericonpath}${i.sender_icon}">
                            <div style="padding-right:5vmin;"><p class="chatboxpleft">${i.content}</p></div>                  
                        </div>
                        `;
                    }
                }
            }

            _maxmessage_id = maxmessage_id;
            $('#contentWindow').append(messages);
            if(messages !== "")scrollbarTobottom();

       }
    });
}

function sendmessage(){
    $('.inputWindowButton>div').on('click',function(){
       let message = $('.inputWindowText>textarea').val();
       if(message.length > 0){
           let relationship_id = $('#friendslist').children('.chosen').children('input:eq(1)').val();

           $.ajax({
                method:"post",
                url:"/sendmessage",
                data:{"relationship_id":relationship_id,"message":message,"type":"text"},
               success:function(resp) {
                    $('.inputWindowText>textarea').val('');

                    selector = $('#friendslist').children('.chosen');
                    showmessage();
                    clickToRead();

               }
           });
       }
    });
}

function logout(){
    $('#logoutbutton').on('click',function () {
       clearInterval(getnewsclockid);
       clearInterval(newfriendreqclockid);
       clearInterval(newmessageclockid);
       clearInterval(newmessagereqclockid);
    });
}

function scrollbarTobottom(){
    let bottom = $('#contentWindow').prop("scrollHeight");
    $('#contentWindow').scrollTop(bottom);
}

function getEachUnRead(){
    if(selector !== "")clickToRead();

    let arr = new Array();
    for(let i = 1;i<totalchatfriend;i++){
        arr.push($(`#chatfriend${i}`).children('input:eq(1)').val());
    }

    $.ajax({
       method:"post",
       url:"/geteachunread",
       data: JSON.stringify(arr),
        contentType: "application/json",
       success:function(resp){
            for(let i = 1;i<totalchatfriend;i++){
                if(resp[i-1].count > 0){
                    $(`#chatfriend${i}`).children('div:eq(0)').removeClass('hidden');
                    $(`#chatfriend${i}`).children('div:eq(1)').children('span:eq(1)').html(resp[i-1].newestmessage);
                }else{
                    $(`#chatfriend${i}`).children('div:eq(0)').addClass('hidden');
                }
            }
       }
    });
}

function clickToRead(){
    let relationship_id = selector.children('input:eq(1)').val();
    //console.log(relationship_id)
    $.ajax({
       method:"post",
       url:"/setRead",
       data:{"relationship_id":relationship_id},
       success:function(resp){
       }
    });
}
