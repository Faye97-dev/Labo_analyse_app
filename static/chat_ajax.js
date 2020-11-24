var dataForCron = function () {
    current_chat = {}
    current_chat['last_msgId_sender'] = ''
    $('.senderMsgClass').each(function(){
        current_chat['last_msgId_sender'] = $(this).attr('id').split('-')[1]
    }) 
    current_chat['chat_id'] = {{chat.id}}
    //console.log('current chat data ...',current_chat) 
    //
    chats_data = {}
    $('.chat-Class').each(function(){
        temp = {'chat_id':$(this).attr('id').split('-')[1]}
        temp['last_msgId'] = $('#chatLastMsg-'+temp['chat_id']).text().trim()
        chats_data[temp['chat_id']] = temp
    })
    console.log('list of chats data  ... ',chats_data)

    data_cron = {}
    data_cron['current_chat'] = JSON.stringify(current_chat)
    data_cron['chats'] = JSON.stringify(chats_data)
    
    //console.log('current chat data ...',data_cron) 
    return data_cron;
}

var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
var success_cron = function (data) {
    console.log('sucess' , data) 
    current_chat_ajax = data[1]
    list_chats = data[0]

    data_cron = dataForCron()
    //console.log(get_active_chat() , current_chat['chat_id'])
    if(data_cron['chats'] == "{}"){
        console.log('Exit chat app end of the cron ... ', current_chat['chat_id'])
    }else if(get_active_chat() !== current_chat['chat_id'] ){
        console.log('Switch to a new chat end of the cron ... ', current_chat['chat_id'])
    }else{
        for(var i=0 ; i<list_chats.length ; i++){
            if (list_chats[i]['status']){
                $('#chatLastMsg-'+list_chats[i]['chat_id']).html(list_chats[i]['message']['id'])
                if($('#notifBadge-'+list_chats[i]['chat_id']).text().trim() === ''){
                    if(list_chats[i]['count']!==0){
                        $('#notifBadge-'+list_chats[i]['chat_id']).html(list_chats[i]['count'])
                        $('#notifBadge-'+list_chats[i]['chat_id']).css('display','block')
                    }
                }else{
                    nfbg = $('#notifBadge-'+list_chats[i]['chat_id']).text().trim()
                    nfbg = parseInt(nfbg)
                    nfbg = nfbg+list_chats[i]['count']
                    if(nfbg!==0){
                        $('#notifBadge-'+list_chats[i]['chat_id']).html(nfbg)
                        $('#notifBadge-'+list_chats[i]['chat_id']).css('display','block')
                    }   
                }
                $('#contentLastMsg-'+list_chats[i]['chat_id']).html(list_chats[i]['message']['content'])
            }
            
        }

       

        for(var i=0 ; i<current_chat_ajax['message'].length ; i++){
            //console.log(current_chat_ajax['message'][i])
            $("#next-new_msg-"+counter).html(addMsg_recived(current_chat_ajax['message'][i]['content'],current_chat_ajax['message'][i]['timestamp']))
            $("#next-new_msg-"+counter).attr('id' ,`msg_id-${current_chat_ajax['message'][i]['id']}`)
            counter = counter+1
            //$("#chat_msg_area").append(`<section class="g-mb-30" id='next-new_msg'></section>`)
            $("#chat_msg_area").mCustomScrollbar("scrollTo","bottom",{scrollInertia:0})
        }

        
       /* setTimeout(function(){
            ServiceBakend.ajax.SendData('msgListner-json', data_cron, csrftoken,success_cron, function(reponse){console.log(' failed ....')})
        },40000) */
    }      
}

ServiceBakend.ajax.SendData('msgListner-json', dataForCron(), csrftoken,success_cron, function(reponse){console.log(' failed ....')})


var get_active_chat = function(){
    var id
    $('.chat-Class').each(function(){   
        if($(this).hasClass('active')){
            id = $(this).attr('id').split('-')[1]
        }   
    })
    //console.log('current active ', id)
    return parseInt(id)
   
}