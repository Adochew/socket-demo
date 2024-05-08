$(document).ready(function() {
    // 输入框
    var textarea = document.querySelector('.resize-none');
    textarea.addEventListener('input', adjustHeight);

    function adjustHeight() {
        this.style.height = '38px';
        var maxHeight = 114;
        if (this.scrollHeight <= maxHeight) {
            this.style.height = `${this.scrollHeight}px`;
        } else {
            this.style.height = `${maxHeight}px`;
        }
    }

    // 当发送按钮被点击
    $('button').click(function() {
        $('button').prop('disabled', true);
        var message = $('textarea').val();
        if (message.trim() !== '') {
            displayMessage(message, 'end');  // 显示用户消息
            $('textarea').val('');  // 清空输入区域
            textarea.style.height = '38px';  // 重置输入区域高度

            // 发送消息到服务器并获取响应
            $.ajax({
                url: '/chat-stream',  // 后端处理聊天的端点
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({ content: message }),
                success: function() {
                    // 假设响应是一个简单的字符串
                    displayMessage('...', 'start');
                },
                error: function() {
                    displayMessage('Sorry, there was an error.', 'start');
                }
            });
        }
    });

    // 监听来自服务器的事件
    var eventSource = new EventSource('/update');
    eventSource.onmessage = function(event) {
        let lastDiv = $('.bg-light.p-2.rounded.mt-1.mb-1.message-box').last();
        let pTag = lastDiv.find('p');
        pTag[0].innerHTML += event.data;
        // 滚动到聊天容器的底部以确保最新消息可见
        $('.chat-container').scrollTop($('.chat-container')[0].scrollHeight);
    };

    // 监听事件流的开始
    eventSource.addEventListener('start', function(event) {
        console.log(event)
        let lastDiv = $('.bg-light.p-2.rounded.mt-1.mb-1.message-box').last();
        let pTag = lastDiv.find('p');
        pTag[0].innerHTML = '';
    });

    // 监听事件流的结束
    eventSource.addEventListener('end', function(event) {
        $('button').prop('disabled', false);
    });


    // 函数用于在聊天界面显示消息
    function displayMessage(message, align) {
        message = message.replace(/\n/g, '<br>');
        let messageAlign = (align === 'start') ? 'justify-content-start' : 'justify-content-end';
        let messageBox = '<div class="d-flex ' + messageAlign + '"><div class="bg-light p-2 rounded mt-1 mb-1 message-box"><p class="mb-0">' + message + '</p></div></div>';
        if (align === 'end') {
            messageBox = '<div class="d-flex ' + messageAlign + '"><div class="bg-primary text-white p-2 rounded mt-1 mb-1 message-box"><p class="mb-0">' + message + '</p></div></div>';
        }
        $('.card-body').append(messageBox); // 将消息添加到聊天界面
        // 滚动到最新消息
        $('.chat-container').scrollTop($('.chat-container')[0].scrollHeight);
    }

});
